import os
import re

import imgkit
import time
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session, flash, g
import requests
from lxml import etree
from decorators import login_required
from exts import mail, db
from flask_mail import Message
from models import EmailCaptchaModel, UserModel, WenjuanModel, WenjuanAnswerModel, StudentUserExtsModel, \
    PsychologistModel, TesttimesModel, WenjuanExtsModel, PrivateMessagesModel
import string
import random
from .forms import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
import base64
import pdfkit

bp = Blueprint("wenjuan", __name__, url_prefix="/wenjuan")
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))  # 返回本项目的绝对路径
ALLOWED_EXTENSIONS = ['png', 'jpg', 'JPG', 'PNG', 'gif', 'GIF', 'jpeg', 'JPEG']  # 此为允许上传的图片格式


@bp.route("/before_wenjuan/<wname>", methods=['GET', 'POST'])
@login_required
def before_wenjuan( wname):  # 用于获取当前的问卷的名字，第一题的id，问卷总长
    wenjuan_list1 = []
    wenjuan_list0 = WenjuanAnswerModel.query.filter_by(wenjuan_uid=g.user.id).with_entities(
        WenjuanAnswerModel.wenjuan_name).distinct().all()
    for x in wenjuan_list0:
        wenjuan_list1.append(x[0])  # 把问卷名取出并去重
    # if wname in wenjuan_list1:
    #   return redirect(url_for('wenjuan.wenjuan_report', wname=wname))
    wenjuan_num = len(WenjuanModel.query.filter_by(wenjuan_name=wname).all())
    first_id = WenjuanModel.query.filter_by(wenjuan_name=wname)[0].id
    last_id = WenjuanModel.query.filter_by(wenjuan_name=wname)[wenjuan_num - 1].id
    if len(TesttimesModel.query.filter_by(u_id=g.user.id).filter_by(wenjuan_name=wname).all()) == 0:
        test_times_model = TesttimesModel(u_id=g.user.id, wenjuan_name=wname)
        db.session.add(test_times_model)
        db.session.commit()
    test_times = TesttimesModel.query.filter_by(u_id=g.user.id).filter_by(wenjuan_name=wname)[0]
    # return redirect(url_for("wenjuan.show_wenjuan", wid=wid, first_id=first_id, wenjuan_num=wenjuan_num, wname=wname,last_id=last_id))
    return render_template("before_wenjuan.html", wenjuan_num=wenjuan_num, wname=wname,
                           test_times=test_times)


@bp.route("/test_report", methods=['GET', 'POST'])
@login_required
def test_report():
    all_report=WenjuanExtsModel.query.filter_by(u_id=g.user.id).all()
    return render_template("test_report.html",all_report=all_report)


@bp.route("/test_history", methods=['GET', 'POST'])
@login_required
def test_history():
    wenjuan_list1 = []
    wenjuan_list0 = WenjuanAnswerModel.query.filter_by(wenjuan_uid=g.user.id).with_entities(
        WenjuanAnswerModel.test_times).distinct().all()
    for x in wenjuan_list0:
        wenjuan_list1.append(x[0])
    wenjuan_name1 = []
    wenjuan_name0 = WenjuanAnswerModel.query.filter_by(wenjuan_uid=g.user.id).with_entities(
        WenjuanAnswerModel.wenjuan_name).distinct().all()
    for j in wenjuan_name0:
        wenjuan_name1.append(j[0])

    one_of_wenjuan_list = []
    wenjuan_exts_list = WenjuanExtsModel.query.filter_by(u_id=g.user.id).all()
    for i in range(len(wenjuan_exts_list)):
        one_of_wenjuan_list.append(WenjuanAnswerModel.query.filter_by(wenjuan_uid=g.user.id).filter_by(
            wenjuan_name=wenjuan_exts_list[i].wenjuan_name).filter_by(
            test_times=wenjuan_exts_list[i].test_times).first())
    wenjuan_List_copy = TesttimesModel.query.filter_by(u_id=g.user.id).all()
    wenjuan_List=[]
    for each in wenjuan_List_copy:
        if each.test_times!=0:
            wenjuan_List.append(each)
    print(wenjuan_List)
    return render_template('test_history.html', one_of_wenjuan_list=one_of_wenjuan_list,
                           len_of_wenjuan_exts=len(wenjuan_exts_list), wenjuan_exts_list=wenjuan_exts_list,
                           wenjuan_name1=wenjuan_name1, wenjuan_List=wenjuan_List)


