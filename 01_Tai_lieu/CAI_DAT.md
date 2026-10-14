# Cài đặt KWS

## Môi trường

Python 3.12 trở lên, PostgreSQL 15 trở lên; máy chạy desktop cần Tk và thư viện hệ thống của Pillow/pypdfium2. Trên Ubuntu: cài `python3-venv python3-tk postgresql`. Kiểm thử giao diện cần `xvfb`; sinh sơ đồ cần `graphviz poppler-utils` và font DejaVu.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-app-lock.txt
python -m pip install -e '.[server,desktop,dev]'
```

## Máy chủ

Tạo PostgreSQL database và user riêng cho KWS. Thiết lập biến môi trường bằng công cụ quản lý bí mật của môi trường triển khai, không ghi mật khẩu vào repository. `.env.example` chỉ là mẫu, ứng dụng không tự đọc tệp này.

- `KWS_DATABASE_URL`: URL `postgresql+psycopg://…` trỏ vào database KWS.
- `KWS_MFA_ENCRYPTION_KEY`: khóa Fernet tạo một lần, giữ bền vững và sao lưu riêng.
- `KWS_HOST`, `KWS_PORT`: mặc định `127.0.0.1`, `8000`.
- `KWS_BUSINESS_TIMEZONE`: mặc định `Asia/Ho_Chi_Minh`.

```bash
python -m apps.server.infrastructure.migrations
python -m apps.server.bootstrap --username admin --display-name 'Quản trị KWS'
python -m apps.server
```

Bootstrap hỏi mật khẩu trong terminal. Tài khoản SYSADMIN phải bật MFA để quản trị; quyền kho được cấp riêng. Tạo danh mục kho/vị trí, sản phẩm, đối tác và cấp quyền nghiệp vụ qua giao diện. Thiết lập kỳ đầu của kho trước khi ghi sổ:

```bash
python -m apps.server.bootstrap_period --warehouse-code KHO01 --starts-on 2026-01-01 --ends-on 2026-12-31 --reason 'Thiết lập kỳ đầu'
```

Thay mã kho và khoảng ngày bằng thông tin thực tế. Công cụ chỉ tạo kỳ đầu cho kho chưa có lịch sử; API `/api/v1/periods` quản lý kỳ tiếp theo theo quyền và điều kiện đối soát.

## Worker

Chạy các tiến trình sau cùng cấu hình DB/MFA và thư mục tệp của máy chủ:

```bash
python -m apps.server.worker
python -m apps.server.export_worker
python -m apps.server.print_worker
python -m apps.server.export_cleanup
python -m apps.server.print_cleanup
```

Outbox tạo tác vụ, export/print xử lý tệp, cleanup dọn tệp hết hạn. Không có worker import trong KWS. Nếu bật xác minh email/SMS hoặc quên mật khẩu qua nhà cung cấp, cấu hình và chạy thêm `apps.server.auth_delivery_worker`.

Các biến `KWS_EXPORT_STORAGE_ROOT` và `KWS_PRINT_STORAGE_ROOT` phải trỏ vào hai thư mục riêng, không lồng nhau. Worker PDF không gửi lệnh trực tiếp đến máy in; spool diễn ra trên máy khách sau thao tác người dùng.

## Máy khách

```bash
export KWS_API_URL=http://127.0.0.1:8000/api/v1
python -m apps.desktop
```

HTTP chỉ dùng trên loopback. Qua LAN dùng HTTPS và cấu hình CA bằng `KWS_CA_FILE`. Mặc định dữ liệu cục bộ nằm ở `%LOCALAPPDATA%/kws-lan` (Windows), `~/.local/share/kws-lan` (Linux) hoặc vị trí do hệ điều hành trả về; có thể đặt `KWS_LOCAL_DATA_DIR`. Không dùng chung thư mục WMS.

Đăng nhập, xác thực, chọn kho. Nút **Tải lại** chờ tác vụ hoàn tất rồi khởi động lại ứng dụng để nhận mã nguồn/gói đã cập nhật trên máy; không tự tải bản phát hành từ Internet. Khi thoát có hộp xác nhận để quay lại lưu phần đang nhập.

## Kiểm thử

```bash
xvfb-run -a python scripts/check_application.py --gui
python scripts/export_runtime_contract.py --check
python scripts/check_artifacts.py
```

Cần cài PostgreSQL server tools, Nginx, Tk và Xvfb; nếu Nginx không nằm trong PATH, đặt `KWS_TEST_NGINX_BINARY` tới executable.

Runner tạo PostgreSQL tạm và không sử dụng `KWS_DATABASE_URL` vận hành. Có thể chỉ rõ tệp bằng `--test-path`. Kết quả nằm trong `.reports`.

## Đóng gói

Có cấu hình PyInstaller trong `packaging/windows/KWS.spec` và `packaging/macos/KWS.spec`. Chạy build trên đúng hệ điều hành; tên ứng dụng là KWS, icon từ `apps/desktop/assets/kws-logo.png`. Repository chưa cung cấp bộ cài KWS được ký phát hành.
