#먼저 데이터 베이스 만든 다음에  순서대로 실행할 것!!!
# 데이터베이스 세팅(자신이 만든 계정이 있는지, 만든 데이터베이를 쓰기위해 로그인, car_insert를 전역으로 권한을 바꿔준다. 즉 모두 들어올수 있는 계정이다.)
#SELECT user, host FROM mysql.user WHERE user = 'car_insert';
#CREATE USER 'car_insert'@'%' IDENTIFIED BY 'car1234'; 
#GRANT ALL PRIVILEGES ON car_insert.* TO 'car_insert'@'%';

show databases; # 여기에서 아직은 안만들어서 지금은 안보일것이다.


CREATE database car_insert DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci; # 데이터베이스를 만들고 뒤에 SET utf8mb4 COLLATE utf8mb4_unicode_ci 이건 한글 깨짐과 이모지를 등록할 수 있도록 한다.

# car_insert 데이터베이스 사용
use car_insert;
# 여기서부터 ev_eco_car.sql에 들어가서 세미콜론(;)이 있는 부분마다 ctrl + enter 키를 눌러 실행한다.(모두 드래그 하여 할 경우 에러난다........)

# 다했으면 테이블 다 만들어졌는지 확인
show tables;

# 테이블에 값이 다 들어갔나 확인
select * from base_year;
select * from charger_yearly;
select * from ev_registration;
select * from hydrogen_regional;
select * from hydrogen_yearly;
select * from population;
select * from region;
select * from subsidy;
select * from temperature_yearly;
select * from total_vehicle_yearly;
select * from transport_co2;


# 한꺼번에 보고싶은때
select 'region' as 테이블, count(*) as 행수 from region
UNION ALL
select 'charger_yearly' , count(*) from charger_yearly
UNION ALL
select 'ev_registration' , count(*) from ev_registration
UNION ALL
select 'hydrogen_regional' , count(*) from hydrogen_regional
UNION ALL
select 'hydrogen_yearly' , count(*) from hydrogen_yearly
UNION ALL
select 'population' , count(*) from population
UNION ALL
select 'base_year' , count(*) from base_year
UNION ALL
select 'subsidy' , count(*) from subsidy
UNION ALL
select 'temperature_yearly' , count(*) from temperature_yearly
UNION ALL
select 'total_vehicle_yearly' , count(*) from total_vehicle_yearly
UNION ALL
select 'transport_co2' , count(*) from transport_co2;

DESC temperature_yearly;

SELECT re
    FROM total_vehicle_yearly;
