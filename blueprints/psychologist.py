import json
import os
import time
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for,jsonify,session,flash,g
from sqlalchemy import or_
from decorators import login_required
from exts import mail,db
from flask_mail import Message
from models import EmailCaptchaModel, UserModel, PsychologistModel, PrivateMessagesModel, StudentUserExtsModel,WenjuanExtsModel,FollowModel, WenjuanModel,WenjuanAnswerModel,TesttimesModel
import string
import random
from .forms import RegisterForm,LoginForm
from werkzeug.security import generate_password_hash,check_password_hash
import base64
bp = Blueprint("psychologist", __name__, url_prefix="/psychologist")

@bp.route("/show_psychologist",methods=['GET','POST'])
@login_required
def show_psychologist():
    psyc = PsychologistModel.query.all()
    tag_list=[]
    for each in psyc:
        List=str(each.tag).split(' ')
        tag_list.append(List)
    return render_template("show_psychologist.html",psyc=psyc,psyc_len=len(psyc),tag_list=tag_list)

@bp.route("/psyc_search",methods=['GET','POST'])
def psyc_search():
    search = request.form.get("psyc_search")
    psyc = PsychologistModel.query.filter(or_(PsychologistModel.name.contains(search), PsychologistModel.tag.contains(search))).all()
    tag_list=[]
    for each in psyc:
        List=str(each.tag).split(' ')
        tag_list.append(List)
    return render_template("show_psychologist.html",psyc=psyc,psyc_len=len(psyc),tag_list=tag_list)


@bp.route("/get_psychologist/<int:psyc_id>",methods=['GET','POST'])
@login_required
def get_psychologist(psyc_id):
    psyc=PsychologistModel.query.filter_by(id=psyc_id)[0]
    is_follow=FollowModel.query.filter_by(stu_id=StudentUserExtsModel.query.filter_by(u_id=g.user.id)[0].id).filter_by(psyc_id=psyc_id).first()
    print(is_follow)
    return render_template('user_psyc_central.html',psyc=psyc,tag_list=str(psyc.tag).split(' '),is_follow=is_follow)


@bp.route("/private_messages/<int:p_id>",methods=['GET','POST'])
@login_required
def private_messages(p_id):
    psyc=PsychologistModel.query.filter_by(id=p_id)[0]
    all_msg=PrivateMessagesModel.query.filter_by(author_id=g.user.id).filter_by(psyc_id=p_id).all()
    return render_template('private_messages.html',p_id=p_id,psyc=psyc,user=g.user,all_msg=all_msg)

@bp.route("/stu_sent_messages",methods=['GET','POST'])
@login_required
def stu_sent_messages():
    #通过ajax进行局部传参数
        private_messages_model=PrivateMessagesModel(content=request.form.get("messages"),author_id=request.form.get("user_id"),psyc_id=request.form.get("psyc_id"),msg_type='question')
        psyc=PsychologistModel.query.filter_by(id=request.form.get("psyc_id"))[0]
        psyc.question_times=psyc.question_times+1
        db.session.add(private_messages_model)
        db.session.commit()
        return 'success'


@bp.route("/psyc_answer_messages",methods=['GET','POST'])
@login_required
def psyc_answer_messages():
        private_messages_model=PrivateMessagesModel(content=request.form.get("messages"),author_id=request.form.get("stu_id"),psyc_id=request.form.get("psyc_id"),msg_type='answer')
        psyc=PsychologistModel.query.filter_by(u_id=g.user.id)[0]
        psyc.answer_times=psyc.answer_times+1
        db.session.add(private_messages_model)
        db.session.commit()
        return 'success'

@bp.route("/amd_show_psyc", methods=['GET', 'POST'])
def amd_show_psyc():
    all_psyc=PsychologistModel.query.all()
    return render_template('amd_show_psyc.html',all_psyc=all_psyc)

@bp.route("/psyc_personal_central", methods=['GET', 'POST'])
def psyc_personal_central():
    psyc = PsychologistModel.query.filter_by(u_id=g.user.id)[0]
    tag_list=str(psyc.tag).split(' ')
    return render_template('psyc_personal_central.html',psyc=psyc,tag_list=tag_list,len_of_tag=len(tag_list))

@bp.route("/psyc_change", methods=['GET', 'POST'])#改变心理医生的个人信息
def psyc_change():
    psyc = PsychologistModel.query.filter_by(u_id=g.user.id)[0]
    psyc.name=request.form.get("p_name")
    psyc.gender = request.form.get("p_gender")
    psyc.age=request.form.get("p_age")
    tag_len=request.form.get("p_len")
    tag=''
    for i in range(int(tag_len)):
        print(request.form.get("tag"+str(i)))
        tag=tag+request.form.get("tag"+str(i))
        tag=tag+' '
    tag=str.rstrip(tag)
    psyc.tag=tag
    db.session.commit()
    return redirect(url_for('psychologist.psyc_personal_central'))

@bp.route("/get_new_tag", methods=['GET', 'POST'])#心理医生回答私信
def get_new_tag():
    new_tag=request.form.get("new_tag")
    print(new_tag)
    psyc = PsychologistModel.query.filter_by(u_id=g.user.id)[0]
    psyc.tag=psyc.tag+' '+new_tag
    db.session.commit()
    return redirect(url_for('psychologist.psyc_personal_central'))



