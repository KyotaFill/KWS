# Kiểm tra KWS

Kết quả ngày **14/10/2026**, trên Linux x86_64, Python 3.12, PostgreSQL tạm, Nginx 1.24 và Xvfb.

| Kiểm tra | Kết quả |
|---|---|
| Ứng dụng, nghiệp vụ, API, giao diện, bảo mật và cạnh tranh | 733 ca đạt; 0 ca còn lỗi hoặc bị bỏ qua |
| Cấu hình triển khai, quyền database và HTTPS proxy | 29 ca đạt |
| Hợp đồng API | 109 đường dẫn, 139 thao tác khớp mã chạy |
| Tài liệu và ảnh | 12 chức năng, 13 ảnh và checksum hợp lệ |
| Sơ đồ | 36 hình; kiểm tra BPMN, UML, ERD và nguồn giáo trình đạt |
| Ruff | Đạt |
| Gói Python | Build thành công `kws_lan-0.1.0-py3-none-any.whl` |

Kết quả ứng dụng tổng hợp lượt toàn bộ và các lượt chạy lại nhóm liên quan sau sửa; mỗi ca dùng kết quả gần nhất. [Danh sách ca và nguồn kết quả](results.json). Cơ sở dữ liệu và dữ liệu trong ảnh được tạo riêng cho kiểm thử.

Các kiểm tra gồm: quyền theo kho, MFA/thu hồi phiên, duyệt độc lập, nhập/xuất trực tiếp, chống ghi sổ trùng khi mất phản hồi hoặc tiến trình bị dừng, tranh chấp cùng serial, đối soát sổ/số dư và chạy worker. Bài hồi quy tải dùng **15 phiên đồng thời, 1 giây làm nóng và 5 giây đo**, với ghi sổ thật qua HTTPS trên database kiểm thử. Đây là kiểm tra hồi quy ngắn, không phải cam kết năng lực vận hành.

## Chạy lại

```bash
xvfb-run -a python scripts/check_application.py --gui --jobs 4
python scripts/check_application.py --test-path deploy/lan/tests --report .reports/deployment.xml
python scripts/export_runtime_contract.py --check
python scripts/check_report_current.py
python scripts/check_diagram_notation.py
python scripts/check_artifacts.py
python -m ruff check apps packages tests scripts
python -m build --wheel --no-isolation
```

Cần PostgreSQL server tools, Nginx, Tk và Xvfb. Nếu Nginx không nằm trong PATH, đặt `KWS_TEST_NGINX_BINARY`. Runner tạo database tạm và không dùng `KWS_DATABASE_URL` vận hành.

Windows/macOS và bộ cài ký phát hành chưa được kiểm thử cho KWS. Chưa có phép đo so sánh dung lượng cài đặt hoặc RAM với WMS. Starlette hiện phát cảnh báo deprecation cho HTTPX trong TestClient; các ca kiểm tra vẫn thực thi đầy đủ.
