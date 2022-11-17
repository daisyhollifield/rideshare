use rideshare_db;

drop table if exists `Comment`;
drop table if exists `Post`;
drop table if exists `User`;


CREATE TABLE `User` (
  `username` varchar(30),
  `name` varchar(30),
  `password` varchar(30),
  `phone_number` varchar(12),
  PRIMARY KEY (`username`)
);

CREATE TABLE `Post` (
  `pid` int auto_increment,
  `username` varchar(30),
  `type` ENUM('looking for', 'offering'),
  `destination` varchar(1000),
  `time` datetime,
  `title` varchar(100),
  `seats` int,
  `special_request` varchar(1000),
  `display_now` boolean,
  `cost` int,
  PRIMARY KEY (`pid`)
);

CREATE TABLE `Comment` (
  `cid` int auto_increment,
  `username` varchar(30),
  `pid` int,
  `content` varchar(2200),
  `time` datetime,
  PRIMARY KEY (`cid`)
);

ALTER TABLE `Comment` ADD FOREIGN KEY (`username`) REFERENCES `User` (`username`);

ALTER TABLE `Comment` ADD FOREIGN KEY (`pid`) REFERENCES `Post` (`pid`);

ALTER TABLE `Post` ADD FOREIGN KEY (`username`) REFERENCES `User` (`username`);
