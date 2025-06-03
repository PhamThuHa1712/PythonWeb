USE MASTER;
GO
CREATE DATABASE Hotel_Booking;
GO
USE Hotel_Booking;
GO

-- Bảng DiaDiem
CREATE TABLE DiaDiem (
    diadiem_id VARCHAR(20) PRIMARY KEY,
    tenDiaDiem VARCHAR(100)
);

-- Bảng QuanHuyen
CREATE TABLE QuanHuyen (
    quanhuyen_id VARCHAR(20) PRIMARY KEY,
    tenQuanHuyen VARCHAR(100),
    DiaDiemdiadiem_id VARCHAR(20),
	FOREIGN KEY (DiaDiemdiadiem_id) REFERENCES DiaDiem(diadiem_id)
);

-- Bảng KhachSan
CREATE TABLE KhachSan (
    khachsan_id VARCHAR(20) PRIMARY KEY,
    tenKhachSan VARCHAR(200),
    diaChi VARCHAR(100),
    thanhPho VARCHAR(100),
    moTa VARCHAR(1000),
    ngayThem DATE,
    DiaDiemdiadiem_id VARCHAR(20), -- Khóa ngoại tham chiếu đến bảng DiaDiem
    FOREIGN KEY (DiaDiemdiadiem_id) REFERENCES DiaDiem(diadiem_id)
);

-- Bảng LoaiPhong
CREATE TABLE LoaiPhong (
    phong_id VARCHAR(20) PRIMARY KEY,
    tenPhong VARCHAR(100),
    soGiuong INTEGER,
    gia FLOAT,
    moTa VARCHAR(1000),
    ngayThemPhong DATE,
    KhachSankhachsan_id VARCHAR(20), -- Khóa ngoại tham chiếu đến bảng KhachSan
    FOREIGN KEY (KhachSankhachsan_id) REFERENCES KhachSan(khachsan_id)
);

-- Bảng HinhAnh
CREATE TABLE HinhAnh (
    anh_id VARCHAR(20) PRIMARY KEY,
    urlHinhAnh VARCHAR(100),
    Phongphong_id VARCHAR(20), -- Khóa ngoại tham chiếu đến bảng LoaiPhong
	FOREIGN KEY (Phongphong_id) REFERENCES LoaiPhong(phong_id)
);

-- Bảng NguoiDung
CREATE TABLE NguoiDung (
    nguoidung_id VARCHAR(20) PRIMARY KEY,
    tenNguoiDung VARCHAR(100),
    email VARCHAR(100),
    matKhau VARCHAR(100),
    dienThoai VARCHAR(100),
    vaiTro VARCHAR(10),
    ngayTaoTK DATE
);

-- Bảng lichsuDatPhong
CREATE TABLE DonDatPhong (
    lichsu_id VARCHAR(20) PRIMARY KEY,
    ngayDat DATE,
    ngayTra DATE,
    tongTien FLOAT,
    trangThai VARCHAR(20),
    thoiGianDat DATE, 
    NguoiDungnguoidung_id VARCHAR(20), -- Khóa ngoại tham chiếu đến bảng NguoiDung
    Phongphong_id VARCHAR(20), -- Khóa ngoại tham chiếu đến bảng LoaiPhong
    FOREIGN KEY (NguoiDungnguoidung_id) REFERENCES NguoiDung(nguoidung_id),
    FOREIGN KEY (Phongphong_id) REFERENCES LoaiPhong(phong_id)
);

-- Dữ liệu mẫu cho bảng DiaDiem
INSERT INTO DiaDiem VALUES
('DD001', 'Ha Noi'),
('DD002', 'Da Nang'),
('DD003', 'TP Ho Chi Minh');

-- Dữ liệu mẫu cho bảng QuanHuyen
INSERT INTO QuanHuyen VALUES
('QH001', 'Cau Giay', 'DD001'),
('QH002', 'Hai Chau', 'DD002'),
('QH003', 'Quan 1', 'DD003');

-- Dữ liệu mẫu cho bảng KhachSan
INSERT INTO KhachSan VALUES
('KS001', 'Khach san Hoang Ha', '12 Nguyen Van Cu', 'Ha Noi', 'Gan trung tam thanh pho', '2024-05-01', 'DD001'),
('KS002', 'Khach san Bien Xanh', '45 Tran Phu', 'Da Nang', 'Gan bai bien My Khe', '2024-05-10', 'DD002'),
('KS003', 'Khach san Sai Gon Star', '78 Le Loi', 'TP Ho Chi Minh', 'Gan cho Ben Thanh', '2024-05-15', 'DD003');

-- Dữ liệu mẫu cho bảng LoaiPhong
INSERT INTO LoaiPhong VALUES
('LP001', 'Phong don', 1, 500000, 'Phong cho 1 nguoi', '2024-05-01', 'KS001'),
('LP002', 'Phong doi', 2, 800000, 'Phong cho 2 nguoi', '2024-05-10', 'KS002'),
('LP003', 'Phong gia dinh', 3, 1200000, 'Phong cho gia dinh 4 nguoi', '2024-05-15', 'KS003');

-- Dữ liệu mẫu cho bảng HinhAnh
INSERT INTO HinhAnh VALUES
('HA001', 'https://example.com/phongdon.jpg', 'LP001'),
('HA002', 'https://example.com/phongdoi.jpg', 'LP002'),
('HA003', 'https://example.com/phonggiadinh.jpg', 'LP003');

-- Dữ liệu mẫu cho bảng NguoiDung
INSERT INTO NguoiDung VALUES
('ND001', 'Nguyen Van A', 'vana@example.com', 'matkhau1', '0905123456', 'user', '2024-05-01'),
('ND002', 'Tran Thi B', 'thib@example.com', 'matkhau2', '0905234567', 'admin', '2024-05-05'),
('ND003', 'Le Van C', 'vanc@example.com', 'matkhau3', '0905345678', 'user', '2024-05-10');

-- Dữ liệu mẫu cho bảng DonDatPhong
INSERT INTO DonDatPhong VALUES
('DDP001', '2024-06-01', '2024-06-03', 1000000, 'Da dat', '2024-05-20', 'ND001', 'LP001'),
('DDP002', '2024-06-05', '2024-06-07', 1600000, 'Da dat', '2024-05-21', 'ND002', 'LP002'),
('DDP003', '2024-06-10', '2024-06-13', 3600000, 'Cho xac nhan', '2024-05-22', 'ND003', 'LP003');

-- Chọn tất cả dữ liệu từ bảng DiaDiem
SELECT * FROM DiaDiem;

-- Chọn tất cả dữ liệu từ bảng QuanHuyen
SELECT * FROM QuanHuyen;

-- Chọn tất cả dữ liệu từ bảng KhachSan
SELECT * FROM KhachSan;

-- Chọn tất cả dữ liệu từ bảng LoaiPhong
SELECT * FROM LoaiPhong;

-- Chọn tất cả dữ liệu từ bảng HinhAnh
SELECT * FROM HinhAnh;

-- Chọn tất cả dữ liệu từ bảng NguoiDung
SELECT * FROM NguoiDung;

-- Chọn tất cả dữ liệu từ bảng DonDatPhong
SELECT * FROM DonDatPhong;