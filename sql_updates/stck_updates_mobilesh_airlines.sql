-- SELECT * FROM `vpws_main`.`borotrade_json` where products_descr5 is not null and products_descr5 <> '';
-- where products_descr_short like '%karcher-borotrade%';

-- select * from vpws_main.borotrade_json;

--  where products_descr5 like '%машина KARCHER K 4 Classic, 369, 369, 1, 0, 0, 0, 0, 0, null, 0, <p style=%';


-- SELECT category_id, category_name, count(*) FROM vpws_main.borotrade_json GROUP BY category_id, category_name;

-- SELECT * FROM vpws_main.borotrade_json where category_id = 2;

-- SELECT products_order, count(*) FROM vpws_main.borotrade_json group by products_order;
-- SELECT * FROM vpws_main.borotrade_json where products_crrsale_price <> products_sale_price;
-- SELECT * FROM vpws_main.borotrade_json where length(gallery) <> 0;

-- DROP TABLE `acnt`, `acnta`, `acnt_a`, `acnt_aa`, `acnt_f`, `acnt_fa`, `acnt_i`, `acnt_ia`, `acnt_m`, `acnt_ma`, `acnt_n`, `acnt_na`, `acnt_s`, `acnt_sa`, `acnt_t`, `acnt_ta`, `acnt_v`, `acnt_va`, `acnt_x`, `acnt_xa`, `attr`, `attra`, `attr_l`, `attr_la`, `bank`, `catg`, `catga`, `catg_l`, `catg_la`, `cnfg`, `cnfga`, `curr`, `curra`, `curr_i`, `curr_ia`, `disc`, `disca`, `disc_i`, `docx`, `docxa`, `docx_i`, `docx_ia`, `dscr`, `dscr_i`, `file`, `gett`, `help`, `lang`, `langa`, `lang_i`, `lang_ia`, `logx`, `memb`, `memba`, `mesx`, `mesx_i`, `mony`, `monya`, `mony_i`, `napx`, `nmcl`, `nmcla`, `nmcl_i`, `nmcl_ia`, `nomx`, `objt`, `objta`, `pers`, `persa`, `pers_a`, `pers_aa`, `pers_b`, `pers_ba`, `pers_c`, `pers_ca`, `pers_f`, `pers_fa`, `pers_n`, `pers_na`, `pers_p`, `pers_pa`, `prgn`, `prgna`, `recp`, `recp_i`, `regx`, `regx_i`, `stck`, `stcka`, `stck_a`, `stck_aa`, `stck_i`, `stck_ia`, `stck_l`, `stck_la`, `stck_r`, `stck_ra`, `stck_x`, `stck_xa`, `term`, `terma`, `term_l`, `term_la`, `user`, `usera`, `user_i`, `user_ia`, `vatx`, `vatxa`;

-- use borotrade_crm;



-- SELECT  `borotrade_json`.`products_featured`, `borotrade_json`.`products_topsale`, `borotrade_json`.`products_credit`, `borotrade_json`.`products_best_price`, `borotrade_json`.`products_lowest_price`, `borotrade_json`.`products_delay`, `borotrade_json`.`products_new`,  count(*) FROM `vpws_main`.`borotrade_json`GROUP BY `borotrade_json`.`products_featured`, `borotrade_json`.`products_topsale`, `borotrade_json`.`products_credit`, `borotrade_json`.`products_best_price`, `borotrade_json`.`products_lowest_price`, `borotrade_json`.`products_delay`, `borotrade_json`.`products_new`;

-- SELECT products_id, products_sku, count(*) FROM vpws_main.borotrade_json GROUP BY products_id, products_sku;
-- SELECT products_id, count(*) FROM vpws_main.borotrade_json GROUP BY products_id;
-- SELECT * FROM vpws_main.borotrade_json where products_sku = '16800180';


-- DROP TABLE `borotrade_gallery_json`;

