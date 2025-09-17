# Simple File Explorer

Một ứng dụng web đơn giản được xây dựng bằng Python và Flask để duyệt, xem và tải xuống các tệp tin trên máy chủ cục bộ.

## Tính năng nổi bật

- **Giao diện duyệt file trực quan:** Dễ dàng điều hướng qua các thư mục và xem danh sách tệp tin.
- **Tự động tạo thư mục:** Ứng dụng sẽ tự động tạo thư mục `files` để chứa các tệp cần chia sẻ trong lần khởi động đầu tiên nếu nó chưa tồn tại.
- **Sắp xếp thông minh:** Sắp xếp danh sách tệp tin theo Tên, Ngày sửa đổi, Loại tệp, và Kích thước.
- **Xem trước file:** Hỗ trợ xem trước nhiều định dạng file phổ biến (ảnh, video, audio, text, PDF,...) trực tiếp trên trình duyệt mà không cần tải về.
- **Tải xuống & Sao chép link:** Cho phép tải xuống bất kỳ tệp nào và cung cấp nút sao chép đường dẫn tải xuống trực tiếp vào clipboard.
- **Thiết kế Responsive:** Giao diện được tối ưu để hoạt động mượt mà trên cả máy tính và thiết bị di động.

## Công nghệ sử dụng

- **Backend:** Python 3, Flask
- **Frontend:** HTML5, CSS3, JavaScript (không sử dụng framework)

## Hướng dẫn Cài đặt và Sử dụng

### Yêu cầu

- Đã cài đặt [Python 3](https://www.python.org/downloads/).

### Các bước cài đặt

1.  Tải về hoặc clone toàn bộ mã nguồn của dự án này.
2.  Mở Terminal (hoặc Command Prompt) trong thư mục gốc của dự án.
3.  Cài đặt thư viện Flask cần thiết bằng lệnh:
    ```sh
    pip install -r requirements.txt
    ```

### Sử dụng

1.  **Thêm tệp tin:** Đặt tất cả các tệp và thư mục bạn muốn chia sẻ vào trong thư mục `files` ở thư mục gốc của dự án.
    *(Lưu ý: Nếu thư mục `files` không tồn tại, ứng dụng sẽ tự tạo nó cho bạn khi khởi động.)*

2.  **Khởi động server:**
    - **Trên Windows:** Chạy tệp `run.bat`.
    - **Trên các hệ điều hành khác (hoặc chạy thủ công):** Mở terminal và chạy lệnh:
      ```sh
      python app.py
      ```

3.  **Truy cập ứng dụng:** Mở trình duyệt web và truy cập vào địa chỉ `http://localhost:5006` (hoặc cổng mà bạn đã tùy chỉnh).

## Tùy chỉnh

### Thay đổi cổng (Port)

- Mặc định, server chạy ở cổng `5006`.
- Để thay đổi, bạn có thể sửa số cổng trong tệp `run.bat`.
- Hoặc, bạn có thể truyền số cổng mong muốn như một tham số khi chạy ứng dụng:
  ```sh
  python app.py 8000
  ```
  Lệnh trên sẽ khởi động server ở cổng `8000`.
