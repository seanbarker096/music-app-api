USE gigs;

DROP TABLE IF EXISTS gigs.post;
CREATE TABLE gigs.post (
    id int(10) unsigned auto_increment,
    owner_id int(10) unsigned NOT NULL,
    owner_type enum('user', 'artist') NOT NULL,
    content text NULL,
    create_time datetime NOT NULL,
    update_time datetime DEFAULT NULL,
    is_deleted tinyint(1) NOT NULL DEFAULT 0,
    PRIMARY KEY (id)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;

DROP TABLE IF EXISTS gigs.post_attachments;
CREATE TABLE gigs.post_attachment (
    id int(10) unsigned auto_increment,
    file_id varchar(255) NOT NULL,
    post_id int(10) unsigned NOT NULL,
    create_time datetime NOT NULL,
    PRIMARY KEY (id)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;

DROP TABLE IF EXISTS gigs.files;
CREATE TABLE gigs.files (
    id bigint(10) unsigned auto_increment,
    uuid varchar(255) NOT NULL,
    file_name varchar(1024) NOT NULL,
    file_size int(10) NULL,
    mime_type varchar(255) NOT NULL,
    url varchar(512) NULL,
    PRIMARY KEY (id),
    UNIQUE INDEX uuid_idx(uuid)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;

DROP TABLE IF EXISTS gigs.auth_tokens;
CREATE TABLE gigs.auth_tokens (
  id int(10) unsigned auto_increment,
  token varchar(255) NOT NULL UNIQUE,
  owner_id int NOT NULL,
  session_id varchar(128) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE INDEX owner_id_session_id_idx(owner_id, session_id)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;

DROP TABLE IF EXISTS gigs.users;
CREATE TABLE gigs.users (
  id int(10) unsigned auto_increment,
  username varchar(16) NOT NULL,
  first_name varchar(128) NOT NULL,
  second_name varchar(128) NOT NULL,
  create_time datetime NOT NULL,
  is_deleted tinyint(1) NOT NULL DEFAULT '0',
  email varchar(100) NOT NULL,
  last_login_date datetime NOT NULL,
  language_id int(10) unsigned NOT NULL,
  timezone_id int(10) unsigned NOT NULL, 
  avatar_file_uuid varchar(255) DEFAULT NULL,
  password_hash varchar(256) NOT NULL,
  salt varchar(16) NULL,
  PRIMARY KEY (id),
  UNIQUE INDEX username_idx(username),
  UNIQUE INDEX email_idx(email)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;

DROP TABLE IF EXISTS gigs.artists;
CREATE TABLE gigs.artists (
  id int(10) unsigned auto_increment,
  artist_name varchar(128) NOT NULL,
  biography varchar(500) default NULL,
  create_time datetime NOT NULL,
  update_time datetime default NULL,
  uuid varchar(255) NOT NULL,
  owner_id int(10) unsigned,
  image_url varchar(512) NULL,
  PRIMARY KEY (id),
  INDEX artist_name_idx(artist_name),
  UNIQUE INDEX owner_id_idx(owner_id),
  UNIQUE INDEX uuid_idx(uuid)  
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;

DROP TABLE IF EXISTS gigs.feature;
CREATE TABLE gigs.feature (
  id int(10) unsigned auto_increment,
  context_type varchar(60) NOT NULL,
  context_id int(10) unsigned NOT NULL,
  owner_type varchar(60) NOT NULL,
  owner_id int(10) unsigned NOT NULL,
  PRIMARY KEY (id),
  INDEX owner_type_owner_id_context_id_idx(owner_type, owner_id, context_id)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;

DROP TABLE IF EXISTS gigs.tag;
CREATE TABLE gigs.tag (
  id int(10) unsigned auto_increment,
  tagged_in_entity_type varchar(60) NOT NULL, -- e.g. a user is tagged in a post. tagged_in_entity_type = user
  tagged_in_entity_id int(10) unsigned NOT NULL,
  tagged_entity_type varchar(60) NOT NULL,
  tagged_entity_id int(10) unsigned NOT NULL,
  creator_type varchar(60) NOT NULL,
  creator_id int(10) unsigned NOT NULL,
  PRIMARY KEY (id),
  INDEX tagged_in_id_tagged_entity_type_idx(tagged_entity_id, tagged_entity_type),
  INDEX tagged_entity_id_tagged_entity_type_idx(tagged_entity_id, tagged_entity_type)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;