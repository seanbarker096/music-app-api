USE gigs;

DROP TABLE IF EXISTS gigs.post;
CREATE TABLE gigs.post (
    id int(10) unsigned auto_increment,
    attachment_type enum('video', 'image') NULL,
    attachment_uuid varchar(255) NULL,
    owner_id int(10) unsigned NOT NULL,
    content text NULL,
    PRIMARY KEY (id)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;

DROP TABLE IF EXISTS gigs.post_attachments;
CREATE TABLE gigs.post_attachments (
    id int(10) unsigned auto_increment,
    attachment_uuid varchar(255) NOT NULL,
    post_id int(10) unsigned NOT NULL,
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
    download_url varchar(255) NULL,
    PRIMARY KEY (id),
    UNIQUE INDEX uuid_idx(uuid)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;

DROP TABLE IF EXISTS gigs.auth_tokens;
CREATE TABLE gigs.auth_tokens (
  id int(10) unsigned auto_increment,
  token varchar(255) NOT NULL,
  owner_id int NOT NULL UNIQUE,
  PRIMARY KEY (id),
  UNIQUE INDEX owner_id_idx(owner_id)
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
  last_login_date datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  language_id int(10) unsigned NOT NULL,
  timezone_id int(10) unsigned NOT NULL, 
  password_hash varchar(32) NOT NULL,
  salt varchar(16) NOT NULL,
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;
