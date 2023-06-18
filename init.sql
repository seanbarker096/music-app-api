
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
INSERT INTO `event` VALUES (1,'Glastonbury','Glastonbury','2023-04-15','2023-04-16','music_festival','2023-06-18 16:11:04',NULL),(2,'O2 Academy Brixton','O2 Academy Brixton','2023-04-17','2023-04-18','music_concert','2023-06-18 16:11:04',NULL),(3,'Primavera Sound','Primavera Sound','2023-04-17','2023-04-18','music_festival','2023-06-18 16:11:04',NULL);
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
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `files`
--

LOCK TABLES `files` WRITE;
/*!40000 ALTER TABLE `files` DISABLE KEYS */;
INSERT INTO `files` VALUES (1,'show1','show1.mp4',NULL,'video/mp4','https://file-service-bff149a0b.s3.amazonaws.com/show1?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAR56DCSXK3Z75BQB2%2F20230618%2Feu-west-2%2Fs3%2Faws4_request&X-Amz-Date=20230618T161051Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=44131a8ecf93659a7dd0765d6b35062c6e2c2acf0ac469ca7f7d429c63f30228'),(2,'show2','show2.mp4',NULL,'video/mp4','https://file-service-bff149a0b.s3.amazonaws.com/show2?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAR56DCSXK3Z75BQB2%2F20230618%2Feu-west-2%2Fs3%2Faws4_request&X-Amz-Date=20230618T161052Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=1578ea48846b4a248b18fcb8809d16f3574f079cc09f9ae2e75c0cec4f91dc30'),(3,'show3','show3.mp4',NULL,'video/mp4','https://file-service-bff149a0b.s3.amazonaws.com/show3?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAR56DCSXK3Z75BQB2%2F20230618%2Feu-west-2%2Fs3%2Faws4_request&X-Amz-Date=20230618T161057Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=f6f28116ae2382eedfdaf40873c7baec506f88db29e6cda754bafec43ed720ae'),(4,'show4','show4.mp4',NULL,'video/mp4','https://file-service-bff149a0b.s3.amazonaws.com/show4?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAR56DCSXK3Z75BQB2%2F20230618%2Feu-west-2%2Fs3%2Faws4_request&X-Amz-Date=20230618T161059Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=c70ba05ea3835cf8473296b875c0c47c3a7c265a12fb63ca477a5f5542802855'),(5,'show5','show5.mp4',NULL,'video/mp4','https://file-service-bff149a0b.s3.amazonaws.com/show5?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAR56DCSXK3Z75BQB2%2F20230618%2Feu-west-2%2Fs3%2Faws4_request&X-Amz-Date=20230618T161101Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=ee37ed712bfbe6fc87fd2b60a60ef7058327b5bccc61310577305d92003c211a'),(6,'202','dog.mp4',NULL,'video/mp4','https://file-service-bff149a0b.s3.amazonaws.com/202?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAR56DCSXK3Z75BQB2%2F20230618%2Feu-west-2%2Fs3%2Faws4_request&X-Amz-Date=20230618T161103Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=a7cd6f94427e3f2d4c76cbaeb5d06c6347ad07d4bfcc349451950d6735907cd1'),(7,'123456','profile-pic.jpg',NULL,'image/jpeg','https://file-service-bff149a0b.s3.amazonaws.com/123456?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAR56DCSXK3Z75BQB2%2F20230618%2Feu-west-2%2Fs3%2Faws4_request&X-Amz-Date=20230618T161103Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=db11cc304e90dc58fbe60b8c70ac2d74675483c446ba8b7745d764c8d1f236e3'),(8,'aaaaaaaaaaaaaaa','profile-pic2.jpg',NULL,'image/jpeg','https://file-service-bff149a0b.s3.amazonaws.com/aaaaaaaaaaaaaaa?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAR56DCSXK3Z75BQB2%2F20230618%2Feu-west-2%2Fs3%2Faws4_request&X-Amz-Date=20230618T161104Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=af063c91d0c74e81b8ddf0a2687823d8edb940e765201ce85d3996c43a304f84');
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
INSERT INTO `performance` VALUES (1,1,1,'2023-06-18','2023-06-18 16:11:05',NULL),(2,3,1,'2023-06-18','2023-06-18 16:11:05',NULL),(3,2,1,'2023-06-20','2023-06-18 16:11:05',NULL),(4,1,1,'2023-06-23','2023-06-18 16:11:05',NULL),(5,2,1,'2023-06-23','2023-06-18 16:11:05',NULL),(6,2,3,'2023-06-26','2023-06-18 16:11:05',NULL);
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
INSERT INTO `performance_attendance` VALUES (1,1,1,'2023-06-18 16:11:05'),(2,2,4,'2023-06-18 16:11:05'),(3,6,1,'2023-06-18 16:11:05');
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
INSERT INTO `performers` VALUES (1,'Taylor Swift','Taylor Alison Swift is an American singer-songwriter. Her narrative songwriting, which often centers around her personal life, has received widespread critical plaudits and media coverage.','2023-06-18 16:11:05',NULL,'06HL4z0CvFAxyc27GXpf02',3,'https://i.scdn.co/image/ab6761610000f1785a00969a4698c3132a15fbb0'),(2,'Eminem','Eminem is an American rapper, songwriter, record producer, record executive, and actor. He is consistently cited as one of the greatest and most influential rappers of all time and was labeled the King of Hip Hop by Rolling Stone magazine.','2023-06-18 16:11:05',NULL,'7dGJo4pcD2V6oG8kP0tJRR',1,'https://i.scdn.co/image/ab6761610000f178a00b11c129b27a88fc72f36b'),(3,'Kendrick Lamar','Kendrick Lamar Duckworth is an American rapper, songwriter, and record producer. Since his debut into the mainstream with Good Kid, M.A.A.D City, Lamar has been regarded as one of the most influential artists of his generation, as well as one of the greatest rappers and lyricists of all time.','2023-06-18 16:11:05',NULL,'2YZyLoL8N0Wb9xBt1NhZWg',5677,'https://i.scdn.co/image/ab6761610000f178437b9e2a82505b3d93ff1022'),(4,'J cole','Jermaine Lamarr Cole, known professionally as J. Cole, is an American rapper, singer, songwriter, record producer, and record executive. Born on a military base in Germany and raised in Fayetteville, North Carolina, Cole initially gained recognition as a rapper following the release of his debut mixtape, The Come Up, in early 2007.','2023-06-18 16:11:09',NULL,'6l3HvQ5sa6mXTsMTB19rO5',46,'https://i.scdn.co/image/ab6761610000f1785a00969a4698c3132a15fbb0');
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
  `is_deleted` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `post`
