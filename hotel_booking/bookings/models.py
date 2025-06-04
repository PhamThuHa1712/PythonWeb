from django.db import models
from rooms.models import Dondatphong

class ThanhToan(models.Model):
    thanhtoan_id = models.CharField(primary_key=True, max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')
    dondatphong = models.ForeignKey(Dondatphong, models.CASCADE, db_column='DonDatPhong_lichsu_id')
    sothe = models.CharField(max_length=16, blank=True, null=True)
    ngayhethan = models.CharField(max_length=5, blank=True, null=True)  # Format: MM/YY
    cvv = models.CharField(max_length=4, blank=True, null=True)
    ngaythanhtoan = models.DateTimeField(auto_now_add=True)
    trangthai = models.CharField(max_length=20, choices=[
        ('PENDING', 'Chờ xử lý'),
        ('SUCCESS', 'Thành công'),
        ('FAILED', 'Thất bại')
    ], default='PENDING')

    class Meta:
        db_table = 'ThanhToan'