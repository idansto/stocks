SELECT * FROM shares.feature_data;
SELECT count(*) FROM shares.feature_data;

insert into shares.feature_data (company_id, feature_id, date, value) values (4300, 22, "2001-2-21", 1233) ON DUPLICATE KEY UPDATE value=1244;

select t.ticker, t.date, revevnue, t.Cost_Of_Goods_Sold
from
	(SELECT 
		c.ticker,
		dates.date,
		(select d.value from shares.feature_data d where d.company_id = c.id and d.date = dates.date and d.feature_id = 1) as revevnue,
		(select d.value from shares.feature_data d where d.company_id = c.id and d.date = dates.date and d.feature_id = 2) as Cost_Of_Goods_Sold
	from
		shares.companies c,
		(select '2020-3-31' date from dual) as dates
	) as t
where t.revevnue is not null;

SELECT 
    c.comp_name, dates.date, d.value
FROM
    shares.companies c,
    shares.features f,
    shares.feature_data d,
    (SELECT '2020-3-31' date FROM DUAL) AS dates
WHERE
    d.company_id = c.id
        AND d.date = dates.date
        AND d.feature_id = 1

select '2020-3-31' date from dual union all
select '2020-6-30' date from dual ;

(select '2020-3-31' date from dual union all
select '2020-6-30' date from dual) 

select * from shares.companies c where c.ticker = 'club';