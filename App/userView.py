import datetime
import json
import uuid

from flask import Blueprint, request, render_template, session, redirect, url_for, jsonify

from App.ext import db
from App.models import User, ParkSpace, Parkinfoall, Parkinfo, Depotcard, Cardtype, Income, Depotinfo

user = Blueprint('user', __name__)


@user.route('/creatAll')
def create_all():
    db.create_all()
    return 'ok'


@user.route('/index')
def index():
    user1 = session.get('username')
    # 取数据
    # session.query(User).all()
    user0 = User.query.filter_by(username=user1).first()
    parkSpaces = ParkSpace.query.filter_by().all()

    if user1:
        user1 = session.get('username')
        return render_template('index.html', user1=user1, parkSpaces=parkSpaces, user0=user0)
    else:
        return render_template('login.html')


# 车辆入库
@user.route('/addParkSpace', methods=['POST', 'GET'])
def add_ParkSpace():
    id = request.form.get('id')
    parkNum = request.form.get('parkNum')
    cardnum = request.form.get('cardNum')
    carnum = request.form.get('carNum')
    parktemp = request.form.get('parkTem')
    parkspace = ParkSpace.query.filter_by(parkid=parkNum).first()
    parkspace.status = 1
    parkspace.cardnum = cardnum
    tag = parkspace.tag
    db.session.commit()

    cur_time = datetime.datetime.now()

    parkinfo = Parkinfo.query.filter_by(parknum=parkNum).first()
    parkinfo.cardnum = cardnum
    parkinfo.carnum = carnum
    parkinfo.parkin = cur_time
    parkinfo.parktemp = parktemp
    db.session.commit()

    # 添加停车记录-入库
    parkinfo = Parkinfo.query.filter_by(parknum=parkNum).first()
    parkinfoall = Parkinfoall(parknum=parkinfo.parknum, cardnum=parkinfo.cardnum,
                              carnum=parkinfo.carnum, parktemp=parkinfo.parktemp,
                              parkin=parkinfo.parkin)

    db.session.add(parkinfoall)
    db.session.commit()
    return jsonify({'code': 200, 'id': tag})


# 查看停车详情
@user.route('/parkDetail', methods=['POST', 'GET'])
def parkDetail():
    parknum = request.args.get('parkNum')
    parkSpace = ParkSpace.query.filter_by(parkid=parknum).first()
    cardnum = parkSpace.cardnum
    parkinfo = Parkinfo.query.filter_by(parknum=parknum).first()

    if parkinfo.carnum:
        depotcard = Depotcard.query.filter_by(cardnum=cardnum).first()
        # 判断是否有卡
        if depotcard:
            username = depotcard.username
        else:
            username = "临时停车"
        data = {'code': 200, 'cardnum': parkinfo.cardnum, 'parknum': parknum, 'carnum': parkinfo.carnum,
                'parkin': parkinfo.parkin,
                'parktemp': parkinfo.parktemp, 'username': username}
    else:
        data = {'code': 500}
    return jsonify(data)


# 车辆出库车位详情
@user.route('/ExParkSpace', methods=['POST', 'GET'])
def ex_ParkSpace():
    parknum = request.args.get('parkNum')
    parkspace = ParkSpace.query.filter_by(parkid=parknum).first()
    cardnum = parkspace.cardnum

    parkinfo = Parkinfo.query.filter_by(parknum=parknum).first()
    return jsonify({'code': 200, 'parknum': parkinfo.parknum,
                    'cardnum': parkinfo.cardnum, 'carnum': parkinfo.carnum, 'parktemp': parkinfo.parktemp})


# 否扫码支付
@user.route('/isPay', methods=['POST', 'GET'])
def isPay():
    parknum = request.args.get('parknum')
    cardnum = request.args.get('cardnum')
    carnum = request.args.get('carnum')
    cur_time = datetime.datetime.now()
    parkinfo = Parkinfo.query.filter_by(parknum=parknum, cardnum=cardnum, carnum=carnum).all()[-1]
    parktime = cur_time - parkinfo.parkin
    park_time = (parktime.seconds / 60) / 60
    money_pay = round(park_time * 5, 2)
    # 如果收费小于3元，收费3元
    if money_pay < 3:
        money_pay = 3.00
    # 是否刷停车卡
    if parkinfo.cardnum:
        # 可正常扣费
        type = 0
        depotcard = Depotcard.query.filter_by(cardnum=cardnum).first()
        if depotcard.money < money_pay:
            # 余额不足
            type = 9
        return jsonify({'code': 400, 'money_pay': money_pay, 'type': type, 'va_msg': '准备进入支付......确认出库？'})
    else:
        return jsonify({'code': 200, 'money_pay': money_pay, 'va_msg': '准备进入支付......确认出库？'})


