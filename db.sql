-- MySQL dump 10.13  Distrib 5.7.25, for Linux (x86_64)
--
-- Host: localhost    Database: buildrtest
-- ------------------------------------------------------
-- Server version	5.7.25-0ubuntu0.18.04.2

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `gpu`
--

DROP TABLE IF EXISTS `gpu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gpu` (
  `id` varchar(40) NOT NULL,
  `model` varchar(10) DEFAULT NULL,
  `brand` enum('AMD','NVIDIA') DEFAULT NULL,
  `vendor` varchar(30) DEFAULT NULL,
  `image` varchar(200) DEFAULT NULL,
  `min_price` int(6) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `gpu_prices`
--

DROP TABLE IF EXISTS `gpu_prices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gpu_prices` (
  `id` varchar(40) NOT NULL,
  `price` int(6) DEFAULT NULL,
  `link` varchar(200) NOT NULL,
  `seller` varchar(20) NOT NULL,
  PRIMARY KEY (`id`,`seller`),
  CONSTRAINT `gpu_prices_ibfk_1` FOREIGN KEY (`id`) REFERENCES `gpu` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `motherboard`
--

DROP TABLE IF EXISTS `motherboard`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `motherboard` (
  `id` varchar(30) NOT NULL,
  `brand` enum('AMD','INTEL') DEFAULT NULL,
  `chipset` varchar(20) NOT NULL,
  `vendor` varchar(20) NOT NULL,
  `socket` varchar(20) NOT NULL,
  `image` varchar(200) DEFAULT NULL,
  `min_price` int(6) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `motherboard_prices`
--

DROP TABLE IF EXISTS `motherboard_prices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `motherboard_prices` (
  `id` varchar(30) NOT NULL,
  `price` int(6) DEFAULT NULL,
  `link` varchar(200) NOT NULL,
  `seller` varchar(20) NOT NULL,
  PRIMARY KEY (`id`,`seller`),
  CONSTRAINT `motherboard_prices_ibfk_1` FOREIGN KEY (`id`) REFERENCES `motherboard` (`id`),
  CONSTRAINT `motherboard_prices_ibfk_2` FOREIGN KEY (`id`) REFERENCES `motherboard` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `processor`
--

DROP TABLE IF EXISTS `processor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `processor` (
  `id` varchar(7) NOT NULL,
  `brand` enum('AMD','INTEL') DEFAULT NULL,
  `series` varchar(10) NOT NULL,
  `gen` int(1) NOT NULL,
  `socket` varchar(20) NOT NULL,
  `codename` varchar(20) NOT NULL,
  `unlocked` varchar(3) NOT NULL,
  `image` varchar(200) DEFAULT NULL,
  `min_price` int(6) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `processor_prices`
--

DROP TABLE IF EXISTS `processor_prices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `processor_prices` (
  `id` varchar(7) NOT NULL,
  `price` int(6) DEFAULT NULL,
  `link` varchar(200) NOT NULL,
  `seller` varchar(20) NOT NULL,
  PRIMARY KEY (`id`,`seller`),
  CONSTRAINT `processor_prices_ibfk_2` FOREIGN KEY (`id`) REFERENCES `processor` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `processor_prices_ibfk_3` FOREIGN KEY (`id`) REFERENCES `processor` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `product`
--

DROP TABLE IF EXISTS `product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `product` (
  `id` varchar(50) NOT NULL,
  `title` varchar(300) DEFAULT NULL,
  `category` varchar(30) DEFAULT NULL,
  `image` varchar(300) DEFAULT NULL,
  `min_price` int(6) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ram`
--

DROP TABLE IF EXISTS `ram`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ram` (
  `id` varchar(40) NOT NULL,
  `brand` varchar(30) DEFAULT NULL,
  `size` varchar(5) DEFAULT NULL,
  `rate` varchar(4) DEFAULT NULL,
  `speed` varchar(7) DEFAULT NULL,
  `image` varchar(200) DEFAULT NULL,
  `min_price` int(6) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ram_prices`
--

DROP TABLE IF EXISTS `ram_prices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ram_prices` (
  `id` varchar(30) NOT NULL,
  `price` int(6) DEFAULT NULL,
  `link` varchar(200) NOT NULL,
  `seller` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`,`link`),
  CONSTRAINT `ram_prices_ibfk_1` FOREIGN KEY (`id`) REFERENCES `ram` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-04-28 21:49:28
