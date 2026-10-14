-- Chạy bằng tài khoản đọc, kết quả mong đợi: 0 dòng mỗi truy vấn.
SET search_path TO wms, public;
WITH legs AS (
 SELECT stock_item_id,destination_location_id AS location_id,quantity_base AS qty FROM stock_move
 UNION ALL SELECT stock_item_id,source_location_id,-quantity_base FROM stock_move
), ledger AS (
 SELECT stock_item_id,location_id,SUM(qty) qty FROM legs JOIN location l ON l.id=location_id
 WHERE l.kind IN ('STORAGE','RECEIVING','QUARANTINE','SHIPPING','TRANSIT') GROUP BY stock_item_id,location_id
)
SELECT COALESCE(l.stock_item_id,b.stock_item_id) stock_item_id,COALESCE(l.location_id,b.location_id) location_id,l.qty,b.on_hand
FROM ledger l FULL JOIN stock_balance b USING(stock_item_id,location_id) WHERE COALESCE(l.qty,0) <> COALESCE(b.on_hand,0);
WITH r AS (SELECT stock_item_id,location_id,SUM(quantity-consumed-released) qty FROM reservation GROUP BY stock_item_id,location_id)
SELECT COALESCE(r.stock_item_id,b.stock_item_id),COALESCE(r.location_id,b.location_id),r.qty,b.reserved
FROM r FULL JOIN stock_balance b USING(stock_item_id,location_id) WHERE COALESCE(r.qty,0) <> COALESCE(b.reserved,0);
SELECT si.serial_id,COUNT(*) positive_positions,SUM(b.on_hand) qty
FROM stock_balance b JOIN stock_item si ON si.id=b.stock_item_id
WHERE si.serial_id IS NOT NULL AND b.on_hand > 0 GROUP BY si.serial_id HAVING COUNT(*) <> 1 OR SUM(b.on_hand) <> 1;
SELECT sm.id FROM stock_move sm JOIN inventory_transaction it ON it.id=sm.transaction_id
JOIN document_line dl ON dl.id=sm.line_id JOIN stock_item si ON si.id=sm.stock_item_id
JOIN product p ON p.id=si.product_id
WHERE dl.document_id<>it.document_id OR dl.product_id<>si.product_id OR sm.base_uom_id<>p.base_uom_id;
