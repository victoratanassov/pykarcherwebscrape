
-- check for differences in attr and attr_l?!


-- update sactx with 1 for all non existant attr

update borotrade_crm.attr a right join
(select attr, name, id from
(select attr, name, id from
(SELECT DISTINCT attr FROM vpws_main.borotrade_attr group by attr) src_a
left join
-- (select id, name from borotrade_crm.attr) dst_a
(WITH attru AS (SELECT * FROM borotrade_crm.`attr` UNION SELECT * FROM borotrade_crm.`attra`) SELECT DISTINCT b.id, b.name FROM (SELECT abs(id) AS id, MAX(stime) AS stime FROM attru GROUP BY abs(id)) a LEFT JOIN attru b ON a.id=abs(b.id) AND a.stime=b.stime) dst_a
on src_a.attr = dst_a.name
UNION
select attr, name, id from
(SELECT DISTINCT attr FROM vpws_main.borotrade_attr group by attr) src_a
right join
-- (select id, name from borotrade_crm.attr) dst_a
(WITH attru AS (SELECT * FROM borotrade_crm.`attr` UNION SELECT * FROM borotrade_crm.`attra`) SELECT DISTINCT b.id, b.name FROM (SELECT abs(id) AS id, MAX(stime) AS stime FROM attru GROUP BY abs(id)) a LEFT JOIN attru b ON a.id=abs(b.id) AND a.stime=b.stime) dst_a
on src_a.attr = dst_a.name) a
where a.attr is null) src on src.id = a.id
set a.sactx = 1;

-- (SELECT * FROM `vpws_main`.`borotrade_attr`)


-- select attr, name, id from
-- (select attr, name, id from
-- (SELECT attr FROM vpws_main.borotrade_attr group by attr) src_a
-- left join
-- (select id, name from borotrade_crm.attr) dst_a
-- on src_a.attr = dst_a.name
-- UNION
-- select attr, name, id from
-- (SELECT attr FROM vpws_main.borotrade_attr group by attr) src_a
-- right join
-- (select id, name from borotrade_crm.attr) dst_a
-- on src_a.attr = dst_a.name) a
-- where a.attr is null;

-- insert all new rows into attr

insert into borotrade_crm.attr (name)
select attr from
(select attr, name, id from
(SELECT DISTINCT attr FROM vpws_main.borotrade_attr group by attr) src_a
left join
-- (select id, name from borotrade_crm.attr) dst_a
(WITH attru AS (SELECT * FROM borotrade_crm.`attr` UNION SELECT * FROM borotrade_crm.`attra`) SELECT DISTINCT b.id, b.name FROM (SELECT abs(id) AS id, MAX(stime) AS stime FROM attru GROUP BY abs(id)) a LEFT JOIN attru b ON a.id=abs(b.id) AND a.stime=b.stime) dst_a
on src_a.attr = dst_a.name
UNION
select attr, name, id from
(SELECT DISTINCT attr FROM vpws_main.borotrade_attr group by attr) src_a
right join
-- (select id, name from borotrade_crm.attr) dst_a
(WITH attru AS (SELECT * FROM borotrade_crm.`attr` UNION SELECT * FROM borotrade_crm.`attra`) SELECT DISTINCT b.id, b.name FROM (SELECT abs(id) AS id, MAX(stime) AS stime FROM attru GROUP BY abs(id)) a LEFT JOIN attru b ON a.id=abs(b.id) AND a.stime=b.stime) dst_a
on src_a.attr = dst_a.name) a
where a.name is null;

-- update attr_id into src table -> borotrade_attr

update vpws_main.borotrade_attr src_a left join 
(select id, name from borotrade_crm.attr where sactx <> 1) dst_a
on src_a.attr = dst_a.name
set src_a.attr_id = dst_a.id;

-- update sactx with 1 for all non existant attr_l

update borotrade_crm.attr_l al left join borotrade_crm.attr a on al.id_attr = a.id set al.sactx = a.sactx;

-- insert new values into attr_l

INSERT INTO `borotrade_crm`.`attr_l` (`id_attr`, `id_lang`, `title`)
select a.id, 1, a.name from `borotrade_crm`.`attr` a left join `borotrade_crm`.`attr_l` al on a.id = al.id_attr where al.id_attr is null;

-- check both tables are ok

SELECT attr FROM `vpws_main`.`borotrade_attr`group by attr;
select * from `borotrade_crm`.`attr` where sactx <> 1;
select * from `borotrade_crm`.`attr_l` where sactx <> 1;

SELECT attr FROM `mobilesh_borotest`.`borotrade_attr`group by attr;
select * from `mobilesh_borotest`.`attr` where sactx <> 1;
select * from `mobilesh_borotest`.`attr_l` where sactx <> 1;


-- update stck_id in borotrade_attr from borotrade_json

update vpws_main.borotrade_attr a left join vpws_main.borotrade_json j on a.products_sku = j.products_sku and a.products_id = j.products_id set a.stck_id = j.stck_id;

