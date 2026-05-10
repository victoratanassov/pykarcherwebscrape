SELECT * FROM borotrade_crm.term where sactx <> 1;
select * from vpws_main.borotrade_attr;

-- update sactx in term where not found in borotrade_attr

update borotrade_crm.term t left join 
(SELECT attr_id, val FROM vpws_main.borotrade_attr group by attr_id, val) a
on t.name = a.val and t.id_attr = a.attr_id and t.sactx <> 1
set t.sactx = 1
where a.val is null;

-- insert into term the new vals

INSERT INTO `borotrade_crm`.`term` (`id_attr`, `name`)
select a.attr_id, a.val from 
(SELECT attr_id, val FROM vpws_main.borotrade_attr group by attr_id, val) a
left join
borotrade_crm.term t
on a.val = t.name and t.id_attr = a.attr_id and t.sactx <> 1
where t.id is null;

-- update term_id into src table -> borotrade_attr

update vpws_main.borotrade_attr src_a left join 
(select id, id_attr, name from borotrade_crm.term where sactx <> 1) dst_a
on src_a.val = dst_a.name and src_a.attr_id = dst_a.id_attr
set src_a.term_id = dst_a.id;

-- update sactx with 1 for all non existant term_l

update borotrade_crm.term_l tl left join borotrade_crm.term t on tl.id_term = t.id set tl.sactx = t.sactx;

-- insert new values into term_l

INSERT INTO `borotrade_crm`.`term_l` (`id_term`, `id_lang`, `title`)
select t.id, 1, t.name from `borotrade_crm`.`term` t left join `borotrade_crm`.`term_l` tl on t.id = tl.id_term where tl.id_term is null;

-- check both tables are ok

select attr_id, val from vpws_main.borotrade_attr group by attr_id, val;
select * from `borotrade_crm`.`term` where sactx <> 1;
select * from `borotrade_crm`.`term_l` where sactx <> 1;


select * from `borotrade_crm`.`term` t left join borotrade_crm.attr_l a on t.id_attr = a.id_attr where t.sactx <> 1;