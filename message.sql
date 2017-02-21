/*
Navicat MySQL Data Transfer

Source Server         : db1
Source Server Version : 50713
Source Host           : localhost:3306
Source Database       : join

Target Server Type    : MYSQL
Target Server Version : 50713
File Encoding         : 65001

Date: 2016-10-13 22:30:00
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for courses
-- ----------------------------
DROP TABLE IF EXISTS `courses`;
CREATE TABLE `courses` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `summary` varchar(2550) DEFAULT NULL,
  `former_teachers` varchar(500) DEFAULT NULL,
  `present_teacher_id` int(255) DEFAULT NULL,
  `create_time` varchar(255) DEFAULT NULL,
  `update_time` varchar(255) DEFAULT NULL,
  `hours_per_class` float(255,1) unsigned zerofill DEFAULT '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000.0',
  `fee_per_class` float(255,1) unsigned zerofill DEFAULT '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000.0',
  `modules` varchar(2550) DEFAULT NULL,
  `present_class` int(255) DEFAULT '0',
  `total_class` int(255) DEFAULT '1',
  `active` int(1) DEFAULT '1',
  `dates` varchar(2550) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `teancher.id` (`present_teacher_id`),
  CONSTRAINT `teancher.id` FOREIGN KEY (`present_teacher_id`) REFERENCES `teachers` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of courses
-- ----------------------------
INSERT INTO `courses` VALUES ('1', '机器人A', null, 'aa', '12', null, null, '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001.5', '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000200.0', 'm1,m2,m3,m4,m5', '2', '5', '1', '06/15/2016, 09/01/2016, 11/02/2016, 12/06/2016, 12/16/2016');
INSERT INTO `courses` VALUES ('2', '机器人B', 'asdad', null, '11', null, null, '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001.5', '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000300.0', 'm1,m2,m3,m4,m5', '1', '5', '1', '06/15/2016, 09/01/2016, 11/02/2016, 12/06/2016, 12/16/2016');

-- ----------------------------
-- Table structure for records
-- ----------------------------
DROP TABLE IF EXISTS `records`;
CREATE TABLE `records` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` varchar(255) DEFAULT NULL,
  `course_id` int(11) DEFAULT NULL,
  `teacher_id` int(11) DEFAULT NULL,
  `substitute` tinyint(4) DEFAULT '0',
  `substitute_id` int(11) DEFAULT NULL,
  `attend_list` varchar(255) DEFAULT NULL,
  `comment` varchar(2550) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `courserecord` (`course_id`),
  KEY `subteacherrecord` (`teacher_id`),
  CONSTRAINT `courserecord` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`),
  CONSTRAINT `subteacherrecord` FOREIGN KEY (`teacher_id`) REFERENCES `teachers` (`id`),
  CONSTRAINT `teacherrecord` FOREIGN KEY (`teacher_id`) REFERENCES `teachers` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of records
-- ----------------------------
INSERT INTO `records` VALUES ('1', null, null, null, '0', null, null, null);

-- ----------------------------
-- Table structure for role
-- ----------------------------
DROP TABLE IF EXISTS `role`;
CREATE TABLE `role` (
  `id` int(255) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of role
-- ----------------------------
INSERT INTO `role` VALUES ('1', 'admin', null);
INSERT INTO `role` VALUES ('2', 'teacher', null);

-- ----------------------------
-- Table structure for role_teacher
-- ----------------------------
DROP TABLE IF EXISTS `role_teacher`;
CREATE TABLE `role_teacher` (
  `role_id` int(255) DEFAULT NULL,
  `teacher_id` int(255) DEFAULT NULL,
  KEY `teacherId` (`teacher_id`),
  KEY `roleId` (`role_id`),
  CONSTRAINT `roleId` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`),
  CONSTRAINT `teacherId` FOREIGN KEY (`teacher_id`) REFERENCES `teachers` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of role_teacher
-- ----------------------------
INSERT INTO `role_teacher` VALUES (null, null);
INSERT INTO `role_teacher` VALUES ('1', '11');
INSERT INTO `role_teacher` VALUES ('2', '12');

-- ----------------------------
-- Table structure for students
-- ----------------------------
DROP TABLE IF EXISTS `students`;
CREATE TABLE `students` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `chinese_name` varchar(255) DEFAULT NULL,
  `alias_names` varchar(255) DEFAULT NULL,
  `gender` int(1) DEFAULT NULL,
  `birthday` varchar(255) DEFAULT NULL,
  `grade` varchar(255) DEFAULT NULL,
  `school` varchar(255) DEFAULT NULL,
  `adress` varchar(255) DEFAULT NULL,
  `photo` varchar(255) DEFAULT NULL,
  `former_courses` varchar(255) DEFAULT NULL,
  `create_time` varchar(255) DEFAULT NULL,
  `update_time` varchar(255) DEFAULT NULL,
  `present_course_id` int(255) DEFAULT NULL,
  `former_hours` float(255,1) DEFAULT '0.0',
  `present_class` varchar(255) DEFAULT NULL,
  `former_fee` float(255,1) DEFAULT '0.0',
  `fomer_discount` float(255,0) DEFAULT '0',
  `present_discount` varchar(255) DEFAULT '0',
  `attend_records` varchar(15000) DEFAULT NULL,
  `comment` varchar(2550) DEFAULT NULL,
  `account` float(45,0) DEFAULT '0',
  `mobile` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `course.id` (`present_course_id`),
  CONSTRAINT `course.id` FOREIGN KEY (`present_course_id`) REFERENCES `courses` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of students
-- ----------------------------
INSERT INTO `students` VALUES ('1', '学生1', null, null, null, null, null, null, null, null, null, null, '1', null, null, null, null, null, '{\"11/02/2016\": {\"courseId\": 1, \"comment\": \"\"}}', null, '0', null);
INSERT INTO `students` VALUES ('2', '学生2', null, null, null, null, null, null, null, null, null, null, '2', null, null, null, null, null, '{}', null, '0', null);
INSERT INTO `students` VALUES ('3', null, null, null, null, null, null, null, null, null, null, null, null, '0.0', null, '0.0', '0', '0', '', null, '0', null);

-- ----------------------------
-- Table structure for teachers
-- ----------------------------
DROP TABLE IF EXISTS `teachers`;
CREATE TABLE `teachers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `chinese_name` varchar(255) DEFAULT NULL,
  `alias_name` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `mobile` varchar(255) DEFAULT NULL,
  `password` varchar(555) DEFAULT NULL,
  `history` varchar(2550) DEFAULT NULL,
  `comment` varchar(2550) DEFAULT NULL,
  `photo` varchar(255) DEFAULT NULL,
  `total_hours` float DEFAULT '0',
  `stage_id` int(3) DEFAULT NULL,
  `prizes` varchar(255) DEFAULT NULL,
  `school` varchar(255) DEFAULT NULL,
  `active` int(255) DEFAULT '0',
  `confirm` int(1) DEFAULT '0',
  `gender` int(11) DEFAULT '0',
  `birthday` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `stage.id` (`stage_id`),
  CONSTRAINT `stage.id` FOREIGN KEY (`stage_id`) REFERENCES `teacherstages` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of teachers
-- ----------------------------
INSERT INTO `teachers` VALUES ('11', '管理员l', 'admin', 'admin', null, '$pbkdf2-sha512$25000$bI2RUgrBOKc0BqD0XiuFEA$1JoSq6IUh9XNJLCcvRA2sqG1cYOxozadi9nnam8Eqsblp0msXBEpQ6AT1PYsG9Ge9cQZ7weqSrS0y0iELBLBlA', null, null, null, '0', '1', null, 'aa', '1', '1', '0', null);
INSERT INTO `teachers` VALUES ('12', '老师ld', null, 'teacher1', null, '$pbkdf2-sha512$25000$bI2RUgrBOKc0BqD0XiuFEA$1JoSq6IUh9XNJLCcvRA2sqG1cYOxozadi9nnam8Eqsblp0msXBEpQ6AT1PYsG9Ge9cQZ7weqSrS0y0iELBLBlA', null, null, null, '1.5', '1', null, 'aaa', '1', '1', '0', null);
INSERT INTO `teachers` VALUES ('15', null, null, '475098936@qq.com', null, '$pbkdf2-sha512$25000$MUao9Z5TypmT0lqL8R7j3A$3X3Lwrln6fCIAUaJclQXoRRFCycZyVJZZft.TttBFQGFVGSGXBvPe9fbAQZfapNL11.N3pCcuSTA1OvHeB3HmA', null, null, null, '0', null, null, null, '1', '0', '0', null);
INSERT INTO `teachers` VALUES ('16', '1231', null, null, null, '$pbkdf2-sha512$25000$K.UcAwAAgBACgFBKCQHA.A$UgRms7rQkUl.rQwXXuG.OYCLUn2sfdGdalGShh5GhNnZHp2z2KUeoofEbXKkgKaScDUT3gDiTYnRRL9/4dxiMg', null, null, null, '0', '1', null, null, null, null, '0', null);

-- ----------------------------
-- Table structure for teacherstages
-- ----------------------------
DROP TABLE IF EXISTS `teacherstages`;
CREATE TABLE `teacherstages` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `payment_per_hour` float(255,1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of teacherstages
-- ----------------------------
INSERT INTO `teacherstages` VALUES ('1', '初级', '80.0');
