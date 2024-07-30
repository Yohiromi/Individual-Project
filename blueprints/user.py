import os
import time
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session, flash, g

from decorators import login_required
from exts import mail, db
from flask_mail import Message
from models import EmailCaptchaModel, UserModel, StudentUserExtsModel, PsychologistModel, PrivateMessagesModel, FollowModel,WenjuanModel
import string
import random
from .forms import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
import base64
from datetime import datetime
bp = Blueprint("user", __name__, url_prefix="/user")

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))  # 返回本项目的绝对路径
ALLOWED_EXTENSIONS = ['png', 'jpg', 'JPG', 'PNG', 'gif', 'GIF', 'jpeg', 'JPEG']  # 此为允许上传的图片格式


@bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user1 = UserModel.query.filter_by(email=email).first()
            # 查看登录者的身份

            if user1 and check_password_hash(user1.password, password):
                session['user_id'] = user1.id
                return redirect("/")
            else:
                flash("邮箱和密码不匹配！")
                return redirect(url_for("user.login"))
        else:
            flash("邮箱或密码格式错误！")
            return redirect(url_for("user.login"))


@bp.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        form = RegisterForm(request.form)  # request.form会存储前端返回的表单
        if form.validate():
            username = form.username.data
            email = form.email.data
            jurisdiction = "普通用户"  # 权限
            img_path = basedir.replace('\\', '/') + "/static/images/" + "默认用户头像.jpg"  # 绝对路径
            img_name = "默认用户头像.jpg"

            with open(img_path, "rb") as f:
                # b64encode是编码，b64decode是解码
                base64_data = base64.b64encode(f.read())
                # base64.b64decode(base64data)

            captcha = form.captcha.data
            password = form.password.data
            # 用md5对用户进行加密
            hash_password = generate_password_hash(password)
            identity = request.form.get("identity")
            user = UserModel(email=email, username=username, password=hash_password, identity=identity,
                             jurisdiction=jurisdiction, img_name=img_name,
                             img_base64=str(base64_data)[1:].replace("'", ''))
            db.session.add(user)
            db.session.commit()
            User=UserModel.query.filter_by(email=email)[0]
            if User.identity == "学生" or User.identity == "管理员":
                stu_exts = StudentUserExtsModel(name="name", gender="gender", age=0, tel="tel", school="school",
                                                major="major",
                                                grade="grade", u_id=User.id, Users=User)
                db.session.add(stu_exts)
                db.session.commit()
            elif User.identity == "心理医生":
                psyc = PsychologistModel(name="name", age=0, gender="gender", tag="tag", question_times=0,
                                         answer_times=0, follow_times=0, u_id=User.id, Users=User)
                db.session.add(psyc)
                db.session.commit()
            return redirect(url_for("user.login"))
        else:
            return redirect(url_for("user.login"))


@bp.route("/captcha", methods=['POST'])
def get_captcha():
    email = request.form.get("email")
    letters = string.ascii_letters + string.digits
    captcha = "".join(random.sample(letters, 4))
    if email:
        message = Message(
            subject="TEST",
            recipients=[email],
            body="您好您的验证码为：{}".format(captcha),
        )
        mail.send(message)
        captcha_model = EmailCaptchaModel.query.filter_by(email=email).first()
        if captcha_model:
            captcha_model.captcha = captcha
            captcha_model.creat_time = datetime.now()
            db.session.commit()
        else:
            captcha_model = EmailCaptchaModel(email=email, captcha=captcha)
            db.session.add(captcha_model)
            db.session.commit()
        print("captcha", captcha)
        # code:200，表示请求成功
        return jsonify({"code": 200})
    else:
        # code：400，表示客户端错误
        return jsonify({"code": 400, "message": "请先输入邮箱！"})


@bp.route("/del_user/<int:u_id>")
def del_user(u_id):
    user=UserModel.query.filter_by(id=u_id)[0]
    db.session.execute('DELETE FROM user WHERE id={}'.format(u_id))
    db.session.commit()
    return redirect(url_for("user.show_users"))

@bp.route("/logout")
def logout():
    # 清除session中所有的内容
    session.clear()
    return redirect(url_for("user.login"))


