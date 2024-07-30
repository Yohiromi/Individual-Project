import json

from flask import Flask, session, g, render_template, url_for, request,redirect
#   g变量是python独有的一种全局变量
from sqlalchemy import and_

import config
from decorators import login_required
from exts import db
from blueprints import QA_bp
from blueprints import user_bp
from blueprints import wenjuan_bp
from blueprints import psychologist_bp
from exts import mail
from flask_migrate import Migrate
from models import UserModel, WenjuanModel, StudentUserExtsModel, PsychologistModel,PrivateMessagesModel,TesttimesModel,WenjuanAnswerModel,WenjuanExtsModel

from datetime import datetime

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
mail.init_app(app)

migrate=Migrate(app,db)

app.register_blueprint(QA_bp)
app.register_blueprint(user_bp)
app.register_blueprint(wenjuan_bp)
app.register_blueprint(psychologist_bp)
#页面请求来了->  before_request -> 视图函数 -> 视图返回页面 -> context_processor

#钩子函数，每次进入页面前就调用
@app.before_request
def before_request():
    user_id=session.get("user_id")
    if user_id:
        try:
            user=UserModel.query.get(user_id)
            #给g绑定一个叫user的变量，它的值是user的值
            g.user=user
        except:
            g.user=None
            pass

#上下文处理器：所有页面都会执行这个函数
@app.context_processor
def context_processor():
    if hasattr(g,"user"):
        if g.user.identity=="学生":
            user_exts = StudentUserExtsModel.query.filter(StudentUserExtsModel.u_id == g.user.id)[0]

            private_msg_num1=[]
            private_msg_num0 = PrivateMessagesModel.query.filter_by(author_id=g.user.id).filter_by(msg_type="answer").with_entities(PrivateMessagesModel.psyc_id).distinct().all()
            for x in private_msg_num0:
                private_msg_num1.append(x[0])
            psyc_list=[]
            psyc_user_list = []
            for ii in range(len(private_msg_num1)):
                psyc_list.append(PsychologistModel.query.filter_by(id=private_msg_num1[ii])[0])
                psyc_user_list.append(UserModel.query.filter_by(id=PsychologistModel.query.filter_by(id=private_msg_num1[ii])[0].u_id).first())
            return {"user": g.user, "user_exts": user_exts,"len_of_user_msg":len(private_msg_num1),"psyc_list":psyc_list,"psyc_user_list":psyc_user_list}
        elif g.user.identity == "心理医生":
            psyc = PsychologistModel.query.filter_by(u_id=g.user.id)[0]
            private_msg_num1=[]
            private_msg_num0 = PrivateMessagesModel.query.filter_by(psyc_id=PsychologistModel.query.filter_by(u_id=g.user.id)[0].id).filter_by(msg_type="question").with_entities(PrivateMessagesModel.author_id).distinct().all()
            for x in private_msg_num0:
                private_msg_num1.append(x[0])
            user_list=[]
            for ii in range(len(private_msg_num1)):
                user_list.append(UserModel.query.filter_by(id=private_msg_num1[ii])[0])
            psyc_exts=PsychologistModel.query.filter(PsychologistModel.u_id == g.user.id)[0]
            return {"user":g.user,"psyc_exts":psyc_exts,"psyc":psyc,"len_of_msg":len(private_msg_num1),"user_list":user_list,"user_exts": psyc_exts}
        else:
            wenjuan_list1 = []
            wenjuan_list0 = WenjuanModel.query.with_entities(WenjuanModel.wenjuan_name).distinct().all()
            for x in wenjuan_list0:
                wenjuan_list1.append(x[0])  # 把问卷名取出并去重
            all_wenjuan=[]
            for each in wenjuan_list1:
                all_wenjuan.append(WenjuanModel.query.filter_by(wenjuan_name=each)[0])
            user_exts = StudentUserExtsModel.query.filter(StudentUserExtsModel.u_id == g.user.id)[0]
            return {"user": g.user, "user_exts": user_exts,"amd_all_wenjuan":all_wenjuan}
    else:
        return {}
@app.route("/")
@login_required
def first_page():
    if not g.user:
        return render_template("first_page.html")
    if g.user.jurisdiction=='普通用户':
        if g.user.identity=="学生":
            return redirect(url_for('psychologist.show_psychologist'))
        if g.user.identity=="心理医生":
            wenjuan_list1 = []
            wenjuan_list0 = WenjuanModel.query.filter_by(u_id=g.user.id).with_entities(WenjuanModel.wenjuan_name).distinct().all()
            for x in wenjuan_list0:
                wenjuan_list1.append(x[0])  # 把问卷名取出并去重
            all_wenjuan=[]
            for each in wenjuan_list1:
                all_wenjuan.append(WenjuanModel.query.filter_by(wenjuan_name=each)[0])
            return render_template('psyc_index.html',all_wenjuan=all_wenjuan)
    if g.user.jurisdiction=='管理员':
        all_user = UserModel.query.all()
        time_now=datetime.now().strftime('%Y-%m-%d %H:%M:%S')#时间变量转为字符串
        time_now=datetime.strptime(time_now,'%Y-%m-%d %H:%M:%S')#字符串转换为时间变量
        time_dir={}
        for ii in range(len(all_user)):
            time_sub=time_now-all_user[ii].join_time
            if time_sub.days in time_dir:
                time_dir[time_sub.days]+=1
            else:
                time_dir[time_sub.days]=1
        answer_dir={}
        test_times_model_copy=TesttimesModel.query.all()
        test_times_model=[]
        for each in test_times_model_copy:
            if each.test_times!=0:
                test_times_model.append(each)
        for ee in test_times_model:
            if ee.wenjuan_name in answer_dir:
                answer_dir[ee.wenjuan_name]+=1
            else:
                answer_dir[ee.wenjuan_name]=1
        wenjuan_all=WenjuanExtsModel.query.all()
        one_of_wenjuan_answer=[]
        answer_now_dir={}
        for key in wenjuan_all:
            one_of_wenjuan_answer.append(WenjuanAnswerModel.query.filter_by(wenjuan_name=key.wenjuan_name,wenjuan_uid=key.u_id,test_times=key.test_times).first())
        for kk in one_of_wenjuan_answer:
            if (time_now-kk.create_time).days==0:
                if kk.wenjuan_name in answer_now_dir:
                    answer_now_dir[kk.wenjuan_name]+=1
                else:
                    answer_now_dir[kk.wenjuan_name]= 1
        print(answer_now_dir)
        return render_template("amd_index.html",time_dir=time_dir,answer_dir=answer_dir,answer_now_dir=answer_now_dir)
if __name__ == '__main__':
    app.run(debug=True)
