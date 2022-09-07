USE gigs;

DROP TABLE IF EXISTS gigs.post;
CREATE TABLE gigs.post (
    id int(10) unsigned auto_increment,
    attachment_type enum('video', 'image') NULL,
    attachment_uuid varchar(255) NULL,
    owner_id int(10) unsigned NOT NULL,
    body_text text NULL,
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
    id int(10) unsigned auto_increment,
    uuid varchar(255) NOT NULL,
    file_location varchar(255) NOT NULL,
    PRIMARY KEY (id)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;