@bp.route("/user_central")
def user_central():
    # 跳转到用户中心
    user = UserModel.query.get(g.user.id)
    psyc_id_list1 = []
    psyc_id_list0 = PrivateMessagesModel.query.filter_by(author_id=g.user.id).filter_by(
        msg_type="answer").with_entities(PrivateMessagesModel.psyc_id).distinct().all()
    for x in psyc_id_list0:
        psyc_id_list1.append(x[0])

    psyc_user_list = []

    psyc_list = []

    for each in psyc_id_list1:  # 取出所有答复学生的心理医生和心理医生对应的用户
        psyc_list.append(PsychologistModel.query.filter_by(id=each)[0])
        psyc_user_list.append(UserModel.query.filter_by(id=PsychologistModel.query.filter_by(id=each)[0].u_id)[0])

    return render_template("user_central.html", user=user, psyc_user_list=psyc_user_list, psyc_list=psyc_list,
                           len_of_psyc=len(psyc_list))


''''@bp.route("/show_user_change")
def show_user_change():
    #查询出要改的用户
    user = UserModel.query.get(g.user.id)
    user_exts=StudentUserExtsModel.query.filter(StudentUserExtsModel.u_id == g.user.id)[0]
    return render_template("change_user_central.html",user=user,user_exts=user_exts)'''

@bp.route("/defollow_psyc/<int:p_id>/<follow_type>", methods=['GET', 'POST'])  # 关注
def defollow_psyc(p_id, follow_type):
    if follow_type == '取消关注':
        is_follow = FollowModel.query.filter_by(
            stu_id=StudentUserExtsModel.query.filter_by(u_id=g.user.id)[0].id).filter_by(psyc_id=p_id).first()
        psyc = PsychologistModel.query.filter_by(id=p_id)[0]
        psyc.follow_times = psyc.follow_times - 1
        db.session.delete(is_follow)
        db.session.commit()
        return redirect(url_for('first_page'))


@bp.route("/change_user", methods=['GET', 'POST'])
def change_user():
    if request.method == "GET":
        user_exts = StudentUserExtsModel.query.filter(StudentUserExtsModel.u_id == g.user.id)[0]
        return render_template("change_user_central.html", user=g.user, user_exts=user_exts)
    else:
        img = request.files.get('photo')
        path = basedir.replace('\\', '/') + "/static/images/"
        List = img.filename.split('.')
        result = UserModel.query.filter(UserModel.id == g.user.id)[0]
        search = StudentUserExtsModel.query.filter(StudentUserExtsModel.u_id == g.user.id)[0]
        search.name = request.form.get("name")
        search.gender = request.form.get("gender")
        search.age = request.form.get("age")
        search.tel = request.form.get("tel")
        search.school = request.form.get("school")
        search.major = request.form.get("major")
        search.grade = request.form.get("grade")
        username_1 = g.user.username
        if List[0] == '':
            db.session.commit()
            return redirect(url_for("user.user_central"))
        if List[0] != '':
            if List[1] in ALLOWED_EXTENSIONS:
                img.filename = username_1 + time.strftime("%Y%m%d%H%M%S", time.localtime()) + '.' + List[1]
                # 保存图片的名称以用户名+当前时间组成，保证不重复
                file_path = path + img.filename
                img.save(file_path)
                if float(format(os.path.getsize(file_path) / 1024, '.1f')) > 30:
                    flash("图片过大！")
                    os.remove(file_path)
                    return redirect(url_for("user.change_user"))
                else:
                    with open(file_path, "rb") as f:
                        # b64encode是编码，b64decode是解码
                        base64_data = base64.b64encode(f.read())
                        # base64.b64decode(base64data)
                    result.img_name = img.filename
                    result.img_base64 = str(base64_data)[1:].replace("'", '')
                    db.session.commit()
                    os.remove(file_path)
                    return redirect(url_for("user.user_central"))

#---------------------后台管理---用户
@bp.route("/amd_change_user/<int:u_id>", methods=['GET', 'POST'])  # 关注
def amd_change_user(u_id):
    img = request.files.get('photo')
    path = basedir.replace('\\', '/') + "/static/images/"
    List = img.filename.split('.')
    username=request.form.get("username")
    email=request.form.get("email")
    result = UserModel.query.filter_by(id=u_id)[0]
    result.username=username
    result.email=email
    if List[0] == '':
        db.session.commit()
        return redirect(url_for("user.show_users"))
    if List[0] != '':
        if List[1] in ALLOWED_EXTENSIONS:
            img.filename = username + time.strftime("%Y%m%d%H%M%S", time.localtime()) + '.' + List[1]
            # 保存图片的名称以用户名+当前时间组成，保证不重复
            file_path = path + img.filename
            img.save(file_path)
            if float(format(os.path.getsize(file_path) / 1024, '.1f')) > 30:
                os.remove(file_path)
                return render_template('404_error.html',msg='图片过大！')
            else:
                with open(file_path, "rb") as f:
                    # b64encode是编码，b64decode是解码
                    base64_data = base64.b64encode(f.read())
                    # base64.b64decode(base64data)
                result.img_name = img.filename
                result.img_base64 = str(base64_data)[1:].replace("'", '')
                db.session.commit()
                os.remove(file_path)
                return redirect(url_for("user.show_users"))

        else:
            return render_template('404_error.html', msg='图片格式不符合！')
