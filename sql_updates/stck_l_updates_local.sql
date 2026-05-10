-- QUERIES EXECUTED ON THE HOSTING WITH THE mobilesh_borotest DATABASE!!!

-- UPDATE stck.isbn with borotrade_json.products_id!!!

-- STEP 1

-- update of sku / id - done already in stck

-- STEP 2

-- check if any updates!

SELECT sl.`id`, sl.`id_stck`, sl.`id_lang`, sl.`title`, sl.`description`, sl.`suser`, sl.`stime`, sl.`sactx`, sl.`wid` FROM
`vpws_main`.`borotrade_json` bj left join borotrade_crm.stck s on bj.products_sku = s.sku and bj.products_id = s.isbn left join
-- brortrade_crm.stck_l
(WITH stck_lu AS (SELECT * FROM borotrade_crm.`stck_l` UNION SELECT * FROM borotrade_crm.`stck_la`) SELECT DISTINCT b.* FROM (SELECT abs(id) AS id, MAX(stime) AS stime FROM stck_lu GROUP BY abs(id)) a LEFT JOIN stck_lu b ON a.id=abs(b.id) AND a.stime=b.stime)
 sl on s.id = sl.id_stck
where bj.products_name <> sl.title or CONCAT(ifnull(bj.products_descr_short, ''), ifnull(bj.products_descr_short_upd, '')) <> sl.description;

-- STEP 3

-- INSERT INTO stck_la THE UPDATED RECORDS

INSERT INTO `borotrade_crm`.`stck_la`
-- SELECT -sl.`id`, sl.`id_stck`, sl.`id_lang`, sl.`title`, sl.`description`, sl.`suser`, sl.`stime`, sl.`sactx`, sl.`wid` FROM
SELECT -sl.`id`, sl.`id_stck`, sl.`id_lang`, bj.products_name, CONCAT(ifnull(bj.products_descr_short, ''), ifnull(bj.products_descr_short_upd, '')), sl.`suser`, sl.`stime`, sl.`sactx`, sl.`wid` FROM
`vpws_main`.`borotrade_json` bj left join borotrade_crm.stck s on bj.products_sku = s.sku and bj.products_id = s.isbn left join
-- borotrade_crm.stck_l
(WITH stck_lu AS (SELECT * FROM borotrade_crm.`stck_l` UNION SELECT * FROM borotrade_crm.`stck_la`) SELECT DISTINCT b.* FROM (SELECT abs(id) AS id, MAX(stime) AS stime FROM stck_lu GROUP BY abs(id)) a LEFT JOIN stck_lu b ON a.id=abs(b.id) AND a.stime=b.stime)
sl on s.id = sl.id_stck
where bj.products_name <> sl.title or CONCAT(ifnull(bj.products_descr_short, ''), ifnull(bj.products_descr_short_upd, '')) <> sl.description;

-- STEP 4

-- UPDATE stck_l ALL FIELDS WHERE ANY CHANGES!!!

-- UPDATE `borotrade_crm`.`stck_l` sl
-- left join borotrade_crm.stck s on s.id = sl.id_stck left join `vpws_main`.`borotrade_json` bj on bj.products_sku = s.sku and bj.products_id = s.isbn
-- SET sl.title = bj.products_name, sl.description = CONCAT(ifnull(bj.products_descr_short, ''), ifnull(bj.products_descr_short_upd, ''))
-- where bj.products_name <> sl.title or CONCAT(ifnull(bj.products_descr_short, ''), ifnull(bj.products_descr_short_upd, '')) <> sl.description;

-- STEP 5

-- INSERT ALL NEW PRODUCTS MISSING IN stck_l

INSERT INTO `borotrade_crm`.`stck_l` (`id_stck`, `id_lang`, `title`, `description`)
SELECT s.`id`, 1, bj.products_name, CONCAT(ifnull(bj.products_descr_short, ''), ifnull(bj.products_descr_short_upd, '')) FROM
`vpws_main`.`borotrade_json` bj left join borotrade_crm.stck s on bj.products_sku = s.sku and bj.products_id = s.isbn left join borotrade_crm.stck_l sl on s.id = sl.id_stck
where sl.id is null;

-- STEP 6

-- UPDATE stck_l.sactx with 1 to "delete" all mising in borotrade_json PRODUCTS!!!

UPDATE borotrade_crm.stck_l sl left join borotrade_crm.stck s on sl.id_stck = s.id
left join `vpws_main`.`borotrade_json` bj on bj.products_sku = s.sku and bj.products_id = s.isbn
set sl.sactx = 1
where bj.products_sku is null;

-- STEP 7

-- skip id update - already done

-- STEP 8

-- check active products count in stck
select * from `borotrade_crm`.stck_l where sactx <> 1;