@bp.route("/test_analyse/<wname>", methods=['GET', 'POST'])
def test_analyse(wname):
    wenjuan_exts_list = WenjuanExtsModel.query.filter_by(u_id=g.user.id).filter_by(wenjuan_name=wname).all()
    wenjuan = WenjuanModel.query.filter_by(wenjuan_name=wname).all()
    private_msg = PrivateMessagesModel.query.filter_by(author_id=g.user.id).filter_by(msg_type='answer').filter_by(
        psyc_id=PsychologistModel.query.filter_by(u_id=wenjuan[0].u_id).first().id).first()
    point_list = []
    Max = 0
    one_of_wenjuan_list = []
    len_of_wenjuan = len(wenjuan)
    for i in range(len(wenjuan_exts_list)):
        one_of_wenjuan_list.append(WenjuanAnswerModel.query.filter_by(wenjuan_uid=g.user.id).filter_by(
            wenjuan_name=wenjuan_exts_list[i].wenjuan_name).filter_by(
            test_times=wenjuan_exts_list[i].test_times).first())
    for ee in range(len_of_wenjuan):
        point_list.append(str(wenjuan[ee].option_point).split(' '))
    for ii in point_list:
        Max = Max + int(ii[-1])

    analysis_msg = ''
    if len(wenjuan_exts_list)>=2:
        if wenjuan_exts_list[-1].total_score < wenjuan_exts_list[-2].total_score:
            analysis_msg = '心理健康状态有所好转'
        elif wenjuan_exts_list[-1].total_score > wenjuan_exts_list[-2].total_score:
            analysis_msg = '心理健康状态变得严重，请咨询心理医生'
    elif len(wenjuan_exts_list) <= 1:
        analysis_msg = '无法比较！'
    return render_template('test_analyse.html', wenjuan_exts_list=wenjuan_exts_list,
                           one_of_wenjuan_list=one_of_wenjuan_list, len_of_wenjuan_exts=len(wenjuan_exts_list),
                           analysis_msg=analysis_msg, wname=wname)


@bp.route("/del_history/<wname>/<int:test_times>", methods=['GET', 'POST'])  # 此处有删除序号混乱的bug
def del_history(wname, test_times):
    test_times_model = TesttimesModel.query.filter_by(u_id=g.user.id, wenjuan_name=wname)[0]
    wenjuan_answer = WenjuanAnswerModel.query.filter_by(wenjuan_name=wname).filter_by(wenjuan_uid=g.user.id).filter_by(
        test_times=test_times).all()
    wenjuan_exts = WenjuanExtsModel.query.filter_by(wenjuan_name=wname).filter_by(u_id=g.user.id).filter_by(
        test_times=test_times).first()
    for each in wenjuan_answer:
        db.session.delete(each)
        db.session.commit()
    db.session.delete(wenjuan_exts)
    test_times_model.test_times = test_times_model.test_times - 1
    db.session.commit()
    # 把删除后的测试序号查出
    wenjuan_exts_after = WenjuanExtsModel.query.filter_by(wenjuan_name=wname).filter_by(u_id=g.user.id).all()
    test_times_list = []
    for ee in wenjuan_exts_after:
        test_times_list.append(ee.test_times)
    x = 1  # 进行测试序号修正的变量
    wenjuan_answer_after = []
    for i in test_times_list:
        wenjuan_answer_after.append(
            WenjuanAnswerModel.query.filter_by(wenjuan_name=wname).filter_by(test_times=i).filter_by(
                wenjuan_uid=g.user.id).all())

    print(wenjuan_answer_after)
    for ii in range(len(wenjuan_answer_after)):
        wenjuan_exts_after[ii].test_times = x
        for key in wenjuan_answer_after[ii]:
            key.test_times = x
            db.session.commit()
        x = x + 1
    return redirect(url_for("wenjuan.test_history", wname=wname))


@bp.route("/history_to_report/<wname>/<int:test_times>", methods=['GET', 'POST'])
def history_to_report(wname, test_times):
    one_of_wenjuan = WenjuanModel.query.filter_by(wenjuan_name=wname)[0]
    wenjuan_exts = WenjuanExtsModel.query.filter_by(wenjuan_name=wname).filter_by(u_id=g.user.id).filter_by(
        test_times=test_times).first()
    wenjuan = WenjuanModel.query.filter_by(wenjuan_name=wname).all()
    all_psyc = PsychologistModel.query.all()
    tag_list = []
    point_list = []
    Max = 0
    Min = 0
    len_of_wenjuan = len(wenjuan)
    print(len_of_wenjuan)
    for ee in range(len_of_wenjuan):
        point_list.append(str(wenjuan[ee].option_point).split(' '))
    for ii in point_list:
        Max = Max + int(ii[-1])
        Min = Min + int(ii[0])
    for key in all_psyc:
        tag_list.append(str(key.tag).split(' '))
    for i in range(len(all_psyc)):
        tag_list[i].append(all_psyc[i])  # 在每一个标签的后面加上心理医生对象
        tag_list[i].append(UserModel.query.filter_by(id=all_psyc[i].u_id)[0])
    level = wenjuan_exts.level
    Sum = wenjuan_exts.total_score
    return render_template('wenjuan_report.html', wname=wname, level=level, degree=Sum, one_of_wenjuan=one_of_wenjuan,
                           tag_list=tag_list, Max=Max, test_times=test_times)


