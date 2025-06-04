from django.db import models

class Nguoidung(models.Model):
    nguoidung_id = models.CharField(primary_key=True, max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')
    tennguoidung = models.CharField(db_column='tenNguoiDung', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    email = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    matkhau = models.CharField(db_column='matKhau', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    dienthoai = models.CharField(db_column='dienThoai', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    vaitro = models.CharField(db_column='vaiTro', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    ngaytaotk = models.DateField(db_column='ngayTaoTK', blank=True, null=True)

    class Meta:
        db_table = 'NguoiDung'