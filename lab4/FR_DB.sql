CREATE TABLE `Employee_Position`
(
 `positionID` char(1) NOT NULL ,
 `postion`    char(10) NOT NULL ,

PRIMARY KEY (`positionID`)
);


CREATE TABLE `Employee`
(
 `userID`             char(6) NOT NULL ,
 `firstname`          char(20) NOT NULL ,
 `surname`            char(20) NOT NULL ,
 `nickname`           char(10) NOT NULL ,
 `lineID`             char(20) NOT NULL ,
 `phone`              char(10) NOT NULL ,
 `status`             tinyint NOT NULL ,
 `notificaiotnStatus` tinyint NOT NULL ,
 `positionID`         char(1) NOT NULL ,

PRIMARY KEY (`userID`),
KEY `FK_Employee_EmployeePos` (`positionID`),
CONSTRAINT `FK_Employee_Position` FOREIGN KEY `FK_Employee_EmployeePos` (`positionID`) REFERENCES `Employee_Position` (`positionID`)
);


CREATE TABLE `Authentication`
(
 `user`      char(6) NOT NULL ,
 `password`  char(20) NOT NULL ,
 `loginDate` datetime NOT NULL ,
 `picFile`   char(10) NOT NULL ,
 `level`     char(1) NOT NULL ,
 `userID`    char(6) NOT NULL ,

PRIMARY KEY (`userID`),
KEY `FK_Auth_Employee` (`userID`),
CONSTRAINT `FK_Auth` FOREIGN KEY `FK_Auth_Employee` (`userID`) REFERENCES `Employee` (`userID`)
);

CREATE TABLE `Customer_Type`
(
 `typeID` char(1) NOT NULL ,
 `type`   char(10) NOT NULL ,

PRIMARY KEY (`typeID`)
);

CREATE TABLE `Customer`
(
 `userID`     char(6) NOT NULL ,
 `fullname`   char(20) NOT NULL ,
 `surname`    char(20) NOT NULL ,
 `nickname`   char(10) NOT NULL ,
 `dateCreate` datetime NOT NULL ,
 `status`     tinyint NOT NULL ,
 `picFolder`  char(10) NOT NULL ,
 `typeID`     char(1) NOT NULL ,

PRIMARY KEY (`userID`),
KEY `FK_Customer_CustomerType` (`typeID`),
CONSTRAINT `FK_TypeID` FOREIGN KEY `FK_Customer_CustomerType` (`typeID`) REFERENCES `Customer_Type` (`typeID`)
);

CREATE TABLE `User_Entry`
(
 `userID`  char(6) NOT NULL ,
 `dateIn`  datetime NOT NULL ,
 `dateOut` datetime NOT NULL ,
 `picFile` char(10) NOT NULL ,

PRIMARY KEY (`userID`),
KEY `FK_UserEntry_Custome` (`userID`),
CONSTRAINT `FK_UserID_Employee` FOREIGN KEY `FK_UserEntry_Custome` (`userID`) REFERENCES `Employee` (`userID`),
KEY `FK_UserEntry_Custome2` (`userID`),
CONSTRAINT `FK_UserID_Customer` FOREIGN KEY `FK_UserEntry_Custome2` (`userID`) REFERENCES `Customer` (`userID`)
);