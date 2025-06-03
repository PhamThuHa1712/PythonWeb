from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from rooms.models import Dondatphong, Loaiphong, Khachsan, Nguoidung
from .models import ThanhToan
from django.contrib.auth.decorators import login_required
from datetime import datetime


def booking_detail(request, booking_id):
    booking = get_object_or_404(Dondatphong, lichsu_id=booking_id)
    room = booking.phongphong
    hotel = room.khachsankhachsan
    user = booking.nguoidungnguoidung
    nights = (booking.ngaytra - booking.ngaydat).days
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
        'booking.nights': nights,
        'booking.guests': 1,  # Giả định 1 khách
        'booking.created_display': booking.thoigiandat,
        'booking.show_cancel': booking.trangthai == 'PENDING' and payment_status != 'SUCCESS',
    }
    return render(request, 'booking_detail.html', context)

def payment(request, booking_id):
    booking = get_object_or_404(Dondatphong, lichsu_id=booking_id)
    context = {
        'booking': booking,
    }
    return render(request, 'payment.html', context)

@require_POST
def process_payment(request, booking_id):
    booking = get_object_or_404(Dondatphong, lichsu_id=booking_id)
    sothe = request.POST.get('credit_card_number')
    ngayhethan = request.POST.get('expiration_date')
    cvv = request.POST.get('cvv')

    # Giả lập kiểm tra thanh toán
    # if len(sothe) == 16 and len(cvv) in [3, 4] and len(ngayhethan) == 5:
    #     payment = ThanhToan.objects.create(
    #         thanhtoan_id=f'PAY{booking.lichsu_id}',
    #         dondatphong=booking,
    #         sothe=sothe[-4:],  # Lưu 4 số cuối
    #         ngayhethan=ngayhethan,
    #         cvv=cvv,
    #         trangthai='SUCCESS'
    #     )
    #     booking.trangthai = 'CONFIRMED'
    #     booking.save()
    #     messages.success(request, 'Thanh toán thành công!')
    # else:
    #     messages.error(request, 'Thông tin thanh toán không hợp lệ.')
    #     return redirect('bookings:booking_detail', booking_id=booking_id)

    return redirect('bookings:booking_detail', booking_id=booking_id)

# @login_required
def booking_history(request):
    if not request.user.is_authenticated:
        return redirect('login')
    bookings = Dondatphong.objects.filter(nguoidungnguoidung__nguoidung_id=request.user.username)
    context = {
        'bookings': bookings,
    }
    return render(request, 'booking_history.html', context)


# @login_required
def create_booking(request, room_id):
    room = get_object_or_404(Loaiphong, phong_id=room_id)
    if request.method == 'POST':
        checkin_date = request.POST.get('checkin_date')
        checkout_date = request.POST.get('checkout_date')
        checkin = datetime.strptime(checkin_date, '%Y-%m-%d').date()
        checkout = datetime.strptime(checkout_date, '%Y-%m-%d').date()
        nights = (checkout - checkin).days
        total_price = room.gia * nights
        booking = Dondatphong.objects.create(
            lichsu_id=f'BK{int(datetime.now().timestamp())}',
            ngaydat=checkin,
            ngaytra=checkout,
            tongtien=total_price,
            trangthai='PENDING',
            thoigiandat=datetime.now().date(),
            nguoidungnguoidung=request.user,
            phongphong=room
        )
        return redirect('bookings:booking_detail', booking_id=booking.lichsu_id)
    return render(request, 'bookings/create_booking.html', {'room': room})


@require_POST
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Dondatphong, lichsu_id=booking_id)
    if booking.trangthai == 'PENDING' and not ThanhToan.objects.filter(dondatphong=booking, trangthai='SUCCESS').exists():
        booking.trangthai = 'CANCELLED'
        booking.save()
        messages.success(request, 'Đã hủy đặt phòng thành công!')
    else:
        messages.error(request, 'Không thể hủy đặt phòng.')
    return redirect('bookings:booking_detail', booking_id=booking_id)