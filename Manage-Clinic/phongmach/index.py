from flask import render_template, request, redirect, url_for, session, jsonify
from phongmach import app, utils, login
import cloudinary.uploader
from flask_login import login_user, logout_user, current_user
from phongmach.models import UserRole, User
import hashlib
from datetime import datetime


@login.user_loader
def load_user(user_id):
    return utils.get_user_by_id(user_id=user_id)


@app.route("/")
def home():
    return render_template('index.html')


@app.route('/register', methods=['get', 'post'])
def user_register():
    err_msg = ""
    if request.method.__eq__('POST'):
        # name = request.form['name']
        # email = request.form.get('email')
        # username = request.form['username']
        password = request.form['password']
        confirm = request.form['confirm']
        avatar = None

        if password.__eq__(confirm):
            avatar = ''
            if request.files:
                res = cloudinary.uploader.upload(request.files['avatar'])
                avatar = res['secure_url']

            try:
                utils.add_user(name=request.form['name'],
                               username=request.form['username'],
                               password=request.form['password'],
                               avatar=avatar)

                return redirect('/login')
            except:
                err_msg = 'Có lỗi xảy ra! Vui lòng quay lại sau!'
        else:
            err_msg = 'Mật khẩu KHÔNG khớp!'

    return render_template('register.html', err_msg=err_msg)


@app.route('/login', methods=['get', 'post'])
def login():
    err_msg = ''
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            role = request.form["role"]
            if role == "1":
                role = UserRole.USER
            else:
                role = UserRole.BACSI

            user = utils.check_login(username=username, password=password, role=role)
            if user:

                login_user(user)

                u = request.args.get('next')
                return redirect(u if u else '/')
            else:
                err_msg = 'Tài khoản hoặc mật khẩu KHÔNG chính xác! Vui lòng thử lại!'

        except Exception as ex:
            error_msg = str(ex)

    return render_template('login.html', err_msg=err_msg)


@app.route('/admin-login', methods=['post'])
def login_admin():
    username = request.form['username']
    password = request.form['password']

    user = utils.check_login(username=username, password=password, role=UserRole.ADMIN)
    if user:
        login_user(user=user)

    return redirect("/admin")

@app.context_processor
def common():
    return {'UserRole' : UserRole,
            'tienToaThuoc': utils.dem_thuoc(session.get('ketoa'))}

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/login')


@app.route('/lichkhambenh', methods=['get', 'post'])
def lichkhambenh():
    if request.method.__eq__('POST'):
        thoi_gian = request.form['thoi_gian']
        trieu_chung = request.form['trieu_chung']
        utils.addLich(thoi_gian=thoi_gian, trieu_chung=trieu_chung,
                      user=current_user)
        return redirect('/')

    return render_template('lichkhambenh.html')


@app.route('/danhsachlichkham')
def lichkhambenh_list():
    kw = request.args.get('keyword')
    lichkham = utils.load_lichKham(kw=kw)

    return render_template('danhsachlichkham.html', lichkham=lichkham)


@app.route('/thuoc')
def thuoc_list():
    kw = request.args.get('keyword')
    thuoc = utils.load_thuoc(kw=kw)

    return render_template('thuoc.html', thuoc=thuoc)


@app.route('/danhsachphieukham')
def phieukhambenh_list():
    phieukham = utils.load_phieuKham()
    benhnhan = []
    bacsi = []
    for p in phieukham:
        b = utils.get_user_by_id(p.benh_nhan_id)
        bs = utils.get_user_by_id(p.bac_si_id)
        benhnhan.append(b)
        bacsi.append(bs)

    data = list(zip(phieukham, benhnhan, bacsi))
    return render_template('danhsachphieukham.html', data=data)


@app.route('/phieukhambenh/<int:benh_nhan>')
def phieukhambenh(benh_nhan):
    # data = request.json
    # benh_nhan_id = data.get('benh_nhan_id')
    benhnhan = utils.get_user_by_id(benh_nhan)

    return render_template('phieukhambenh.html', benhnhan=benhnhan)

@app.route('/add-phieukham', methods=['post'])
def tao_phieukham():
    thoi_gian = request.form['thoi_gian']
    trieu_chung = request.form['trieu_chung']
    chuan_doan = request.form['chuan_doan']
    benhnhan= request.form['benhnhan']
    phieukham = utils.taoPhieuKham(thoi_gian=thoi_gian, trieu_chung=trieu_chung, chuan_doan=chuan_doan, user=benhnhan)
    return redirect(url_for('phieukhambenh', benh_nhan = benhnhan))

@app.route('/api/add-thuoc', methods=['post'])
def add_thuoc():
    data = request.json
    id = str(data.get('id'))
    ten = data.get('ten')
    gia = data.get('gia')
    ghi_chu = data.get('ghi_chu')

    # import pdb
    # pdb.set_trace()

    ketoa = session.get('ketoa')
    if not ketoa:
        ketoa = {}

    if id in ketoa:
        ketoa[id]['so_luong'] = ketoa[id]['so_luong'] + 1
    else:
        ketoa[id] = {
            'id': id,
            'ten': ten,
            'gia': gia,
            'ghi_chu': ghi_chu,
            'so_luong': 1
        }

    session['ketoa'] = ketoa

    return jsonify(utils.dem_thuoc(ketoa))


# @app.route('/api/themtoathuoc', methods=['post'])
# def add_toathuoc():
#     key = app.config['KETOA_KEY']
#     ketoa = session.get(key)
#     # try:
#     #     utils.luu_toathuoc(ketoa)
#     # except:
#     #     return jsonify({'status': 500})
#     # else:
#     #     return jsonify({'status': 200})
#     if utils.luu_toathuoc(ketoa=ketoa):
#         del session[key]
#     else:
#         err_msg = 'Đã có lỗi xảy ra!'
#
#     return jsonify({'err_msg': err_msg})

@app.route('/kethuoc')
def ke_thuoc():

    return render_template('kethuoc.html', tienThuoc=utils.dem_thuoc(session['ketoa']))



# @app.route('/api/add-thuoc', methods=['post'])
# def add_thuoc():
#     data = request.json
#     id = str(data['id'])
#
#     key = app.config['KETOA_KEY']
#     ketoa = session[key] if key in session else {}
#
#     if id in ketoa:
#         ketoa[id]['so_luong'] = ketoa[id]['so_luong'] + 1
#     else:
#         ten = data['ten']
#         gia = data['gia']
#
#         ketoa[id] = {
#             "id": id,
#             "name": ten,
#             "price": gia,
#             "quantity": 1
#         }
#
#     session[key] = ketoa
#
#     return jsonify(utils.dem_thuoc(ketoa))

# @app.route('/ketoa')
# def ketoa():
#     key = app.config['KETOA_KEY']
#     session[key] = {
#         "1": {
#             "id": "1",
#             "ten": "Thuốc Sổ",
#             "gia": 1000,
#             "so_luong": 1
#         }
#     }
#     return render_template('phiekhambenh.html')

if __name__ == '__main__':
    from phongmach.admin import *

    app.run(debug=True)