--

LOCK TABLES `post` WRITE;
/*!40000 ALTER TABLE `post` DISABLE KEYS */;
INSERT INTO `post` VALUES (1,1,'user','What a great day at Glastonbury!',1,'2023-06-18 16:11:05',NULL,0),(2,3,'user','This is a post which user one will be tagged in',3,'2023-06-18 16:11:05',NULL,0),(3,1,'user','Taylor swifts show was good!',1,'2023-06-18 16:11:05',NULL,0),(4,4,'user','Taylor swifts show at prima was sick!',1,'2023-06-18 16:11:05',NULL,0),(5,4,'user','Cool show mite',1,'2023-06-18 16:11:05',NULL,0),(6,4,'user','Eminems show was good!',4,'2023-06-18 16:11:05',NULL,0),(7,1,'user','Kendrick at o2',1,'2023-06-18 16:11:05',NULL,0),(8,1,'user','Post 0',1,'2023-06-18 16:11:05',NULL,0),(9,1,'user','Post 1',1,'2023-06-18 16:11:05',NULL,0),(10,1,'user','Post 2',1,'2023-06-18 16:11:05',NULL,0),(11,1,'user','Post 3',1,'2023-06-18 16:11:05',NULL,0),(12,1,'user','Post 4',1,'2023-06-18 16:11:05',NULL,0),(13,1,'user','Post 5',1,'2023-06-18 16:11:05',NULL,0),(14,1,'user','Post 6',1,'2023-06-18 16:11:05',NULL,0),(15,1,'user','Post 7',1,'2023-06-18 16:11:05',NULL,0),(16,1,'user','Post 8',1,'2023-06-18 16:11:05',NULL,0),(17,1,'user','Post 9',1,'2023-06-18 16:11:05',NULL,0),(18,1,'user','Post 10',1,'2023-06-18 16:11:05',NULL,0),(19,1,'user','Post 11',1,'2023-06-18 16:11:05',NULL,0),(20,1,'user','Post 12',1,'2023-06-18 16:11:05',NULL,0),(21,1,'user','Post 13',1,'2023-06-18 16:11:05',NULL,0),(22,1,'user','Post 14',1,'2023-06-18 16:11:05',NULL,0),(23,1,'user','Post 15',1,'2023-06-18 16:11:05',NULL,0),(24,1,'user','Post 16',1,'2023-06-18 16:11:05',NULL,0),(25,1,'user','Post 17',1,'2023-06-18 16:11:05',NULL,0),(26,1,'user','Post 18',1,'2023-06-18 16:11:05',NULL,0),(27,1,'user','Post 19',1,'2023-06-18 16:11:05',NULL,0),(28,1,'user','Post 20',1,'2023-06-18 16:11:05',NULL,0),(29,1,'user','Post 21',1,'2023-06-18 16:11:05',NULL,0),(30,1,'user','Post 22',1,'2023-06-18 16:11:05',NULL,0),(31,1,'user','Post 23',1,'2023-06-18 16:11:05',NULL,0),(32,1,'user','Post 24',1,'2023-06-18 16:11:05',NULL,0),(33,1,'user','Post 25',1,'2023-06-18 16:11:05',NULL,0),(34,1,'user','Post 26',1,'2023-06-18 16:11:05',NULL,0);
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
INSERT INTO `post_attachment` VALUES (1,'1',1,'2023-06-18 16:11:05'),(2,'2',2,'2023-06-18 16:11:05'),(3,'3',3,'2023-06-18 16:11:05'),(4,'5',4,'2023-06-18 16:11:05'),(5,'1',5,'2023-06-18 16:11:05'),(6,'1',6,'2023-06-18 16:11:05'),(7,'6',7,'2023-06-18 16:11:05'),(8,'4',8,'2023-06-18 16:11:05'),(9,'4',9,'2023-06-18 16:11:05'),(10,'1',10,'2023-06-18 16:11:05'),(11,'1',11,'2023-06-18 16:11:05'),(12,'2',12,'2023-06-18 16:11:05'),(13,'2',13,'2023-06-18 16:11:05'),(14,'3',14,'2023-06-18 16:11:05'),(15,'5',15,'2023-06-18 16:11:05'),(16,'5',16,'2023-06-18 16:11:05'),(17,'1',17,'2023-06-18 16:11:05'),(18,'3',18,'2023-06-18 16:11:05'),(19,'2',19,'2023-06-18 16:11:05'),(20,'5',20,'2023-06-18 16:11:05'),(21,'4',21,'2023-06-18 16:11:05'),(22,'2',22,'2023-06-18 16:11:05'),(23,'1',23,'2023-06-18 16:11:05'),(24,'4',24,'2023-06-18 16:11:05'),(25,'4',25,'2023-06-18 16:11:05'),(26,'2',26,'2023-06-18 16:11:05'),(27,'2',27,'2023-06-18 16:11:05'),(28,'4',28,'2023-06-18 16:11:05'),(29,'1',29,'2023-06-18 16:11:05'),(30,'4',30,'2023-06-18 16:11:05'),(31,'2',31,'2023-06-18 16:11:05'),(32,'4',32,'2023-06-18 16:11:05'),(33,'2',33,'2023-06-18 16:11:05'),(34,'3',34,'2023-06-18 16:11:05');
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
INSERT INTO `users` VALUES (1,'sean','Sean','Barker','SeanBarker','I love music and live in London','2023-06-18 16:11:04',0,'seanbarker6@sky.com','2023-06-18 16:11:04',1,1,'123456','$argon2id$v=19$m=16384,t=12,p=4$NvzvVaaJeYoB1Gw6g2ZlGQ$8nRJk+/QsqfUPbHw2kZv69tC6161No5ziR9gnGUG9gE',NULL),(2,'gregory','Greg','Baxter','GregBaxter',NULL,'2023-06-18 16:11:04',0,'gg_no_re@sky.com','2023-06-18 16:11:04',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$NvzvVaaJeYoB1Gw6g2ZlGQ$8nRJk+/QsqfUPbHw2kZv69tC6161No5ziR9gnGUG9gE',NULL),(3,'tim14','Tim','Smith','TimSmith','Mi nem Geoff. Mi like watching people play music and venues and shit','2023-06-18 16:11:04',0,'timsmith@sky.com','2023-06-18 16:11:04',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$hBuo7Tuwb4qhbyuNRHSE8A$qBU4CeAu7s/E+NjS5LNI2k7zj4iTmtr7X9xkPWIKJl4',NULL),(4,'seanborker','Sean','Borker','SeanBorker','Reeeeeeeeeeee. Im 28 years old and moved to London 2 years ago. I love music and live in London','2023-06-18 16:11:04',0,'seanborker@sky.com','2023-06-18 16:11:04',1,1,'123456','$argon2id$v=19$m=16384,t=12,p=4$l5o/p6V+JX5gvX2ML8eQiQ$HBpMW5HF7z6CPI6UR+Vaal2YCCcrdUclVJll4TSmYgA',NULL),(5,'newuser','Geoff','Mi Name','GeoffMi Name',NULL,'2023-06-18 16:11:05',0,'newuser@sky.com','2023-06-18 16:11:05',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$J1HGfqTdgotBhrOYl3MwAw$KgcCeOhX8T0vYOw5Ad4dvSNjXCSme3uBcfvmQhw+d3Q',NULL),(6,'user0','User 0','Second name is 0','User 0Second name is 0',NULL,'2023-06-18 16:11:05',0,'user0@gmail.com','2023-06-18 16:11:05',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$z7MTR0Df7Yyk5av25c2Lpg$3sWITpnErgtutS8SdYWZiO7KKy2emJdQD/izaEFbgz0',NULL),(7,'user1','User 1','Second name is 1','User 1Second name is 1',NULL,'2023-06-18 16:11:05',0,'user1@gmail.com','2023-06-18 16:11:05',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$ykX4LdRPLRCPogHpIUg6cw$OcidBhYwU1d2aG3s0hnRKQ+5AwyPb5XjotMRfd7uERs',NULL),(8,'user2','User 2','Second name is 2','User 2Second name is 2',NULL,'2023-06-18 16:11:05',0,'user2@gmail.com','2023-06-18 16:11:05',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$M1Vsq9445PghHMCn0XGrrA$TKzR8LpullGpcGxtazA4QrbBduNjOD0z3wPe/Ki/HMo',NULL),(9,'user3','User 3','Second name is 3','User 3Second name is 3',NULL,'2023-06-18 16:11:05',0,'user3@gmail.com','2023-06-18 16:11:05',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$SyH2RAFdHI2WkkhdPVUY0Q$RpIK3zo2OTaSXQtf/5pCpBbbkWMv26RqJUagcsKK0Q8',NULL),(10,'user4','User 4','Second name is 4','User 4Second name is 4',NULL,'2023-06-18 16:11:05',0,'user4@gmail.com','2023-06-18 16:11:05',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$NU2ehzhTWe6pXxu3dHrHCg$uCb90yOhx/NRKt2+sOv9bbiT43elQ/8RrrQuHuMBqAs',NULL),(11,'user5','User 5','Second name is 5','User 5Second name is 5',NULL,'2023-06-18 16:11:06',0,'user5@gmail.com','2023-06-18 16:11:06',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$ZXf++3Sr/zIa8CRLT7ln1w$0Q4Zh30yxGWPiBi9n1d/ZDGMP+V+GCirg1Gsar+570c',NULL),(12,'user6','User 6','Second name is 6','User 6Second name is 6',NULL,'2023-06-18 16:11:06',0,'user6@gmail.com','2023-06-18 16:11:06',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$oVEVWhu/q9S6FfI+ZFfT8A$V4WSZ/p9ya7UewRdKf3nbK9FygR95XJZOEZXbOyMygs',NULL),(13,'user7','User 7','Second name is 7','User 7Second name is 7',NULL,'2023-06-18 16:11:06',0,'user7@gmail.com','2023-06-18 16:11:06',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$GtS5PpYUF10ZpR9Y8Cd/UA$egKq2xAE6XdVEDKTaf5EC8OWOoPo3r4+e8qYUPqWmvw',NULL),(14,'user8','User 8','Second name is 8','User 8Second name is 8',NULL,'2023-06-18 16:11:06',0,'user8@gmail.com','2023-06-18 16:11:06',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$wqTU1xqRWdjQarsmQWkvAQ$hTfm6qlfV5MxVYdgmH+2NBIEyrRGmdhR1SPWNJ747D0',NULL),(15,'user9','User 9','Second name is 9','User 9Second name is 9',NULL,'2023-06-18 16:11:06',0,'user9@gmail.com','2023-06-18 16:11:06',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$WyUrADNP2yKabj2BxhB2Tg$qhssdOos3Vzy7Rhqlu+FHpaF2uyPJ9V++TKqSfjF6xo',NULL),(16,'user10','User 10','Second name is 10','User 10Second name is 10',NULL,'2023-06-18 16:11:06',0,'user10@gmail.com','2023-06-18 16:11:06',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$evZuLe+rz4EqYnXEnBqmPA$TJkLlEaq7LW3xp90L0SXf41BhJRsjgEfgNkuoMEQhik',NULL),(17,'user11','User 11','Second name is 11','User 11Second name is 11',NULL,'2023-06-18 16:11:06',0,'user11@gmail.com','2023-06-18 16:11:06',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$KSgzz/mmMsMj6FzeRUZufQ$W2friG19VJhjrsDN8f8fp1YjgLpv44IP18rW13WicPs',NULL),(18,'user12','User 12','Second name is 12','User 12Second name is 12',NULL,'2023-06-18 16:11:06',0,'user12@gmail.com','2023-06-18 16:11:06',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$huiK+jxwmwKX/8XLOHk0qA$kkgqYPmloKRtl9n+D4CcpjLvExn9dU02uK/d2THsFI0',NULL),(19,'user13','User 13','Second name is 13','User 13Second name is 13',NULL,'2023-06-18 16:11:06',0,'user13@gmail.com','2023-06-18 16:11:06',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$drKgx000hJZ4Wr+nml1UWQ$rUb0LXUHrfwuQlR4bmcTXJn++NLJ5dMRrQUU6ojaI38',NULL),(20,'user14','User 14','Second name is 14','User 14Second name is 14',NULL,'2023-06-18 16:11:06',0,'user14@gmail.com','2023-06-18 16:11:06',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$y851VlSWuMsc/+ZNAYwkhQ$+Q3XIFvGa7pKGcmXcsdh4ugXtj6DYN9Yi1fFOU9NKqk',NULL),(21,'user15','User 15','Second name is 15','User 15Second name is 15',NULL,'2023-06-18 16:11:06',0,'user15@gmail.com','2023-06-18 16:11:06',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$FdojBt+qSjeimWeSV5vNsA$/adnS9OivUi2GAvyF5180u6C26Izr0MZlMcHlFwbCJo',NULL),(22,'user16','User 16','Second name is 16','User 16Second name is 16',NULL,'2023-06-18 16:11:07',0,'user16@gmail.com','2023-06-18 16:11:07',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$RhY2QWKoy0aIqS4zqsUXKg$fdted0ukbIRqKHy6qkTeedxDDilUpc19bUqH6cbWVOI',NULL),(23,'user17','User 17','Second name is 17','User 17Second name is 17',NULL,'2023-06-18 16:11:07',0,'user17@gmail.com','2023-06-18 16:11:07',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$b/Uieu/GdYw6Xeds6Hjsrg$zGBp1n+Ut6+TkYv2zu4xj/xsyqxVWy3ANuVMEf/SbIw',NULL),(24,'user18','User 18','Second name is 18','User 18Second name is 18',NULL,'2023-06-18 16:11:07',0,'user18@gmail.com','2023-06-18 16:11:07',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$7gG0V6tOCm7EXqQ248XEwQ$o9qSRg4TnA/44TENF/ruwb8ud3yjsVXOs9xvZnB04L0',NULL),(25,'user19','User 19','Second name is 19','User 19Second name is 19',NULL,'2023-06-18 16:11:07',0,'user19@gmail.com','2023-06-18 16:11:07',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$WXlx/4CPJfH91geavX3L8g$1M+LyA8Lo8CnCKYuQ3hdiquSVpl7lHh0hxapYJLYJTw',NULL),(26,'user20','User 20','Second name is 20','User 20Second name is 20',NULL,'2023-06-18 16:11:07',0,'user20@gmail.com','2023-06-18 16:11:07',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$KowCxdC6iZZiS3KRp1UxYw$XbT1FIv7cC0TaJC3CmCx5mIu3G5NvHsaEic+s71Tio0',NULL),(27,'user21','User 21','Second name is 21','User 21Second name is 21',NULL,'2023-06-18 16:11:07',0,'user21@gmail.com','2023-06-18 16:11:07',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$go7rCqyt9+m/ODJeap05WQ$0Mu2v/fAYZ+blei5vneTE7cW384/yBVKDCmj/wTdMTU',NULL),(28,'user22','User 22','Second name is 22','User 22Second name is 22',NULL,'2023-06-18 16:11:07',0,'user22@gmail.com','2023-06-18 16:11:07',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$DlIUCGzahpOwB0Kc/87RWA$jLhfW+gQoqISlJ1Xrq3k5TOWv0ususbav+ECUuuEIxM',NULL),(29,'user23','User 23','Second name is 23','User 23Second name is 23',NULL,'2023-06-18 16:11:07',0,'user23@gmail.com','2023-06-18 16:11:07',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$6VCbWPRQLlR99NEZhyE3fA$kRdxd+X/96zKm8fQy60HYcBMsVJt/WQtTFRs42Y6ip8',NULL),(30,'user24','User 24','Second name is 24','User 24Second name is 24',NULL,'2023-06-18 16:11:07',0,'user24@gmail.com','2023-06-18 16:11:07',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$Fq0+DTXmTNwUfgA1sbzo8A$aVwDKqNtrQw8z0IIuL9nBOxXVf8d1ECzCn1k5sGts9I',NULL),(31,'user25','User 25','Second name is 25','User 25Second name is 25',NULL,'2023-06-18 16:11:07',0,'user25@gmail.com','2023-06-18 16:11:07',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$wTXZM24/lRKitsOfp5ssZw$ZDzs6RPOxcB2uGg9C65tI7JPbiq1hTZcwTI0a3vx4cs',NULL),(32,'user26','User 26','Second name is 26','User 26Second name is 26',NULL,'2023-06-18 16:11:07',0,'user26@gmail.com','2023-06-18 16:11:07',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$Juaim1kk59oocoYnYYWGlA$bFxNLyOMYeNr0CREZNd6jHBnjf1w+UW3FglQckx7iTo',NULL),(33,'user27','User 27','Second name is 27','User 27Second name is 27',NULL,'2023-06-18 16:11:08',0,'user27@gmail.com','2023-06-18 16:11:08',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$KcwekMFROChIt7W1CqnR1Q$S/jyia+9PSgUgNJdbE2QQ51edmuWaYQQhA2qi2lfoD0',NULL),(34,'user28','User 28','Second name is 28','User 28Second name is 28',NULL,'2023-06-18 16:11:08',0,'user28@gmail.com','2023-06-18 16:11:08',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$rnj5lBjQBrQjpxlC+Y/0jg$uVRsjtX2hEC7hjQ9vbT30Y4gQ5DVuGcsuKZ4J54Cxnw',NULL),(35,'user29','User 29','Second name is 29','User 29Second name is 29',NULL,'2023-06-18 16:11:08',0,'user29@gmail.com','2023-06-18 16:11:08',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$X+poe3p7ykss18POE5ERQg$0cRYvZcO+LONENGAzoHS7+S8pat87I4N8UqQuBbYQ1c',NULL),(36,'user30','User 30','Second name is 30','User 30Second name is 30',NULL,'2023-06-18 16:11:08',0,'user30@gmail.com','2023-06-18 16:11:08',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$iq7W9WXnvUjUQ2CRgzFlAA$k6R3UH+x3DcNMfpIxJP0VeKBUb3vkuiLcHfYtNFWMtY',NULL),(37,'user31','User 31','Second name is 31','User 31Second name is 31',NULL,'2023-06-18 16:11:08',0,'user31@gmail.com','2023-06-18 16:11:08',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$nongK9QIRE/f0m4SkPYvcg$9eXFof707MNmxf1J7NnxqffTvmUNrIMq/EOsW2clzI8',NULL),(38,'user32','User 32','Second name is 32','User 32Second name is 32',NULL,'2023-06-18 16:11:08',0,'user32@gmail.com','2023-06-18 16:11:08',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$Gn+RU59Hs19bg4zFdx1MnQ$9yEkknDso+H+cY2P0tL1vo26yCbJnJNCrSeaIidujaw',NULL),(39,'user33','User 33','Second name is 33','User 33Second name is 33',NULL,'2023-06-18 16:11:08',0,'user33@gmail.com','2023-06-18 16:11:08',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$zBRSeOVI7isGvfHGZ0asag$9G1JQ5hsR7j1TAQdmIacKivQloEthx6FdF5lLx3ytgE',NULL),(40,'user34','User 34','Second name is 34','User 34Second name is 34',NULL,'2023-06-18 16:11:08',0,'user34@gmail.com','2023-06-18 16:11:08',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$KaOuopqDhP2V+UTle4LyPQ$BNV61z9u2MX77ZJJ1CU3B3WND0iP1WEKrn7clW2a8U8',NULL),(41,'user35','User 35','Second name is 35','User 35Second name is 35',NULL,'2023-06-18 16:11:08',0,'user35@gmail.com','2023-06-18 16:11:08',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$pOHkBccqyWYAfu4R+/fuAA$74YX+uA4Dif8Xmk5N9WygUWy67wyHjdBRwAJK5om8Oc',NULL),(42,'user36','User 36','Second name is 36','User 36Second name is 36',NULL,'2023-06-18 16:11:08',0,'user36@gmail.com','2023-06-18 16:11:08',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$0txWFBS0GPJY7xwXaO/xLQ$0j1Uq4QyD2JGRQ7AnI7aHQIi+9ueIyI+txifYOC2ojA',NULL),(43,'user37','User 37','Second name is 37','User 37Second name is 37',NULL,'2023-06-18 16:11:08',0,'user37@gmail.com','2023-06-18 16:11:08',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$yn3VQo9PzH7sLWs/llwjWg$pdj8h4cNRsceZwssdjVlPIpJvAji2Ie+2lr4bfe4E3c',NULL),(44,'user38','User 38','Second name is 38','User 38Second name is 38',NULL,'2023-06-18 16:11:09',0,'user38@gmail.com','2023-06-18 16:11:09',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$VX/7wX7W0CrS76Yedzz3+A$uYcd/thlNPEbDW5V9lHX4DW1xWoddX4A1k2lbEokWrc',NULL),(45,'user39','User 39','Second name is 39','User 39Second name is 39',NULL,'2023-06-18 16:11:09',0,'user39@gmail.com','2023-06-18 16:11:09',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$ynmAqCtRhfNma9OJ/yCMEw$JaEjYo5gGD/ZtVJN46cTOt+oic0XicxXF4ZmLdp31Y8',NULL),(46,'emptystateuser','Empty','State','EmptyState',NULL,'2023-06-18 16:11:09',0,'emptystateuser@gmail.com','2023-06-18 16:11:09',1,1,NULL,'$argon2id$v=19$m=16384,t=12,p=4$v971kN8Q9wGziU4U5dJVYA$jsGCiGdPcPv5o8GxTGrS3rz1vrRnaEfo8O+FbFSyDrk',NULL);
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

-- Dump completed on 2023-06-18 16:12:07