@bp.route("/show_users")
def show_users():
    all_users = UserModel.query.all()
    print(all_users)
    return render_template("show_users.html", all_users=all_users)

@bp.route("/amd_add_user", methods=['GET', 'POST'])
def amd_add_user():
    img = request.files.get('photo')
    path = basedir.replace('\\', '/') + "/static/images/"
    List = img.filename.split('.')
    username=request.form.get("username")
    email=request.form.get("email")
    password=request.form.get("password")
    identity=request.form.get("identity")
    jurisdiction=request.form.get("jurisdiction")
    hash_password = generate_password_hash(password)
    if List[0] == '':
        img_path = basedir.replace('\\', '/') + "/static/images/" + "默认用户头像.jpg"  # 绝对路径
        img_name = "默认用户头像.jpg"
        with open(img_path, "rb") as f:
            # b64encode是编码，b64decode是解码
            base64_data = base64.b64encode(f.read())
            # base64.b64decode(base64data)
        user = UserModel(email=email, username=username, password=hash_password, identity=identity,
                         jurisdiction=jurisdiction, img_name=img_name,
                         img_base64=str(base64_data)[1:].replace("'", ''))
        db.session.add(user)
        db.session.commit()
        User = UserModel.query.filter_by(email=email)[0]
        if User.identity == "学生" or User.identity == "管理员":
            stu_exts = StudentUserExtsModel(name="name", gender="gender", age=0, tel="tel", school="school",
                                            major="major",
                                            grade="grade", u_id=User.id, Users=User)
            db.session.add(stu_exts)
            db.session.commit()
        elif User.identity == "心理医生":
            psyc = PsychologistModel(name="name", age=0, gender="gender", tag="tag", question_times=0,
                                     answer_times=0, follow_times=0, u_id=User.id, Users=User)
            db.session.add(psyc)
            db.session.commit()
        return redirect(url_for("user.show_users"))
    else:
        if List[1] in ALLOWED_EXTENSIONS:
            img.filename = username + time.strftime("%Y%m%d%H%M%S", time.localtime()) + '.' + List[1]
            # 保存图片的名称以用户名+当前时间组成，保证不重复
            file_path = path + img.filename
            img.save(file_path)
            if float(format(os.path.getsize(file_path) / 1024, '.1f')) > 30:
                os.remove(file_path)
                return render_template('404_error.html',msg='图片过大！')
            else:
                with open(file_path, "rb") as f:
                    # b64encode是编码，b64decode是解码
                    base64_data = base64.b64encode(f.read())
                    # base64.b64decode(base64data)
            user = UserModel(email=email, username=username, password=hash_password, identity=identity,
                             jurisdiction=jurisdiction, img_name=img.filename,
                             img_base64=str(base64_data)[1:].replace("'", ''))
            db.session.add(user)
            db.session.commit()
            User=UserModel.query.filter_by(email=email)[0]
            if User.identity == "学生" or User.identity == "管理员":
                stu_exts = StudentUserExtsModel(name="name", gender="gender", age=0, tel="tel", school="school",
                                                major="major",
                                                grade="grade", u_id=User.id, Users=User)
                db.session.add(stu_exts)
                db.session.commit()
            elif User.identity == "心理医生":
                psyc = PsychologistModel(name="name", age=0, gender="gender", tag="tag", question_times=0,
                                         answer_times=0, follow_times=0, u_id=User.id, Users=User)
                db.session.add(psyc)
                db.session.commit()
        return redirect(url_for("user.show_users"))



#---------------------后台管理---心理医生
@bp.route("/amd_show_psyc")
def amd_show_psyc():
    all_psyc = PsychologistModel.query.all()
    return render_template("amd_show_psyc.html", all_psyc=all_psyc)