@bp.route("/show_wenjuan/<string:wname>", methods=['GET', 'POST'])
@login_required
def show_wenjuan(wname):
    #if int(wid) - first_id != wenjuan_num:  # 未循环到该问卷名的问卷的最后一个
        wenjuan_list1 = []
        wenjuan_list0 = WenjuanModel.query.with_entities(WenjuanModel.wenjuan_name).distinct().all()
        test_times_model = TesttimesModel.query.filter_by(u_id=g.user.id).filter_by(wenjuan_name=wname)[0]
        for x in wenjuan_list0:
            wenjuan_list1.append(x[0])  # 把问卷名取出并去重
        if len(wenjuan_list1) != 0:  # 数据库不为空
            # wenjuan_search = WenjuanModel.query.filter_by(wenjuan_name=wname).filter_by(id=wid)[0]
            wenjuan_search0 = WenjuanModel.query.filter_by(wenjuan_name=wname).all()
            wenjuan_search = ['#']
            for ii in wenjuan_search0:
                wenjuan_search.append(ii)
            option_List = ['#']
            point_list = ['#']
            for i in range(1, len(wenjuan_search)):
                List = ['#']
                List1 = ['#']
                for each in str(wenjuan_search[i].option).split(' '):
                    List.append(each)
                for eee in str(wenjuan_search[i].option_point).split(' '):
                    List1.append(eee)
                option_List.append(List)
                point_list.append(List1)
            return render_template("wenjuan.html", wenjuan_search=wenjuan_search, option_all=option_List,
                                     wname=wname,
                                   wenjuan_len=len(wenjuan_search), option_len=len(option_List[1]),
                                   point_list=point_list, test_times=test_times_model.test_times)
        else:  # 数据库为空
            return redirect(url_for("first_page"))
    #else:  # 跳到了问卷的最后一个
        #return redirect(url_for("first_page"))

@bp.route("/get_answer/<wname>", methods=['GET', 'POST'])
def get_answer(wname):
    option_dir = request.get_json()
    test_times_model = TesttimesModel.query.filter_by(u_id=g.user.id, wenjuan_name=wname)[0]
    print(option_dir)
    for each in option_dir:
        option_List = str(option_dir[each]).split('|')
        print(option_List)
        wenjuanAnswer_model = WenjuanAnswerModel(option_content=option_List[0], wenjuan_uid=g.user.id, wenjuan_id=each,
                                                 option_type=option_List[-2], point=option_List[-1], wenjuan_name=wname,
                                                 test_times=test_times_model.test_times + 1)
        db.session.add(wenjuanAnswer_model)
        db.session.commit()
    test_times_model.test_times = test_times_model.test_times + 1  # 问卷测试次数加1
    db.session.commit()
    test_times_model = TesttimesModel.query.filter_by(u_id=g.user.id).filter_by(wenjuan_name=wname)[0]
    w_answer = WenjuanAnswerModel.query.filter_by(wenjuan_name=wname).filter_by(wenjuan_uid=g.user.id).filter_by(
        test_times=test_times_model.test_times).all()
    one_of_wenjuan = WenjuanModel.query.filter_by(wenjuan_name=wname)[0]
    span_list = []
    for each in str(one_of_wenjuan.judgment).split(' '):
        span_list.append(each.split('|'))
    Sum = 0
    for kk in w_answer:
        Sum = Sum + kk.point
    level = ''
    for key in span_list:
        if float(Sum) > float(key[-1]):
            continue
        elif float(Sum) >= float(key[0]) and float(Sum) <= float(key[-1]):
            level = key[1]
    wenjuan_exts = WenjuanExtsModel(u_id=g.user.id, wenjuan_name=wname, total_score=Sum, level=level,
                                    test_times=test_times_model.test_times)
    db.session.add(wenjuan_exts)
    db.session.commit()
    return "获取成功"


