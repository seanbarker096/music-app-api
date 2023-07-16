-- Dump completed on 2023-06-20 20:38:59
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

USE gigs;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_tokens`
--

LOCK TABLES `auth_tokens` WRITE;
/*!40000 ALTER TABLE `auth_tokens` DISABLE KEYS */;
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
INSERT INTO `event` VALUES (1,'Glastonbury','Glastonbury','2023-04-15','2023-04-16','music_festival','2023-07-16 12:05:50',NULL),(2,'O2 Academy Brixton','O2 Academy Brixton','2023-04-17','2023-04-18','music_concert','2023-07-16 12:05:50',NULL),(3,'Primavera Sound','Primavera Sound','2023-04-17','2023-04-18','music_festival','2023-07-16 12:05:50',NULL);
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
INSERT INTO `files` VALUES (1,'show1','show1.mp4',NULL,'video/mp4','https://fileservice-bucket-post.s3.amazonaws.com/show1?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAR56DCSXK3Z75BQB2%2F20230716%2Fus-east-2%2Fs3%2Faws4_request&X-Amz-Date=20230716T120526Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=55293f30ec91eb69eb5ae9330681aa9f38b21d2ef7a3d924729c06d7af2858a7'),(2,'show1thumbnail','show1-thumbnail.png',NULL,'img/png','https://fileservice-bucket-post.s3.amazonaws.com/show1thumbnail?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAR56DCSXK3Z75BQB2%2F20230716%2Fus-east-2%2Fs3%2Faws4_request&X-Amz-Date=20230716T120527Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=7098f75ead964ed3f4d33d9f1f10cc0364603cd1073a5468ff894108e39315d4'),(3,'show2','show2.mp4',NULL,'video/mp4','https://fileservice-bucket-post.s3.amazonaws.com/show2?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAR56DCSXK3Z75BQB2%2F20230716%2Fus-east-2%2Fs3%2Faws4_request&X-Amz-Date=20230716T120530Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=4afe889dada9aadf17ec89ef1d2ae2d1f531e48c9c5d7d3b138a03826df9d45a'),(4,'show2thumbnail','show2-thumbnail.png',NULL,'img/png','https://fileservice-bucket-post.s3.amazonaws.com/show2thumbnail?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAR56DCSXK3Z75BQB2%2F20230716%2Fus-east-2%2Fs3%2Faws4_request&X-Amz-Date=20230716T120531Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=ce2a5328d8c9c377b1432573d0ef844d4be5839ba31c2e44c4a3eaf7857160e3'),(5,'show3','show3.mp4',NULL,'video/mp4','https://fileservice-bucket-post.s3.amazonaws.com/show3?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAR56DCSXK3Z75BQB2%2F20230716%2Fus-east-2%2Fs3%2Faws4_request&X-Amz-Date=20230716T120536Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=3b3bbace9973b1139ac69247ad1b0607452dd6c88d195a25c727ac9bca873017'),(6,'show3thumbnail','show3-thumbnail.png',NULL,'img/png','https://fileservice-bucket-post.s3.amazonaws.com/show3thumbnail?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAR56DCSXK3Z75BQB2%2F20230716%2Fus-east-2%2Fs3%2Faws4_request&X-Amz-Date=20230716T120537Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=3665b44e2bd6056e1ff4feff3fe2439b2f3b9e51f325a7d0877436e67058a448'),(7,'show4','show4.mp4',NULL,'video/mp4','https://fileservice-bucket-post.s3.amazonaws.com/show4?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAR56DCSXK3Z75BQB2%2F20230716%2Fus-east-2%2Fs3%2Faws4_request&X-Amz-Date=20230716T120540Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=f7f1eadad139c62c9e9e54d61655025cb73397af212e200a92747655f4efd2cf'),(8,'show4thumbnail','show4-thumbnail.png',NULL,'img/png','https://fileservice-bucket-post.s3.amazonaws.com/show4thumbnail?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAR56DCSXK3Z75BQB2%2F20230716%2Fus-east-2%2Fs3%2Faws4_request&X-Amz-Date=20230716T120542Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=cb7e6d7720cc5396d909255aaa3501470b68f494c5cb1c1f3fd8a9d5312b76cf'),(9,'show5','show5.mp4',NULL,'video/mp4','https://fileservice-bucket-post.s3.amazonaws.com/show5?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAR56DCSXK3Z75BQB2%2F20230716%2Fus-east-2%2Fs3%2Faws4_request&X-Amz-Date=20230716T120544Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=35e9508c772073a3440b6bc68f405834be5b9bd287b02cdd81d4c8a500e6c2f0'),(10,'show5thumbnail','show5-thumbnail.png',NULL,'img/png','https://fileservice-bucket-post.s3.amazonaws.com/show5thumbnail?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAR56DCSXK3Z75BQB2%2F20230716%2Fus-east-2%2Fs3%2Faws4_request&X-Amz-Date=20230716T120545Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=944bebb1d599c43b7e9433b3a85b1b5fdbad41b24876cffff537d5d779d84158'),(11,'202','dog.mp4',NULL,'video/mp4','https://fileservice-bucket-post.s3.amazonaws.com/202?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAR56DCSXK3Z75BQB2%2F20230716%2Fus-east-2%2Fs3%2Faws4_request&X-Amz-Date=20230716T120549Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=68bbe0cc58126ad3fb58247f8ffc13ea7cc7c424355c0b1765405349cf1a3bea'),(12,'123456','profile-pic.jpg',NULL,'image/jpeg','https://fileservice-bucket-post.s3.amazonaws.com/123456?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAR56DCSXK3Z75BQB2%2F20230716%2Fus-east-2%2Fs3%2Faws4_request&X-Amz-Date=20230716T120550Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=f948506fa40f72f4e0f9e4860dcddbd701bed40f2da44f85edb7792aedbfcec4'),(13,'aaaaaaaaaaaaaaa','profile-pic2.jpg',NULL,'image/jpeg','https://fileservice-bucket-post.s3.amazonaws.com/aaaaaaaaaaaaaaa?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAR56DCSXK3Z75BQB2%2F20230716%2Fus-east-2%2Fs3%2Faws4_request&X-Amz-Date=20230716T120551Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=81478d6f65cc8d9ba9549e61983f261d97f84b8f9bdef0068336c6e282e5cade');
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
INSERT INTO `performance` VALUES (1,1,1,'2023-07-16','2023-07-16 12:05:51',NULL),(2,3,1,'2023-07-16','2023-07-16 12:05:52',NULL),(3,2,1,'2023-07-18','2023-07-16 12:05:52',NULL),(4,1,1,'2023-07-21','2023-07-16 12:05:52',NULL),(5,2,1,'2023-07-21','2023-07-16 12:05:52',NULL),(6,2,3,'2023-07-24','2023-07-16 12:05:52',NULL);
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
INSERT INTO `performance_attendance` VALUES (1,1,1,'2023-07-16 12:05:52'),(2,2,4,'2023-07-16 12:05:52'),(3,6,1,'2023-07-16 12:05:52');
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
INSERT INTO `performers` VALUES (1,'Taylor Swift','Taylor Alison Swift is an American singer-songwriter. Her narrative songwriting, which often centers around her personal life, has received widespread critical plaudits and media coverage.','2023-07-16 12:05:51',NULL,'06HL4z0CvFAxyc27GXpf02',3,'https://i.scdn.co/image/ab6761610000f1785a00969a4698c3132a15fbb0'),(2,'Eminem','Eminem is an American rapper, songwriter, record producer, record executive, and actor. He is consistently cited as one of the greatest and most influential rappers of all time and was labeled the King of Hip Hop by Rolling Stone magazine.','2023-07-16 12:05:52',NULL,'7dGJo4pcD2V6oG8kP0tJRR',1,'https://i.scdn.co/image/ab6761610000f178a00b11c129b27a88fc72f36b'),(3,'Kendrick Lamar','Kendrick Lamar Duckworth is an American rapper, songwriter, and record producer. Since his debut into the mainstream with Good Kid, M.A.A.D City, Lamar has been regarded as one of the most influential artists of his generation, as well as one of the greatest rappers and lyricists of all time.','2023-07-16 12:05:52',NULL,'2YZyLoL8N0Wb9xBt1NhZWg',5677,'https://i.scdn.co/image/ab6761610000f178437b9e2a82505b3d93ff1022'),(4,'J cole','Jermaine Lamarr Cole, known professionally as J. Cole, is an American rapper, singer, songwriter, record producer, and record executive. Born on a military base in Germany and raised in Fayetteville, North Carolina, Cole initially gained recognition as a rapper following the release of his debut mixtape, The Come Up, in early 2007.','2023-07-16 12:05:56',NULL,'6l3HvQ5sa6mXTsMTB19rO5',46,'https://i.scdn.co/image/ab6761610000f1785a00969a4698c3132a15fbb0');
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
INSERT INTO `post` VALUES (1,1,'user','What a great day at Glastonbury!',1,'2023-07-16 12:05:51',NULL,NULL,0),(2,3,'user','This is a post which user one will be tagged in',3,'2023-07-16 12:05:51',NULL,NULL,0),(3,1,'user','Taylor swifts show was good!',1,'2023-07-16 12:05:52',NULL,NULL,0),(4,4,'user','Taylor swifts show at prima was sick!',1,'2023-07-16 12:05:52',NULL,NULL,0),(5,4,'user','Cool show mite',1,'2023-07-16 12:05:52',NULL,NULL,0),(6,4,'user','Eminems show was good!',4,'2023-07-16 12:05:52',NULL,NULL,0),(7,1,'user','Kendrick at o2',1,'2023-07-16 12:05:52',NULL,NULL,0),(8,1,'user','Post 0',1,'2023-07-16 12:05:52',NULL,NULL,0),(9,1,'user','Post 1',1,'2023-07-16 12:05:52',NULL,NULL,0),(10,1,'user','Post 2',1,'2023-07-16 12:05:52',NULL,NULL,0),(11,1,'user','Post 3',1,'2023-07-16 12:05:52',NULL,NULL,0),(12,1,'user','Post 4',1,'2023-07-16 12:05:52',NULL,NULL,0),(13,1,'user','Post 5',1,'2023-07-16 12:05:52',NULL,NULL,0),(14,1,'user','Post 6',1,'2023-07-16 12:05:52',NULL,NULL,0),(15,1,'user','Post 7',1,'2023-07-16 12:05:52',NULL,NULL,0),(16,1,'user','Post 8',1,'2023-07-16 12:05:52',NULL,NULL,0),(17,1,'user','Post 9',1,'2023-07-16 12:05:52',NULL,NULL,0),(18,1,'user','Post 10',1,'2023-07-16 12:05:52',NULL,NULL,0),(19,1,'user','Post 11',1,'2023-07-16 12:05:52',NULL,NULL,0),(20,1,'user','Post 12',1,'2023-07-16 12:05:52',NULL,NULL,0),(21,1,'user','Post 13',1,'2023-07-16 12:05:52',NULL,NULL,0),(22,1,'user','Post 14',1,'2023-07-16 12:05:52',NULL,NULL,0),(23,1,'user','Post 15',1,'2023-07-16 12:05:52',NULL,NULL,0),(24,1,'user','Post 16',1,'2023-07-16 12:05:52',NULL,NULL,0),(25,1,'user','Post 17',1,'2023-07-16 12:05:52',NULL,NULL,0),(26,1,'user','Post 18',1,'2023-07-16 12:05:52',NULL,NULL,0),(27,1,'user','Post 19',1,'2023-07-16 12:05:52',NULL,NULL,0),(28,1,'user','Post 20',1,'2023-07-16 12:05:52',NULL,NULL,0),(29,1,'user','Post 21',1,'2023-07-16 12:05:52',NULL,NULL,0),(30,1,'user','Post 22',1,'2023-07-16 12:05:52',NULL,NULL,0),(31,1,'user','Post 23',1,'2023-07-16 12:05:52',NULL,NULL,0),(32,1,'user','Post 24',1,'2023-07-16 12:05:52',NULL,NULL,0),(33,1,'user','Post 25',1,'2023-07-16 12:05:52',NULL,NULL,0),(34,1,'user','Post 26',1,'2023-07-16 12:05:52',NULL,NULL,0);
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
INSERT INTO `post_attachment` VALUES (1,'1','2',1,'2023-07-16 12:05:51'),(2,'3','4',2,'2023-07-16 12:05:51'),(3,'5','6',3,'2023-07-16 12:05:52'),(4,'9','10',4,'2023-07-16 12:05:52'),(5,'1','2',5,'2023-07-16 12:05:52'),(6,'1','2',6,'2023-07-16 12:05:52'),(7,'11','13',7,'2023-07-16 12:05:52'),(8,'5','6',8,'2023-07-16 12:05:52'),(9,'9','10',9,'2023-07-16 12:05:52'),(10,'9','10',10,'2023-07-16 12:05:52'),(11,'5','6',11,'2023-07-16 12:05:52'),(12,'1','2',12,'2023-07-16 12:05:52'),(13,'5','6',13,'2023-07-16 12:05:52'),(14,'1','2',14,'2023-07-16 12:05:52'),(15,'5','6',15,'2023-07-16 12:05:52'),(16,'7','8',16,'2023-07-16 12:05:52'),(17,'5','6',17,'2023-07-16 12:05:52'),(18,'5','6',18,'2023-07-16 12:05:52'),(19,'9','10',19,'2023-07-16 12:05:52'),(20,'5','6',20,'2023-07-16 12:05:52'),(21,'3','4',21,'2023-07-16 12:05:52'),(22,'9','10',22,'2023-07-16 12:05:52'),(23,'1','2',23,'2023-07-16 12:05:52'),(24,'9','10',24,'2023-07-16 12:05:52'),(25,'3','4',25,'2023-07-16 12:05:52'),(26,'9','10',26,'2023-07-16 12:05:52'),(27,'1','2',27,'2023-07-16 12:05:52'),(28,'5','6',28,'2023-07-16 12:05:52'),(29,'9','10',29,'2023-07-16 12:05:52'),(30,'9','10',30,'2023-07-16 12:05:52'),(31,'1','2',31,'2023-07-16 12:05:52'),(32,'7','8',32,'2023-07-16 12:05:52'),(33,'3','4',33,'2023-07-16 12:05:52'),(34,'3','4',34,'2023-07-16 12:05:52');
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
INSERT INTO `users` VALUES (1,'sean','Sean','Barker','SeanBarker','I love music and live in London','2023-07-16 12:05:50',0,'seanbarker6@sky.com','2023-07-16 12:05:50',1,1,'123456','$argon2id$v=19$m=16384,t=12,p=4$+8PeqdyIRDg+nhziDgL9RA$dDjMIOw/l0a/UkhL2+gbN1Tth6KlIR12WnsHsV/9xQA',NULL),(2,'gregory','Greg','Baxter','GregBaxter',NULL,'2023-07-16 12:05:50',0,'gg_no_re@sky.com','2023-07-16 12:05:50',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$+8PeqdyIRDg+nhziDgL9RA$dDjMIOw/l0a/UkhL2+gbN1Tth6KlIR12WnsHsV/9xQA',NULL),(3,'tim14','Tim','Smith','TimSmith','Mi nem Geoff. Mi like watching people play music and venues and shit','2023-07-16 12:05:50',0,'timsmith@sky.com','2023-07-16 12:05:50',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$41MxGS+z89jFRSwBNyAsfQ$Ak4MwslWdm7hJrKpX0OnDXjES08oI1PmFPLvStX/FdE',NULL),(4,'seanborker','Sean','Borker','SeanBorker','Reeeeeeeeeeee. Im 28 years old and moved to London 2 years ago. I love music and live in London','2023-07-16 12:05:50',0,'seanborker@sky.com','2023-07-16 12:05:50',1,1,'123456','$argon2id$v=19$m=16384,t=12,p=4$vTMZNqAi4MDjoShwxBC/8g$z9JIOW/se8k9jhj+1F/W8dmoca0y0AQNZH3i8zhkTfg',NULL),(5,'newuser','Geoff','Mi Name','GeoffMi Name',NULL,'2023-07-16 12:05:52',0,'newuser@sky.com','2023-07-16 12:05:52',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$dT7TxwmUHPFm/HL2xTbXRA$FNz0b3L6hffAOx4rGc9dC1bNTftOEy3BwRoHT7ssBak',NULL),(6,'user0','User 0','Second name is 0','User 0Second name is 0',NULL,'2023-07-16 12:05:52',0,'user0@gmail.com','2023-07-16 12:05:52',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$X5l9xtLOg/Oi4S1Vbz+Z1w$08HISPk0r6LnqJ9Wm44vKZhIv28YKdfP//4lNSm4wIY',NULL),(7,'user1','User 1','Second name is 1','User 1Second name is 1',NULL,'2023-07-16 12:05:52',0,'user1@gmail.com','2023-07-16 12:05:52',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$+ipQBrVG7J5DPv1FK4q9PA$RzQJgw5cSqfoQNjUfX8vt1eW4QArO2KsNNF9IQmcCcU',NULL),(8,'user2','User 2','Second name is 2','User 2Second name is 2',NULL,'2023-07-16 12:05:52',0,'user2@gmail.com','2023-07-16 12:05:52',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$o5nf9opiKeYH/9W6zuryjA$ys6YUdLwvkrlq6pnnktiZ9ZPZvLcLCasKnZFA7eZfTQ',NULL),(9,'user3','User 3','Second name is 3','User 3Second name is 3',NULL,'2023-07-16 12:05:52',0,'user3@gmail.com','2023-07-16 12:05:52',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$UpoE1v5q05nqSfDF890EVA$YYkv3IlPBShyS5Yo7yl02bq/xlFw0IMZzhnZjNhzF2A',NULL),(10,'user4','User 4','Second name is 4','User 4Second name is 4',NULL,'2023-07-16 12:05:52',0,'user4@gmail.com','2023-07-16 12:05:52',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$2eKV8Gkbd39Iyo9kJkmLZg$cM2S7p8daOWpqaG8hs0k9kYX7vviBV1zMTEQrRoYbSI',NULL),(11,'user5','User 5','Second name is 5','User 5Second name is 5',NULL,'2023-07-16 12:05:52',0,'user5@gmail.com','2023-07-16 12:05:52',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$P0DZLDY7w06aoQybyWQUAw$k/adCso5YmuL+rGTDXRFz/Jn5jHmeqXbVj0pxGXwgdU',NULL),(12,'user6','User 6','Second name is 6','User 6Second name is 6',NULL,'2023-07-16 12:05:53',0,'user6@gmail.com','2023-07-16 12:05:53',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$jOkZUff5oRzbWWvO5rpzxw$7SEcR8sa7n3xy8yLC++1+GlvIqWe6/XzKjsHFsjx90M',NULL),(13,'user7','User 7','Second name is 7','User 7Second name is 7',NULL,'2023-07-16 12:05:53',0,'user7@gmail.com','2023-07-16 12:05:53',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$mSmIfpI9ZhGzJ5jBlf3Oug$JfDunewGQBhN2svTJavktxupSsjzBMX57+145Z9a4Zs',NULL),(14,'user8','User 8','Second name is 8','User 8Second name is 8',NULL,'2023-07-16 12:05:53',0,'user8@gmail.com','2023-07-16 12:05:53',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$DE6MAPfvWTQiSSYdRg90wA$8tRk3lBg5jlfuk0mgpT98AdlAbIh84bQkFH7gAm8sl0',NULL),(15,'user9','User 9','Second name is 9','User 9Second name is 9',NULL,'2023-07-16 12:05:53',0,'user9@gmail.com','2023-07-16 12:05:53',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$xF2Km1uJhwJfseZu7YzYmw$9fvD3rSMPJxCkRtHtLcRZr1zdcYpXBnLq00rp0ZBX/k',NULL),(16,'user10','User 10','Second name is 10','User 10Second name is 10',NULL,'2023-07-16 12:05:53',0,'user10@gmail.com','2023-07-16 12:05:53',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$7rIhVJ/TA1XTmB57rC60RA$g/RcbOUKlSVfIMcOzsTSdy+1SXBJIgimWg94d8WYZfQ',NULL),(17,'user11','User 11','Second name is 11','User 11Second name is 11',NULL,'2023-07-16 12:05:53',0,'user11@gmail.com','2023-07-16 12:05:53',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$Il/MPvPYrzUn4eaLUnqzRg$Jd9eDdVf9qFyicO8zilUauqduHnT/5JP7U4hhL7vkI0',NULL),(18,'user12','User 12','Second name is 12','User 12Second name is 12',NULL,'2023-07-16 12:05:53',0,'user12@gmail.com','2023-07-16 12:05:53',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$18FbTLLyp00Vw/270cN2dw$IbOtwz29mWr4c89U5cuWUWCe2klykpusxJYz1CxKXd4',NULL),(19,'user13','User 13','Second name is 13','User 13Second name is 13',NULL,'2023-07-16 12:05:53',0,'user13@gmail.com','2023-07-16 12:05:53',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$KtBXjybIwvga3LCbLL2xPw$pk8gSK52vHclz2kUeyoOwhLif2s3zEZ9VuBfjqLT+Lc',NULL),(20,'user14','User 14','Second name is 14','User 14Second name is 14',NULL,'2023-07-16 12:05:53',0,'user14@gmail.com','2023-07-16 12:05:53',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$4N8VZ866+97pnuINHHC5bg$1oeZGglTDufCpwQ9eYrtG1EvfGzLELfQugUPoWsEfqM',NULL),(21,'user15','User 15','Second name is 15','User 15Second name is 15',NULL,'2023-07-16 12:05:53',0,'user15@gmail.com','2023-07-16 12:05:53',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$k8hsCHBMPf+BfC4L+aoWhw$hQK6u5zN3Kpca9npambBpjfsidVe2L0X58jdQ17dB2M',NULL),(22,'user16','User 16','Second name is 16','User 16Second name is 16',NULL,'2023-07-16 12:05:53',0,'user16@gmail.com','2023-07-16 12:05:53',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$QzBCOiXqo5ceSbdMPMjkoA$Kymoquw7Oq8TcN+ZI7Uq42tGNCXfWDcJNQh/TUfl6L4',NULL),(23,'user17','User 17','Second name is 17','User 17Second name is 17',NULL,'2023-07-16 12:05:54',0,'user17@gmail.com','2023-07-16 12:05:54',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$a6J+qCBkf6Y08K8Uq/TzMA$FtVPV14hLB+dgjvIwVhtyiJ69668AG6XXY7ghvIhFBA',NULL),(24,'user18','User 18','Second name is 18','User 18Second name is 18',NULL,'2023-07-16 12:05:54',0,'user18@gmail.com','2023-07-16 12:05:54',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$gqrtGtXbR5yFkTH8cH41kA$l+PyvvVMMV6egI7FpAvXDflmaCkmeD1tAapGLHWDdXk',NULL),(25,'user19','User 19','Second name is 19','User 19Second name is 19',NULL,'2023-07-16 12:05:54',0,'user19@gmail.com','2023-07-16 12:05:54',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$zA8IMbHF7AFOgbq8lNSXRA$p/WrVngK0u21k6WB2gTJTb9G7k0XoOy886IEBKzTxxw',NULL),(26,'user20','User 20','Second name is 20','User 20Second name is 20',NULL,'2023-07-16 12:05:54',0,'user20@gmail.com','2023-07-16 12:05:54',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$5xkksMpFMVJQVRX9sXxOoA$uH5Qjb/HEx0sdS8uec/IZHJx+AeZefJ0BpNVGkyAsrY',NULL),(27,'user21','User 21','Second name is 21','User 21Second name is 21',NULL,'2023-07-16 12:05:54',0,'user21@gmail.com','2023-07-16 12:05:54',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$D+qnY3vk/q9xPpRfjiMYCA$GeLvFowAOC4jKXVNpW2DT3BDnY/ql+DzRxlrOjdrNko',NULL),(28,'user22','User 22','Second name is 22','User 22Second name is 22',NULL,'2023-07-16 12:05:54',0,'user22@gmail.com','2023-07-16 12:05:54',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$iho2hq3nwICd/V0hwVFmJw$fP9eIRPlKp8aVHU2C7PM8V/Q7g+MKEs42Wl//1SzecQ',NULL),(29,'user23','User 23','Second name is 23','User 23Second name is 23',NULL,'2023-07-16 12:05:54',0,'user23@gmail.com','2023-07-16 12:05:54',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$z6djwFut2c4uewBOnUERcw$gON6aTjdsIXlE2XbDqcNbuKGYMWtNGiDFJBpVbVLPWY',NULL),(30,'user24','User 24','Second name is 24','User 24Second name is 24',NULL,'2023-07-16 12:05:54',0,'user24@gmail.com','2023-07-16 12:05:54',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$ZF+DMyVMDoUIrs9zKVoVFw$o0UdYz5q0zC7LmRUm6JeL7CwjV91/vGfKl5JCUL6/1Y',NULL),(31,'user25','User 25','Second name is 25','User 25Second name is 25',NULL,'2023-07-16 12:05:54',0,'user25@gmail.com','2023-07-16 12:05:54',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$+x2/mcIMNaf8rSVVvnIJ2w$eaxERiTCrU6bo5lqBTxzCRKt+cSGYq6auwrTs2FZQ/Q',NULL),(32,'user26','User 26','Second name is 26','User 26Second name is 26',NULL,'2023-07-16 12:05:54',0,'user26@gmail.com','2023-07-16 12:05:54',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$j3GRTk6GiRFa/7GWbY9Wwg$vUP49KdAT4Uskk4MiYasW9adUrgonG3mPdj6SuM8qpo',NULL),(33,'user27','User 27','Second name is 27','User 27Second name is 27',NULL,'2023-07-16 12:05:54',0,'user27@gmail.com','2023-07-16 12:05:54',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$xyos2axxgeMSps6h/PAEiQ$eaABwOHR9KUDQ37Ay5Smvox/r8yW8xczCwhrAdxbM6E',NULL),(34,'user28','User 28','Second name is 28','User 28Second name is 28',NULL,'2023-07-16 12:05:55',0,'user28@gmail.com','2023-07-16 12:05:55',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$JxnV8IJsJWZ99qckuUuxpg$w5kx5bwiB06KxaL77M0KnzOdLTdWPAhH3WHVjgLNi6I',NULL),(35,'user29','User 29','Second name is 29','User 29Second name is 29',NULL,'2023-07-16 12:05:55',0,'user29@gmail.com','2023-07-16 12:05:55',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$QmIg7eCmUbQvYZpv1P72lQ$X3E7ASfo3fXr5egW9g8yEx6szPwnWFywunQ1V8ubIFA',NULL),(36,'user30','User 30','Second name is 30','User 30Second name is 30',NULL,'2023-07-16 12:05:55',0,'user30@gmail.com','2023-07-16 12:05:55',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$rWKkV6YvmgYBd96IwQAU4g$KB+zU/3MRIKHkpTrm6swfN5P4mTA2sBAazgRuEo3kzM',NULL),(37,'user31','User 31','Second name is 31','User 31Second name is 31',NULL,'2023-07-16 12:05:55',0,'user31@gmail.com','2023-07-16 12:05:55',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$peImo/WqUNL9BEU0D7TQiA$DB3nNGcc6utEj8f4qTsIL6bNYb3B0fFvt7hx3u6a1uA',NULL),(38,'user32','User 32','Second name is 32','User 32Second name is 32',NULL,'2023-07-16 12:05:55',0,'user32@gmail.com','2023-07-16 12:05:55',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$M4ofFgUxyB5j7dL17otOmw$atlEWwwsCEGiJLB5trJg3a1ZvdNcxchG+Rysq2apEW0',NULL),(39,'user33','User 33','Second name is 33','User 33Second name is 33',NULL,'2023-07-16 12:05:55',0,'user33@gmail.com','2023-07-16 12:05:55',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$v1d64zBxEPagGyGGFEGHow$eQlnUxkCDEubefas8n4NjD3Z1XmcEd3OjZd3hSS4+vk',NULL),(40,'user34','User 34','Second name is 34','User 34Second name is 34',NULL,'2023-07-16 12:05:55',0,'user34@gmail.com','2023-07-16 12:05:55',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$dxa2pqDEkLFiTU0cE+iAVA$BvX4TwbhHko6oRRQRkLtW2/yZnKOWI0aHuRI8BuiAqQ',NULL),(41,'user35','User 35','Second name is 35','User 35Second name is 35',NULL,'2023-07-16 12:05:55',0,'user35@gmail.com','2023-07-16 12:05:55',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$jEEXWV54XImtoJF+vworMA$iCJeSDOugW818FnhXQqoSGgqecjSndOxtwE/0sdVWaE',NULL),(42,'user36','User 36','Second name is 36','User 36Second name is 36',NULL,'2023-07-16 12:05:55',0,'user36@gmail.com','2023-07-16 12:05:55',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$DkKrqRRlNKoCAfngeKGTeg$rRnYu4tlFwA9b2mDugvY+vX5X4MMb7q06b5kK6aMTts',NULL),(43,'user37','User 37','Second name is 37','User 37Second name is 37',NULL,'2023-07-16 12:05:55',0,'user37@gmail.com','2023-07-16 12:05:55',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$k5MJuj8tF3EFuIIxu5+G4w$XD5+slgVruKUgUf6cgU+5EU4VzxX5XPXIdQnxh4P8Ec',NULL),(44,'user38','User 38','Second name is 38','User 38Second name is 38',NULL,'2023-07-16 12:05:56',0,'user38@gmail.com','2023-07-16 12:05:56',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$XPGW7hD4b8uaXGRZfmjZuA$y6KmaGTJxiEDuF2shLD+TxVISjtRAZLNV+bj/624bKo',NULL),(45,'user39','User 39','Second name is 39','User 39Second name is 39',NULL,'2023-07-16 12:05:56',0,'user39@gmail.com','2023-07-16 12:05:56',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$Q6D0gJbasmSOa3+i4ELsNw$PbIikIDtHwnOXJPr7JVSq1Z86bn4U613koJ6UD8gQFE',NULL),(46,'emptystateuser','Empty','State','EmptyState',NULL,'2023-07-16 12:05:56',0,'emptystateuser@gmail.com','2023-07-16 12:05:56',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$jpgRbZnufXw13QIlA2QEgA$eGwezHID3gX0L0/MphkE8/DXls2SqoGl3zWHH6qmLyE',NULL);
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

-- Dump completed on 2023-07-16 12:10:11
