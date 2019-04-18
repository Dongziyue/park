# import random
#
# from flask import Blueprint, render_template
#
# from App.ext import db
# from App.models import User, Address
#
# user = Blueprint('user', __name__)
#
#
#
# def init_blue(app):
#     app.register_blueprint(blueprint=user, url_prefix='/user')
#     app.register_blueprint(blueprint=admin, url_prefix='/admin')
#
#
# @user.route('/')
# def index():
#     return 'user'


# @blue.route('/')
# def index():
#     content="layUiTest"
#     return render_template('layuiTest.html',content=content)
#
# @blue.route('/UploadItem')
# def upload():
#     return render_template("UploadItem.html")
# @blue.route('/addUser')
# def add_user():
#     # 删除 所有继承自db.Model的表
#     db.drop_all()
#     # 创建 所有的继承自db.Model的表
#     db.create_all()
#     # """只通过外键来关联/查询数据 操作复杂"""
#     # # 添加用户
#     # user = User(name="zs")
#     # db.session.add(user)
#     # db.session.commit()  # 必须先提交, 否则没有生成主键, 设置外键无效
#     #
#     # # 添加地址
#     # adr1 = Address(detail="中关村1号", user_id=user.id)
#     # adr2 = Address(detail="陆家嘴1号", user_id=user.id)
#     # db.session.add_all([adr1, adr2])
#     # db.session.commit()
#
#     # # 查询数据  根据用户查询地址
#     # user=User(name="zs")
#     # print(user.id)
#     # adrs = Address.query.filter_by(user_id=user.id).all()
#     # for adr in adrs:
#     #     print(adr.detail)
#
#     """通过关系属性来关系/查询数据 操作简单  1> 仍需要定义外键 2> 定义关系属性 3> 使用关系属性来关联数据"""
#     user = User(name="zs")
#     adr1 = Address(detail="中关村1号", user_id=user.id)
#     adr2 = Address(detail="陆家嘴1号", user_id=user.id)
#     # 关联数据
#     user.addresses = [adr1, adr2]
#     user.addresses.append(adr1)
#     user.addresses.append(adr2)
#     # 添加到数据库中
#     db.session.add_all([user, adr1, adr2])
#     db.session.commit()
#     # 使用关系属性来查询数据
#     adrs=user.addresses
#     for adr in adrs:
#         print(adr.user_id)
#     print(adr1.user.name)
#
#     return 'success!'
#
#
#