# 确认出库
@user.route('/checkOut', methods=['POST', 'GET'])
def checkOut():
    parknum = request.form.get("parkNum")
    cardNum = request.form.get('cardNum')
    pay_money = request.form.get('pay_money')
    # 收入记录
    method = request.form.get("payid")
    carnum = request.form.get("carNum")

    parkspace = ParkSpace.query.filter_by(parkid=parknum).first()
    parkspace.status = 0
    parkspace.cardnum = ''
    db.session.commit()

    # 停车历史记录添加
    parkinfo = Parkinfo.query.filter_by(parknum=parknum).first()
    cur_time = datetime.datetime.now()
    parkinfoall = Parkinfoall.query.filter_by(parknum=parknum, cardnum=parkinfo.cardnum,
                                              carnum=parkinfo.carnum, parkin=parkinfo.parkin).first()
    parkinfoall.parkout = cur_time
    parktime = cur_time - parkinfo.parkin
    db.session.commit()
    # 停车时长
    park_time = (parktime.seconds / 60)
    # parkinfo表置空数据
    parkinfo = Parkinfo.query.filter_by(parknum=parknum).first()
    parkinfo.cardnum = ''
    parkinfo.carnum = ''
    db.session.commit()
    # 扣费
    if cardNum:
        # 有停车卡
        depotcard = Depotcard.query.filter_by(cardnum=cardNum).first()
        depotcard.money = depotcard.money - float(pay_money)
        db.session.commit()
        type = depotcard.type
        # 添加一条收费记录
        income = Income(money=pay_money, method=method, type=type,
                        carnum=carnum, cardnum=cardNum, source=1,
                        time=cur_time, duration=park_time, trueincome=1)
        db.session.add(income)
        db.session.commit()
    else:
        # 临时停车
        income = Income(money=pay_money, method=method, type=0,
                        carnum=carnum, cardnum="临时停车", source=1,
                        time=cur_time, duration=park_time, trueincome=1)
        db.session.add(income)
        db.session.commit()
        print("临时停车出库成功")

    return jsonify({'code': 200})


# 按车牌出库
@user.route('/checkOutByCardnum', methods=['POST', 'GET'])
def checkOutByCardnum():
    carnum = request.args.get('carnum')
    # parkspace = ParkSpace.query.filter_by(carnum=carnum).first()
    # parknum = parkspace.parkid
    parkinfo = Parkinfo.query.filter_by(carnum=carnum).first()
    if parkinfo:
        data = {'code': 200, 'parknum': parkinfo.parknum,
                'cardnum': parkinfo.cardnum, 'carnum': parkinfo.carnum, 'parktemp': parkinfo.parktemp}
    else:
        data = {'code': 500}
    return jsonify(data)


# 按tag查看停车位
@user.route('/tagParkSpace', methods=['POST', 'GET'])
def tagParkSpace():
    user1 = session.get('username')
    user0 = User.query.filter_by(username=user1).first()
    tag = request.args.get('tag')
    parkSpaces = ParkSpace.query.filter_by(tag=tag).all()

    if int(tag) == 4:
        parkSpaces = ParkSpace.query.filter_by(status=1).all()
        db_list = []
        for parkSpace in parkSpaces:
            parkSpace.status = 0
            parkSpace.cardnum = ''
            db_list.append(parkSpace)
        db.session.add_all(db_list)
        db.session.commit()
        return redirect(url_for('user.index'))
    return render_template('index.html', parkSpaces=parkSpaces, user0=user0)


@user.route('/index/toindex')
def toindex():
    user1 = session.get('username')
    if user1:
        return render_template('index.html', user1=session.get('username'))
    else:
        return render_template('login.html')


