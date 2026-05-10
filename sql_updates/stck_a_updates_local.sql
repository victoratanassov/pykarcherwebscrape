-- update stck_a where not found in borotrade_attr
update borotrade_crm.stck_a s left join vpws_main.borotrade_attr a on s.id_attr = a.attr_id and s.id_term = a.term_id and s.id_stck = a.stck_id and s.sactx <> 1 set s.sactx = 1 where a.id is null;

-- insert into stck_a where new found in borotrade_attr
INSERT INTO `borotrade_crm`.`stck_a` (`id_stck`, `id_attr`, `id_term`)
SELECT a.stck_id, a.attr_id, a.term_id FROM vpws_main.borotrade_attr a left join borotrade_crm.stck_a s on a.attr_id = s.id_attr and a.term_id = s.id_term and a.stck_id = s.id_stck and s.sactx <> 1 where s.id is null;


	-- update stck_id in borotrade_lgallery_json from borotrade_json

	update `vpws_main`.borotrade_gallery_json g left join `vpws_main`.borotrade_json j on g.products_sku = j.products_sku and g.products_id = j.products_id set g.stck_id = j.stck_id;


-- update stck_g where not found in borotrade_gallery_json
update borotrade_crm.stck_g s left join vpws_main.borotrade_gallery_json a on s.id_stck = a.stck_id and s.sactx <> 1 set s.sactx = 1 where a.id is null;

-- insert into stck_g where new found in borotrade_gallery_json
INSERT INTO `borotrade_crm`.`stck_g` (`id_stck`, `urlx`, `path`)
SELECT a.stck_id, a.gallery, a.path FROM vpws_main.borotrade_gallery_json a left join borotrade_crm.stck_g s on a.stck_id = s.id_stck and s.sactx <> 1 where s.id is null;


select count(*) from vpws_main.borotrade_attr;
select count(*) from borotrade_crm.stck_a where sactx <> 1;

call borotrade_crm.boroimport(@output);


SELECT count(*) FROM borotrade_crm.`stck_a` s;

SELECT * FROM vpws_main.borotrade_attr;

SELECT * FROM borotrade_crm.`stck_a` s left join borotrade_crm.attr a on a.id=s.id_attr left join borotrade_crm.term t on t.id=s.id_term where s.id_attr<>t.id_attr;

-- 'Initial feed count -> 1331\nUpdates found -> 0\nInserts into archive table stcka -> 0\nUpdate stck where changes found -> 0\nInsert into stck where new rows found -> 1331\nUpdate stck to mark as delete where feed items not found -> 0\nUpdate stck stck_id into feed table -> 1331\nUpdated destination table active items after import -> 1331\nUpdates stck_l found -> 0\nInserts into archive table stck_la -> 0\nUpdate stck_l where changes found -> 0\nInsert into stck_l where new rows found -> 1331\nUpdate stck_l to mark as delete where feed items not found -> 0\nUpdated destination table active items after import -> 1331\nUpdate attr to mark as delete where feed items not found -> 0\nInsert into attr where new rows found -> 824\nUpdate attr_id into feed table -> 5971\nUpdate attr_l to mark as delete where feed items not found -> 0\nInsert into attr_l where new rows found -> 824\nFeed table attr active items -> 824\nUpdated destination table attr active items after impot -> 824\nUpdated destination table attr_l active items after impot -> 824\nUpdated feed table attr_l -> 824\nInsert into term where new rows found -> 3588\nUpdate term_id into feed table -> 5971\nUpdate term to mark as delete where feed items not found -> 0\nInsert into term_l where new rows found -> 3588\nFeed table term active items -> 3588\nUpdated destination table term active items after impot -> 3588\nUpdated destination table term_l active items after impot -> 3588\nUpdate term to mark as delete where feed items not found -> 0\nInsert into term_l where new rows found -> 5971\nFeed table stck_a active items -> 5971\nUpdated destination table stck_a active items after impot -> 5971\nUpdate stck_r to mark as delete where feed items not found -> 0\nInsert into stck_r where new rows found -> 871\nFeed table linkedp active items -> 871\nUpdated destination table stck_r active items after impot -> 871\nUpdate borotrade_gallery_json id_stck -> 3351\nUpdate stck_g to mark as delete where feed items not found -> 0\nInsert into stck_g where new rows found -> 3351\nFeed table gallery_json active items -> 3351\nUpdated destination table stck_g active items after impot -> 3351\n'

