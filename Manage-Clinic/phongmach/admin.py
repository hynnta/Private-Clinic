from phongmach import app, db
from flask_admin import Admin, expose, BaseView
from flask_admin.contrib.sqla import ModelView
from phongmach.models import DanhMucThuoc, Thuoc, LichKhamBenh, UserRole
from flask_login import current_user, logout_user
from flask import redirect

admin = Admin(app=app, name='Quản lý phòng mạch', template_mode='bootstrap4')


class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class DanhMucView(AuthenticatedModelView):
    column_display_pk = True  # hiện id
    can_view_details = True  # xem chi tiết
    can_export = True  # tải dữ liệu xuống
    column_searchable_list = ['ten']  # search theo...
    column_exclude_list = ['created_date', 'active']  # ẩn
    column_sortable_list = ['id']  # sắp xếp
    column_labels = {  # đổi tên
        'ten': 'Loại thuốc'
    }

class ThuocView(AuthenticatedModelView):
    column_display_pk = True  # hiện id
    can_view_details = True  # xem chi tiết
    can_export = True  # tải dữ liệu xuống
    column_searchable_list = ['ten']  # search theo...
    column_exclude_list = ['created_date', 'active']  # ẩn
    column_sortable_list = ['id']  # sắp xếp
    column_labels = {  # đổi tên
        'ten': 'Loại thuốc'
    }

class Back(BaseView):
    @expose('/')
    def index(self):
        return redirect("/")

class StatsView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/stats.html')

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


# class AuthenticatedView(BaseView):
#     def is_accessible(self):
#         return current_user.is_authenticated

class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated

admin.add_view(Back(name='BACK'))
admin.add_view(AuthenticatedModelView(DanhMucThuoc, db.session, name='Danh mục thuốc'))
# admin.add_view(DanhMucView(DanhMucThuoc, db.session, name='Danh mục thuốc'))
admin.add_view(AuthenticatedModelView(Thuoc, db.session, name='Thuốc'))
admin.add_view(StatsView(name='Thống kê - Báo cáo'))
admin.add_view(LogoutView(name='Đăng xuất'))