@bp.route("/input_question/<input_type>/<wname>/<test_type>/<img_name>", methods=['GET', 'POST'])
@login_required
def input_question(input_type, wname, test_type, img_name):
    if input_type == 'same':
        if request.method == "GET":
            return render_template("input_question.html", input_type=input_type, wname=wname, test_type=test_type,
                                   img_name=img_name)
        else:
            title_list0 = request.form.get("title").split("\n")
            title_list1 = []
            option_num = request.form.get("option_num")
            point = ''
            option = ''
            print()
            for i in range(1, int(option_num) + 1):
                point = point + request.form.get("point" + str(i))
                point = point + ' '
                option = option + request.form.get("option" + str(i))
                option = option + ' '
            point = point[:len(point) - 1]
            option = option[:len(option) - 1]
            print("point", point, len(point.split(' ')))
            if len(point.split(' ')) != len(option.split(' ')):
                flash("选项个数与分值个数不相等！")
                return redirect(
                    url_for("wenjuan.input_question", input_type=input_type, wname=wname, test_type=test_type,
                            img_name=img_name))
            else:
                # test_type = request.form.get("test_type")
                # wname = request.form.get("wname")
                for each in title_list0:
                    title_list1.append(each.replace(' ', '').replace('\r', ''))
                for each in title_list1:
                    exercise_title = each
                    exercise_type = "radio"
                    wenjuan = WenjuanModel(exercise_title=exercise_title, option=option, exercise_type=exercise_type,
                                           wenjuan_name=wname, option_point=point, test_type=test_type, u_id=g.user.id,
                                           img_name=img_name)
                    db.session.add(wenjuan)
                    db.session.commit()
                return redirect(url_for("first_page"))
    else:
        if request.method == "GET":
            return render_template("input_question.html", input_type=input_type, wname=wname, test_type=test_type,
                                   img_name=img_name)
        else:
            title = request.form.get("title")
            option_num = request.form.get("option_num")
            point = ''
            option = ''
            for i in range(1, int(option_num) + 1):
                point = point + request.form.get("point" + str(i))
                point = point + ' '
                option = option + request.form.get("option" + str(i))
                option = option + ' '
            point = point[:len(point) - 1]
            option = option[:len(option) - 1]
            if len(point.split(' ')) != len(option.split(' ')):
                flash("选项个数与分值个数不相等！")
                return redirect(
                    url_for("wenjuan.input_question", input_type=input_type, wname=wname, test_type=test_type,
                            img_name=img_name))
            else:
                exercise_type = "radio"
                print(point, test_type)
                wenjuan = WenjuanModel(exercise_title=title, option=option, exercise_type=exercise_type,
                                       wenjuan_name=wname, option_point=point, test_type=test_type, u_id=g.user.id,
                                       img_name=img_name)
                db.session.add(wenjuan)
                db.session.commit()
                return redirect(
                    url_for("wenjuan.input_question", input_type=input_type, wname=wname, test_type=test_type,
                            img_name=img_name))


@bp.route("/before_input", methods=['GET', 'POST'])
def before_input():  # 让问卷的类型与心理健康医生的类型相同
    psyc = PsychologistModel.query.filter_by(u_id=g.user.id).first()
    tag_list = psyc.tag.split(' ')
    print(tag_list)
    return render_template("before_input_wenjuan.html", psyc=psyc, tag_list=tag_list)


@bp.route("/before_input_pro/<input_type>", methods=['GET', 'POST'])
def before_input_pro(input_type):
    wname = request.form.get("wname")
    wenjuan_list1 = []
    wenjuan_list0 = WenjuanModel.query.with_entities(WenjuanModel.wenjuan_name).distinct().all()
    for x in wenjuan_list0:
        wenjuan_list1.append(x[0])  # 把问卷名取出并去重
    if wname in wenjuan_list1:
        flash("问卷名重复！")
        return redirect(url_for('wenjuan.before_input', method=['GET']))
    if wname not in wenjuan_list1:
        test_type = request.form.get("test_type")
        img = request.files.get(input_type + '_' + 'photo')
        save_path = basedir.replace('\\', '/') + "/static/images/"
        name_List = img.filename.split('.')
        if name_List[0] == '':  # 未提交文件时
            img_name = "默认问卷头像.jpg"  # 绝对路径
            return redirect(url_for('wenjuan.input_question', input_type=input_type, wname=wname, test_type=test_type,
                                    img_name=img_name))
        else:
            if name_List[-1] in ALLOWED_EXTENSIONS:  # 上传的图片的格式是所规定的
                img.filename = g.user.username + time.strftime("%Y%m%d%H%M%S", time.localtime()) + '.' + name_List[-1]
                # 保存图片的名称以用户名+当前时间组成，保证不重复
                file_path = save_path + img.filename
                img.save(file_path)
                img_name = img.filename
                return redirect(
                    url_for('wenjuan.input_question', input_type=input_type, wname=wname, test_type=test_type,
                            img_name=img_name))


