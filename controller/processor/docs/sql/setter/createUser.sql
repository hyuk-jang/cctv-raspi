create user 'cctv'@'%' IDENTIFIED BY 'cctv';
grant all privileges on cctv_db.* to cctv@'%';
flush privileges;'

