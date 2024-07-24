from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, Text, Enum, DateTime
from phongmach import db, app
from sqlalchemy.orm import relationship, backref
from enum import Enum as UserEnum
from flask_login import UserMixin


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


class UserRole(UserEnum):
    USER = 1
    ADMIN = 2
    BACSI = 3


class DanhMucThuoc(BaseModel):
    __tablename__ = 'danh_muc_thuoc'

    active = Column(Boolean, default=True)
    created_date = Column(DateTime, default=datetime.now())
    ten = Column(String(45), nullable=False)
    thuoc = relationship('Thuoc', backref='thuoc', lazy=False)

    def __str__(self):
        return self.ten


class Thuoc(BaseModel):
    __tablename__ = 'thuoc'

    active = Column(Boolean, default=True)
    created_date = Column(DateTime, default=datetime.now())
    ten = Column(String(45), nullable=False)
    so_luong = Column(Integer, nullable=False)
    gia = Column(Float, default=0)
    ghi_chu = Column(Text)
    danh_muc_id = Column(Integer, ForeignKey(DanhMucThuoc.id), nullable=False)
    toathuocdetails = relationship('ToaThuocDetails', backref='Thuoc', lazy=False)

    def __str__(self):
        return self.name


class ToaThuoc(BaseModel):
    __tablename__ = 'toa_thuoc'

    active = Column(Boolean, default=True)
    created_date = Column(DateTime, default=datetime.now())
    tong_tien = Column(Float, default=0)
    # phieukhambenh = relationship('PhieuKhamBenh', backref='ToaThuoc', lazy=False)
    phieukhambenh = Column(Integer, ForeignKey('phieu_kham_benh.id'), nullable=False)
    toathuocdetails = relationship('ToaThuocDetails', backref='ToaThuoc', lazy=False)

    def __str__(self):
        return self.name


class ToaThuocDetails(BaseModel):
    __tablename__ = 'toa_thuoc_details'

    so_luong = Column(Integer, nullable=False)
    gia = Column(Float, default=0)
    thuoc_id = Column(Integer, ForeignKey(Thuoc.id), nullable=False)
    toa_thuoc_id = Column(Integer, ForeignKey(ToaThuoc.id), nullable=False)

    def __str__(self):
        return self.name


class User(BaseModel, UserMixin):
    active = Column(Boolean, default=True)
    name = Column(String(50), nullable=False)
    email = Column(String(50))
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    avatar = Column(String(100))
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    lichkhambenh = relationship('LichKhamBenh', backref='user', lazy=False)

    def __str__(self):
        return self.name


class LichKhamBenh(BaseModel):
    __tablename__ = 'lich_kham_benh'

    active = Column(Boolean, default=True)
    thoi_gian = Column(DateTime, nullable=False)
    trieu_chung = Column(Text)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)


class PhieuKhamBenh(BaseModel):
    __tablename__ = 'phieu_kham_benh'

    active = Column(Boolean, default=True)
    created_date = Column(DateTime, default=datetime.now())
    thoi_gian = Column(DateTime, nullable=False)
    trieu_chung = Column(Text)
    chuan_doan = Column(Text)
    bac_si_id = Column(Integer, ForeignKey(User.id), nullable=False)
    benh_nhan_id = Column(Integer, ForeignKey(User.id), nullable=False)
    # toa_thuoc_id = Column(Integer, ForeignKey(ToaThuoc.id), nullable=False)
    toathuoc = relationship('ToaThuoc', backref='PhieuKhamBenh', lazy=False)
    hoadon = relationship('HoaDon', backref='PhieuKhamBenh', lazy=False)



class HoaDon(BaseModel):
    __tablename__ = 'hoa_don'

    active = Column(Boolean, default=True)
    created_date = Column(DateTime, default=datetime.now())
    thanh_tien = Column(Float, default=0)
    phieu_kham_benh_id = Column(Integer, ForeignKey(PhieuKhamBenh.id), nullable=False)

    def __str__(self):
        return self.name


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
