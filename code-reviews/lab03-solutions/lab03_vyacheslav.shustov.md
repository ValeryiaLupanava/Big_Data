```
select
uid,
case when g11 > 9 or g12 > 9 or g13 > 9 then 1 else 0 end g1, 
case when g21 > 9 or g22 > 9 or g23 > 9 then 1 else 0 end g2,
case when g31 > 9 or g32 > 9 or g33 > 9 then 1 else 0 end g3,
case when g41 > 9 or g42 > 9 or g33 > 9 then 1 else 0 end g4
from 
( 
select
uid,
sum(g11) g11, sum(g12) g12, sum(g13) g13,
sum(g21) g21, sum(g22) g22, sum(g23) g23,
sum(g31) g31, sum(g32) g32, sum(g33) g33,
sum(g41) g41, sum(g42) g42, sum(g43) g43
from 
(
select
uid,
case urlnew when 'cars.ru'           then 1 else 0 end g11,
case urlnew when 'avto-russia.ru'    then 1 else 0 end g12,
case urlnew when 'bmwclub.ru'        then 1 else 0 end g13,
case urlnew when 'vk.com'            then 1 else 0 end g21,
case urlnew when 'mail.qip.ru'       then 1 else 0 end g22,
case urlnew when 'lk.ssl.mts.ru'     then 1 else 0 end g23,
case urlnew when 'games.mail.ru'     then 1 else 0 end g31,
case urlnew when 'igrystrelyalki.ru' then 1 else 0 end g32,
case urlnew when 'consol-games.net'  then 1 else 0 end g33,
case urlnew when '5ballov.qip.ru'    then 1 else 0 end g41,
case urlnew when 'mgimo.ru'          then 1 else 0 end g42,
case urlnew when 'referat.arxiv.uz'  then 1 else 0 end g43 
from shu_lab3
) a group by a.uid
) b```