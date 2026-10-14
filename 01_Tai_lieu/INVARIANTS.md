# Bất biến dữ liệu KWS

PostgreSQL là nguồn dữ liệu chính thức. Desktop chỉ gọi API; SQLite chứa nháp và nhật ký, không dùng để ghi sổ tồn khi mất kết nối.

## Số lượng và danh tính

Số lượng dùng Decimal, đổi đơn vị theo hệ số chụp tại dòng chứng từ; không âm thầm làm tròn. Đơn vị cơ sở/tracking không đổi sau phát sinh. Hàng trong KWS thuộc COMPANY; lô và serial phải đúng sản phẩm. Mỗi serial chỉ có một vị trí tồn hiện hữu và được ghi theo lượng một đơn vị.

## Phát sinh và số dư

Sổ stock_move chỉ thêm; on_hand bằng tổng nhập trừ tổng xuất. reserved bằng lượng giữ chưa tiêu thụ hoặc giải phóng. Lượng khả dụng không gồm hàng hết hạn hoặc nguồn bị khóa. Nhập và tồn đầu kỳ mới đi vào STORAGE; xuất dùng nguồn đã giữ. Không vượt lượng đơn nguồn, phiếu, tồn hay reservation còn lại.

## Giao dịch

Khóa idempotency theo actor/key trước; kiểm quyền hiện tại, hash yêu cầu và phiên bản. Khóa chứng từ nguồn trước chứng từ thực hiện; khóa kho/kỳ, vị trí, sản phẩm, số dư và reservation theo thứ tự ổn định. Kiểm tra mọi dòng trước khi ghi. Sổ, số dư, tiêu thụ giữ hàng, tiến độ chứng từ, audit, outbox và ACK cùng transaction; lỗi rollback toàn bộ.

Ghi sổ kiểm tra execution_key ngoài idempotency key. Cùng khóa khác nội dung bị từ chối. Khi mất phản hồi, tra ACK bằng yêu cầu gốc; không tự tạo khóa mới hoặc tự gửi lúc khởi động.

## Phê duyệt và quyền

Kiểm tra quyền hiện tại, phạm vi kho và thời hạn cấp quyền trên máy chủ. Người lập không tự duyệt; nội dung phê duyệt gắn với phiên bản chứng từ. Sửa sau duyệt làm mất hiệu lực phê duyệt theo quy trình. Ngày ghi sổ phải thuộc một kỳ OPEN; công cụ bootstrap chỉ tạo kỳ đầu cho kho mới.

## Tệp và tiến trình

Không gọi HTTP, spool máy in hay I/O tệp trong transaction ghi sổ. Snapshot báo cáo/in và quyền truy cập được kiểm tra lại khi tải. Worker có lease và cơ chế chống chạy trùng. Giao diện Tk chỉ được cập nhật/hủy ở luồng chính; đóng ứng dụng chờ worker kết thúc.

## Tương thích lưu trữ

Migration PostgreSQL 001–026 và SQLite 001–003 giữ nguyên. Schema `wms` chứa bảng kế thừa của các phân hệ không được cung cấp trong KWS; không đưa điều đó thành một tính năng trong báo cáo. Không dùng chung database, cache hoặc kho token với WMS.