-- CREATE TABLE `borotrade_gallery_json` (
--    `id` bigint NOT NULL AUTO_INCREMENT,
--   `products_id` int DEFAULT NULL,
--   `products_sku` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
--   `gallery` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
--    `datasize` bigint DEFAULT NULL,
--    `dataname` text DEFAULT NULL,
--    `datanameupd` text DEFAULT NULL,
--   `data` longblob,
--   PRIMARY KEY (`id`)
-- ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=COMPRESSED;

-- ALTER TABLE `vpws_main`.`borotrade_gallery_json` ADD UNIQUE INDEX `unique_idx` (`products_id` ASC, `products_sku` ASC, `gallery`(512) ASC) VISIBLE;

-- ALTER TABLE `vpws_main`.`borotrade_gallery_json` 
-- CHANGE COLUMN `gallery` `gallery` VARCHAR(512) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_unicode_ci' NULL DEFAULT NULL ,
-- ADD UNIQUE INDEX `unique_idx` (`products_id` ASC, `products_sku` ASC, `gallery` ASC) VISIBLE;

-- ALTER TABLE `borotrade_gallery_json` ADD `updatedurl` VARCHAR(512) NULL DEFAULT NULL AFTER `gallery`;

-- CREATE TABLE vpws_main.`borotrade_attr` (
--   `id` bigint(20) NOT NULL,
--   `products_id` int(11) DEFAULT NULL,
--   `products_sku` varchar(16) DEFAULT NULL,
--   `attr` varchar(512) DEFAULT NULL,
--   `val` varchar(512) DEFAULT NULL
-- ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=COMPRESSED;

-- ALTER TABLE vpws_main.`borotrade_attr` ADD `icnt` INT NULL DEFAULT NULL AFTER `products_sku`;

-- ALTER TABLE vpws_main.`borotrade_attr` CHANGE `id` `id` BIGINT(20) NOT NULL AUTO_INCREMENT, ADD PRIMARY KEY (`id`);

-- ALTER TABLE vpws_main.`borotrade_attr` DROP INDEX `unique_idx`;
-- ALTER TABLE `vpws_main`.`borotrade_attr` ADD UNIQUE `unique_idx` (`products_id`, `products_sku`, icnt, `attr`);

-- ALTER TABLE vpws_main.`borotrade_json` ADD `products_descr_short_upd` LONGTEXT NULL DEFAULT NULL AFTER `products_descr_short`;

-- CREATE TABLE `borotrade_linkedp` (
--   `id` bigint(20) NOT NULL,
--   `products_id` int(11) DEFAULT NULL,
--   `products_sku` varchar(16) DEFAULT NULL,
--   `linkedp` varchar(512) DEFAULT NULL
-- ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=COMPRESSED;

-- ALTER TABLE `borotrade_linkedp`
--   ADD PRIMARY KEY (`id`),
--   ADD UNIQUE KEY `unique_idx` (`products_id`,`products_sku`,`linkedp`);

-- ALTER TABLE `borotrade_linkedp` CHANGE `linkedp` `linkedp` VARCHAR(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL;

-- ALTER TABLE `borotrade_linkedp` CHANGE `id` `id` BIGINT(20) NOT NULL AUTO_INCREMENT;

-- ALTER TABLE `borotrade_json` ADD `galleryupd` TEXT NULL DEFAULT NULL AFTER `gallery`;


-- SELECT `id_catg`, `id_inet`, `sku`, `isbn`, `name`, `oprice`, `ocurrency`, `dprice`, `dcurrency`, `id_vatx`, `image`, `description` FROM borotrade_crm.stck WHERE sku = '47625620';

-- SELECT c1.id_catg, c2.id_catg, products_sku, products_id, products_name, products_sale_price, products_sale_price_curr, products_crrsale_price, products_sale_price_curr, 1, galleryupd, products_descr_short_upd FROM `vpws_main`.`borotrade_json` bj left join (SELECT * FROM borotrade_crm.catg WHERE xtype = 1) c1 on bj.category_id = c1.fid left join (SELECT * FROM borotrade_crm.catg WHERE xtype = 2) c2 on bj.category_id = c2.fid WHERE products_sku = '47625620';

-- SELECT * FROM `vpws_main`.`borotrade_json`; -- WHERE products_sku = '47625620';

-- SELECT c1.id_catg, c2.id_catg, products_sku, products_id, products_name, products_sale_price, products_sale_price_curr, products_crrsale_price, products_sale_price_curr, 1, galleryupd, CONCAT(ifnull(products_descr_short, ''), ifnull(products_descr_short_upd, '')) FROM `vpws_main`.`borotrade_json` bj left join (SELECT * FROM borotrade_crm.catg WHERE xtype = 1) c1 on bj.category_id = c1.fid left join (SELECT * FROM borotrade_crm.catg WHERE xtype = 2) c2 on bj.category_id = c2.fid;








-- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


-- QUERIES EXECUTED ON THE HOSTING WITH THE mobilesh_borotest DATABASE!!!

-- UPDATE stck.isbn with borotrade_json.products_id!!!

-- STEP 1

-- don't update!!!

-- update `mobilesh_borotest`.stck b left join  `mobilesh_borotest`.`borotrade_json` a
-- on b.sku = a.products_sku
-- set b.isbn = a.products_id;

-- update `mobilesh_borotest`.stck bb left join
-- (select b.`id`, b.`id_catg`, b.`id_inet`, b.`id_stck`, b.`id_manf`, b.`id_supl`, b.`xtype`, b.`sku`, b.`skux`, b.`ean`, b.`isbn`, b.`upc`, b.`name`, b.`weight`, b.`punit`, b.`sunit`, b.`xunit`, b.`qunit`, b.`plus`, b.`minus`, b.`allqty`, b.`minqty`, b.`iprice`, b.`icurrency`, b.`oprice`, b.`ocurrency`, b.`dperc`, b.`dprice`, b.`dcurrency`, b.`id_vatx`, b.`minpr`, b.`maxpr`, b.`avgpr`, b.`image_uri`, b.`image`, b.`suser`, b.`stime`, b.`sactx`, b.`wid`, b.`lot`, b.`description` as bdescription, a.* from 
-- (SELECT c1.id as catgw, c2.id as catgi, products_sku, products_id, products_name, products_sale_price, products_sale_price_curr, products_crrsale_price, 1 as curr, galleryupd, CONCAT(ifnull(products_descr_short, ''), ifnull(products_descr_short_upd, '')) as description FROM `mobilesh_borotest`.`borotrade_json` bj left join (SELECT * FROM `mobilesh_borotest`.catg WHERE xtype = 1) c1 on bj.category_id = c1.fid left join (SELECT * FROM `mobilesh_borotest`.catg WHERE xtype = 2) c2 on bj.category_id = c2.fid) a
-- left join
-- (SELECT * FROM `mobilesh_borotest`.stck) b
-- on a.products_sku = b.sku) aa on bb.id = aa.id
-- set bb.isbn = aa.products_id where aa.id is not null;


-- check for updated records

-- STEP 2

-- check if any updates!

-- local DB


-- test category, name, image diff

select b.`id`, b.`id_catg`, b.`id_inet`, b.`id_stck`, b.`id_manf`, b.`id_supl`, b.`xtype`, b.`sku`, b.`skux`, b.`ean`, b.`isbn`, b.`upc`, b.`name`, b.`weight`, b.`punit`, b.`sunit`, b.`xunit`, b.`qunit`, b.`plus`, b.`minus`, b.`allqty`, b.`minqty`, b.`iprice`, b.`icurrency`, b.`oprice`, b.`ocurrency`, b.`dperc`, b.`dprice`, b.`dcurrency`, b.`id_vatx`, b.`minpr`, b.`maxpr`, b.`avgpr`, b.`image_uri`, b.`image`, b.`suser`, b.`stime`, b.`sactx`, b.`wid`, b.`lot`, b.`description` from 
(SELECT c1.id as catgw, c2.id as catgi, products_sku, products_id, products_name, products_sale_price, products_sale_price_curr, products_crrsale_price, 1 as curr, galleryupd, CONCAT(ifnull(products_descr_short, ''), ifnull(products_descr_short_upd, '')) as description FROM `vpws_main`.`borotrade_json` bj left join (SELECT * FROM `borotrade_crm`.catg WHERE xtype = 1) c1 on bj.category_id = c1.fid left join (SELECT * FROM `borotrade_crm`.catg WHERE xtype = 2) c2 on bj.category_id = c2.fid) a
left join
(SELECT * FROM `borotrade_crm`.stck) b
on a.products_sku = b.sku and a.products_id = b.isbn
where a.catgw <> b.id_catg or a.catgi <> b.id_inet or a.products_name <> b.name or a.galleryupd  <> b.image;

-- test prices diff

select b.`id`, b.`id_catg`, b.`id_inet`, b.`id_stck`, b.`id_manf`, b.`id_supl`, b.`xtype`, b.`sku`, b.`skux`, b.`ean`, b.`isbn`, b.`upc`, b.`name`, b.`weight`, b.`punit`, b.`sunit`, b.`xunit`, b.`qunit`, b.`plus`, b.`minus`, b.`allqty`, b.`minqty`, b.`iprice`, b.`icurrency`, b.`oprice`, b.`ocurrency`, b.`dperc`, b.`dprice`, b.`dcurrency`, b.`id_vatx`, b.`minpr`, b.`maxpr`, b.`avgpr`, b.`image_uri`, b.`image`, b.`suser`, b.`stime`, b.`sactx`, b.`wid`, b.`lot`, b.`description` from 
(SELECT c1.id as catgw, c2.id as catgi, products_sku, products_id, products_name, products_sale_price, products_sale_price_curr, products_crrsale_price, 1 as curr, galleryupd, CONCAT(ifnull(products_descr_short, ''), ifnull(products_descr_short_upd, '')) as description FROM `vpws_main`.`borotrade_json` bj left join (SELECT * FROM `borotrade_crm`.catg WHERE xtype = 1) c1 on bj.category_id = c1.fid left join (SELECT * FROM `borotrade_crm`.catg WHERE xtype = 2) c2 on bj.category_id = c2.fid) a
left join
(SELECT * FROM `borotrade_crm`.stck) b
on a.products_sku = b.sku and a.products_id = b.isbn
where cast(a.products_sale_price as decimal) <> cast(b.oprice as decimal) or a.products_sale_price_curr  <> b.ocurrency;

-- test description diff

select b.`id`, b.`id_catg`, b.`id_inet`, b.`id_stck`, b.`id_manf`, b.`id_supl`, b.`xtype`, b.`sku`, b.`skux`, b.`ean`, b.`isbn`, b.`upc`, b.`name`, b.`weight`, b.`punit`, b.`sunit`, b.`xunit`, b.`qunit`, b.`plus`, b.`minus`, b.`allqty`, b.`minqty`, b.`iprice`, b.`icurrency`, b.`oprice`, b.`ocurrency`, b.`dperc`, b.`dprice`, b.`dcurrency`, b.`id_vatx`, b.`minpr`, b.`maxpr`, b.`avgpr`, b.`image_uri`, b.`image`, b.`suser`, b.`stime`, b.`sactx`, b.`wid`, b.`lot`, b.`description` from 
(SELECT c1.id as catgw, c2.id as catgi, products_sku, products_id, products_name, products_sale_price, products_sale_price_curr, products_crrsale_price, 1 as curr, galleryupd, CONCAT(ifnull(products_descr_short, ''), ifnull(products_descr_short_upd, '')) as description FROM `vpws_main`.`borotrade_json` bj left join (SELECT * FROM `borotrade_crm`.catg WHERE xtype = 1) c1 on bj.category_id = c1.fid left join (SELECT * FROM `borotrade_crm`.catg WHERE xtype = 2) c2 on bj.category_id = c2.fid) a
left join
(SELECT * FROM `borotrade_crm`.stck) b
on a.products_sku = b.sku and a.products_id = b.isbn
where a.description <>  b.description;


-- test all diff

select b.`id`, b.`id_catg`, b.`id_inet`, b.`id_stck`, b.`id_manf`, b.`id_supl`, b.`xtype`, b.`sku`, b.`skux`, b.`ean`, b.`isbn`, b.`upc`, b.`name`, b.`weight`, b.`punit`, b.`sunit`, b.`xunit`, b.`qunit`, b.`plus`, b.`minus`, b.`allqty`, b.`minqty`, b.`iprice`, b.`icurrency`, b.`oprice`, b.`ocurrency`, b.`dperc`, b.`dprice`, b.`dcurrency`, b.`id_vatx`, b.`minpr`, b.`maxpr`, b.`avgpr`, b.`image_uri`, b.`image`, b.`suser`, b.`stime`, b.`sactx`, b.`wid`, b.`lot`, b.`description` from 
(SELECT c1.id as catgw, c2.id as catgi, products_sku, products_id, products_name, products_sale_price, products_sale_price_curr, products_crrsale_price, 1 as curr, galleryupd, CONCAT(ifnull(products_descr_short, ''), ifnull(products_descr_short_upd, '')) as description FROM `vpws_main`.`borotrade_json` bj left join (SELECT * FROM `borotrade_crm`.catg WHERE xtype = 1) c1 on bj.category_id = c1.fid left join (SELECT * FROM `borotrade_crm`.catg WHERE xtype = 2) c2 on bj.category_id = c2.fid) a
left join
(WITH stcku AS (
    SELECT
    `stck`.`id`,
    `stck`.`id_catg`,
    `stck`.`id_inet`,
    `stck`.`id_stck`,
    `stck`.`id_manf`,
    `stck`.`id_supl`,
    `stck`.`xtype`,
    `stck`.`sku`,
    `stck`.`skux`,
    `stck`.`ean`,
    `stck`.`isbn`,
    `stck`.`upc`,
    `stck`.`name`,
    `stck`.`weight`,
    `stck`.`punit`,
    `stck`.`sunit`,
    `stck`.`xunit`,
    `stck`.`qunit`,
    `stck`.`plus`,
    `stck`.`minus`,
    `stck`.`allqty`,
    `stck`.`minqty`,
    `stck`.`iprice`,
    `stck`.`icurrency`,
    `stck`.`oprice`,
    `stck`.`ocurrency`,
    `stck`.`dperc`,
    `stck`.`dprice`,
    `stck`.`dcurrency`,
    `stck`.`id_vatx`,
    `stck`.`minpr`,
    `stck`.`maxpr`,
    `stck`.`avgpr`,
    `stck`.`image_uri`,
    `stck`.`image`,
    `stck`.`suser`,
    `stck`.`stime`,
    `stck`.`sactx`,
    `stck`.`wid`,
    `stck`.`lot`,
    `stck`.`description`
    FROM borotrade_crm.`stck`
    UNION
    SELECT 
    	`stcka`.`id`,
    `stcka`.`id_catg`,
    `stcka`.`id_inet`,
    `stcka`.`id_stck`,
    `stcka`.`id_manf`,
    `stcka`.`id_supl`,
    `stcka`.`xtype`,
    `stcka`.`sku`,
    `stcka`.`skux`,
    `stcka`.`ean`,
    `stcka`.`isbn`,
    `stcka`.`upc`,
    `stcka`.`name`,
    `stcka`.`weight`,
    `stcka`.`punit`,
    `stcka`.`sunit`,
    `stcka`.`xunit`,
    `stcka`.`qunit`,
    `stcka`.`plus`,
    `stcka`.`minus`,
    `stcka`.`allqty`,
    `stcka`.`minqty`,
    `stcka`.`iprice`,
    `stcka`.`icurrency`,
    `stcka`.`oprice`,
    `stcka`.`ocurrency`,
    `stcka`.`dperc`,
    `stcka`.`dprice`,
    `stcka`.`dcurrency`,
    `stcka`.`id_vatx`,
    `stcka`.`minpr`,
    `stcka`.`maxpr`,
    `stcka`.`avgpr`,
    `stcka`.`image_uri`,
    `stcka`.`image`,
    `stcka`.`suser`,
    `stcka`.`stime`,
    `stcka`.`sactx`,
    `stcka`.`wid`,
    `stcka`.`lot`,
    `stcka`.`description`
	FROM borotrade_crm.`stcka`
)
SELECT DISTINCT b.* FROM
(SELECT 
abs(id) AS id, MAX(stime) AS stime
FROM stcku
GROUP BY abs(id)) a
LEFT JOIN stcku b ON a.id=abs(b.id) AND a.stime=b.stime) b
on a.products_sku = b.sku and a.products_id = b.isbn
where a.catgw <> b.id_catg or a.catgi <> b.id_inet or a.products_name <> b.name or cast(a.products_sale_price as decimal) <> cast(b.oprice as decimal) or a.products_sale_price_curr  <> b.ocurrency or a.galleryupd  <> b.image or a.description <>  b.description;

-- where a.catgw <> b.id_catg or a.catgi <> b.id_inet or a.products_name <> b.name or cast(a.products_sale_price as decimal) <> cast(b.oprice as decimal) or a.products_sale_price_curr  <> b.ocurrency or cast(a.products_crrsale_price as decimal) <> cast(b.dprice as decimal) or cast(a.products_crrsale_price as decimal) <> cast(b.dprice as decimal) or cast(a.products_sale_price as decimal) <> cast(b.iprice as decimal) or a.galleryupd  <> b.image or a.description <>  b.description;

-- hosting DB

select b.`id`, b.`id_catg`, b.`id_inet`, b.`id_stck`, b.`id_manf`, b.`id_supl`, b.`xtype`, b.`sku`, b.`skux`, b.`ean`, b.`isbn`, b.`upc`, b.`name`, b.`weight`, b.`punit`, b.`sunit`, b.`xunit`, b.`qunit`, b.`plus`, b.`minus`, b.`allqty`, b.`minqty`, b.`iprice`, b.`icurrency`, b.`oprice`, b.`ocurrency`, b.`dperc`, b.`dprice`, b.`dcurrency`, b.`id_vatx`, b.`minpr`, b.`maxpr`, b.`avgpr`, b.`image_uri`, b.`image`, b.`suser`, b.`stime`, b.`sactx`, b.`wid`, b.`lot`, b.`description` from 
(SELECT c1.id as catgw, c2.id as catgi, products_sku, products_id, products_name, products_sale_price, products_sale_price_curr, products_crrsale_price, 1 as curr, galleryupd, CONCAT(ifnull(products_descr_short, ''), ifnull(products_descr_short_upd, '')) as description FROM `mobilesh_borotest`.`borotrade_json` bj left join (SELECT * FROM `mobilesh_borotest`.catg WHERE xtype = 1) c1 on bj.category_id = c1.fid left join (SELECT * FROM `mobilesh_borotest`.catg WHERE xtype = 2) c2 on bj.category_id = c2.fid) a
left join
(SELECT * FROM `mobilesh_borotest`.stck) b
on a.products_sku = b.sku and a.products_id = b.isbn
where a.catgw <> b.id_catg or a.catgi <> b.id_inet or a.products_name <> b.name or cast(a.products_sale_price as decimal) <> cast(b.oprice as decimal) or a.products_sale_price_curr  <> b.ocurrency or cast(a.products_crrsale_price as decimal) <> cast(b.dprice as decimal) or cast(a.products_crrsale_price as decimal) <> cast(b.dprice as decimal) or cast(a.products_sale_price as decimal) <> cast(b.iprice as decimal) or a.galleryupd  <> b.image or a.description <>  b.description;

-- result is 560 in 0.2349 sec

-- INSERT INTO stcka THE UPDATED RECORDS when stck.isbn is updated with products_id!!!

-- STEP 3

-- local DB

INSERT INTO `borotrade_crm`.`stcka`
(`id`, `id_catg`, `id_inet`, `id_stck`, `id_manf`, `id_supl`, `xtype`, `sku`, `skux`, `ean`, `isbn`, `upc`, `name`, `weight`, `punit`, `sunit`, `xunit`, `qunit`, `plus`, `minus`, `allqty`, `minqty`, `iprice`, `icurrency`, `oprice`, `ocurrency`, `dperc`, `dprice`, `dcurrency`, `id_vatx`, `minpr`, `maxpr`, `avgpr`, `image_uri`, `image`, `suser`, `stime`, `sactx`, `wid`, `lot`, `description`)
-- select -b.`id`, b.`id_catg`, b.`id_inet`, b.`id_stck`, b.`id_manf`, b.`id_supl`, b.`xtype`, b.`sku`, b.`skux`, b.`ean`, b.`isbn`, b.`upc`, b.`name`, b.`weight`, b.`punit`, b.`sunit`, b.`xunit`, b.`qunit`, b.`plus`, b.`minus`, b.`allqty`, b.`minqty`, b.`iprice`, b.`icurrency`, b.`oprice`, b.`ocurrency`, b.`dperc`, b.`dprice`, b.`dcurrency`, b.`id_vatx`, b.`minpr`, b.`maxpr`, b.`avgpr`, b.`image_uri`, b.`image`, b.`suser`, b.`stime`, b.`sactx`, b.`wid`, b.`lot`, b.`description` from 
select -b.`id`, a.catgw, a.catgi, b.`id_stck`, b.`id_manf`, b.`id_supl`, b.`xtype`, b.`sku`, b.`skux`, b.`ean`, b.`isbn`, b.`upc`, a.products_name, b.`weight`, b.`punit`, b.`sunit`, b.`xunit`, b.`qunit`, b.`plus`, b.`minus`, b.`allqty`, b.`minqty`, b.`iprice`, b.`icurrency`, a.products_sale_price, b.`ocurrency`, b.`dperc`, b.`dprice`, b.`dcurrency`, b.`id_vatx`, b.`minpr`, b.`maxpr`, b.`avgpr`, b.`image_uri`, a.galleryupd, b.`suser`, b.`stime`, b.`sactx`, b.`wid`, b.`lot`, a.description from 
(SELECT c1.id as catgw, c2.id as catgi, products_sku, products_id, products_name, products_sale_price, products_sale_price_curr, products_crrsale_price, 1 as curr, galleryupd, CONCAT(ifnull(products_descr_short, ''), ifnull(products_descr_short_upd, '')) as description FROM `vpws_main`.`borotrade_json` bj left join (SELECT * FROM `borotrade_crm`.catg WHERE xtype = 1) c1 on bj.category_id = c1.fid left join (SELECT * FROM `borotrade_crm`.catg WHERE xtype = 2) c2 on bj.category_id = c2.fid) a
left join
(WITH stcku AS (
    SELECT
    `stck`.`id`,
    `stck`.`id_catg`,
    `stck`.`id_inet`,
    `stck`.`id_stck`,
    `stck`.`id_manf`,
    `stck`.`id_supl`,
    `stck`.`xtype`,
    `stck`.`sku`,
    `stck`.`skux`,
    `stck`.`ean`,
    `stck`.`isbn`,
    `stck`.`upc`,
    `stck`.`name`,
    `stck`.`weight`,
    `stck`.`punit`,
    `stck`.`sunit`,
    `stck`.`xunit`,
    `stck`.`qunit`,
    `stck`.`plus`,
    `stck`.`minus`,
    `stck`.`allqty`,
    `stck`.`minqty`,
    `stck`.`iprice`,
    `stck`.`icurrency`,
    `stck`.`oprice`,
    `stck`.`ocurrency`,
    `stck`.`dperc`,
    `stck`.`dprice`,
    `stck`.`dcurrency`,
    `stck`.`id_vatx`,
    `stck`.`minpr`,
    `stck`.`maxpr`,
    `stck`.`avgpr`,
    `stck`.`image_uri`,
    `stck`.`image`,
    `stck`.`suser`,
    `stck`.`stime`,
    `stck`.`sactx`,
    `stck`.`wid`,
    `stck`.`lot`,
    `stck`.`description`
    FROM borotrade_crm.`stck`
    UNION
    SELECT 
    	`stcka`.`id`,
    `stcka`.`id_catg`,
    `stcka`.`id_inet`,
    `stcka`.`id_stck`,
    `stcka`.`id_manf`,
    `stcka`.`id_supl`,
    `stcka`.`xtype`,
    `stcka`.`sku`,
    `stcka`.`skux`,
    `stcka`.`ean`,
    `stcka`.`isbn`,
    `stcka`.`upc`,
    `stcka`.`name`,
    `stcka`.`weight`,
    `stcka`.`punit`,
    `stcka`.`sunit`,
    `stcka`.`xunit`,
    `stcka`.`qunit`,
    `stcka`.`plus`,
    `stcka`.`minus`,
    `stcka`.`allqty`,
    `stcka`.`minqty`,
    `stcka`.`iprice`,
    `stcka`.`icurrency`,
    `stcka`.`oprice`,
    `stcka`.`ocurrency`,
    `stcka`.`dperc`,
    `stcka`.`dprice`,
    `stcka`.`dcurrency`,
    `stcka`.`id_vatx`,
    `stcka`.`minpr`,
    `stcka`.`maxpr`,
    `stcka`.`avgpr`,
    `stcka`.`image_uri`,
    `stcka`.`image`,
    `stcka`.`suser`,
    `stcka`.`stime`,
    `stcka`.`sactx`,
    `stcka`.`wid`,
    `stcka`.`lot`,
    `stcka`.`description`
	FROM borotrade_crm.`stcka`
)
SELECT DISTINCT b.* FROM
(SELECT 
abs(id) AS id, MAX(stime) AS stime
FROM stcku
GROUP BY abs(id)) a
LEFT JOIN stcku b ON a.id=abs(b.id) AND a.stime=b.stime) b
on a.products_sku = b.sku and a.products_id = b.isbn
where a.catgw <> b.id_catg or a.catgi <> b.id_inet or a.products_name <> b.name or cast(a.products_sale_price as decimal) <> cast(b.oprice as decimal) or a.products_sale_price_curr  <> b.ocurrency or a.galleryupd  <> b.image or a.description <>  b.description;

-- where a.catgw <> b.id_catg or a.catgi <> b.id_inet or a.products_name <> b.name or cast(a.products_sale_price as decimal) <> cast(b.oprice as decimal) or cast(a.products_sale_price as decimal) <> cast(b.iprice as decimal) or a.products_sale_price_curr  <> b.ocurrency or cast(a.products_crrsale_price as decimal) <> cast(b.dprice as decimal) or a.galleryupd  <> b.image or a.description <>  b.description;

-- hosting DB


INSERT INTO `mobilesh_borotest`.`stcka`
(`id`, `id_catg`, `id_inet`, `id_stck`, `id_manf`, `id_supl`, `xtype`, `sku`, `skux`, `ean`, `isbn`, `upc`, `name`, `weight`, `punit`, `sunit`, `xunit`, `qunit`, `plus`, `minus`, `allqty`, `minqty`, `iprice`, `icurrency`, `oprice`, `ocurrency`, `dperc`, `dprice`, `dcurrency`, `id_vatx`, `minpr`, `maxpr`, `avgpr`, `image_uri`, `image`, `suser`, `stime`, `sactx`, `wid`, `lot`, `description`)
select b.`id`, b.`id_catg`, b.`id_inet`, b.`id_stck`, b.`id_manf`, b.`id_supl`, b.`xtype`, b.`sku`, b.`skux`, b.`ean`, b.`isbn`, b.`upc`, b.`name`, b.`weight`, b.`punit`, b.`sunit`, b.`xunit`, b.`qunit`, b.`plus`, b.`minus`, b.`allqty`, b.`minqty`, b.`iprice`, b.`icurrency`, b.`oprice`, b.`ocurrency`, b.`dperc`, b.`dprice`, b.`dcurrency`, b.`id_vatx`, b.`minpr`, b.`maxpr`, b.`avgpr`, b.`image_uri`, b.`image`, b.`suser`, b.`stime`, b.`sactx`, b.`wid`, b.`lot`, b.`description` from 
(SELECT c1.id as catgw, c2.id as catgi, products_sku, products_id, products_name, products_sale_price, products_sale_price_curr, products_crrsale_price, 1 as curr, galleryupd, CONCAT(ifnull(products_descr_short, ''), ifnull(products_descr_short_upd, '')) as description FROM `mobilesh_borotest`.`borotrade_json` bj left join (SELECT * FROM `mobilesh_borotest`.catg WHERE xtype = 1) c1 on bj.category_id = c1.fid left join (SELECT * FROM `mobilesh_borotest`.catg WHERE xtype = 2) c2 on bj.category_id = c2.fid) a
left join
(SELECT * FROM `mobilesh_borotest`.stck) b
on a.products_sku = b.sku and a.products_id = b.isbn
where a.catgw <> b.id_catg or a.catgi <> b.id_inet or a.products_name <> b.name or cast(a.products_sale_price as decimal) <> cast(b.oprice as decimal) or cast(a.products_sale_price as decimal) <> cast(b.iprice as decimal) or a.products_sale_price_curr  <> b.ocurrency or cast(a.products_crrsale_price as decimal) <> cast(b.dprice as decimal) or a.galleryupd  <> b.image or a.description <>  b.description;

-- result 560 in 19.17 sec

-- OR 
-- insert into stcka the updated records when stck.isbn is null
-- should not have such!!!
-- INSERT INTO `mobilesh_borotest`.`stcka`
-- (`id`, `id_catg`, `id_inet`, `id_stck`, `id_manf`, `id_supl`, `xtype`, `sku`, `skux`, `ean`, `isbn`, `upc`, `name`, `weight`, `punit`, `sunit`, `xunit`, `qunit`, `plus`, `minus`, `allqty`, `minqty`, `iprice`, `icurrency`, `oprice`, `ocurrency`, `dperc`, `dprice`, `dcurrency`, `id_vatx`, `minpr`, `maxpr`, `avgpr`, `image_uri`, `image`, `suser`, `stime`, `sactx`, `wid`, `lot`, `description`)
-- select b.`id`, b.`id_catg`, b.`id_inet`, b.`id_stck`, b.`id_manf`, b.`id_supl`, b.`xtype`, b.`sku`, b.`skux`, b.`ean`, b.`isbn`, b.`upc`, b.`name`, b.`weight`, b.`punit`, b.`sunit`, b.`xunit`, b.`qunit`, b.`plus`, b.`minus`, b.`allqty`, b.`minqty`, b.`iprice`, b.`icurrency`, b.`oprice`, b.`ocurrency`, b.`dperc`, b.`dprice`, b.`dcurrency`, b.`id_vatx`, b.`minpr`, b.`maxpr`, b.`avgpr`, b.`image_uri`, b.`image`, b.`suser`, b.`stime`, b.`sactx`, b.`wid`, b.`lot`, b.`description` from 
-- (SELECT c1.id as catgw, c2.id as catgi, products_sku, products_id, products_name, products_sale_price, products_sale_price_curr, products_crrsale_price, 1 as curr, galleryupd, CONCAT(ifnull(products_descr_short, ''), ifnull(products_descr_short_upd, '')) as description FROM `mobilesh_borotest`.`borotrade_json` bj left join (SELECT * FROM `mobilesh_borotest`.catg WHERE xtype = 1) c1 on bj.category_id = c1.fid left join (SELECT * FROM `mobilesh_borotest`.catg WHERE xtype = 2) c2 on bj.category_id = c2.fid) a
-- left join
-- (SELECT * FROM `mobilesh_borotest`.stck) b
-- on a.products_sku = b.sku
-- where a.catgw <> b.id_catg or a.catgi <> b.id_inet or a.products_name <> b.name or cast(a.products_sale_price as decimal) <> cast(b.oprice as decimal) or a.products_sale_price_curr  <> b.ocurrency or cast(a.products_crrsale_price as decimal) <> cast(b.dprice as decimal) or a.galleryupd  <> b.image or a.description <>  b.description;



-- insert stck_pa where difference in prices

INSERT INTO `borotrade_crm`.`stck_pa`
(`id_stck`, `xtype`, `price`, `currency`, `suser`, `sactx`)
select -b.`id` as id_stck, 'o' as xtype, a.products_sale_price as price, 1 as currency, -1 as suser, 0 as sactx from 
(SELECT stck_id, c1.id as catgw, c2.id as catgi, products_sku, products_id, products_name, products_sale_price, products_sale_price_curr, products_crrsale_price, 1 as curr, galleryupd, CONCAT(ifnull(products_descr_short, ''), ifnull(products_descr_short_upd, '')) as description FROM `vpws_main`.`borotrade_json` bj left join (SELECT * FROM `borotrade_crm`.catg WHERE xtype = 1) c1 on bj.category_id = c1.fid left join (SELECT * FROM `borotrade_crm`.catg WHERE xtype = 2) c2 on bj.category_id = c2.fid) a
left join
(WITH stck_pu AS (SELECT * FROM borotrade_crm.`stck_p` UNION SELECT * FROM borotrade_crm.`stck_pa`) SELECT DISTINCT b.* FROM (SELECT abs(id) AS id, MAX(stime) AS stime FROM stck_pu GROUP BY abs(id)) a LEFT JOIN stck_pu b ON a.id=abs(b.id) AND a.stime=b.stime) b
on a.stck_id = b.id_stck
where cast(a.products_sale_price as decimal) <> cast(b.price as decimal);

-- insert in stck_p where id_stck price doesn't exist

insert into `borotrade_crm`.stck_p
(`id_stck`, `xtype`, `price`, `currency`, `suser`, `sactx`)
select a.stck_id, '0' as xtype, a.products_sale_price as price, a.products_sale_price_curr as currency, -1 as suser, 0 as sactx from 
(SELECT stck_id, c1.id as catgw, c2.id as catgi, products_sku, products_id, products_name, products_sale_price, products_sale_price_curr, products_crrsale_price, 1 as curr, galleryupd, CONCAT(ifnull(products_descr_short, ''), ifnull(products_descr_short_upd, '')) as description FROM `vpws_main`.`borotrade_json` bj left join (SELECT * FROM `borotrade_crm`.catg WHERE xtype = 1) c1 on bj.category_id = c1.fid left join (SELECT * FROM `borotrade_crm`.catg WHERE xtype = 2) c2 on bj.category_id = c2.fid) a
left join
(WITH stck_pu AS (SELECT * FROM borotrade_crm.`stck_p` UNION SELECT * FROM borotrade_crm.`stck_pa`) SELECT DISTINCT b.* FROM (SELECT abs(id) AS id, MAX(stime) AS stime FROM stck_pu GROUP BY abs(id)) a LEFT JOIN stck_pu b ON a.id=abs(b.id) AND a.stime=b.stime) b
on a.stck_id = b.id_stck
where b.id is null;


-- UPDATE stck ALL FIELDS WHERE ANY CHANGES!!!

-- STEP 4

-- local DB

-- update `borotrade_crm`.stck bb left join
-- (select b.`id`, b.`id_catg`, b.`id_inet`, b.`id_stck`, b.`id_manf`, b.`id_supl`, b.`xtype`, b.`sku`, b.`skux`, b.`ean`, b.`isbn`, b.`upc`, b.`name`, b.`weight`, b.`punit`, b.`sunit`, b.`xunit`, b.`qunit`, b.`plus`, b.`minus`, b.`allqty`, b.`minqty`, b.`iprice`, b.`icurrency`, b.`oprice`, b.`ocurrency`, b.`dperc`, b.`dprice`, b.`dcurrency`, b.`id_vatx`, b.`minpr`, b.`maxpr`, b.`avgpr`, b.`image_uri`, b.`image`, b.`suser`, b.`stime`, b.`sactx`, b.`wid`, b.`lot`, b.`description` as bdescription, a.* from 
-- (SELECT c1.id as catgw, c2.id as catgi, products_sku, products_id, products_name, products_sale_price, products_sale_price_curr, products_crrsale_price, 1 as curr, galleryupd, CONCAT(ifnull(products_descr_short, ''), ifnull(products_descr_short_upd, '')) as description FROM `vpws_main`.`borotrade_json` bj left join (SELECT * FROM `borotrade_crm`.catg WHERE xtype = 1) c1 on bj.category_id = c1.fid left join (SELECT * FROM `borotrade_crm`.catg WHERE xtype = 2) c2 on bj.category_id = c2.fid) a
-- left join
-- (SELECT * FROM `borotrade_crm`.stck) b
-- on a.products_sku = b.sku and a.products_id = b.isbn
-- where a.catgw <> b.id_catg or a.catgi <> b.id_inet or a.products_name <> b.name or cast(a.products_sale_price as decimal) <> cast(b.oprice as decimal) or a.products_sale_price_curr  <> b.ocurrency or a.galleryupd  <> b.image or a.description <>  b.description) aa on bb.id = aa.id
-- -- where a.catgw <> b.id_catg or a.catgi <> b.id_inet or a.products_name <> b.name or cast(a.products_sale_price as decimal) <> cast(b.oprice as decimal) or a.products_sale_price_curr  <> b.ocurrency or cast(a.products_crrsale_price as decimal) <> cast(b.dprice as decimal) or cast(a.products_sale_price as decimal) <> cast(b.iprice as decimal) or a.galleryupd  <> b.image or a.description <>  b.description) aa on bb.id = aa.id
-- set bb.id_catg = aa.catgw, bb.id_inet = aa.catgi, bb.name = aa.products_name, bb.oprice = aa.products_sale_price, bb.ocurrency = aa.products_sale_price_curr, bb.image = aa.galleryupd, bb.description = aa.description where aa.id is not null;
-- -- set bb.id_catg = aa.catgw, bb.id_inet = aa.catgi, bb.name = aa.products_name, bb.oprice = aa.products_sale_price, bb.ocurrency = aa.products_sale_price_curr, bb.dprice = aa.products_crrsale_price, bb.iprice = products_sale_price, bb.image = aa.galleryupd, bb.description = aa.description where aa.id is not null;

-- hosting DB

update `mobilesh_borotest`.stck bb left join
(select b.`id`, b.`id_catg`, b.`id_inet`, b.`id_stck`, b.`id_manf`, b.`id_supl`, b.`xtype`, b.`sku`, b.`skux`, b.`ean`, b.`isbn`, b.`upc`, b.`name`, b.`weight`, b.`punit`, b.`sunit`, b.`xunit`, b.`qunit`, b.`plus`, b.`minus`, b.`allqty`, b.`minqty`, b.`iprice`, b.`icurrency`, b.`oprice`, b.`ocurrency`, b.`dperc`, b.`dprice`, b.`dcurrency`, b.`id_vatx`, b.`minpr`, b.`maxpr`, b.`avgpr`, b.`image_uri`, b.`image`, b.`suser`, b.`stime`, b.`sactx`, b.`wid`, b.`lot`, b.`description` as bdescription, a.* from 
(SELECT c1.id as catgw, c2.id as catgi, products_sku, products_id, products_name, products_sale_price, products_sale_price_curr, products_crrsale_price, 1 as curr, galleryupd, CONCAT(ifnull(products_descr_short, ''), ifnull(products_descr_short_upd, '')) as description FROM `mobilesh_borotest`.`borotrade_json` bj left join (SELECT * FROM `mobilesh_borotest`.catg WHERE xtype = 1) c1 on bj.category_id = c1.fid left join (SELECT * FROM `mobilesh_borotest`.catg WHERE xtype = 2) c2 on bj.category_id = c2.fid) a
left join
(SELECT * FROM `mobilesh_borotest`.stck) b
on a.products_sku = b.sku and a.products_id = b.isbn
where a.catgw <> b.id_catg or a.catgi <> b.id_inet or a.products_name <> b.name or cast(a.products_sale_price as decimal) <> cast(b.oprice as decimal) or a.products_sale_price_curr  <> b.ocurrency or cast(a.products_crrsale_price as decimal) <> cast(b.dprice as decimal) or cast(a.products_sale_price as decimal) <> cast(b.iprice as decimal) or a.galleryupd  <> b.image or a.description <>  b.description) aa on bb.id = aa.id
set bb.id_catg = aa.catgw, bb.id_inet = aa.catgi, bb.name = aa.products_name, bb.oprice = aa.products_sale_price, bb.ocurrency = aa.products_sale_price_curr, bb.dprice = aa.products_crrsale_price, bb.iprice = products_sale_price, bb.image = aa.galleryupd, bb.description = aa.description where aa.id is not null;

-- result 328 in 17.9212

-- INSERT ALL NEW PRODUCTS MISSING IN stck

-- STEP 5

-- local DB

insert into `borotrade_crm`.stck (`id_catg`, `id_inet`, `sku`, `isbn`, `name`, `oprice`, `iprice`, `ocurrency`, `dprice`, `dcurrency`, `xtype`, `punit`, `xunit`, `sunit`, `id_vatx`, `image`, `description`)
select a.catgw as id_catg, a.catgi as id_inet, a.products_sku as sku, a.products_id as isbn, a.products_name as name, a.products_sale_price as oprice, a.products_sale_price as iprice, a.products_sale_price_curr as ocurrency, a.products_crrsale_price as dprice, a.products_sale_price_curr as dcurrency, 1 as xtype, 2 as punit, 1 as xunit, 2 as sunit, 1 as id_vatx, a.galleryupd as image, a.description from 
(SELECT c1.id as catgw, c2.id as catgi, products_sku, products_id, products_name, products_sale_price, products_sale_price_curr, products_crrsale_price, 1 as curr, galleryupd, CONCAT(ifnull(products_descr_short, ''), ifnull(products_descr_short_upd, '')) as description FROM `vpws_main`.`borotrade_json` bj left join (SELECT * FROM `borotrade_crm`.catg WHERE xtype = 1) c1 on bj.category_id = c1.fid left join (SELECT * FROM `borotrade_crm`.catg WHERE xtype = 2) c2 on bj.category_id = c2.fid) a
left join
(SELECT `id`, `id_catg`, `id_inet`, `sku`, `isbn`, `name`, `oprice`, `ocurrency`, `dprice`, `dcurrency`, `id_vatx`, `image`, `description` FROM `borotrade_crm`.stck where sactx <> 1) b
on a.products_sku = b.sku and a.products_id = b.isbn
where b.id is null;

-- hosting DB

insert into `mobilesh_borotest`.stck (`id_catg`, `id_inet`, `sku`, `isbn`, `name`, `oprice`, `iprice`, `ocurrency`, `dprice`, `dcurrency`, `xtype`, `punit`, `xunit`, `sunit`, `id_vatx`, `image`, `description`)
select a.catgw as id_catg, a.catgi as id_inet, a.products_sku as sku, a.products_id as isbn, a.products_name as name, a.products_sale_price as oprice, a.products_sale_price as iprice, a.products_sale_price_curr as ocurrency, a.products_crrsale_price as dprice, a.products_sale_price_curr as dcurrency, 1 as xtype, 2 as punit, 1 as xunit, 2 as sunit, 1 as id_vatx, a.galleryupd as image, a.description from 
(SELECT c1.id as catgw, c2.id as catgi, products_sku, products_id, products_name, products_sale_price, products_sale_price_curr, products_crrsale_price, 1 as curr, galleryupd, CONCAT(ifnull(products_descr_short, ''), ifnull(products_descr_short_upd, '')) as description FROM `mobilesh_borotest`.`borotrade_json` bj left join (SELECT * FROM `mobilesh_borotest`.catg WHERE xtype = 1) c1 on bj.category_id = c1.fid left join (SELECT * FROM `mobilesh_borotest`.catg WHERE xtype = 2) c2 on bj.category_id = c2.fid) a
left join
(SELECT `id`, `id_catg`, `id_inet`, `sku`, `isbn`, `name`, `oprice`, `ocurrency`, `dprice`, `dcurrency`, `id_vatx`, `image`, `description` FROM `mobilesh_borotest`.stck where sactx <> 1) b
on a.products_sku = b.sku and a.products_id = b.isbn
where b.id is null;

-- result 1 in 4.5045

-- UPDATE stck.sactx with 1 to "delete" all mising in borotrade_json PRODUCTS!!!

-- STEP 6

-- local DB

update `borotrade_crm`.stck b left join 
(SELECT c1.id as catgw, c2.id as catgi, products_sku, products_id, products_name, products_sale_price, products_sale_price_curr, products_crrsale_price, 1 as curr, galleryupd, CONCAT(ifnull(products_descr_short, ''), ifnull(products_descr_short_upd, '')) as bdescription FROM `vpws_main`.`borotrade_json` bj left join (SELECT * FROM `borotrade_crm`.catg WHERE xtype = 1) c1 on bj.category_id = c1.fid left join (SELECT * FROM `borotrade_crm`.catg WHERE xtype = 2) c2 on bj.category_id = c2.fid) a
on a.products_sku = b.sku and a.products_id = b.isbn
set b.sactx = 1
where a.products_sku is null;

-- hosting DB

update `mobilesh_borotest`.stck b left join 
(SELECT c1.id as catgw, c2.id as catgi, products_sku, products_id, products_name, products_sale_price, products_sale_price_curr, products_crrsale_price, 1 as curr, galleryupd, CONCAT(ifnull(products_descr_short, ''), ifnull(products_descr_short_upd, '')) as bdescription FROM `mobilesh_borotest`.`borotrade_json` bj left join (SELECT * FROM `mobilesh_borotest`.catg WHERE xtype = 1) c1 on bj.category_id = c1.fid left join (SELECT * FROM `mobilesh_borotest`.catg WHERE xtype = 2) c2 on bj.category_id = c2.fid) a
on a.products_sku = b.sku and a.products_id = b.isbn
set b.sactx = 1
where a.products_sku is null;

-- result 1 in 7.4022



-- UPDATE borotrade_json.stck_id with stck.id

-- update `mobilesh_borotest`.`borotrade_json` aa left join
-- (select * from 
-- (SELECT * FROM `mobilesh_borotest`.`borotrade_json`) a
-- left join
-- (SELECT * FROM `mobilesh_borotest`.stck) b
-- on a.products_sku = b.sku and a.products_id = b.isbn and b.sactx <> 1) bb on aa.products_sku = bb.sku and aa.products_id = bb.isbn
-- set aa.stck_id = bb.id;

-- STEP 7

-- local DB

update `vpws_main`.`borotrade_json` a left join
(SELECT * FROM `borotrade_crm`.stck where sactx <> 1) b
on a.products_sku = b.sku and a.products_id = b.isbn
set a.stck_id = b.id;

-- hosting DB

update `mobilesh_borotest`.`borotrade_json` a left join
(SELECT * FROM `mobilesh_borotest`.stck where sactx <> 1) b
on a.products_sku = b.sku and a.products_id = b.isbn
set a.stck_id = b.id;

-- result 1332 in 207.5223


-- STEP 8

-- check active products count in stck

-- local DB

select * from `borotrade_crm`.stck where sactx <> 1;

-- hosting DB

select * from `mobilesh_borotest`.stck where sactx <> 1;







-- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


-- UPDATE stck_l

-- STEP 2

-- check if any updates!

SELECT sl.`id`, sl.`id_stck`, sl.`id_lang`, sl.`title`, sl.`description`, sl.`suser`, sl.`stime`, sl.`sactx`, sl.`wid` FROM
`mobilesh_borotest`.`borotrade_json` bj left join `mobilesh_borotest`.stck s on bj.products_sku = s.sku and bj.products_id = s.isbn left join `mobilesh_borotest`.stck_l sl on s.id = sl.id_stck
where bj.products_name <> sl.title or CONCAT(ifnull(bj.products_descr_short, ''), ifnull(bj.products_descr_short_upd, '')) <> sl.description;

-- STEP 3

-- INSERT INTO stck_la THE UPDATED RECORDS

INSERT INTO `mobilesh_borotest`.`stck_la`
SELECT sl.`id`, sl.`id_stck`, sl.`id_lang`, sl.`title`, sl.`description`, sl.`suser`, sl.`stime`, sl.`sactx`, sl.`wid` FROM
`mobilesh_borotest`.`borotrade_json` bj left join `mobilesh_borotest`.stck s on bj.products_sku = s.sku and bj.products_id = s.isbn left join `mobilesh_borotest`.stck_l sl on s.id = sl.id_stck
where bj.products_name <> sl.title or CONCAT(ifnull(bj.products_descr_short, ''), ifnull(bj.products_descr_short_upd, '')) <> sl.description;


-- STEP 4

-- UPDATE stck_l ALL FIELDS WHERE ANY CHANGES!!!

UPDATE `mobilesh_borotest`.`stck_l` sl
left join `mobilesh_borotest`.stck s on s.id = sl.id_stck left join `mobilesh_borotest`.`borotrade_json` bj on bj.products_sku = s.sku and bj.products_id = s.isbn
SET sl.title = bj.products_name, sl.description = CONCAT(ifnull(bj.products_descr_short, ''), ifnull(bj.products_descr_short_upd, ''))
where bj.products_name <> sl.title or CONCAT(ifnull(bj.products_descr_short, ''), ifnull(bj.products_descr_short_upd, '')) <> sl.description;

-- STEP 5

-- INSERT ALL NEW PRODUCTS MISSING IN stck_l

INSERT INTO `mobilesh_borotest`.`stck_l` (`id_stck`, `id_lang`, `title`, `description`)
SELECT s.`id`, 1, bj.products_name, CONCAT(ifnull(bj.products_descr_short, ''), ifnull(bj.products_descr_short_upd, '')) FROM
`mobilesh_borotest`.`borotrade_json` bj left join `mobilesh_borotest`.stck s on bj.products_sku = s.sku and bj.products_id = s.isbn left join `mobilesh_borotest`.stck_l sl on s.id = sl.id_stck
where sl.id is null;


-- STEP 6

-- UPDATE stck_l.sactx with 1 to "delete" all mising in borotrade_json PRODUCTS!!!

UPDATE `mobilesh_borotest`.stck_l sl left join `mobilesh_borotest`.stck s on sl.id_stck = s.id
left join `mobilesh_borotest`.`borotrade_json` bj on bj.products_sku = s.sku and bj.products_id = s.isbn
set sl.sactx = 1
where bj.products_sku is null;

-- STEP 7

-- skip id update - already done

-- STEP 8

-- check active products count in stck





-- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


-- UPDATE attr

-- update sactx with 1 for all non existant attr

update mobilesh_borotest.attr a right join
(select attr, name, id from
(select attr, name, id from
(SELECT DISTINCT attr FROM mobilesh_borotest.borotrade_attr group by attr) src_a
left join
(select id, name from mobilesh_borotest.attr) dst_a
on src_a.attr = dst_a.name
UNION
select attr, name, id from
(SELECT DISTINCT attr FROM mobilesh_borotest.borotrade_attr group by attr) src_a
right join
(select id, name from mobilesh_borotest.attr) dst_a
on src_a.attr = dst_a.name) a
where a.attr is null) src on src.id = a.id
set a.sactx = 1;

-- insert all new rows into attr

insert into mobilesh_borotest.attr (name)
select attr from
(select attr, name, id from
(SELECT DISTINCT attr FROM mobilesh_borotest.borotrade_attr group by attr) src_a
left join
(select id, name from mobilesh_borotest.attr) dst_a
on src_a.attr = dst_a.name
UNION
select attr, name, id from
(SELECT DISTINCT attr FROM mobilesh_borotest.borotrade_attr group by attr) src_a
right join
(select id, name from mobilesh_borotest.attr) dst_a
on src_a.attr = dst_a.name) a
where a.name is null;

-- update attr_id into src table -> borotrade_attr

update mobilesh_borotest.borotrade_attr src_a left join 
(select id, name from mobilesh_borotest.attr where sactx <> 1) dst_a
on src_a.attr = dst_a.name
set src_a.attr_id = dst_a.id;

-- update sactx with 1 for all non existant attr_l

update mobilesh_borotest.attr_l al left join mobilesh_borotest.attr a on al.id_attr = a.id set al.sactx = a.sactx;

-- insert new values into attr_l

INSERT INTO `mobilesh_borotest`.`attr_l` (`id_attr`, `id_lang`, `title`)
select a.id, 1, a.name from `mobilesh_borotest`.`attr` a left join `mobilesh_borotest`.`attr_l` al on a.id = al.id_attr where al.id_attr is null;

-- check both tables are ok

SELECT attr FROM `mobilesh_borotest`.`borotrade_attr`group by attr;
select * from `mobilesh_borotest`.`attr` where sactx <> 1;
select * from `mobilesh_borotest`.`attr_l` where sactx <> 1;


-- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-- update stck_id in borotrade_attr from borotrade_json

update mobilesh_borotest.borotrade_attr a left join mobilesh_borotest.borotrade_json j on a.products_sku = j.products_sku and a.products_id = j.products_id set a.stck_id = j.stck_id;


-- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

-- update sactx in term where not found in borotrade_attr

update mobilesh_borotest.term t left join 
(SELECT attr_id, val FROM mobilesh_borotest.borotrade_attr group by attr_id, val) a
on t.name = a.val and t.id_attr = a.attr_id and t.sactx <> 1
set t.sactx = 1
where a.val is null;

-- insert into term the new vals

INSERT INTO `mobilesh_borotest`.`term` (`id_attr`, `name`)
select a.attr_id, a.val from 
(SELECT attr_id, val FROM mobilesh_borotest.borotrade_attr group by attr_id, val) a
left join
mobilesh_borotest.term t
on a.val = t.name and t.id_attr = a.attr_id and t.sactx <> 1
where t.id is null;

-- update term_id into src table -> borotrade_attr

update mobilesh_borotest.borotrade_attr src_a left join 
(select id, name from mobilesh_borotest.term where sactx <> 1) dst_a
on src_a.val = dst_a.name
set src_a.term_id = dst_a.id;

-- update sactx with 1 for all non existant term_l

update mobilesh_borotest.term_l tl left join mobilesh_borotest.term t on tl.id_term = t.id set tl.sactx = t.sactx;

-- insert new values into term_l

INSERT INTO `mobilesh_borotest`.`term_l` (`id_term`, `id_lang`, `title`)
select t.id, 1, t.name from `mobilesh_borotest`.`term` t left join `mobilesh_borotest`.`term_l` tl on t.id = tl.id_term where tl.id_term is null;

-- check both tables are ok

select attr_id, val from mobilesh_borotest.borotrade_attr group by attr_id, val;
select * from `mobilesh_borotest`.`term` where sactx <> 1;
select * from `mobilesh_borotest`.`term_l` where sactx <> 1;


-- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

-- update stck_a where not found in borotrade_attr
update mobilesh_borotest.stck_a s left join mobilesh_borotest.borotrade_attr a on s.id_attr = a.attr_id and s.id_term = a.term_id and s.id_stck = a.stck_id and s.sactx <> 1 set s.sactx = 1 where a.id is null;

-- insert into stck_a where new found in borotrade_attr
INSERT INTO `mobilesh_borotest`.`stck_a` (`id_stck`, `id_attr`, `id_term`)
SELECT a.stck_id, a.attr_id, a.term_id FROM mobilesh_borotest.borotrade_attr a left join mobilesh_borotest.stck_a s on a.attr_id = s.id_attr and a.term_id = s.id_term and a.stck_id = s.id_stck and s.sactx <> 1 where s.id is null;


select count(*) from mobilesh_borotest.borotrade_attr;
select count(*) from mobilesh_borotest.stck_a where sactx <> 1;


-- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-- update stck_id in borotrade_linkedp from borotrade_json

update mobilesh_borotest.borotrade_linkedp p left join mobilesh_borotest.borotrade_json j on p.products_sku = j.products_sku and p.products_id = j.products_id set p.stck_id = j.stck_id;


-- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-- update final (added by Desso
UPDATE mobilesh_borotest.stck
JOIN (
    SELECT id_stck, MIN(id) as id_gall
    FROM mobilesh_borotest.stck_g
    GROUP BY id_stck
) AS subquery
ON stck.id = subquery.id_stck
SET stck.id_gall = subquery.id_gall;

