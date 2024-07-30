from flask import g,redirect,url_for
from functools import wraps

def login_required(func):
    #@wraps一定要写
    @wraps(func)
    def wrapper(*args,**kwargs):#*args就是就是传递一个可变参数列表给函数实参，这个参数列表的数目未知，甚至长度可以为0
                                #而**kwargs则是将一个可变的关键字参数的字典传给函数实参，同样参数列表长度可以为0或为其他值。
        if hasattr(g,"user"):
            return func(*args,**kwargs)
        else:
            return redirect(url_for("user.login"))
    return wrapper