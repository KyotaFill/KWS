# Triển khai KWS

KWS dùng database riêng tên `kws`, dịch vụ `kws-*`, thư mục `/etc/kws`, `/opt/kws`, `/srv/kws`. Các mẫu trong `lan` dành cho máy chủ chuyên biệt; cần cấu hình hostname/TLS, user hệ điều hành và khóa MFA trước triển khai. Vai trò SQL `wms_owner`/`wms_app` và schema `wms` được giữ để tương thích migration.

[Hướng dẫn chạy và worker](../01_Tai_lieu/CAI_DAT.md). Chưa có nghiệm thu máy chủ vận hành cho KWS; không sử dụng số liệu nghiệm thu WMS làm bằng chứng KWS.
