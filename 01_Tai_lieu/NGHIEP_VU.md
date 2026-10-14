# Nghiệp vụ KWS

## Phạm vi

KWS quản lý hàng thuộc doanh nghiệp theo kho, vị trí, sản phẩm và đơn vị cơ sở. Người vận hành thực hiện đơn mua/bán, duyệt, nhập, xuất, tồn đầu kỳ, báo cáo và in. Tài khoản/phân quyền, kết nối và phục hồi bảo vệ các luồng này.

| Thao tác | Điều kiện | Kết quả |
|---|---|---|
| Lập PO/SO | Danh mục hợp lệ, quyền lập theo kho | Chứng từ nháp, chưa ảnh hưởng tồn |
| Gửi duyệt | Dòng hàng hợp lệ, đúng phiên bản và policy | Yêu cầu phê duyệt gắn nội dung chứng từ |
| Phê duyệt | Đúng bước, quyền còn hiệu lực, không tự duyệt | Phiếu đủ điều kiện thực hiện hoặc bị từ chối |
| Nhận hàng | PO/phiếu nhận đã duyệt, còn lượng, kỳ mở | Ghi lượng thực nhận vào STORAGE; cập nhật tiến độ PO |
| Tồn đầu kỳ | Kho chưa ghi sổ vận hành, biên bản, phê duyệt | Tồn ban đầu hàng doanh nghiệp tại STORAGE |
| Giữ hàng | Phiếu xuất đã duyệt, tồn khả dụng | Giữ nguồn hàng cụ thể cho phiếu |
| Xuất hàng | Giữ chỗ hợp lệ, nguồn đủ tồn, kỳ mở | Giảm tồn và lượng giữ, cập nhật SO/phiếu xuất |
| Báo cáo/in | Quyền đọc/in và phạm vi kho hiện tại | Snapshot/tệp/PDF; không ghi sổ tồn |

## Quy tắc bảo toàn dữ liệu

Số lượng dùng Decimal, không dùng float để ghi sổ. Số dư và phát sinh phải khớp; không cho tồn hoặc khả dụng âm. Lô/serial, hạn dùng, phạm vi kho và đơn vị được kiểm tra tại máy chủ. Chứng từ nguồn không được thực hiện vượt lượng còn lại.

Mỗi lệnh có idempotency key, hash nội dung và expected_version. Ghi sổ còn có execution_key. Cùng khóa và nội dung trả ACK đã lưu; cùng khóa nhưng khác nội dung bị từ chối. Mất phản hồi không được coi là thất bại để tạo một lệnh mới.

Phê duyệt áp dụng policy và tách nhiệm vụ. Quyền được kiểm tra lại khi ghi sổ, tải tệp và gửi lại lệnh. Không bỏ các kiểm tra này trong bản rút gọn.

## Khác biệt so với WMS

KWS nhận thẳng vào vị trí lưu trữ và xuất trực tiếp từ nguồn đã giữ. Các màn hình và router ký gửi, bảo hành, trường mở rộng, soạn/đóng kiện, kiểm định, di chuyển, chuyển kho, trả hàng, kiểm kê, đảo giao dịch và nhập tệp không được cung cấp. R05/R07 và mẫu in chuyển kho/kiểm kê bị loại khỏi hợp đồng API.

Kỳ kho không có màn hình riêng. Quản trị viên thiết lập kỳ đầu bằng công cụ bootstrap và quản lý kỳ tiếp qua API có phân quyền; việc này vẫn bắt buộc để kiểm soát ngày ghi sổ. Không tự mở kỳ hoặc nới quyền để bỏ qua lỗi nghiệp vụ.

Migration PostgreSQL 001–026 và SQLite 001–003 giữ nguyên. KWS dùng cơ sở dữ liệu, thư mục nháp và token riêng. Các bảng và một số hàm dùng chung kế thừa không được mô tả là tính năng đang bật.

## Trạng thái chứng từ

Nháp → Chờ duyệt → Đã duyệt → Thực hiện một phần → Hoàn tất. Từ chối quay lại bước sửa/gửi; hủy và chỉnh sửa chịu điều kiện trạng thái. Sơ đồ trạng thái mô tả điều kiện chi tiết theo mã thực thi.

## Nguồn đối chiếu

`apps/desktop/views/admin_workspace.py`, `apps/server/api/app.py`, `apps/server/application/orders.py`, `receipts.py`, `openings.py`, `issues.py`, `reservations.py` và các hợp đồng trong `packages/contracts`.
