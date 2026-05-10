
-- update into stck_r not found
update `vpws_main`.borotrade_linkedp p left join `borotrade_crm`.stck_r r on p.stck_id = r.id_stck and r.sactx <> 1 set r.sactx = 1 where p.stck_id is null;

-- insert into stck_r the new found rows
INSERT INTO `borotrade_crm`.`stck_r` (`id_stck`, `text`)
select p.stck_id, p.linkedp from `vpws_main`.borotrade_linkedp p left join `borotrade_crm`.stck_r r on p.stck_id = r.id_stck and r.sactx <> 1 where r.id_stck is null;

-- check
SELECT * FROM `vpws_main`.borotrade_linkedp;
SELECT * FROM `borotrade_crm`.`stck_r` where sactx <> 1;
