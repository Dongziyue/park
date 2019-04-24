from App.ext import db


# 用户表
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), default='')
    username = db.Column(db.String(64), default='')
    password = db.Column(db.String(64), default='')
    sex = db.Column(db.String(64), default='')
    tel = db.Column(db.String(64), default='')
    role = db.Column(db.INT, default=1)
    cardid = db.Column(db.INT, default=0)
    cardnum = db.Column(db.String(64), default='')


class ParkSpace(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parkid = db.Column(db.INT)
    status = db.Column(db.INT, default=0)
    tag = db.Column(db.INT, default=1)
    cardnum = db.Column(db.String(64), unique=True)
    # tag=0">全部车位tag=1">正常车位tag=2">临时车位tag=3">紧急车位tag=4">置空车位


# 停车所有信息
class Parkinfoall(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parknum = db.Column(db.Integer)
    cardnum = db.Column(db.String(255))
    carnum = db.Column(db.String(255))
    parkin = db.Column(db.Integer)
    parkout = db.Column(db.Integer)
    parktemp = db.Column(db.Integer)

    def to_dic(self):
        dic = {
            'id': self.id,
            'parknum': self.parknum,
            'cardnum': self.cardnum,
            'carnum': self.carnum,
            'parkin': self.parkin,
            'parkout': self.parkout,
            'parktemp': self.parktemp
        }
        return dic


# 停车信息
class Parkinfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parknum = db.Column(db.Integer)
    cardnum = db.Column(db.String(50))
    carnum = db.Column(db.String(50))
    parkin = db.Column(db.DATE)
    parktemp = db.Column(db.Integer)


# 停车场卡信息表
class Depotcard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))  # 用户名
    cardnum = db.Column(db.String(64))  # 卡号
    type = db.Column(db.Integer)  # 卡类型
    money = db.Column(db.FLOAT, default=0.00)  # 余额
    time = db.Column(db.DATE)  # 发卡时间
    illegalcount = db.Column(db.Integer, default=0)  # 是否挂失
    deductedtime = db.Column(db.DATE)  # 扣费时间

    def to_dic(self):
        dic = {
            'id': self.id,
            'username': self.username,
            'cardnum': self.cardnum,
            'type': self.type,
            'money': self.money,
            'time': self.time,
            'illegalcount': self.illegalcount,
            'deductedtime': self.deductedtime
        }
        return dic


# 停车卡类型
class Cardtype(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))  # 卡类型


# 车场收入
class Income(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    money = db.Column(db.FLOAT, default=0.00)  # 收入
    method = db.Column(db.Integer, default=0)  # 收入方式（0现金，1支付宝，2微信，9从卡中扣费）
    type = db.Column(db.Integer, default=0)  # 收入类型（0临时停车，1普通卡，2月卡，3年卡）
    cardnum = db.Column(db.String(64), default="")  # 卡号
    carnum = db.Column(db.String(64), default="")  # 车号
    isillegal = db.Column(db.Integer, default=0)  # 是否有违规
    source = db.Column(db.Integer, default=1)  # 收入来源，0充值卡，1出库收费
    time = db.Column(db.DATE, default="")  # 收入时间
    duration = db.Column(db.FLOAT, default=0.00)  # 停车时长
    trueincome = db.Column(db.Integer, default=0)  # 是否真正收入（0：否，1：是）