@bp.route("/amd_del_psyc/<int:psyc_id>")
def amd_del_psyc(psyc_id):
    psyc=PsychologistModel.query.filter_by(id=psyc_id)[0]
    db.session.execute('DELETE FROM psychologist WHERE id={}'.format(psyc_id))
    db.session.execute('DELETE FROM user WHERE id={}'.format(psyc.u_id))
    db.session.commit()
    return redirect(url_for("user.amd_show_psyc"))


@bp.route("/amd_change_psyc/<int:psyc_id>", methods=['GET', 'POST'])
def amd_change_psyc(psyc_id):
    psyc=PsychologistModel.query.filter_by(id=psyc_id)[0]
    wenjuan=WenjuanModel.query.filter_by(u_id=psyc.u_id).all()
    wenjuan_type_list1 = []
    wenjuan_type_list0 = WenjuanModel.query.filter_by(u_id=psyc.u_id).with_entities(WenjuanModel.test_type).distinct().all()
    for x in wenjuan_type_list0:
        wenjuan_type_list1.append(x[0])
    print(wenjuan_type_list1)
    tag = request.form.get("tag")
    flag=0
    for each in wenjuan_type_list1:
        if each in tag:
            flag=flag+1
    if flag==0:#tag被修改后，提交的问卷的类型中没有符合该tag列表的
        for key in wenjuan:
            key.test_type='tag'

    psyc.name=request.form.get('name')
    psyc.gender = request.form.get('gender')
    psyc.age = request.form.get('age')
    psyc.tag = tag
    db.session.commit()
    return redirect(url_for('user.amd_show_psyc'))




#---------------------后台管理---学生

@bp.route("/amd_show_stu")
def amd_show_stu():
    all_stu = StudentUserExtsModel.query.all()
    return render_template("amd_show_students.html", all_stu=all_stu)

@bp.route("/amd_del_stu/<int:stu_id>")
def amd_del_stu(stu_id):
    stu=StudentUserExtsModel.query.filter_by(id=stu_id)[0]
    db.session.execute('DELETE FROM student_user_exts WHERE id={}'.format(stu_id))
    db.session.execute('DELETE FROM user WHERE id={}'.format(stu.u_id))
    db.session.commit()
    return redirect(url_for("user.amd_show_stu"))

@bp.route("/amd_change_stu/<int:stu_id>", methods=['GET', 'POST'])
def amd_change_stu(stu_id):
    stu=StudentUserExtsModel.query.filter_by(id=stu_id)[0]
    stu.name=request.form.get('name')
    stu.gender = request.form.get('gender')
    stu.age = request.form.get('age')
    stu.tel = request.form.get('tel')
    stu.school = request.form.get('school')
    stu.major = request.form.get('major')
    stu.grade = request.form.get('grade')
    db.session.commit()
    return redirect(url_for('user.amd_show_stu'))


@bp.route("/follow_psyc/<int:p_id>/<follow_type>", methods=['GET', 'POST'])  # 关注
def follow_psyc(p_id, follow_type):
    if follow_type == '关注':
        follow = FollowModel(stu_id=StudentUserExtsModel.query.filter_by(u_id=g.user.id)[0].id,
                             psyc_id=p_id)  # 这里关联的是user的额外表
        psyc = PsychologistModel.query.filter_by(id=p_id)[0]
        psyc.follow_times = psyc.follow_times + 1
        print("psyc", psyc)
        db.session.add(follow)
        db.session.commit()
        return redirect(url_for('psychologist.get_psychologist', psyc_id=p_id))
    elif follow_type == '取消关注':
        is_follow = FollowModel.query.filter_by(
            stu_id=StudentUserExtsModel.query.filter_by(u_id=g.user.id)[0].id).filter_by(psyc_id=p_id).first()
        psyc = PsychologistModel.query.filter_by(id=p_id)[0]
        psyc.follow_times = psyc.follow_times - 1
        db.session.delete(is_follow)
        db.session.commit()
        return redirect(url_for('psychologist.get_psychologist', psyc_id=p_id))

@bp.route("/follow_page", methods=['GET', 'POST'])  # 关注
def follow_page():
    follow_list = FollowModel.query.filter_by(
        stu_id=StudentUserExtsModel.query.filter_by(u_id=g.user.id).first().id).all()
    print(follow_list)
    psyc_list = []
    for each in follow_list:
        psyc_list.append(PsychologistModel.query.filter_by(id=each.psyc_id).first())
    print(psyc_list)
    return render_template("follow.html",follow_list=follow_list,psyc_list=psyc_list)