'''@bp.route("/one_by_one_input", methods=['GET', 'POST'])
@login_required
def one_by_one_input():
    if request.method == "GET":
        return render_template("input_question.html")
    return redirect(url_for("wenjuan.input_question"))

@bp.route("/same_option_input", methods=['GET', 'POST'])
@login_required
def same_option_input():
    if request.method == "GET":
        return render_template("input_question.html")
    return redirect(url_for("wenjuan.input_question"))'''


@bp.route("/del_wenjuan_answer/<wname>", methods=['GET', 'POST'])
def del_wenjuan_answer(wname):
    test_times_model = TesttimesModel.query.filter_by(u_id=g.user.id, wenjuan_name=wname)[0]
    wenjuan_answer = WenjuanAnswerModel.query.filter_by(wenjuan_name=wname).filter_by(wenjuan_uid=g.user.id).filter_by(
        test_times=test_times_model.test_times).all()
    wenjuan_exts = WenjuanExtsModel.query.filter_by(wenjuan_name=wname).filter_by(u_id=g.user.id).filter_by(
        test_times=test_times_model.test_times).first()
    for each in wenjuan_answer:
        db.session.delete(each)
        db.session.commit()
    db.session.delete(wenjuan_exts)
    test_times_model.test_times = test_times_model.test_times - 1
    db.session.commit()
    return redirect(url_for("wenjuan.kinds_of_wenjuan"))


@bp.route("/psyc_del_wenjuan", methods=['GET', 'POST'])
def psyc_del_wenjuan():
    if request.method == "GET":
        wenjuan_list1 = []
        wenjuan_list0 = WenjuanModel.query.filter_by(u_id=g.user.id).with_entities(
            WenjuanModel.wenjuan_name).distinct().all()
        print("wenjuan_list0", wenjuan_list0)
        for x in wenjuan_list0:
            wenjuan_list1.append(x[0])  # 把问卷名取出并去重
        return render_template("del_wenjuan.html", wenjuan_list1=wenjuan_list1)
    else:
        wname = request.form.get("wname")
        wenjuan = WenjuanModel.query.filter_by(wenjuan_name=wname).all()
        one_of_wenjuan = WenjuanModel.query.filter_by(wenjuan_name=wname)[0]
        for each in wenjuan:
            db.session.delete(WenjuanModel.query.get(each.id))
            db.session.commit()
        path = basedir.replace('\\', '/') + "/static/images/"
        file_path = path + one_of_wenjuan.img_name
        if one_of_wenjuan.img_name != '默认问卷头像.jpg':
            os.remove(file_path)
        return redirect(url_for("first_page"))


@bp.route("/kinds_of_wenjuan", methods=['GET', 'POST'])
@login_required
def kinds_of_wenjuan():
    wenjuan_list1 = []
    wenjuan_list0 = WenjuanModel.query.with_entities(WenjuanModel.wenjuan_name).distinct().all()
    for x in wenjuan_list0:
        wenjuan_list1.append(x[0])  # 把问卷名取出并去重
    all_wenjuan = []
    for each in wenjuan_list1:
        all_wenjuan.append(WenjuanModel.query.filter_by(wenjuan_name=each)[0])
    return render_template('show_all_wenjuan.html', all_wenjuan=all_wenjuan)


@bp.route("/report_to_pdf/<wname>/<int:point>/<level>/<int:test_times>/", methods=['GET', 'POST'])
def report_to_pdf(wname, point, level, test_times):
    wenjuan_exts = WenjuanExtsModel.query.filter_by(u_id=g.user.id).filter_by(wenjuan_name=wname).filter_by(
        test_times=test_times).first()
    path = basedir.replace('\\', '/') + '/'
    config = imgkit.config(wkhtmltoimage="D:/毕设项目/wkhtmltopdf/bin/wkhtmltoimage.exe")
    img_name = g.user.username + wname + '第{}次'.format(str(test_times)) + '_report' + '.jpg'
    file_path = path + img_name
    imgkit.from_string('问卷名————' + wname+'第{}次测试'.format(test_times) + '； 分数————' + str(point) + '； 心理健康状态————' + level, img_name, config=config)
    with open(file_path, "rb") as f:
        # b64encode是编码，b64decode是解码
        base64_data = base64.b64encode(f.read())
        # base64.b64decode(base64data)
    wenjuan_exts.report_base64 = base64_data
    db.session.commit()
    os.remove(file_path)
    return redirect(url_for('wenjuan.test_report'))


