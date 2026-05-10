-- select * from
-- (SELECT * FROM vpws_main.borotrade_attr) ba
-- left join
-- (SELECT s.isbn, s.sku, a.name as bbattr, t.name as bbterm, a.id as attrid, t.id as termid, s.id as stckid  FROM borotrade_crm.stck_a sa left join borotrade_crm.stck s on sa.id_stck = s.id left join borotrade_crm.attr a on sa.id_attr = a.id left join borotrade_crm.term t on sa.id_term = t.id where s.sactx <> 1) bb
-- on ba.products_id = bb.isbn and ba.products_sku = bb.sku and trim(ba.attr) = trim(bb.bbattr);

-- SELECT count(*) FROM vpws_main.borotrade_attr;
-- SELECT count(*)  FROM borotrade_crm.stck_a sa left join borotrade_crm.stck s on sa.id_stck = s.id left join borotrade_crm.attr a on sa.id_attr = a.id left join borotrade_crm.term t on sa.id_term = t.id where s.sactx <> 1;

-- truncate table borotrade_crm.attr;
-- truncate table borotrade_crm.attra;
-- truncate table borotrade_crm.attr_l;
-- truncate table borotrade_crm.attr_la;
-- truncate table borotrade_crm.stck;
-- truncate table borotrade_crm.stcka;
-- truncate table borotrade_crm.stck_a;
-- truncate table borotrade_crm.stck_aa;
-- truncate table borotrade_crm.stck_g;
-- truncate table borotrade_crm.stck_ga;
-- truncate table borotrade_crm.stck_l;
-- truncate table borotrade_crm.stck_la;
-- truncate table borotrade_crm.stck_r;
-- truncate table borotrade_crm.stck_ra;
-- truncate table borotrade_crm.term;
-- truncate table borotrade_crm.terma;
-- truncate table borotrade_crm.term_l;
-- truncate table borotrade_crm.term_la;

-- truncate table vpws_main.borotrade_attr;
-- truncate table vpws_main.borotrade_gallery_json;
-- truncate table vpws_main.borotrade_json;
-- truncate table vpws_main.borotrade_linkedp;


-- truncate table mobilesh_borotest.borotrade_attr;
-- truncate table mobilesh_borotest.borotrade_gallery_json;
-- truncate table mobilesh_borotest.borotrade_json;
-- truncate table mobilesh_borotest.borotrade_linkedp;


-- truncate table mobilesh_borotest.attr;
-- truncate table mobilesh_borotest.attra;
-- truncate table mobilesh_borotest.attr_l;
-- truncate table mobilesh_borotest.attr_la;
-- truncate table mobilesh_borotest.stck;
-- truncate table mobilesh_borotest.stcka;
-- truncate table mobilesh_borotest.stck_a;
-- truncate table mobilesh_borotest.stck_aa;
-- truncate table mobilesh_borotest.stck_g;
-- truncate table mobilesh_borotest.stck_ga;
-- truncate table mobilesh_borotest.stck_l;
-- truncate table mobilesh_borotest.stck_la;
-- truncate table mobilesh_borotest.stck_p;
-- truncate table mobilesh_borotest.stck_pa;
-- truncate table mobilesh_borotest.stck_r;
-- truncate table mobilesh_borotest.stck_ra;
-- truncate table mobilesh_borotest.term;
-- truncate table mobilesh_borotest.terma;
-- truncate table mobilesh_borotest.term_l;
-- truncate table mobilesh_borotest.term_la;



-- truncate table techclea_waret.borotrade_attr;
-- truncate table techclea_waret.borotrade_gallery_json;
-- truncate table techclea_waret.borotrade_json;
-- truncate table techclea_waret.borotrade_linkedp;


-- truncate table techclea_ware.attr;
-- truncate table techclea_ware.attra;
-- truncate table techclea_ware.attr_l;
-- truncate table techclea_ware.attr_la;
-- truncate table techclea_ware.stck;
-- truncate table techclea_ware.stcka;
-- truncate table techclea_ware.stck_a;
-- truncate table techclea_ware.stck_aa;
-- truncate table techclea_ware.stck_g;
-- truncate table techclea_ware.stck_ga;
-- truncate table techclea_ware.stck_l;
-- truncate table techclea_ware.stck_la;
-- truncate table techclea_ware.stck_r;
-- truncate table techclea_ware.stck_ra;
-- truncate table techclea_ware.term;
-- truncate table techclea_ware.terma;
-- truncate table techclea_ware.term_l;
-- truncate table techclea_ware.term_la;

-- truncate table techclea_ware.borotrade_attr;
-- truncate table techclea_ware.borotrade_gallery_json;
-- truncate table techclea_ware.borotrade_json;
-- truncate table techclea_ware.borotrade_linkedp;