@bp.route("/psyc_answer_msg", methods=['GET', 'POST'])#心理医生回答私信
def psyc_answer_msg():
    all_msg=PrivateMessagesModel.query.filter_by(author_id=request.form.get("stu_id")).filter_by(psyc_id=PsychologistModel.query.filter_by(u_id=g.user.id)[0].id).all()
    psyc = PsychologistModel.query.filter_by(u_id=g.user.id)[0]
    stu=UserModel.query.filter_by(id=request.form.get("stu_id"))[0]
    return render_template('psyc_answer_page.html',psyc=psyc,all_msg=all_msg,stu=stu)



@bp.route("/psyc_before_chart", methods=['GET', 'POST'])#心理医生数据统计修改
def psyc_before_chart():
    wenjuan_name_list1 = []
    wenjuan_name_list0 = WenjuanModel.query.filter_by(u_id=g.user.id).with_entities(WenjuanModel.wenjuan_name).distinct().all()
    for x in wenjuan_name_list0:
        if WenjuanModel.query.filter_by(wenjuan_name=x[0]).first().judgment!='无':
            wenjuan_name_list1.append(x[0])#存放不同的问卷名
    wenjuan_answer_list=[]
    wenjuan_name_list_copy=wenjuan_name_list1.copy()
    print(wenjuan_name_list_copy)
    for kk in range(len(wenjuan_name_list_copy)):#去除无人答题的问卷名字
        if len(WenjuanAnswerModel.query.filter_by(wenjuan_name=wenjuan_name_list_copy[kk]).all())==0:
            wenjuan_name_list1.remove(wenjuan_name_list_copy[kk])
    for each in wenjuan_name_list1:
        wenjuan_answer_list.append(WenjuanAnswerModel.query.filter_by(wenjuan_name=each)[0])
    stu_answer_list=[]
    test_times_model=[]
    stu_user_list=[]
    stu_exts_list=[]
    len_of_stu_list = []
    for key in  wenjuan_answer_list:
        test_times_model.append(TesttimesModel.query.filter_by(wenjuan_name=key.wenjuan_name).all())
    print("test_times_model",test_times_model)
    test_times_model_copy=test_times_model.copy()
    for i in range(len(test_times_model_copy)):
        for j in range(len(test_times_model_copy[i])):
            if test_times_model_copy[i][j].test_times==0:
                test_times_model[i].pop(j)
    for e1 in test_times_model:
        List=[]
        List1=[]
        List2=[]
        len_of_stu_list.append(len(e1))
        for e2 in e1:
            List.append(UserModel.query.filter_by(id=e2.u_id).first())
            List1.append(WenjuanAnswerModel.query.filter_by(wenjuan_uid=e2.u_id).filter_by(wenjuan_name=e2.wenjuan_name).filter_by(test_times=e2.test_times).first())
            List2.append(StudentUserExtsModel.query.filter_by(u_id=e2.u_id).first())
        stu_user_list.append(List)
        stu_answer_list.append(List1)
        stu_exts_list.append(List2)
    print("stu_answer_list",stu_answer_list)
    print("stu_user_list", stu_user_list)
    print("stu_exts_list", stu_exts_list)
    return render_template('psyc_before_chart.html',wenjuan_list=wenjuan_answer_list,len_of_wenjuan=len(wenjuan_answer_list),len_of_stu_list=len_of_stu_list,test_times_model=test_times_model,stu_user_list=stu_user_list,stu_answer_list=stu_answer_list,stu_exts_list=stu_exts_list)

@bp.route("/psyc_chart/<wname>/<int:u_id>/<username>", methods=['GET', 'POST'])#心理医生回答私信
def psyc_chart(wname,u_id,username):
    print(wname,u_id)
    wenjuan_exts=WenjuanExtsModel.query.filter_by(wenjuan_name=wname).filter_by(u_id=u_id).all()
    print(wenjuan_exts)
    return render_template('psyc_chart.html',wenjuan_exts=wenjuan_exts,username=username)

@bp.route("/psyc_all_user_chart/<wname>", methods=['GET', 'POST'])#心理医生回答私信
def psyc_all_user_chart(wname):
    uid_list1 = []
    uid_list0 = WenjuanExtsModel.query.filter_by(wenjuan_name=wname).with_entities(WenjuanExtsModel.u_id).distinct().all()
    for x in uid_list0:
        uid_list1.append(x[0])
    print(uid_list1)
    stu_user_list=[]
    for each in uid_list1:
        stu_user_list.append(UserModel.query.filter_by(id=each).first())
    print(stu_user_list)
    wenjuan_exts_list=[]
    for key in stu_user_list:
        wenjuan_exts_list.append(WenjuanExtsModel.query.filter_by(u_id=key.id).filter_by(wenjuan_name=wname).all())
    print(wenjuan_exts_list)
    return render_template('psyc_all_user_chart.html',stu_user_list=stu_user_list,wenjuan_exts_list=wenjuan_exts_list,len_of_stu=len(stu_user_list))

@bp.route("/psyc_wenjuan_search", methods=['GET', 'POST'])#心理医生回答私信
def psyc_wenjuan_search():
    search=request.form.get("psyc_wenjuan_search")
    wenjuan_list1 = []
    wenjuan_list0 = WenjuanModel.query.filter_by(u_id=g.user.id).filter(WenjuanModel.wenjuan_name.contains(search)).with_entities(WenjuanModel.wenjuan_name).distinct().all()
    for x in wenjuan_list0:
        wenjuan_list1.append(x[0])  # 把问卷名取出并去重
    all_wenjuan = []
    for each in wenjuan_list1:
        all_wenjuan.append(WenjuanModel.query.filter_by(wenjuan_name=each)[0])
    return render_template('psyc_index.html', all_wenjuan=all_wenjuan)