@bp.route("/change_wenjuan/<wname>/<judgment>", methods=['GET', 'POST'])
def change_wenjuan(wname, judgment):
    wenjuan = WenjuanModel.query.filter_by(wenjuan_name=wname).all()
    img = request.files.get('photo')
    save_path = basedir.replace('\\', '/') + "/static/images/"
    name_List = img.filename.split('.')
    span = ''
    len_of_wenjuan = len(wenjuan)
    len_of_option = []
    for ee in wenjuan:
        len_of_option.append(len(ee.option.split(' ')))
    if request.form.get("is_default") == 'not_default':  # 未选择默认
        for i in range(1, int(request.form.get("span_num")) + 1):
            span = span + request.form.get("span" + str(i) + 'min') + '|' + request.form.get(
                "span" + str(i) + "norm") + '|' + request.form.get("span" + str(i) + 'max')
            span = span + ' '
        span = span[:len(span) - 1]  # 删除掉最后的一个空格
    else:
        span = judgment
    if name_List[0] == '':  # 未提交文件时
        for xx in range(len_of_wenjuan):
            wenjuan[xx].exercise_title = request.form.get("title" + str(xx))
            option = ''
            point=''
            for yy in range(len_of_option[xx]):
                option = option + request.form.get("option" + str(xx) + str(yy))
                point= point+request.form.get("point" + str(xx) + str(yy))
                option = option + ' '
                point=point+' '
            option = option[:len(option) - 1]
            point = point[:len(point)-1]
            wenjuan[xx].option = option
            wenjuan[xx].option_point = point
            wenjuan[xx].judgment = judgment
            wenjuan[xx].judgment = span
            wenjuan[xx].wenjuan_name = request.form.get("wname")
            wenjuan[xx].test_type = request.form.get("test_type")
            db.session.commit()
        return redirect(url_for('first_page'))
    else:
        if name_List[-1] in ALLOWED_EXTENSIONS:  # 上传的图片的格式是所规定的
            img.filename = g.user.username + time.strftime("%Y%m%d%H%M%S", time.localtime()) + '.' + name_List[-1]
            # 保存图片的名称以用户名+当前时间组成，保证不重复
            file_path = save_path + img.filename
            img.save(file_path)
            for xx in range(len_of_wenjuan):
                wenjuan[xx].exercise_title = request.form.get("title" + str(xx))
                option = ''
                point = ''
                for yy in range(len_of_option[xx]):
                    option = option + request.form.get("option" + str(xx) + str(yy))
                    point = point + request.form.get("point" + str(xx) + str(yy))
                    option = option + ' '
                    point = point + ' '
                option = option[:len(option) - 1]
                point = point[:len(point) - 1]
                wenjuan[xx].option = option
                wenjuan[xx].option_point = point
                wenjuan[xx].judgment = judgment
                wenjuan[xx].judgment = span
                wenjuan[xx].wenjuan_name = request.form.get("wname")
                wenjuan[xx].img_name = img.filename
                wenjuan[xx].judgment = span
                wenjuan[xx].wenjuan_name = request.form.get("wname")
                wenjuan[xx].test_type = request.form.get("test_type")
                db.session.commit()
        return redirect(url_for('first_page'))


