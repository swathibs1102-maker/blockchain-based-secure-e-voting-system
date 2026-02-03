-- MySQL Administrator dump 1.4
--
-- ------------------------------------------------------
-- Server version	5.5.19


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


--
-- Create schema evoting
--

CREATE DATABASE IF NOT EXISTS evoting;
USE evoting;

--
-- Definition of table `addparty`
--

DROP TABLE IF EXISTS `addparty`;
CREATE TABLE `addparty` (
  `candidatename` varchar(30) DEFAULT NULL,
  `partyname` varchar(50) DEFAULT NULL,
  `areaname` varchar(100) DEFAULT NULL,
  `image` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `addparty`
--

/*!40000 ALTER TABLE `addparty` DISABLE KEYS */;
/*!40000 ALTER TABLE `addparty` ENABLE KEYS */;


--
-- Definition of table `candidate`
--

DROP TABLE IF EXISTS `candidate`;
CREATE TABLE `candidate` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `candname` varchar(45) NOT NULL,
  `partyname` varchar(45) NOT NULL,
  `cname` varchar(245) NOT NULL,
  `fname` varchar(245) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `candidate`
--

/*!40000 ALTER TABLE `candidate` DISABLE KEYS */;
INSERT INTO `candidate` (`id`,`candname`,`partyname`,`cname`,`fname`) VALUES 
 (1,'Puneeth','BJP','Rajajinagar','bjp.png'),
 (2,'shivanna','congress','Rajajinagar','congress.png'),
 (3,'ROCKYBOY','JDS','Rajajinagar','samajvadi.png');
/*!40000 ALTER TABLE `candidate` ENABLE KEYS */;


--
-- Definition of table `castvote`
--

DROP TABLE IF EXISTS `castvote`;
CREATE TABLE `castvote` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uname` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `castvote`
--

/*!40000 ALTER TABLE `castvote` DISABLE KEYS */;
INSERT INTO `castvote` (`id`,`uname`) VALUES 
 (1,'Mounika');
/*!40000 ALTER TABLE `castvote` ENABLE KEYS */;


--
-- Definition of table `register`
--

DROP TABLE IF EXISTS `register`;
CREATE TABLE `register` (
  `username` varchar(30) NOT NULL,
  `password` varchar(30) DEFAULT NULL,
  `contact` varchar(12) DEFAULT NULL,
  `email` varchar(30) DEFAULT NULL,
  `address` varchar(40) DEFAULT NULL,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `register`
--

/*!40000 ALTER TABLE `register` DISABLE KEYS */;
INSERT INTO `register` (`username`,`password`,`contact`,`email`,`address`) VALUES 
 ('eswar','eswar','9902752525','mindsparkblore@gmail.com','Vijayanagar'),
 ('Mounika','mounika','1234567890','kmouni041234@gmail.com','Rajajinagar'),
 ('rakshitha','rakshitha','9876543210','rakshitharaksha98@gmail.com','Rajajinagar'),
 ('varini','varini','9876523445','variniroyal8@gmail.com','Vijayanagar');
/*!40000 ALTER TABLE `register` ENABLE KEYS */;




/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
