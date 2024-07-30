from exts import db
from datetime import datetime

class EmailCaptchaModel(db.Model):
    __tablename__="email_captcha"
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    email=db.Column(db.String(100),nullable=False,unique=True)
    captcha=db.Column(db.String(10),nullable=False)
    create_time=db.Column(db.DateTime,default=datetime.now)
    #datetime.now不要加圆括号

class UserModel(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username=db.Column(db.String(200),nullable=False,unique=True)
    email=db.Column(db.String(100),nullable=False,unique=True)
    identity = db.Column(db.String(20), nullable=False,default="未填写")#身份
    jurisdiction= db.Column(db.String(20), nullable=False)#权限
    password=db.Column(db.String(20),nullable=False)
    join_time=db.Column(db.DateTime,default=datetime.now)
    img_base64=db.Column(db.Text)#图片的base64编码
    img_name=db.Column(db.String(200),nullable=False)#图片名

class StudentUserExtsModel(db.Model):
    __tablename__ = "student_user_exts"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name=db.Column(db.String(200),nullable=False,default="未填写")
    gender = db.Column(db.String(20), nullable=False,default="未填写")
    age = db.Column(db.Integer,default=0)
    tel = db.Column(db.String(20), nullable=False,default="未填写")
    school = db.Column(db.String(20), nullable=False,default="未填写")
    major = db.Column(db.String(20), nullable=False,default="未填写")#专业
    grade = db.Column(db.String(20), nullable=False,default="未填写")#年级
    u_id=db.Column(db.Integer,db.ForeignKey("user.id",ondelete='CASCADE'))
    Users=db.relationship("UserModel",backref='student_exts')

class QuestionModel(db.Model):
    __tablename__ = "question"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title=db.Column(db.String(200),nullable=False)
    content=db.Column(db.Text,nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    author_id=db.Column(db.Integer,db.ForeignKey("user.id",ondelete='CASCADE' ))
    author=db.relationship("UserModel",backref="questions")


class AnswerModel(db.Model):
    __tablename__ = "answer"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content=db.Column(db.Text,nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    question_id=db.Column(db.Integer,db.ForeignKey("question.id",ondelete='CASCADE'))
    author_id=db.Column(db.Integer,db.ForeignKey("user.id",ondelete='CASCADE'))
    question=db.relationship("QuestionModel",backref=db.backref("answers",order_by=create_time.desc()))
    #db.backref("answers",order_by=create_time.desc())定义回访的排序方式
    author=db.relationship("UserModel",backref="answers")

class WenjuanModel(db.Model):
    __tablename__ = "wenjuan"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    exercise_title = db.Column(db.String(200), nullable=False)#题目
    option=db.Column(db.Text,nullable=False)#选项要用" "分隔
    exercise_type=db.Column(db.String(200),nullable=False)#题型
    create_time = db.Column(db.DateTime, default=datetime.now)
    wenjuan_name= db.Column(db.String(200),nullable=False)#问卷名
    option_point = db.Column(db.String(200),nullable=False)
    img_name = db.Column(db.String(200),nullable=False)  #存储问卷图片名
    test_type = db.Column(db.String(200), nullable=False)#测试的标签
    judgment= db.Column(db.String(200), nullable=False,default="无")#该问卷的判断标准
    u_id = db.Column(db.Integer, db.ForeignKey("user.id",ondelete='CASCADE'))

class WenjuanAnswerModel(db.Model):
    __tablename__ = "wenjuan_answer"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    option_content=db.Column(db.Text,nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    wenjuan_id=db.Column(db.Integer,db.ForeignKey("wenjuan.id",ondelete='CASCADE'))
    wenjuan_uid=db.Column(db.Integer,db.ForeignKey("user.id",ondelete='CASCADE'))
    wenjuan_name=db.Column(db.String(200),nullable=False)#题型
    point=db.Column(db.Integer,default=0)
    option_type=db.Column(db.String(200),nullable=False)
    author=db.relationship("UserModel",backref="options")
    test_times = db.Column(db.Integer, default=0)  # 总分

class PsychologistModel(db.Model):
    __tablename__ = "psychologist"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False, default="未填写")
    age = db.Column(db.Integer,default=0)
    gender = db.Column(db.String(20), nullable=False, default="未填写")
    #img_base64 = db.Column(db.Text)#心理咨询师头像头像
    tag=db.Column(db.String(200),nullable=False)#心理医生的标签
    question_times=db.Column(db.Integer,default=0)#被提问次数
    answer_times=db.Column(db.Integer,default=0)#回答次数
    follow_times = db.Column(db.Integer, default=0)  # 关注数
    u_id=db.Column(db.Integer,db.ForeignKey("user.id",ondelete='CASCADE'))
    Users=db.relationship("UserModel",backref='psyc')

class PrivateMessagesModel(db.Model):
    __tablename__ = "private_messages"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id",ondelete='CASCADE'))
    psyc_id= db.Column(db.Integer, db.ForeignKey("psychologist.id",ondelete='CASCADE'))
    msg_type=db.Column(db.String(200),nullable=False)#信息的类型是提问还是回答

class FollowModel(db.Model):
    __tablename__ = "follow"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    stu_id = db.Column(db.Integer, db.ForeignKey("student_user_exts.id",ondelete='CASCADE'))
    psyc_id= db.Column(db.Integer, db.ForeignKey("psychologist.id",ondelete='CASCADE'))


class TesttimesModel(db.Model):
    __tablename__ = "test_times"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    u_id = db.Column(db.Integer, db.ForeignKey("user.id",ondelete='CASCADE'))
    wenjuan_name=db.Column(db.String(200),nullable=False)#题型
    test_times = db.Column(db.Integer, default=0)  # 测试次数


class WenjuanExtsModel(db.Model):#用于记录每次问卷的分数和评判
    __tablename__ = "wenjuan_exts"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    u_id = db.Column(db.Integer, db.ForeignKey("user.id",ondelete='CASCADE'))
    wenjuan_name=db.Column(db.String(200),nullable=False)
    total_score = db.Column(db.Integer, default=0)  # 总分
    level = db.Column(db.String(200), nullable=False)  # 评判
    test_times = db.Column(db.Integer, default=0)  # 第几次测试
    report_base64 = db.Column(db.Text, default='无')  # 存放健康状态报告的图片
    #create_time = db.Column(db.DateTime, default=datetime.now)


