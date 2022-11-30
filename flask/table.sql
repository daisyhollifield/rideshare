use rideshare_db;

drop table if exists Picfile;
drop table if exists `Comment`;
drop table if exists `Post`;
drop table if exists `User`;



CREATE TABLE `User` (
  `username` varchar(30),
  `name` varchar(30),
  `phone_number` varchar(12),
  `class_year` varchar(4),
  `major` varchar(30),
  `hometown` varchar(100),
  PRIMARY KEY (`username`)
);

CREATE TABLE `Post` (
  `pid` int auto_increment,
  `username` varchar(30),
  `type` ENUM('looking for', 'offering'),
  `destination` varchar(100),
  `street_address` varchar(100),
  `city` varchar(30),
  `state` varchar(2),
  `zipcode` varchar(5),
  `date` date,
  `time` time,
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

create table Picfile (
    `username` varchar(30) primary key,
    filename varchar(50),
    foreign key (`username`) references User(`username`)
        on delete cascade on update cascade
);

ALTER TABLE `Comment` ADD FOREIGN KEY (`username`) REFERENCES `User` (`username`);

ALTER TABLE `Comment` ADD FOREIGN KEY (`pid`) REFERENCES `Post` (`pid`);

ALTER TABLE `Post` ADD FOREIGN KEY (`username`) REFERENCES `User` (`username`);