@user.route('/exit')
def exit():
    session.pop('username')
    return render_template('login.html')


# 登录判断
@user.route('/login', methods=['post', 'get'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # 判断用户名和密码是否填写
        if not all([username, password]):
            msg = '* 请填写好完整的信息'
            return render_template('login.html', msg=msg)
        # 核对用户名和密码是否一致
        user = User.query.filter_by(username=username, password=password).first()
        # 如果用户名和密码一致
        if user:
            session['username'] = user.username
            session['user_id'] = user.id
            return jsonify({'code': 200, 'msg': '登录成功！'})
        # 如果用户名和密码不一致返回登录页面,并给提示信息
        else:
            msg = '* 用户名或者密码不一致'
            return jsonify({'code': 500, 'msg': '登录失败！'})


# 停车卡管理
@user.route('/depotCard', methods=['post', 'get'])
def depotcard():
    if request.method == "GET":
        depotcards = Depotcard.query.filter_by().all()
        return render_template('depotcard.html', depotcards=depotcards)


# 判断能否升级卡
@user.route('/isAlertType', methods=['post', 'get'])
def isAlertType():
    cardnum = request.form.get('cardnum')
    islose = request.form.get('islose')
    type = request.form.get('type')
    print(cardnum)
    print(islose)
    print(type)
    money_pay = 0
    depotinfo = Depotinfo.query.filter_by(id=1).first()
    depotcard = Depotcard.query.filter_by(cardnum=cardnum).first()
    # depotcard.type = type
    # db.session.commit()
    if int(type) == 2:
        # 如果月卡钱不足
        if depotcard.money < depotinfo.monthcard:
            money_pay = depotinfo.monthcard - depotcard.money
            return jsonify({'code': 500, 'money_pay': money_pay})
        else:
            # money_pay = depotcard.money - depotinfo.monthcard
            money_pay = 0
            return jsonify({'code': 200, 'money_pay': money_pay})

    if int(type) == 3:
        # 如果年卡钱不足
        if depotcard.money < depotinfo.yearcard:
            money_pay = depotinfo.yearcard - depotcard.money
            return jsonify({'code': 500, 'money_pay': money_pay})
        else:
            # money_pay = depotcard.money - depotinfo.yearcard
            money_pay = 0
            return jsonify({'code': 200, 'money_pay': money_pay})
    return jsonify({'code': 200, 'money_pay': money_pay})


# 修改停车卡信息
@user.route('/alertDepotCard', methods=['post', 'get'])
def alertDepotCard():
    cardnum = request.form.get('cardnum')
    islose = request.form.get('islose')
    type = request.form.get('type')
    alertpayid = request.form.get('alertpayid')  # 用什么方式支付（0现金，1支付宝，2微信，9从卡中扣费）
    alertpay_money = request.form.get('alertpay_money')  # 需要支付金额
    alertpay_type = request.form.get('alertpay_type')  # 扣费还是月卡或年卡未到期 (0扣费，1不用扣费，9付钱)
    if islose == None:
        islose = 0
    depotcard = Depotcard.query.filter_by(cardnum=cardnum).first()
    depotcard.money = depotcard.money + float(alertpay_money)
    depotcard.type = type
    depotcard.illegalcount = islose
    db.session.commit()
    # 收入管理插入一条数据
    cur_time = datetime.datetime.now()
    if float(alertpay_money) > 0:
        income = Income(money=alertpay_money, method=3, type=type,
                        carnum="升级卡", cardnum=cardnum, source=0,
                        time=cur_time, duration=0, trueincome=0)
        db.session.add(income)
        db.session.commit()
    return jsonify({'code': 200})


# 按手机号查找停车卡
@user.route('/toDepotcardIndex', methods=['POST', 'GET'])
def toDepotcardIndex():
    cardnum = request.args.get('cardnum')
    depotcard = Depotcard.query.filter_by(username=cardnum).all()
    return render_template('depotcard.html', depotcards=depotcard)


# 卡的类型
@user.route('/findAllCardType', methods=['post', 'get'])
def findAllCardType():
    cardtypes = Cardtype.query.filter_by().all()
    content = {}
    payload = []
    for cardtype in cardtypes:
        content = {'id': cardtype.id, 'type': cardtype.type}
        payload.append(content)

    return jsonify({'code': 200, 'cardTypes': payload})


# 添加停车卡
@user.route('/addDepotCard', methods=['post', 'get'])
def add_DepotCard():
    username = request.form.get('username')
    name = request.form.get('name')
    money = request.form.get('money')
    type = request.form.get('type')
    print(username, name, money, type)
    uid = str(uuid.uuid4())
    cuid = ''.join(uid.split('-'))
    print(cuid)
    cur_time = datetime.datetime.now()
    cardnum = cuid
    depotcard = Depotcard(cardnum=cardnum, money=money,
                          type=type, username=username, time=cur_time)
    db.session.add(depotcard)
    db.session.commit()

    user_id = session.get('user_id')
    user = User.query.get(user_id)
    user.cardnum = cardnum
    db.session.commit()

    # 新增一条收入数据
    income = Income(money=money, method=3, type=type,
                    carnum="购卡", cardnum=cardnum, source=0,
                    time=cur_time, duration=0, trueincome=0)
    db.session.add(income)
    db.session.commit()

    data = {'code': 200, 'cardnum': depotcard.cardnum, 'username': user.username}
    return jsonify(data)


# 检验车卡是否存在
@user.route('/checkDepotCard', methods=['post', 'get'])
def check_DepotCard():
    cardnum = request.args.get('cardnum')
    depotcard = Depotcard.query.filter_by(cardnum=cardnum).first()
    if depotcard:
        return jsonify({'code': 200})
    else:
        return jsonify({'code': 500})


# 按id找卡
@user.route('/findDepotCardByCardnum', methods=['post', 'get'])
def findDepotCardByCardnum():
    cardnum = request.args.get('cardnum')
    depotcard = Depotcard.query.filter_by(cardnum=cardnum).first()
    cardtypes = Cardtype.query.filter_by().all()

    payload = []
    for cardtype in cardtypes:
        content = {'id': cardtype.id, 'type': cardtype.type}
        payload.append(content)

    depotcard = depotcard.to_dic()

    return jsonify({'code': 200, 'cardTypes': payload, 'depotcard': depotcard})


# 停车卡充值
@user.route('/chargeDepotCard', methods=['post', 'get'])
def charge_DepotCard():
    cardnum = request.form.get('cardnum')
    money = request.form.get('money')
    pay_money = float(money)
    depotcard = Depotcard.query.filter_by(cardnum=cardnum).first()
    money = depotcard.money + float(money)
    depotcard.money = money
    print(depotcard.money)
    db.session.commit()
    # 添加一条收费记录
    cur_time = datetime.datetime.now()
    income = Income(money=pay_money, method=3, type=depotcard.type,
                    cardnum=cardnum, source=0,
                    time=cur_time, trueincome=0)
    db.session.add(income)
    db.session.commit()

    return jsonify({'code': 200})


# 删除停车卡
@user.route('/deleteDepotCard', methods=['post', 'get'])
def delete_DepotCardSubmit():
    cardnum = request.form.get('cardnum')
    depotcard = Depotcard.query.filter_by(cardnum=cardnum).first()
    db.session.delete(depotcard)
    db.session.commit()
    return jsonify({'code': 200})


# 停车历史
@user.route('/depot', methods=['post', 'get'])
def depot():
    if request.method == "GET":
        parkinfoall = Parkinfoall.query.filter_by().all()
        return render_template('depot.html', parkinfoalls=parkinfoall)


# 按车牌号查找停车历史
@user.route('/findAllDepot', methods=['POST', 'GET'])
def findAllDepot():
    if request.method == "GET":
        carnum = request.args.get('name')
        parkinfoall = Parkinfoall.query.filter_by(carnum=carnum).all()
        return render_template('depot.html', parkinfoalls=parkinfoall)


# 查看停车历史详情
@user.route('/findParkinfoById', methods=['POST', 'GET'])
def findParkinfoById():
    parkinfoallId = request.form.get('id')
    parkinfoall = Parkinfoall.query.filter_by(id=parkinfoallId).first()
    parkinfoall = parkinfoall.to_dic()
    if parkinfoall:
        # data = {'code': 200, 'source': income.source, 'method': income.method, 'carnum': income.carnum,
        #         'cardnum': income.cardnum, 'money': income.money}
        data = {'code': 200, 'parkinfoall': parkinfoall}
    else:
        data = {'code': 500, 'va_msg': '该车未出库'}

    return jsonify(data)


# 用户管理
@user.route('/userManage', methods=['post', 'get'])
def userManage():
    users = User.query.filter_by().all()
    return render_template('user.html', users=users)


# 按id查找用户
@user.route('/findUserById', methods=['post', 'get'])
def findUserById():
    uid = request.args.get('uid')
    user = User.query.get(uid)
    if user:
        data = {'code': 200, 'uid': user.id, 'username': user.username, 'tel': user.tel, 'role': user.role}
    else:
        data = {'code': 500}
    return jsonify(data)


# 添加用户
@user.route('/addUser', methods=['post', 'get'])
def add_User():
    username = request.form.get('username')
    password = request.form.get('password')
    role = request.form.get('role')
    user = User(username=username, password=password, role=role)
    db.session.add(user)
    db.session.commit()
    data = {'code': 200, 'msg': '添加成功！'}
    return jsonify(data)


# 编辑用户
@user.route('/editUser', methods=['post', 'get'])
def editUser():
    uid = request.form.get('id')
    username = request.form.get('username')
    name = request.form.get('name')
    tel = request.form.get('tel')
    sex = request.form.get('sex')

    user = User.query.get(uid)
    user.username = username
    user.name = name
    user.tel = tel
    user.sex = sex

    db.session.commit()
    return jsonify({'code': 200, 'msg': '修改成功！'})


# 检验用户是否存在
@user.route('/checkUser', methods=['post', 'get'])
def check_User():
    username = request.args.get('username')
    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({'code': 200})
    else:
        return jsonify({'code': 500})


# 查看停车情况echart图
@user.route('/line', methods=['post', 'get'])
def line():
    if request.method == "GET":
        return render_template('line.html')

    if request.method == "POST":
        ispark = ParkSpace.query.filter_by(status=1).count()
        return jsonify({'code': 200, 'ispark': ispark})
    return render_template('line.html')


# 查看收入分析echart图
@user.route('/incomeCharts1', methods=['post', 'get'])
def incomeCharts1():
    if request.method == "GET":
        return render_template('incomeCharts.html')

    if request.method == "POST":
        cash = Income.query.filter_by(method=0).count()
        zhifubao = Income.query.filter_by(method=1).count()
        weixin = Income.query.filter_by(method=2).count()
        return jsonify({'code': 200, 'cash': cash, 'zhifubao': zhifubao, 'weixin': weixin})
    return render_template('incomeCharts.html')


# 收入管理
@user.route('/income', methods=['post', 'get'])
def income():
    if request.method == "GET":
        income = Income.query.filter_by().all()
        return render_template('income.html', incomes=income)


# 查看收入详情
@user.route('/findIncomeInfo', methods=['POST', 'GET'])
def findIncomeInfo():
    incomeId = request.args.get('incomeId')
    income = Income.query.filter_by(id=incomeId).first()
    if income:
        data = {'code': 200, 'source': income.source, 'method': income.method, 'carnum': income.carnum,
                'cardnum': income.cardnum, 'money': income.money}
    else:
        data = {'code': 500}

    return jsonify(data)


# 按车牌号查找收入列表
@user.route('/findAllIncome', methods=['POST', 'GET'])
def findAllIncome():
    content = request.args.get('content')
    datetimepickerStart = request.args.get('startTime')
    datetimepickerEnd = request.args.get('endTime')
    num = request.args.get('num')
    income = Income.query.filter_by().all()
    if content != "" and datetimepickerStart == "" and datetimepickerEnd == "":
        income = Income.query.filter_by(carnum=content).all()
    if datetimepickerStart != "" and datetimepickerEnd != "":
        income = Income.query.filter(Income.time.between(datetimepickerStart, datetimepickerEnd))
    if content != "" and datetimepickerStart != "" and datetimepickerEnd != "":
        income = Income.query.filter(Income.time.between(datetimepickerStart, datetimepickerEnd),
                                     Income.carnum == content)
    return render_template('income.html', incomes=income)