@bp.route("/before_change_wenjuan", methods=['GET', 'POST'])
def before_change_wenjuan():
    wname = request.form.get("wenjuan_name")
    Max = 0
    Min = 0
    one_of_wenjuan = WenjuanModel.query.filter_by(wenjuan_name=wname)[0]
    wenjuan = WenjuanModel.query.filter_by(wenjuan_name=wname).all()
    option_list = []
    len_of_wenjuan = len(wenjuan)
    len_of_option = []
    point_list = []
    for ee in range(len_of_wenjuan):
        option_list.append(wenjuan[ee].option.split(' '))
        len_of_option.append(len(wenjuan[ee].option.split(' ')))
        point_list.append(str(wenjuan[ee].option_point).split(' '))
    print("point_list",point_list)
    for ii in point_list:
        Max = Max + int(ii[-1])
        Min = Min + int(ii[0])
    if one_of_wenjuan.judgment == '无':
        Step = (Max - Min) / 4
        span_min = Min
        span_max = Min + Step
        span_list = ['#', [span_min, span_max]]
        for i in range(1, 4):  # 划分区间
            span_min = span_max
            if span_min + Step > Max:
                span_max = Max
            else:
                span_max = span_min + Step
            span_list.append([span_min, span_max])
        judgment = str(span_list[1][0]) + '|正常|' + str(span_list[1][1]) + ' ' + str(span_list[2][0]) + '|轻度|' + str(
            span_list[2][1]) + ' ' + str(span_list[3][0]) + '|中度|' + str(span_list[3][1]) + ' ' + str(
            span_list[4][0]) + '|重度|' + str(span_list[4][1])
        tag_list = PsychologistModel.query.filter_by(u_id=g.user.id)[0].tag.split(' ')
        span_list1 = ['#']
        for each in judgment.split(" "):
            List1 = []
            for each1 in each.split('|'):
                List1.append(each1)
            span_list1.append(List1)
        return render_template('psyc_change_wenjuan.html', len_of_wenjuan=len_of_wenjuan, len_of_option=len_of_option,
                               option_list=option_list, all_wenjuan=wenjuan, wenjuan=one_of_wenjuan, wname=wname,
                               judgment=judgment, len_of_judgment=len(span_list), Max=Max, Min=Min,point_list=point_list,
                               span_list=span_list1, tag_list=tag_list)
    else:
        judgment = one_of_wenjuan.judgment
        span_list = ['#']
        for key in judgment.split(' '):
            span_list.append(key.split('|'))
        tag_list = PsychologistModel.query.filter_by(u_id=g.user.id)[0].tag.split(' ')
        return render_template('psyc_change_wenjuan.html', len_of_wenjuan=len_of_wenjuan, len_of_option=len_of_option,
                               option_list=option_list, all_wenjuan=wenjuan, wenjuan=one_of_wenjuan, wname=wname,
                               judgment=judgment, len_of_judgment=len(span_list), Max=Max, Min=Min, span_list=span_list,
                               point_list=point_list,tag_list=tag_list)


@bp.route("/wenjuan_report/<wname>/<int:test_times>", methods=['GET', 'POST'])
def wenjuan_report(wname, test_times):
    test_times_model = TesttimesModel.query.filter_by(u_id=g.user.id).filter_by(wenjuan_name=wname)[0]
    test_times = test_times_model.test_times
    w_answer = WenjuanAnswerModel.query.filter_by(wenjuan_name=wname).filter_by(wenjuan_uid=g.user.id).filter_by(
        test_times=test_times).all()
    one_of_wenjuan = WenjuanModel.query.filter_by(wenjuan_name=wname)[0]
    wenjuan = WenjuanModel.query.filter_by(wenjuan_name=wname).all()
    all_psyc = PsychologistModel.query.all()
    tag_list = []
    point_list = []
    Max = 0
    Min = 0
    len_of_wenjuan = len(wenjuan)
    print(len_of_wenjuan)
    for ee in range(len_of_wenjuan):
        point_list.append(str(wenjuan[ee].option_point).split(' '))
    for ii in point_list:
        Max = Max + int(ii[-1])
        Min = Min + int(ii[0])
    for key in all_psyc:
        tag_list.append(str(key.tag).split(' '))
    for i in range(len(all_psyc)):
        tag_list[i].append(all_psyc[i])  # 在每一个标签的后面加上心理医生对象
        tag_list[i].append(UserModel.query.filter_by(id=all_psyc[i].u_id)[0])
    print(tag_list)
    span_list = []
    for each in str(one_of_wenjuan.judgment).split(' '):
        print(each.split('|'))
        span_list.append(each.split('|'))
    print(span_list)
    Sum = 0
    for kk in w_answer:
        Sum = Sum + kk.point
    print("Sum:", Sum)
    print(type(Sum))
    level = ''
    for key in span_list:
        if float(Sum) > float(key[-1]):
            continue
        elif float(Sum) >= float(key[0]) and float(Sum) <= float(key[-1]):
            level = key[1]
    return render_template('wenjuan_report.html', wname=wname, level=level, degree=Sum, one_of_wenjuan=one_of_wenjuan,
                           tag_list=tag_list, Min=Min, Max=Max, test_times=test_times)


