# BÁO CÁO ĐỒ ÁN CUỐI KỲ
## ĐỀ TÀI: HỆ THỐNG QUẢN LÝ VÀ DỰ BÁO DỮ LIỆU SẢN PHẨM - ĐƠN HÀNG

## 1. CẤU HÌNH CƠ SỞ DỮ LIỆU VỚI DOCKER
Hệ thống sử dụng PostgreSQL được đóng gói trong Docker Container để quản lý thông tin sản phẩm và đơn hàng.
* File cấu hình hệ thống: `docker-compose.yml`
* Hệ quản trị CSDL: PostgreSQL 15

## 2. KẾT NỐI VÀ XỬ LÝ DỮ LIỆU BẰNG PYTHON
Sử dụng thư viện `pandas` kết hợp với `sqlalchemy` để thực hiện các kết nối, truy vấn dữ liệu từ các bảng `products` (Sản phẩm) và `orders` (Đơn hàng). Hệ thống tự động khởi tạo bảng dữ liệu và nạp dữ liệu mẫu khi ứng dụng khởi chạy lần đầu.

## 3. CHỨC NĂNG NÂNG CAO: MÔ HÌNH HỌC MÁY (MACHINE LEARNING)
Đồ án tích hợp mô hình **Hồi quy tuyến tính (Linear Regression)** từ thư viện `scikit-learn` để dự báo giá trị tổng tiền của đơn hàng dựa trên hai yếu tố đầu vào:
* Số lượng sản phẩm khách hàng đặt mua.
* Đơn giá niêm yết của sản phẩm đó.

## 4. BIỂU DIỄN DỮ LIỆU LÊN MÀN HÌNH BẰNG GRADIO
Giao diện trực quan hóa được xây dựng bằng **Gradio**, chia làm các Tab chức năng thông minh:
* **Tab Xem dữ liệu:** Hiển thị bảng danh sách sản phẩm và đơn hàng trực tiếp từ cơ sở dữ liệu khi nhấn nút làm mới.
* **Tab Dự báo AI:** Cho phép kéo thanh trượt chọn số lượng, nhập đơn giá để mô hình Machine Learning tính toán và trả về kết quả dự báo tổng tiền ngay lập tức.
