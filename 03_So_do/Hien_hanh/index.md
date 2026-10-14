# Sơ đồ hiện hành của KWS

Sinh từ mã nguồn và schema PostgreSQL dựng bằng migration 001–026. Các luồng mô tả xử lý trong phần mềm; không đại diện cho khảo sát quy trình doanh nghiệp.

[Ký pháp và nguồn giáo trình](../NOTATION_GUIDE.md). Use case và BPMN dùng bố cục riêng; ERD dùng Crow’s Foot và lực lượng quan hệ suy từ schema. Lớp dùng các ngăn UML.

| Sơ đồ | Nguồn đối chiếu | Phạm vi / điều kiện |
|---|---|---|
| [Kiến trúc ứng dụng hiện tại](svg/ARCHITECTURE.svg) | `apps/desktop/views/shell.py`; `apps/server/api/app.py`; `deploy/lan`; `apps/desktop/local_store/session_vault.py` |  |
| [Các lớp desktop đang triển khai](svg/CLASS_DESKTOP.svg) | `apps/desktop/views/shell.py`; `apps/desktop/views/orders.py`; `apps/desktop/presenters/orders.py`; `apps/desktop/api/identity.py`; `apps/desktop/local_store/recovery.py`; `apps/desktop/local_store/commands.py` |  |
| [Các lớp xử lý lệnh trên máy chủ](svg/CLASS_SERVER.svg) | `apps/server/application/orders.py`; `apps/server/application/receipts.py`; `apps/server/application/commands.py`; `apps/server/infrastructure/database.py`; `apps/server/infrastructure/database.py`; `apps/server/application/ports.py` |  |
| [Các hợp đồng dữ liệu và lỗi đang triển khai](svg/CLASS_CONTRACTS.svg) | `packages/contracts/orders.py`; `packages/contracts/receipts.py`; `packages/contracts/orders.py`; `packages/contracts/receipts.py`; `apps/server/application/commands.py`; `apps/server/domain/errors.py` |  |
| [Trạng thái chứng từ và điều kiện chuyển](svg/STATE_DOCUMENT.svg) | `apps/server/application/orders.py`; `apps/server/application/receipts.py`; `apps/server/application/issues.py` |  |
| [Luồng xử lý lệnh và phục hồi ACK](svg/COMMAND_RECOVERY.svg) | `apps/desktop/local_store/recovery.py`; `apps/server/api/recovery.py`; `apps/server/application/commands.py` |  |
| [Nhận hàng — phê duyệt và ghi sổ](svg/FLOW_RECEIPT.svg) | `apps/server/application/receipts.py`; `apps/server/application/orders.py` | Nhận thẳng vào STORAGE; từ chối hàng hết hạn, sai kho hoặc vượt đơn mua. |
| [Xuất kho — duyệt, giữ hàng và ghi sổ](svg/FLOW_ISSUE.svg) | `apps/server/application/issues.py`; `apps/server/application/reservations.py` | KWS xuất trực tiếp từ nguồn đã giữ; không có bước soạn hàng hoặc đóng kiện. |
| [Tải lại hoặc đóng ứng dụng](svg/FLOW_LIFECYCLE.svg) | `apps/desktop/views/shell.py`; `apps/desktop/lifecycle.py`; `apps/desktop/__main__.py` | Tải lại khởi động lại phần mềm đang cài sau khi giải phóng tài nguyên; không tải bộ cài từ Internet. |
| [Use case — Không gian làm việc](svg/UC_CURRENT_01.svg) | `apps/desktop/views/admin_workspace.py`; `apps/desktop/views/session.py` | Actor chỉ tham gia use case khi được cấp quyền; scope kho, thời hạn và tách nhiệm vụ vẫn được kiểm tra. |
| [Use case — Dữ liệu](svg/UC_CURRENT_02.svg) | `apps/desktop/views/admin_workspace.py`; `apps/desktop/views/master_data.py` | Actor chỉ tham gia use case khi được cấp quyền; scope kho, thời hạn và tách nhiệm vụ vẫn được kiểm tra. |
| [Use case — Nhập hàng](svg/UC_CURRENT_03.svg) | `apps/desktop/views/admin_workspace.py`; `apps/desktop/views/orders.py`; `apps/desktop/views/approvals.py`; `apps/desktop/views/receipts.py`; `apps/desktop/views/openings.py` | Actor chỉ tham gia use case khi được cấp quyền; scope kho, thời hạn và tách nhiệm vụ vẫn được kiểm tra. |
| [Use case — Vận hành kho](svg/UC_CURRENT_04.svg) | `apps/desktop/views/admin_workspace.py`; `apps/desktop/views/issues.py` | Actor chỉ tham gia use case khi được cấp quyền; scope kho, thời hạn và tách nhiệm vụ vẫn được kiểm tra. |
| [Use case — Kiểm soát](svg/UC_CURRENT_05.svg) | `apps/desktop/views/admin_workspace.py`; `apps/desktop/views/reports.py` | Actor chỉ tham gia use case khi được cấp quyền; scope kho, thời hạn và tách nhiệm vụ vẫn được kiểm tra. |
| [Use case — Công cụ & hệ thống](svg/UC_CURRENT_06.svg) | `apps/desktop/views/admin_workspace.py`; `apps/desktop/printing/view.py`; `apps/desktop/views/admin.py`; `apps/desktop/views/recovery.py`; `apps/desktop/views/shell.py` | Actor chỉ tham gia use case khi được cấp quyền; scope kho, thời hạn và tách nhiệm vụ vẫn được kiểm tra. |
| [ERD · app_user](svg/ERD_app_user.svg) | `02_CSDL/current/schema.json`; `migrations/001_schema.sql … 026_user_avatar.sql` |  |
| [ERD · approval_request](svg/ERD_approval_request.svg) | `02_CSDL/current/schema.json`; `migrations/001_schema.sql … 026_user_avatar.sql` |  |
| [ERD · audit_event](svg/ERD_audit_event.svg) | `02_CSDL/current/schema.json`; `migrations/001_schema.sql … 026_user_avatar.sql` |  |
| [ERD · document](svg/ERD_document.svg) | `02_CSDL/current/schema.json`; `migrations/001_schema.sql … 026_user_avatar.sql` |  |
| [ERD · document_line](svg/ERD_document_line.svg) | `02_CSDL/current/schema.json`; `migrations/001_schema.sql … 026_user_avatar.sql` |  |
| [ERD · idempotency_record](svg/ERD_idempotency_record.svg) | `02_CSDL/current/schema.json`; `migrations/001_schema.sql … 026_user_avatar.sql` |  |
| [ERD · inventory_transaction](svg/ERD_inventory_transaction.svg) | `02_CSDL/current/schema.json`; `migrations/001_schema.sql … 026_user_avatar.sql` |  |
| [ERD · location](svg/ERD_location.svg) | `02_CSDL/current/schema.json`; `migrations/001_schema.sql … 026_user_avatar.sql` |  |
| [ERD · outbox_event](svg/ERD_outbox_event.svg) | `02_CSDL/current/schema.json`; `migrations/001_schema.sql … 026_user_avatar.sql` |  |
| [ERD · partner](svg/ERD_partner.svg) | `02_CSDL/current/schema.json`; `migrations/001_schema.sql … 026_user_avatar.sql` |  |
| [ERD · permission](svg/ERD_permission.svg) | `02_CSDL/current/schema.json`; `migrations/001_schema.sql … 026_user_avatar.sql` |  |
| [ERD · product](svg/ERD_product.svg) | `02_CSDL/current/schema.json`; `migrations/001_schema.sql … 026_user_avatar.sql` |  |
| [ERD · reservation](svg/ERD_reservation.svg) | `02_CSDL/current/schema.json`; `migrations/001_schema.sql … 026_user_avatar.sql` |  |
| [ERD · role](svg/ERD_role.svg) | `02_CSDL/current/schema.json`; `migrations/001_schema.sql … 026_user_avatar.sql` |  |
| [ERD · stock_balance](svg/ERD_stock_balance.svg) | `02_CSDL/current/schema.json`; `migrations/001_schema.sql … 026_user_avatar.sql` |  |
| [ERD · stock_item](svg/ERD_stock_item.svg) | `02_CSDL/current/schema.json`; `migrations/001_schema.sql … 026_user_avatar.sql` |  |
| [ERD · stock_move](svg/ERD_stock_move.svg) | `02_CSDL/current/schema.json`; `migrations/001_schema.sql … 026_user_avatar.sql` |  |
| [ERD · stock_period](svg/ERD_stock_period.svg) | `02_CSDL/current/schema.json`; `migrations/001_schema.sql … 026_user_avatar.sql` |  |
| [ERD · uom](svg/ERD_uom.svg) | `02_CSDL/current/schema.json`; `migrations/001_schema.sql … 026_user_avatar.sql` |  |
| [ERD · user_role_grant](svg/ERD_user_role_grant.svg) | `02_CSDL/current/schema.json`; `migrations/001_schema.sql … 026_user_avatar.sql` |  |
| [ERD · warehouse](svg/ERD_warehouse.svg) | `02_CSDL/current/schema.json`; `migrations/001_schema.sql … 026_user_avatar.sql` |  |
