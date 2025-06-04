from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from rooms.models import Dondatphong, Loaiphong, Khachsan
from .models import ThanhToan
from accounts.models import Nguoidung
from datetime import datetime
from django.conf import settings
import re

def booking_detail(request, booking_id):
    if 'is_logged_in' not in request.session:
        return redirect(f"{settings.LOGIN_URL}?next={request.path}")
    booking = get_object_or_404(Dondatphong, lichsu_id=booking_id)
    room = booking.phongphong
    hotel = room.khachsankhachsan
    user = Nguoidung.objects.get(nguoidung_id=request.session['nguoidung_id'])
    nights = max((booking.ngaytra - booking.ngaydat).days, 1)
    room_rate = room.gia * nights
    taxes = room_rate * 0.1  # Giả định thuế 10%
    total = room_rate + taxes
    payment = ThanhToan.objects.filter(dondatphong=booking).first()
    payment_status = payment.trangthai if payment else 'PENDING'

    context = {
        'booking': booking,
        'room': room,
        'hotel': hotel,
        'user': user,
        'checkin_date': booking.ngaydat,
        'checkout_date': booking.ngaytra,
        'room_rate': room_rate,
        'taxes': taxes,
        'total': total,
        'payment_status': payment_status,
        'nights': nights,
        'guests': 1,  # Giả định 1 khách
        'created_display': booking.thoigiandat,
        'show_cancel': booking.trangthai == 'PENDING' and payment_status != 'SUCCESS',
    }
    return render(request, 'booking_detail.html', context)

def payment(request, booking_id):
    if 'is_logged_in' not in request.session:
        return redirect(f"{settings.LOGIN_URL}?next={request.path}")
    booking = get_object_or_404(Dondatphong, lichsu_id=booking_id)
    payment = ThanhToan.objects.filter(dondatphong=booking).first()
    if payment and payment.trangthai == 'SUCCESS':
        messages.info(request, 'Đặt phòng này đã được thanh toán.')
        return redirect('bookings:booking_detail', booking_id=booking_id)
    context = {
        'booking': booking,
    }
    return render(request, 'payment.html', context)

@require_POST
def process_payment(request, booking_id):
    if 'is_logged_in' not in request.session:
        return redirect(f"{settings.LOGIN_URL}?next={request.path}")
    
    booking = get_object_or_404(Dondatphong, lichsu_id=booking_id)
    sothe = request.POST.get('credit_card_number')
    ngayhethan = request.POST.get('expiration_date')
    cvv = request.POST.get('cvv')

    # In dữ liệu để debug
    print(f"request.POST: {request.POST}")
    print(f"sothe: {sothe}, ngayhethan: {ngayhethan}, cvv: {cvv}")

    # Kiểm tra các trường có giá trị hay không
    if not all([sothe, ngayhethan, cvv]):
        messages.error(request, 'Vui lòng nhập đầy đủ thông tin thanh toán.')
        return redirect('bookings:booking_detail', booking_id=booking_id)

    # Kiểm tra định dạng dữ liệu
    if (
        sothe.isdigit() and len(sothe) == 16 and
        cvv.isdigit() and len(cvv) in [3, 4] and
        re.match(r'^(0[1-9]|1[0-2])/\d{2}$', ngayhethan)
    ):
        try:
            # Tạo bản ghi ThanhToan
            payment = ThanhToan.objects.create(
                thanhtoan_id=f'PAY{booking.lichsu_id}',
                dondatphong=booking,
                sothe=sothe[-4:],  # Lưu 4 số cuối
                ngayhethan=ngayhethan,
                trangthai='SUCCESS'  # Không lưu cvv
            )
            # Cập nhật trạng thái đặt phòng
            booking.trangthai = 'CONFIRMED'
            booking.save()
            messages.success(request, 'Thanh toán thành công!')
        except Exception as e:
            messages.error(request, f'Lỗi khi lưu thông tin thanh toán: {str(e)}')
            return redirect('bookings:booking_detail', booking_id=booking_id)
    else:
        messages.error(request, 'Thông tin thanh toán không hợp lệ. Vui lòng kiểm tra số thẻ (16 chữ số), ngày hết hạn (MM/YY), hoặc CVV (3-4 chữ số).')
        return redirect('bookings:booking_detail', booking_id=booking_id)

    return redirect('bookings:booking_detail', booking_id=booking_id)
def booking_history(request):
    if 'is_logged_in' not in request.session:
        return redirect(f"{settings.LOGIN_URL}?next={request.path}")
    bookings = Dondatphong.objects.filter(nguoidungnguoidung__nguoidung_id=request.session['nguoidung_id'])
    context = {
        'bookings': bookings,
    }
    return render(request, 'booking_history.html', context)

def create_booking(request, room_id):
    if 'is_logged_in' not in request.session:
        return redirect(f"{settings.LOGIN_URL}?next={request.path}")
    room = get_object_or_404(Loaiphong, phong_id=room_id)
    if request.method == 'POST':
        checkin_date = request.POST.get('checkin_date')
        checkout_date = request.POST.get('checkout_date')

        try:
            checkin = datetime.strptime(checkin_date, '%Y-%m-%d').date()
            checkout = datetime.strptime(checkout_date, '%Y-%m-%d').date()

            if checkin < datetime.now().date():
                messages.error(request, 'Ngày check-in không được nhỏ hơn ngày hiện tại.')
                return render(request, 'create_booking.html', {'room': room})
            if checkout <= checkin:
                messages.error(request, 'Ngày check-out phải lớn hơn ngày check-in.')
                return render(request, 'create_booking.html', {'room': room})

            nights = (checkout - checkin).days
            total_price = room.gia * nights

            lichsu_id = f'BK{int(datetime.now().timestamp())}'
            while Dondatphong.objects.filter(lichsu_id=lichsu_id).exists():
                lichsu_id = f'BK{int(datetime.now().timestamp())}'

            booking = Dondatphong.objects.create(
                lichsu_id=lichsu_id,
                ngaydat=checkin,
                ngaytra=checkout,
                tongtien=total_price,
                trangthai='PENDING',
                thoigiandat=datetime.now().date(),
                nguoidungnguoidung=Nguoidung.objects.get(nguoidung_id=request.session['nguoidung_id']),
                phongphong=room
            )
            messages.success(request, 'Đặt phòng thành công! Vui lòng kiểm tra chi tiết.')
            return redirect('bookings:booking_detail', booking_id=booking.lichsu_id)

        except ValueError:
            messages.error(request, 'Định dạng ngày không hợp lệ. Vui lòng nhập đúng định dạng YYYY-MM-DD.')
            return render(request, 'create_booking.html', {'room': room})

    return render(request, 'create_booking.html', {'room': room})

@require_POST
def cancel_booking(request, booking_id):
    if 'is_logged_in' not in request.session:
        return redirect(f"{settings.LOGIN_URL}?next={request.path}")
    booking = get_object_or_404(Dondatphong, lichsu_id=booking_id)
    if booking.trangthai == 'PENDING' and not ThanhToan.objects.filter(dondatphong=booking, trangthai='SUCCESS').exists():
        booking.trangthai = 'CANCELLED'
        booking.save()
        messages.success(request, 'Đã hủy đặt phòng thành công!')
    else:
        messages.error(request, 'Không thể hủy đặt phòng.')
    return redirect('bookings:booking_detail', booking_id=booking_id)