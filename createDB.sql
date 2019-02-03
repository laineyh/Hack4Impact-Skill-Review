CREATE DATABASE applications;
USE applications;
CREATE TABLE applications.applicants (
	applicant_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    applicant_firstname VARCHAR(20) NOT NULL,
	applicant_lastname VARCHAR(30) NOT NULL,
    applicant_prefname VARCHAR(20),
    applicant_pronouns VARCHAR(20),
    applicant_email VARCHAR(50) NOT NULL,
    applicant_year TINYINT(5) UNSIGNED,
    applicant_major VARCHAR(50),
    applicant_minor VARCHAR(50),
    applicant_time TINYINT UNSIGNED,
    applicant_experience TEXT,
    applicant_techimpact TEXT,
    applicant_personalimpact TEXT,
    applicant_other TEXT DEFAULT NULL,
    PRIMARY KEY (applicant_id));
    
DELIMITER //
 CREATE DEFINER=`root`@`localhost` PROCEDURE `createApplication`(
IN firstname VARCHAR(20),
IN lastname VARCHAR(30),
IN prefname VARCHAR(20),
IN pronouns VARCHAR(20),
IN email VARCHAR(50),
IN gradyear TINYINT(5),
IN major VARCHAR(50),
IN minor VARCHAR(50),
IN timeavail TINYINT,
IN experience TEXT,
IN techimpact TEXT,
IN personalimpact TEXT,
IN other TEXT
)
BEGIN
IF (select exists (select 1 from applicants where applicant_email = email) ) THEN
	SELECT "You've already submitted an application";
ELSE
	insert into applicants 
	(
		applicant_firstname,
		applicant_lastname,
		applicant_prefname,
		applicant_pronouns,
		applicant_email,
		applicant_year,
		applicant_major,
		applicant_minor,
		applicant_time,
		applicant_experience,
		applicant_techimpact,
		applicant_personalimpact,
		applicant_other
	)
	values
	(
		firstname,
		lastname,
		prefname,
		pronouns,
		email,
		gradyear,
		major,
		minor,
		timeavail,
		experience,
		techimpact,
		personalimpact,
		other
	);
END IF;
END //
DELIMITER ;
    
    
    
    