@bp.route("/add_to_wenjuan", methods=['GET', 'POST'])
def add_to_wenjuan():
    if request.method == "GET":
        wenjuan_list1 = []
        wenjuan_list0 = WenjuanModel.query.filter_by(u_id=g.user.id).with_entities(
            WenjuanModel.wenjuan_name).distinct().all()
        for x in wenjuan_list0:
            wenjuan_list1.append(x[0])  # 把问卷名取出并去重
        return render_template("add_to_wenjuan.html", wenjuan_list1=wenjuan_list1)
    else:
        wname = request.form.get("wname")
        one_of_wenjuan = WenjuanModel.query.filter_by(wenjuan_name=wname)[0]
        title_list0 = request.form.get("title").split("\n")
        title_list1 = []
        point = request.form.get("point")
        option = request.form.get("options")
        print("point", point, len(point.split(' ')))
        print("option", request.form.get("options"), len(request.form.get("options").split()))
        if len(point.split(' ')) != len(request.form.get("options").split()):
            # return render_template("404_error.html", msg='选项个数与分值个数！')
            flash('选项个数与分值个数不同！')
            return redirect(url_for('wenjuan.add_to_wenjuan', method=['GET']))
        else:
            # test_type = request.form.get("test_type")
            # wname = request.form.get("wname")
            for each in title_list0:
                title_list1.append(each.replace(' ', '').replace('\r', ''))
            for each in title_list1:
                exercise_title = each
                exercise_type = "radio"
                wenjuan = WenjuanModel(exercise_title=exercise_title, option=option, exercise_type=exercise_type,
                                       wenjuan_name=wname, option_point=point, test_type=one_of_wenjuan.test_type,
                                       u_id=g.user.id,
                                       img_name=one_of_wenjuan.img_name, judgment=one_of_wenjuan.judgment)
                db.session.add(wenjuan)
                db.session.commit()
            return redirect(url_for('wenjuan.add_to_wenjuan', method=['GET']))


@bp.route("/wenjuan_search", methods=['GET', 'POST'])
def wenjuan_search():
    name = request.form.get("wenjuan_search")
    print("name:", name)
    wenjuan_list1 = []
    wenjuan_list0 = WenjuanModel.query.filter(WenjuanModel.wenjuan_name.contains(name)).with_entities(
        WenjuanModel.wenjuan_name).distinct().all()
    for x in wenjuan_list0:
        wenjuan_list1.append(x[0])  # 把问卷名取出并去重
    all_wenjuan = []
    for each in wenjuan_list1:
        all_wenjuan.append(WenjuanModel.query.filter_by(wenjuan_name=each)[0])
    return render_template('show_all_wenjuan.html', all_wenjuan=all_wenjuan)


@bp.route("/amd_show_wenjuan/<wname>", methods=['GET', 'POST'])
def amd_show_wenjuan(wname):
    wenjuan = WenjuanModel.query.filter_by(wenjuan_name=wname).all()
    author = PsychologistModel.query.filter_by(u_id=wenjuan[0].u_id).all()
    print(author,)
    return render_template('amd_show_wenjuan.html', wname=wname, wenjuan=wenjuan)


@bp.route("/amd_change_wenjuan/<int:wid>/<wname>", methods=['GET', 'POST'])
def amd_change_wenjuan(wid, wname):
    wenjuan_change = WenjuanModel.query.filter_by(id=wid).first()
    wenjuan_change.exercise_title = request.form.get("exercise_title")
    wenjuan_change.option = request.form.get("option")
    wenjuan_change.option_point = request.form.get("option_point")
    db.session.commit()
    return redirect(url_for('wenjuan.amd_show_wenjuan', wname=wname))


@bp.route("/amd_del_wenjuan/<int:wid>/<wname>", methods=['GET', 'POST'])
def amd_del_wenjuan(wid, wname):
    db.session.execute('DELETE FROM wenjuan WHERE id={}'.format(wid))
    db.session.commit()
    wenjuan_answer=WenjuanAnswerModel.query.filter_by(wenjuan_name=wname).all()
    test_times_list=TesttimesModel.query.filter_by(wenjuan_name=wname).all()
    wenjuan_exts_list=WenjuanExtsModel.query.filter_by(wenjuan_name=wname).all()
    if len(wenjuan_answer)==0:#此时该问卷的题目已经被删除了
        for each in test_times_list:
            each.test_times=0
            db.session.commit()
        for ee in wenjuan_exts_list:
            db.session.execute('DELETE FROM wenjuan_exts WHERE id={}'.format(ee.id))
            db.session.commit()
    return redirect(url_for('wenjuan.amd_show_wenjuan', wname=wname))


@bp.route("/amd_add_wenjuan/<wname>", methods=['GET', 'POST'])
def amd_add_wenjuan(wname):
    one_of_wenjuan = WenjuanModel.query.filter_by(wenjuan_name=wname).first()
    exercise_title = request.form.get("exercise_title")
    option = request.form.get("option")
    option_point = request.form.get("option_point")
    wenjuan = WenjuanModel(exercise_title=exercise_title, option=option, exercise_type="radio", wenjuan_name=wname,
                           option_point=option_point, img_name=one_of_wenjuan.img_name, test_type=one_of_wenjuan.test_type,
                           judgment=one_of_wenjuan.judgment, u_id=one_of_wenjuan.u_id)
    db.session.add(wenjuan)
    db.session.commit()
    return redirect(url_for('wenjuan.amd_show_wenjuan', wname=wname))
