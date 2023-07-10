-- MySQL dump 10.13  Distrib 8.0.32, for Linux (x86_64)
--
-- Host: localhost    Database: gigs
-- ------------------------------------------------------
-- Server version	8.0.32

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_tokens`
--

DROP TABLE IF EXISTS `auth_tokens`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_tokens` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `token` varchar(255) NOT NULL,
  `owner_id` int NOT NULL,
  `session_id` varchar(128) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `token` (`token`),
  UNIQUE KEY `owner_id_session_id_idx` (`owner_id`,`session_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_tokens`
--

LOCK TABLES `auth_tokens` WRITE;
/*!40000 ALTER TABLE `auth_tokens` DISABLE KEYS */;
INSERT INTO `auth_tokens` VALUES (1,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJ0eXBlIjoyLCJyb2xlIjoxLCJzZXNzaW9uX2lkIjoiNTdkczVHTnE1Z2VIN2J4UVVsSktoZyIsImV4cCI6MTY4NzQwMDM4Ny43MDE5Mzh9.E928RJfqeWvx97wWgOixm00NheL87piJmN4K9rukCbU',1,'57ds5GNq5geH7bxQUlJKhg');
/*!40000 ALTER TABLE `auth_tokens` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `event`
--

DROP TABLE IF EXISTS `event`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `event` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  `venue_name` varchar(128) NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `event_type` varchar(60) NOT NULL,
  `create_time` datetime NOT NULL,
  `update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `start_date_end_date_venue_name_idx` (`start_date`,`end_date`,`venue_name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event`
--

LOCK TABLES `event` WRITE;
/*!40000 ALTER TABLE `event` DISABLE KEYS */;
INSERT INTO `event` VALUES (1,'Glastonbury','Glastonbury','2023-04-15','2023-04-16','music_festival','2023-06-20 20:19:04',NULL),(2,'O2 Academy Brixton','O2 Academy Brixton','2023-04-17','2023-04-18','music_concert','2023-06-20 20:19:04',NULL),(3,'Primavera Sound','Primavera Sound','2023-04-17','2023-04-18','music_festival','2023-06-20 20:19:04',NULL);
/*!40000 ALTER TABLE `event` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `feature`
--

DROP TABLE IF EXISTS `feature`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `feature` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `featured_entity_type` varchar(60) NOT NULL,
  `featured_entity_id` int unsigned NOT NULL,
  `featurer_type` varchar(60) NOT NULL,
  `featurer_id` int unsigned NOT NULL,
  `creator_id` int unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ft_type_ft_id_ftured_entity_type_ftured_entity_id_idx` (`featurer_type`,`featurer_id`,`featured_entity_type`,`featured_entity_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `feature`
--

LOCK TABLES `feature` WRITE;
/*!40000 ALTER TABLE `feature` DISABLE KEYS */;
INSERT INTO `feature` VALUES (1,'post',3,'performer',1,3),(2,'post',4,'performer',1,3);
/*!40000 ALTER TABLE `feature` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `files`
--

DROP TABLE IF EXISTS `files`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `files` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `uuid` varchar(255) NOT NULL,
  `file_name` varchar(1024) NOT NULL,
  `file_size` int DEFAULT NULL,
  `mime_type` varchar(255) NOT NULL,
  `url` varchar(512) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uuid_idx` (`uuid`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `files`
--

LOCK TABLES `files` WRITE;
/*!40000 ALTER TABLE `files` DISABLE KEYS */;
INSERT INTO `files` VALUES (1,'show1','show1.mp4',NULL,'video/mp4','https://fileservice-bucket-post.s3.amazonaws.com/show1?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAR56DCSXK3Z75BQB2%2F20230620%2Fus-east-2%2Fs3%2Faws4_request&X-Amz-Date=20230620T201839Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=a109cb298af377591872d646b216bcc138f75692c08ac2f3dc829aa34dbaf8dd'),(2,'show1thumbnail','show1-thumbnail.png',NULL,'img/png','https://fileservice-bucket-post.s3.amazonaws.com/show1thumbnail?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAR56DCSXK3Z75BQB2%2F20230620%2Fus-east-2%2Fs3%2Faws4_request&X-Amz-Date=20230620T201840Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=a940292dd78ecd8a5c1f37c602bd7ce225071fbb2c869d46928d5d19995bbbfa'),(3,'show2','show2.mp4',NULL,'video/mp4','https://fileservice-bucket-post.s3.amazonaws.com/show2?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAR56DCSXK3Z75BQB2%2F20230620%2Fus-east-2%2Fs3%2Faws4_request&X-Amz-Date=20230620T201842Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=a883835e246207106c031b53920c9496020c3b447974a527c8cff8ccaf5d8315'),(4,'show2thumbnail','show2-thumbnail.png',NULL,'img/png','https://fileservice-bucket-post.s3.amazonaws.com/show2thumbnail?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAR56DCSXK3Z75BQB2%2F20230620%2Fus-east-2%2Fs3%2Faws4_request&X-Amz-Date=20230620T201844Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=cb026708448921a8eea56a8d265f5f5545cdba4b9f0ce4ea1353ccd3f487597f'),(5,'show3','show3.mp4',NULL,'video/mp4','https://fileservice-bucket-post.s3.amazonaws.com/show3?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAR56DCSXK3Z75BQB2%2F20230620%2Fus-east-2%2Fs3%2Faws4_request&X-Amz-Date=20230620T201850Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=c179c523123fd32da1b1ffbdb38d6d3cadba9b53e59bdf799c683c7dc9357bb6'),(6,'show3thumbnail','show3-thumbnail.png',NULL,'img/png','https://fileservice-bucket-post.s3.amazonaws.com/show3thumbnail?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAR56DCSXK3Z75BQB2%2F20230620%2Fus-east-2%2Fs3%2Faws4_request&X-Amz-Date=20230620T201851Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=9a2c6100dcbbc7bb0007d2ee4d30dfee67d79599f9cd86a7e93fbe3a815cfb19'),(7,'show4','show4.mp4',NULL,'video/mp4','https://fileservice-bucket-post.s3.amazonaws.com/show4?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAR56DCSXK3Z75BQB2%2F20230620%2Fus-east-2%2Fs3%2Faws4_request&X-Amz-Date=20230620T201855Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=3ee54872f77701b6564a52a5fed7eac20df8e73c9cc995a074b4f88ecf68d341'),(8,'show4thumbnail','show4-thumbnail.png',NULL,'img/png','https://fileservice-bucket-post.s3.amazonaws.com/show4thumbnail?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAR56DCSXK3Z75BQB2%2F20230620%2Fus-east-2%2Fs3%2Faws4_request&X-Amz-Date=20230620T201856Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=7b05129e9083dee404dcca5e1dfcc917502a977d26a194b3992a5148f1121c40'),(9,'show5','show5.mp4',NULL,'video/mp4','https://fileservice-bucket-post.s3.amazonaws.com/show5?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAR56DCSXK3Z75BQB2%2F20230620%2Fus-east-2%2Fs3%2Faws4_request&X-Amz-Date=20230620T201858Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=d2133105d890f6a149024b95d5d663e5ec7f3fee665b97c18ba1137cfc255016'),(10,'show5thumbnail','show5-thumbnail.png',NULL,'img/png','https://fileservice-bucket-post.s3.amazonaws.com/show5thumbnail?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAR56DCSXK3Z75BQB2%2F20230620%2Fus-east-2%2Fs3%2Faws4_request&X-Amz-Date=20230620T201859Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=743fc598f9299bcaa748453a0d89402fed6a005c21c7e82fa37d6eb73732e35b'),(11,'202','dog.mp4',NULL,'video/mp4','https://fileservice-bucket-post.s3.amazonaws.com/202?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAR56DCSXK3Z75BQB2%2F20230620%2Fus-east-2%2Fs3%2Faws4_request&X-Amz-Date=20230620T201903Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=914cf7b1c64bb25dabdead4a36f90a6bf5627ef178716a4347c94f909c21619f'),(12,'123456','profile-pic.jpg',NULL,'image/jpeg','https://fileservice-bucket-post.s3.amazonaws.com/123456?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAR56DCSXK3Z75BQB2%2F20230620%2Fus-east-2%2Fs3%2Faws4_request&X-Amz-Date=20230620T201904Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=d9dd810d9a327b720f8ac4a17239866d65abfed14e08d1a1c3a7dfe197e532b2'),(13,'aaaaaaaaaaaaaaa','profile-pic2.jpg',NULL,'image/jpeg','https://fileservice-bucket-post.s3.amazonaws.com/aaaaaaaaaaaaaaa?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAR56DCSXK3Z75BQB2%2F20230620%2Fus-east-2%2Fs3%2Faws4_request&X-Amz-Date=20230620T201905Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=95cbd825780c594bbd3d56de6f31a371838ece842669786b713fd37e5ffda9c5');
/*!40000 ALTER TABLE `files` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `performance`
--

DROP TABLE IF EXISTS `performance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `performance` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `event_id` int unsigned DEFAULT NULL,
  `performer_id` int unsigned NOT NULL,
  `performance_date` date NOT NULL,
  `create_time` datetime NOT NULL,
  `update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `performer_id_performance_date_event_id_idx` (`performer_id`,`performance_date`,`event_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `performance`
--

LOCK TABLES `performance` WRITE;
/*!40000 ALTER TABLE `performance` DISABLE KEYS */;
INSERT INTO `performance` VALUES (1,1,1,'2023-06-20','2023-06-20 20:19:06',NULL),(2,3,1,'2023-06-20','2023-06-20 20:19:06',NULL),(3,2,1,'2023-06-23','2023-06-20 20:19:06',NULL),(4,1,1,'2023-06-25','2023-06-20 20:19:06',NULL),(5,2,1,'2023-06-25','2023-06-20 20:19:06',NULL),(6,2,3,'2023-06-28','2023-06-20 20:19:06',NULL);
/*!40000 ALTER TABLE `performance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `performance_attendance`
--

DROP TABLE IF EXISTS `performance_attendance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `performance_attendance` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `performance_id` int unsigned NOT NULL,
  `attendee_id` int unsigned NOT NULL,
  `create_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `performance_id_attendee_id_idx` (`performance_id`,`attendee_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `performance_attendance`
--

LOCK TABLES `performance_attendance` WRITE;
/*!40000 ALTER TABLE `performance_attendance` DISABLE KEYS */;
INSERT INTO `performance_attendance` VALUES (1,1,1,'2023-06-20 20:19:06'),(2,2,4,'2023-06-20 20:19:06'),(3,6,1,'2023-06-20 20:19:06');
/*!40000 ALTER TABLE `performance_attendance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `performers`
--

DROP TABLE IF EXISTS `performers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `performers` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `performer_name` varchar(128) NOT NULL,
  `biography` varchar(500) DEFAULT NULL,
  `create_time` datetime NOT NULL,
  `update_time` datetime DEFAULT NULL,
  `uuid` varchar(255) NOT NULL,
  `owner_id` int unsigned DEFAULT NULL,
  `image_url` varchar(512) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uuid_idx` (`uuid`),
  UNIQUE KEY `owner_id_idx` (`owner_id`),
  KEY `performer_name_idx` (`performer_name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `performers`
--

LOCK TABLES `performers` WRITE;
/*!40000 ALTER TABLE `performers` DISABLE KEYS */;
INSERT INTO `performers` VALUES (1,'Taylor Swift','Taylor Alison Swift is an American singer-songwriter. Her narrative songwriting, which often centers around her personal life, has received widespread critical plaudits and media coverage.','2023-06-20 20:19:06',NULL,'06HL4z0CvFAxyc27GXpf02',3,'https://i.scdn.co/image/ab6761610000f1785a00969a4698c3132a15fbb0'),(2,'Eminem','Eminem is an American rapper, songwriter, record producer, record executive, and actor. He is consistently cited as one of the greatest and most influential rappers of all time and was labeled the King of Hip Hop by Rolling Stone magazine.','2023-06-20 20:19:06',NULL,'7dGJo4pcD2V6oG8kP0tJRR',1,'https://i.scdn.co/image/ab6761610000f178a00b11c129b27a88fc72f36b'),(3,'Kendrick Lamar','Kendrick Lamar Duckworth is an American rapper, songwriter, and record producer. Since his debut into the mainstream with Good Kid, M.A.A.D City, Lamar has been regarded as one of the most influential artists of his generation, as well as one of the greatest rappers and lyricists of all time.','2023-06-20 20:19:06',NULL,'2YZyLoL8N0Wb9xBt1NhZWg',5677,'https://i.scdn.co/image/ab6761610000f178437b9e2a82505b3d93ff1022'),(4,'J cole','Jermaine Lamarr Cole, known professionally as J. Cole, is an American rapper, singer, songwriter, record producer, and record executive. Born on a military base in Germany and raised in Fayetteville, North Carolina, Cole initially gained recognition as a rapper following the release of his debut mixtape, The Come Up, in early 2007.','2023-06-20 20:19:10',NULL,'6l3HvQ5sa6mXTsMTB19rO5',46,'https://i.scdn.co/image/ab6761610000f1785a00969a4698c3132a15fbb0');
/*!40000 ALTER TABLE `performers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `post`
--

DROP TABLE IF EXISTS `post`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `post` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `owner_id` int unsigned NOT NULL,
  `owner_type` enum('user','performer') NOT NULL,
  `content` varchar(1000) DEFAULT NULL,
  `creator_id` int unsigned NOT NULL,
  `create_time` datetime NOT NULL,
  `update_time` datetime DEFAULT NULL,
  `note` varchar(1000) DEFAULT NULL,
  `is_deleted` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `post`
--

LOCK TABLES `post` WRITE;
/*!40000 ALTER TABLE `post` DISABLE KEYS */;
INSERT INTO `post` VALUES (1,1,'user','What a great day at Glastonbury!',1,'2023-06-20 20:19:06',NULL,0),(2,3,'user','This is a post which user one will be tagged in',3,'2023-06-20 20:19:06',NULL,0),(3,1,'user','Taylor swifts show was good!',1,'2023-06-20 20:19:06',NULL,0),(4,4,'user','Taylor swifts show at prima was sick!',1,'2023-06-20 20:19:06',NULL,0),(5,4,'user','Cool show mite',1,'2023-06-20 20:19:06',NULL,0),(6,4,'user','Eminems show was good!',4,'2023-06-20 20:19:06',NULL,0),(7,1,'user','Kendrick at o2',1,'2023-06-20 20:19:06',NULL,0),(8,1,'user','Post 0',1,'2023-06-20 20:19:06',NULL,0),(9,1,'user','Post 1',1,'2023-06-20 20:19:06',NULL,0),(10,1,'user','Post 2',1,'2023-06-20 20:19:06',NULL,0),(11,1,'user','Post 3',1,'2023-06-20 20:19:06',NULL,0),(12,1,'user','Post 4',1,'2023-06-20 20:19:06',NULL,0),(13,1,'user','Post 5',1,'2023-06-20 20:19:06',NULL,0),(14,1,'user','Post 6',1,'2023-06-20 20:19:06',NULL,0),(15,1,'user','Post 7',1,'2023-06-20 20:19:06',NULL,0),(16,1,'user','Post 8',1,'2023-06-20 20:19:06',NULL,0),(17,1,'user','Post 9',1,'2023-06-20 20:19:06',NULL,0),(18,1,'user','Post 10',1,'2023-06-20 20:19:06',NULL,0),(19,1,'user','Post 11',1,'2023-06-20 20:19:06',NULL,0),(20,1,'user','Post 12',1,'2023-06-20 20:19:06',NULL,0),(21,1,'user','Post 13',1,'2023-06-20 20:19:06',NULL,0),(22,1,'user','Post 14',1,'2023-06-20 20:19:06',NULL,0),(23,1,'user','Post 15',1,'2023-06-20 20:19:06',NULL,0),(24,1,'user','Post 16',1,'2023-06-20 20:19:06',NULL,0),(25,1,'user','Post 17',1,'2023-06-20 20:19:06',NULL,0),(26,1,'user','Post 18',1,'2023-06-20 20:19:06',NULL,0),(27,1,'user','Post 19',1,'2023-06-20 20:19:06',NULL,0),(28,1,'user','Post 20',1,'2023-06-20 20:19:06',NULL,0),(29,1,'user','Post 21',1,'2023-06-20 20:19:06',NULL,0),(30,1,'user','Post 22',1,'2023-06-20 20:19:06',NULL,0),(31,1,'user','Post 23',1,'2023-06-20 20:19:06',NULL,0),(32,1,'user','Post 24',1,'2023-06-20 20:19:06',NULL,0),(33,1,'user','Post 25',1,'2023-06-20 20:19:06',NULL,0),(34,1,'user','Post 26',1,'2023-06-20 20:19:06',NULL,0);
/*!40000 ALTER TABLE `post` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `post_attachment`
--

DROP TABLE IF EXISTS `post_attachment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `post_attachment` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `file_id` varchar(255) NOT NULL,
  `attachment_thumbnail_file_id` varchar(255) DEFAULT NULL,
  `post_id` int unsigned NOT NULL,
  `create_time` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `post_attachment`
--

LOCK TABLES `post_attachment` WRITE;
/*!40000 ALTER TABLE `post_attachment` DISABLE KEYS */;
INSERT INTO `post_attachment` VALUES (1,'1','2',1,'2023-06-20 20:19:06'),(2,'3','4',2,'2023-06-20 20:19:06'),(3,'5','6',3,'2023-06-20 20:19:06'),(4,'9','10',4,'2023-06-20 20:19:06'),(5,'1','2',5,'2023-06-20 20:19:06'),(6,'1','2',6,'2023-06-20 20:19:06'),(7,'11','13',7,'2023-06-20 20:19:06'),(8,'9','10',8,'2023-06-20 20:19:06'),(9,'3','4',9,'2023-06-20 20:19:06'),(10,'5','6',10,'2023-06-20 20:19:06'),(11,'3','4',11,'2023-06-20 20:19:06'),(12,'5','6',12,'2023-06-20 20:19:06'),(13,'7','8',13,'2023-06-20 20:19:06'),(14,'3','4',14,'2023-06-20 20:19:06'),(15,'1','2',15,'2023-06-20 20:19:06'),(16,'5','6',16,'2023-06-20 20:19:06'),(17,'9','10',17,'2023-06-20 20:19:06'),(18,'9','10',18,'2023-06-20 20:19:06'),(19,'5','6',19,'2023-06-20 20:19:06'),(20,'3','4',20,'2023-06-20 20:19:06'),(21,'7','8',21,'2023-06-20 20:19:06'),(22,'9','10',22,'2023-06-20 20:19:06'),(23,'3','4',23,'2023-06-20 20:19:06'),(24,'3','4',24,'2023-06-20 20:19:06'),(25,'9','10',25,'2023-06-20 20:19:06'),(26,'3','4',26,'2023-06-20 20:19:06'),(27,'5','6',27,'2023-06-20 20:19:06'),(28,'3','4',28,'2023-06-20 20:19:06'),(29,'1','2',29,'2023-06-20 20:19:06'),(30,'3','4',30,'2023-06-20 20:19:06'),(31,'9','10',31,'2023-06-20 20:19:06'),(32,'7','8',32,'2023-06-20 20:19:06'),(33,'5','6',33,'2023-06-20 20:19:06'),(34,'7','8',34,'2023-06-20 20:19:06');
/*!40000 ALTER TABLE `post_attachment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tag`
--

DROP TABLE IF EXISTS `tag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tag` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `tagged_in_entity_type` varchar(60) NOT NULL,
  `tagged_in_entity_id` int unsigned NOT NULL,
  `tagged_entity_type` varchar(60) NOT NULL,
  `tagged_entity_id` int unsigned NOT NULL,
  `creator_id` int unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `tgd_in_ent_type_tgd_in_ent_id_tgd_ent_type_tgd_ent_id` (`tagged_in_entity_type`,`tagged_in_entity_id`,`tagged_entity_type`,`tagged_entity_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tag`
--

LOCK TABLES `tag` WRITE;
/*!40000 ALTER TABLE `tag` DISABLE KEYS */;
INSERT INTO `tag` VALUES (1,'post',3,'performance',1,1),(2,'post',3,'performer',1,1),(3,'post',4,'performance',2,1),(4,'post',4,'performer',1,1),(5,'post',5,'performer',1,1),(6,'post',6,'performer',2,4),(7,'post',7,'performer',3,1),(8,'post',7,'performance',6,1);
/*!40000 ALTER TABLE `tag` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(60) NOT NULL,
  `first_name` varchar(128) DEFAULT NULL,
  `second_name` varchar(128) DEFAULT NULL,
  `full_name` varchar(256) DEFAULT NULL,
  `bio` varchar(150) DEFAULT NULL,
  `create_time` datetime NOT NULL,
  `is_deleted` tinyint(1) NOT NULL DEFAULT '0',
  `email` varchar(100) NOT NULL,
  `last_login_date` datetime NOT NULL,
  `language_id` int unsigned NOT NULL,
  `timezone_id` int unsigned NOT NULL,
  `avatar_file_uuid` varchar(255) DEFAULT NULL,
  `password_hash` varchar(256) NOT NULL,
  `salt` varchar(16) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username_idx` (`username`),
  UNIQUE KEY `email_idx` (`email`),
  KEY `full_name_idx` (`full_name`)
) ENGINE=InnoDB AUTO_INCREMENT=47 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'sean','Sean','Barker','SeanBarker','I love music and live in London','2023-06-20 20:19:04',0,'seanbarker6@sky.com','2023-06-20 20:19:04',1,1,'123456','$argon2id$v=19$m=16384,t=12,p=4$fWAmwGMfA2QcFCK1rq2cPA$Sl4Dn7XIeMEf0r8ATl8iKsc2u8gos2VuS5kz0S2jK+M',NULL),(2,'gregory','Greg','Baxter','GregBaxter',NULL,'2023-06-20 20:19:04',0,'gg_no_re@sky.com','2023-06-20 20:19:04',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$fWAmwGMfA2QcFCK1rq2cPA$Sl4Dn7XIeMEf0r8ATl8iKsc2u8gos2VuS5kz0S2jK+M',NULL),(3,'tim14','Tim','Smith','TimSmith','Mi nem Geoff. Mi like watching people play music and venues and shit','2023-06-20 20:19:04',0,'timsmith@sky.com','2023-06-20 20:19:04',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$FvDbihv7sH1Iylwx2Cw4hw$nuUkersSC3QpIQCGLWDHoYx5C5rekVOOTIKSAn7G4zY',NULL),(4,'seanborker','Sean','Borker','SeanBorker','Reeeeeeeeeeee. Im 28 years old and moved to London 2 years ago. I love music and live in London','2023-06-20 20:19:04',0,'seanborker@sky.com','2023-06-20 20:19:04',1,1,'123456','$argon2id$v=19$m=16384,t=12,p=4$sutqBiw1rjn4Yh2cYtAyxQ$cUuDw6FqSYbZHgrPJCCUu69H0yAMIDV0I1kq3bOVcao',NULL),(5,'newuser','Geoff','Mi Name','GeoffMi Name',NULL,'2023-06-20 20:19:06',0,'newuser@sky.com','2023-06-20 20:19:06',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$Ua/IX4TavDdtoQPg90Khfw$ssoGE826awWApnwvrz7Wq4gDB/JNJCcFg9+v7yAxnNY',NULL),(6,'user0','User 0','Second name is 0','User 0Second name is 0',NULL,'2023-06-20 20:19:06',0,'user0@gmail.com','2023-06-20 20:19:06',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$sbGW277DzveLrPhv3s9JZw$AmYpctMiuMbNuZOjAPgOfWRvJiiaGNEjAk75dMH2iiM',NULL),(7,'user1','User 1','Second name is 1','User 1Second name is 1',NULL,'2023-06-20 20:19:06',0,'user1@gmail.com','2023-06-20 20:19:06',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$mtN68vfKojzCGjbh7GPB2g$dMRp3pyOJzYx68VvTFT+eQaUvw3H88hmEYt8/FSiHyU',NULL),(8,'user2','User 2','Second name is 2','User 2Second name is 2',NULL,'2023-06-20 20:19:06',0,'user2@gmail.com','2023-06-20 20:19:06',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$oSPbqcKaA/Yt7lqENQcT4w$gdU8wTqpVAnLZfbzLjv0BCJ3YuxDzJDToHgZMzkZnko',NULL),(9,'user3','User 3','Second name is 3','User 3Second name is 3',NULL,'2023-06-20 20:19:06',0,'user3@gmail.com','2023-06-20 20:19:06',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$uACJSqa1JAYQMQQBFfffZA$R0poBZXD2H/G5Y5YhVMzG/emKo6uE4c5FqPHKixuBTo',NULL),(10,'user4','User 4','Second name is 4','User 4Second name is 4',NULL,'2023-06-20 20:19:06',0,'user4@gmail.com','2023-06-20 20:19:06',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$t7YKetPBcwxsGFRVo0RLBQ$w/KpVDdWRu7UeJDLXFNilSjYkZ8PZaeKWKhg5rAYeLs',NULL),(11,'user5','User 5','Second name is 5','User 5Second name is 5',NULL,'2023-06-20 20:19:06',0,'user5@gmail.com','2023-06-20 20:19:06',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$RNjzlgBMnKv6KJ/JnNryoQ$C2/EbICINUaSj/Bivr5WbKDehDCzp08/HOtCQJdXxsU',NULL),(12,'user6','User 6','Second name is 6','User 6Second name is 6',NULL,'2023-06-20 20:19:07',0,'user6@gmail.com','2023-06-20 20:19:07',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$CCCcqAeJ15guuauEVRJUZQ$k0gDTfpBgpc+3BObyMtRDmGkCbSVz/2cULOUZVxP4GY',NULL),(13,'user7','User 7','Second name is 7','User 7Second name is 7',NULL,'2023-06-20 20:19:07',0,'user7@gmail.com','2023-06-20 20:19:07',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$MH1MAHx9lYMqywPRoTphYQ$8dm7HvDtlMdYSmnH+i5cFGbCJy9hs7gIt5vyCopDQAE',NULL),(14,'user8','User 8','Second name is 8','User 8Second name is 8',NULL,'2023-06-20 20:19:07',0,'user8@gmail.com','2023-06-20 20:19:07',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$9GAY3MFaZRI8Mgb4ctbuYw$aE09URlUq3cnhg/gNgBx12Snq25DWcoXhaOK0+7wJnE',NULL),(15,'user9','User 9','Second name is 9','User 9Second name is 9',NULL,'2023-06-20 20:19:07',0,'user9@gmail.com','2023-06-20 20:19:07',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$OgEoe22jsd0iCbb2tSpHUA$RhbOkI+/uI7V50WmITAFduEtiWKy4GDZ0DzUnUUVq7g',NULL),(16,'user10','User 10','Second name is 10','User 10Second name is 10',NULL,'2023-06-20 20:19:07',0,'user10@gmail.com','2023-06-20 20:19:07',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$AwpuZJKLjpekfaqZBReyfw$qPBqF4VwC3noxAgEWQpt2epUEO362cBhqgIuHc3PBv8',NULL),(17,'user11','User 11','Second name is 11','User 11Second name is 11',NULL,'2023-06-20 20:19:07',0,'user11@gmail.com','2023-06-20 20:19:07',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$Kbn3QHTGzeHFK0IeXjCJ/A$3J1Xv0ePdpqyKFu8YE6xeKtDQNwY2madVqnf61jCySs',NULL),(18,'user12','User 12','Second name is 12','User 12Second name is 12',NULL,'2023-06-20 20:19:07',0,'user12@gmail.com','2023-06-20 20:19:07',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$gdYCdEnNJcF38719O7BDEg$iJofxgKsPi92Be1aqrlnqsf4U7w+vSgfQwsktKMsACU',NULL),(19,'user13','User 13','Second name is 13','User 13Second name is 13',NULL,'2023-06-20 20:19:07',0,'user13@gmail.com','2023-06-20 20:19:07',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$07I0U9/yOAIO7xW2Ijh2Mw$sypsU1ofGrQiy5L8bdccV0pwfEDicShjm20IpsFqjHY',NULL),(20,'user14','User 14','Second name is 14','User 14Second name is 14',NULL,'2023-06-20 20:19:07',0,'user14@gmail.com','2023-06-20 20:19:07',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$U/wVdG2or3nlgnAJ4lHsDA$MklaXFsTRuUW2ui9+wKXN5cZphPOTtADfof+vUAE4nw',NULL),(21,'user15','User 15','Second name is 15','User 15Second name is 15',NULL,'2023-06-20 20:19:07',0,'user15@gmail.com','2023-06-20 20:19:07',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$ShMWuB39MjNZR5LPWkfQeQ$3/6nlzn3e+NgXLrxW1n1UiIhm1fDWLgaZ+qqUcbVT3k',NULL),(22,'user16','User 16','Second name is 16','User 16Second name is 16',NULL,'2023-06-20 20:19:07',0,'user16@gmail.com','2023-06-20 20:19:07',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$NnPdXLOiUOtbnGZUR5mYlg$FOfZIiWFOmTPn8fQW87i6mQuGCvvoHs5S2KroIDEnQA',NULL),(23,'user17','User 17','Second name is 17','User 17Second name is 17',NULL,'2023-06-20 20:19:08',0,'user17@gmail.com','2023-06-20 20:19:08',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$0JVRwQyHRot5Y+Y9VlJ3Jw$ONp3QwV1TPPoJ/p8Cekm/mzOF+WBU6944Ujfrs8G7co',NULL),(24,'user18','User 18','Second name is 18','User 18Second name is 18',NULL,'2023-06-20 20:19:08',0,'user18@gmail.com','2023-06-20 20:19:08',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$s+t20gYo2EiNj5E0flSGxw$2tq/A2QWVwve88ZFC8LF6jduxfi7fgPlLc1k1l0xcf8',NULL),(25,'user19','User 19','Second name is 19','User 19Second name is 19',NULL,'2023-06-20 20:19:08',0,'user19@gmail.com','2023-06-20 20:19:08',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$B06PqqvnfvUA0FD4tfT6Hw$/1hiAVlOW6MxYtzTPFY9Y8HDjgRY3I2vgHKm5AvUfKE',NULL),(26,'user20','User 20','Second name is 20','User 20Second name is 20',NULL,'2023-06-20 20:19:08',0,'user20@gmail.com','2023-06-20 20:19:08',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$3LKTfVk3VLs68VE57nZAKQ$tiJ9t8oVSGugh46utPIjVEDPFwbmj2tXMwGK0Zthqno',NULL),(27,'user21','User 21','Second name is 21','User 21Second name is 21',NULL,'2023-06-20 20:19:08',0,'user21@gmail.com','2023-06-20 20:19:08',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$NiwGLn8O2k3v/H7rkgdyew$GckKLss5ik0T+a4vS79FRoZJN6R25w/3ufW44mwd6Fs',NULL),(28,'user22','User 22','Second name is 22','User 22Second name is 22',NULL,'2023-06-20 20:19:08',0,'user22@gmail.com','2023-06-20 20:19:08',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$QoWPw7Xsnwp7qF40wiWzlw$fb7i0UVFmRmVfUrZEnTwrDfpwYpeXBspIAj2Adt0KcU',NULL),(29,'user23','User 23','Second name is 23','User 23Second name is 23',NULL,'2023-06-20 20:19:08',0,'user23@gmail.com','2023-06-20 20:19:08',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$d9LZXUNsQznvibVLV0jiBw$+MtqpGXgkhUJZCbOatI0rPmfNvndrSlv+KodaoLeJ8s',NULL),(30,'user24','User 24','Second name is 24','User 24Second name is 24',NULL,'2023-06-20 20:19:08',0,'user24@gmail.com','2023-06-20 20:19:08',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$RRAa6Mrcju3rKiURjjSABg$Er5NLa22Oe7UweHPT5J2QxB4GanGCuaprrOxRL8YgtA',NULL),(31,'user25','User 25','Second name is 25','User 25Second name is 25',NULL,'2023-06-20 20:19:08',0,'user25@gmail.com','2023-06-20 20:19:08',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$GKLX2g0lj788MQQoC74BoA$Lyvne40LlSw1cZli5yAPlkmr/9/+9suXJumqiAgKw3I',NULL),(32,'user26','User 26','Second name is 26','User 26Second name is 26',NULL,'2023-06-20 20:19:08',0,'user26@gmail.com','2023-06-20 20:19:08',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$5CTIIok+9pHmArQXtclHVQ$EhCL0ygxQ16ON+MG2qSfbbdAOvGxSsI45lYEyga7jC0',NULL),(33,'user27','User 27','Second name is 27','User 27Second name is 27',NULL,'2023-06-20 20:19:08',0,'user27@gmail.com','2023-06-20 20:19:08',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$Jdvi3MJr1BZTcfQKgGLjmA$tX1I1VzOr8xFqpKrA2GcF7XSz/1lKoM4Oiz58SwyVoo',NULL),(34,'user28','User 28','Second name is 28','User 28Second name is 28',NULL,'2023-06-20 20:19:08',0,'user28@gmail.com','2023-06-20 20:19:08',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$aaTzrNNMPOu6EKPKOSJfRA$DzJKn24aR0V7RPdlR6YMCLT4Etss680bZEFAeO0OME0',NULL),(35,'user29','User 29','Second name is 29','User 29Second name is 29',NULL,'2023-06-20 20:19:09',0,'user29@gmail.com','2023-06-20 20:19:09',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$3DTQ8/yfRGR97DB6+9JmUg$qNWbXxUUyFcIwtHj/jMG7r25AgIFzXYX5aZiC6jhwd4',NULL),(36,'user30','User 30','Second name is 30','User 30Second name is 30',NULL,'2023-06-20 20:19:09',0,'user30@gmail.com','2023-06-20 20:19:09',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$qgrKvMNzhjeXExEWidQ5Bg$svRU855EJa+ARrFNG5uMzjDE+Yje8a3Q0LUZLRG3zyY',NULL),(37,'user31','User 31','Second name is 31','User 31Second name is 31',NULL,'2023-06-20 20:19:09',0,'user31@gmail.com','2023-06-20 20:19:09',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$Uc+5qQYSiR3gYy+9nruxQA$6jSSHs32JoMkYyYXnn4YgrS6UzyukvcYZCE/U+Sg/i0',NULL),(38,'user32','User 32','Second name is 32','User 32Second name is 32',NULL,'2023-06-20 20:19:09',0,'user32@gmail.com','2023-06-20 20:19:09',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$UqGHI3fXdNpDaL1KrdWOVg$7J87OQ2DqsoUh2LXgyhDYG/DcfFLaiwRCBbVEq+0Wdw',NULL),(39,'user33','User 33','Second name is 33','User 33Second name is 33',NULL,'2023-06-20 20:19:09',0,'user33@gmail.com','2023-06-20 20:19:09',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$1dvun81gxGNoKQEdahg+cA$eeQrAOClCp6lTDX/8PGoeFCAocR+Krg605u36ZkdRWg',NULL),(40,'user34','User 34','Second name is 34','User 34Second name is 34',NULL,'2023-06-20 20:19:09',0,'user34@gmail.com','2023-06-20 20:19:09',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$aKiKWccRF7UxCVm93kIr3g$IOijtbb1pmgYbmPZ1Hb/KAA5EsBNtb/O1XqWoz5YEow',NULL),(41,'user35','User 35','Second name is 35','User 35Second name is 35',NULL,'2023-06-20 20:19:09',0,'user35@gmail.com','2023-06-20 20:19:09',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$x6eVX+Hsv4w6qlnJsyAPew$pY9iw3D8EUrFwh/GC3pDxrt7NBBNxAbl5nmLmfc4bDQ',NULL),(42,'user36','User 36','Second name is 36','User 36Second name is 36',NULL,'2023-06-20 20:19:09',0,'user36@gmail.com','2023-06-20 20:19:09',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$MeX+YUXf5mi+LvpRa1oUUQ$oX9agdXLn7aklWcxmW0I06BrgOCdpXdtMoKcBnRXb24',NULL),(43,'user37','User 37','Second name is 37','User 37Second name is 37',NULL,'2023-06-20 20:19:09',0,'user37@gmail.com','2023-06-20 20:19:09',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$bca7hq7vBOrnTyAEXPtgig$cyGYLwkq3W3zxFh4RjAZB9huMP0LeTN4i03gc1nK5uA',NULL),(44,'user38','User 38','Second name is 38','User 38Second name is 38',NULL,'2023-06-20 20:19:09',0,'user38@gmail.com','2023-06-20 20:19:09',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$ZKGYonGKsvpj2wJKyetLfA$hKj8++hlzV1ljWZXi2OGTBk/uOMCm+O/mJNiMhIhtiQ',NULL),(45,'user39','User 39','Second name is 39','User 39Second name is 39',NULL,'2023-06-20 20:19:09',0,'user39@gmail.com','2023-06-20 20:19:09',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$4Pz40QDjgoy/j2Hq3TbxEg$IYjpzihlK7r3/nMSVUA0HiFie/9S8/awmme60TYzCnk',NULL),(46,'emptystateuser','Empty','State','EmptyState',NULL,'2023-06-20 20:19:10',0,'emptystateuser@gmail.com','2023-06-20 20:19:10',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$lumt/BeYSRvZpeFiy0Wv1w$VUJ7xnd+iRzngvTKiplzyQqrW7wNdcSPDzSYgZmwv10',NULL);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-06-20 20:38:59
