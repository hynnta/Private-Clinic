from phongmach import db, app
from datetime import datetime
from phongmach.models import User, UserRole, LichKhamBenh, Thuoc, ToaThuocDetails, PhieuKhamBenh, ToaThuoc
import hashlib
from flask_login import current_user
from sqlalchemy import func


def check_login(username, password, role):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password),
                             User.user_role.__eq__(role)).first()


def add_user(name, username, password, **kwargs):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
    user = User(name=name, username=username, password=password, email=kwargs.get('email'), avatar=kwargs.get('avatar'))

    db.session.add(user)
    db.session.commit()


def addLich(thoi_gian, trieu_chung, user):
    date_time_str = '12/12/22 20:45:00'
    # c = User.query.get(0)

    date_time_obj = datetime.strptime(thoi_gian, '%Y-%m-%dT%H:%M')

    lichkhambenh = LichKhamBenh(thoi_gian=date_time_obj, trieu_chung=trieu_chung, user=current_user)

    db.session.add(lichkhambenh)
    db.session.commit()


def load_lichKham(kw=None):
    l = LichKhamBenh.query
    if kw:
        user = User.query.filter(User.name.contains(kw)).first()
        l = l.filter(LichKhamBenh.user_id.contains(user.id))

    return l.all()

def load_thuoc(kw=None):
    query = Thuoc.query

    if kw:
        query = query.filter(Thuoc.ten.contains(kw))
    return query.all()

def load_phieuKham(kw=None):
    return PhieuKhamBenh.query.all()


def taoPhieuKham(thoi_gian, trieu_chung, chuan_doan, user):
    date_time_str = '12/12/22 20:45:00'
    # c = User.query.get(0)
    date_time_obj = datetime.strptime(thoi_gian, '%Y-%m-%dT%H:%M')

    phieukhambenh = PhieuKhamBenh(thoi_gian=date_time_obj, trieu_chung=trieu_chung, chuan_doan=chuan_doan, bac_si_id=current_user.id, benh_nhan_id=user)

    db.session.add(phieukhambenh)
    db.session.commit()


def get_user_by_id(user_id):
    return User.query.get(user_id)

def dem_thuoc(ketoa):
    tong_so_luong, tong_tien = 0, 0

    if ketoa:
        for k in ketoa.values():
            tong_so_luong += k['so_luong']
            tong_tien += k['so_luong'] * k['gia']

    return {
        'tong_so_luong': tong_so_luong,
        'tong_tien': tong_tien
    }

def luu_toathuoc(ketoa):
    if ketoa:
        phieukhambenh = PhieuKhamBenh.query.filter(PhieuKhamBenh.id == db.session.query(func.max(PhieuKhamBenh.id))).first()
        toa = ToaThuoc(phieukhambenh = 1)
        db.session.add(toa)

        for t in ketoa.values():
            td = ToaThuocDetails(so_luong=t['so_luong'], gia=t['gia'], thuoc_id=t['id'],
                                 toa_thuoc_id=toa.id)
            db.session.add(td)
        db.session.commit()


# def thuoc_stats(kw=None, from_date=None, to_date=None):
#     t = db.session.query(Thuoc.id, Thuoc.ten,
#                          func.sum(ToaThuocDetails.so_luong * ToaThuocDetails.gia)) \
#         .join(ToaThuocDetails, ToaThuocDetails.thuoc_id.__eq__(Thuoc.id)) \
#         .group_by(Thuoc.id, Thuoc.ten)
#
#     return t.all()

# if __name__ == '__main__':
#     load_thuoc(kw='Thuốc Sổ')
