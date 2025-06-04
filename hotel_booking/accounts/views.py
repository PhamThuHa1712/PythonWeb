# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Nguoidung
from django.contrib import messages
import uuid

def signup_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        fullname = request.POST['fullname']
        phone = request.POST['phone']

        if Nguoidung.objects.filter(email=email).exists():
            messages.error(request, 'Email đã tồn tại.')
            return redirect('accounts:signup')

        nguoidung_id = str(uuid.uuid4())[:8].upper()
        nguoidung = Nguoidung(
            nguoidung_id=nguoidung_id,
            tennguoidung=fullname,
            email=email,
            matkhau=password,  # nên mã hóa sau này
            dienthoai=phone,
            vaitro='user',
            ngaytaotk=timezone.now().date()
        )
        nguoidung.save()
        messages.success(request, 'Tạo tài khoản thành công.')
        return redirect('accounts:login')

    return render(request, 'accounts/signup.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = Nguoidung.objects.get(email=email, matkhau=password)
            request.session['nguoidung_id'] = user.nguoidung_id
            request.session['tennguoidung'] = user.tennguoidung
            request.session['is_logged_in'] = True

            # Lấy URL quay lại từ tham số next
            next_url = request.GET.get('next', 'rooms:room_list')
            messages.success(request, f'Xin chào, {user.tennguoidung}')
            return redirect(next_url)
            # return redirect('rooms:room_list')
        except Nguoidung.DoesNotExist:
            messages.error(request, 'Email hoặc mật khẩu không đúng.')
            return redirect('accounts:login')

    return render(request, 'accounts/login.html')

# xóa session khi đăng xuất.
def logout_view(request):
    if 'is_logged_in' in request.session:
        del request.session['nguoidung_id']
        del request.session['tennguoidung']
        del request.session['is_logged_in']
    return redirect('accounts:login')