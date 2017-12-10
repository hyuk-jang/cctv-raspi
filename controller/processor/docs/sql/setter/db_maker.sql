-- --------------------------------------------------------
-- 호스트:                          127.0.0.1
-- 서버 버전:                        10.2.6-MariaDB - mariadb.org binary distribution
-- 서버 OS:                        Win64
-- HeidiSQL 버전:                  9.4.0.5125
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- cctv_db 데이터베이스 구조 내보내기
CREATE DATABASE IF NOT EXISTS `cctv_db` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `cctv_db`;

-- 테이블 cctv_db.cctv_info 구조 내보내기
CREATE TABLE IF NOT EXISTS `cctv_info` (
  `cctv_id` varchar(50) NOT NULL,
  `name` varchar(20) DEFAULT NULL,
  `address` varchar(100) DEFAULT NULL,
  `writedate` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`cctv_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 테이블 데이터 cctv_db.cctv_info:~5 rows (대략적) 내보내기
/*!40000 ALTER TABLE `cctv_info` DISABLE KEYS */;
INSERT INTO `cctv_info` (`cctv_id`, `name`, `address`, `writedate`) VALUES
	('aaaa', '에스엠 소화전', '전라남도 나주시 빛가람로 115', '2017-12-11 00:07:20'),
	('bbbb', '인희 소화전', '전라남도 나주시 영덕대교 543', '2017-12-11 00:08:02'),
	('cccc', '바우나 소화전', '전라남도 무안군 일사로 667', '2017-12-11 00:08:33'),
	('dddd', '홍길동 소화전', '전라남도 홍길군 동면 123', '2017-12-11 00:09:09'),
	('eeee', '전우치 소화전', '전라남도 전우시 우치면 999', '2017-12-11 00:09:39');
/*!40000 ALTER TABLE `cctv_info` ENABLE KEYS */;

-- 테이블 cctv_db.illegal_data 구조 내보내기
CREATE TABLE IF NOT EXISTS `illegal_data` (
  `illegal_data_seq` mediumint(9) NOT NULL AUTO_INCREMENT,
  `cctv_id` varchar(50) NOT NULL,
  `count` tinyint(4) DEFAULT NULL,
  `status` enum('reset','new','continue','end') DEFAULT NULL,
  `img` varchar(100) DEFAULT NULL,
  `measure_date` datetime DEFAULT NULL,
  `write_date` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`illegal_data_seq`),
  KEY `FK_illegal_data_cctv_info` (`cctv_id`),
  CONSTRAINT `FK_illegal_data_cctv_info` FOREIGN KEY (`cctv_id`) REFERENCES `cctv_info` (`cctv_id`)
) ENGINE=InnoDB AUTO_INCREMENT=202 DEFAULT CHARSET=utf8;

-- 테이블 데이터 cctv_db.illegal_data:~0 rows (대략적) 내보내기
/*!40000 ALTER TABLE `illegal_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `illegal_data` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
