from django.db import models
from accounts.models import Nguoidung

class Diadiem(models.Model):
    diadiem_id = models.CharField(primary_key=True, max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')
    tendiadiem = models.CharField(db_column='tenDiaDiem', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        db_table = 'DiaDiem'

class Quanhuyen(models.Model):
    quanhuyen_id = models.CharField(primary_key=True, max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')
    tenquanhuyen = models.CharField(db_column='tenQuanHuyen', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    diadiemdiadiem = models.ForeignKey(Diadiem, models.CASCADE, db_column='DiaDiemdiadiem_id', blank=True, null=True)

    class Meta:
        db_table = 'QuanHuyen'

class Khachsan(models.Model):
    khachsan_id = models.CharField(primary_key=True, max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')
    tenkhachsan = models.CharField(db_column='tenKhachSan', max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    mota = models.CharField(db_column='moTa', max_length=1000, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    ngaythem = models.DateField(db_column='ngayThem', blank=True, null=True)
    quanhuyenquanhuyen = models.ForeignKey(Quanhuyen, models.CASCADE, db_column='QuanHuyenquanhuyen_id', blank=True, null=True)

    class Meta:
        db_table = 'KhachSan'

class Loaiphong(models.Model):
    phong_id = models.CharField(primary_key=True, max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')
    tenphong = models.CharField(db_column='tenPhong', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    sogiuong = models.IntegerField(db_column='soGiuong', blank=True, null=True)
    gia = models.FloatField(blank=True, null=True)
    mota = models.CharField(db_column='moTa', max_length=1000, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    ngaythemphong = models.DateField(db_column='ngayThemPhong', blank=True, null=True)
    khachsankhachsan = models.ForeignKey(Khachsan, models.CASCADE, db_column='KhachSankhachsan_id', blank=True, null=True)

    class Meta:
        db_table = 'LoaiPhong'

class Dondatphong(models.Model):
    lichsu_id = models.CharField(primary_key=True, max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')
    ngaydat = models.DateField(db_column='ngayDat', blank=True, null=True)
    ngaytra = models.DateField(db_column='ngayTra', blank=True, null=True)
    tongtien = models.FloatField(db_column='tongTien', blank=True, null=True)
    trangthai = models.CharField(db_column='trangThai', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    thoigiandat = models.DateField(db_column='thoiGianDat', blank=True, null=True)
    nguoidungnguoidung = models.ForeignKey(Nguoidung, models.CASCADE, db_column='NguoiDungnguoidung_id', blank=True, null=True)
    phongphong = models.ForeignKey(Loaiphong, models.CASCADE, db_column='Phongphong_id', blank=True, null=True)

    class Meta:
        db_table = 'DonDatPhong'

class Hinhanh(models.Model):
    anh_id = models.CharField(primary_key=True, max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')
    urlhinhanh = models.CharField(db_column='urlHinhAnh', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    phongphong = models.ForeignKey(Loaiphong, models.CASCADE, db_column='Phongphong_id', blank=True, null=True)

    class Meta:
        db_table = 'HinhAnh'