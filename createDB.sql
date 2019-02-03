CREATE DATABASE applications;
USE applications;

/* each row is a submitted application, columns correspond to application questions */
CREATE TABLE applications.applicants (
	applicant_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    applicant_firstname VARCHAR(20) NOT NULL,
	applicant_lastname VARCHAR(30) NOT NULL,
    applicant_prefname VARCHAR(20), /* preferred name, optional field, auto-populates with first name if no preferred name is given */
    applicant_pronouns VARCHAR(20),
    applicant_email VARCHAR(50) NOT NULL,
    applicant_year TINYINT(5) UNSIGNED, /* numbers 1-4 correspond to class years, 5 is for grad students */
    applicant_major VARCHAR(50),
    applicant_minor VARCHAR(50), /* optional field */
    applicant_time TINYINT UNSIGNED, /* hours per week the applicant is willing to commit */
    applicant_experience TEXT, 
    applicant_techimpact TEXT, /* second short-answer application question */
    applicant_personalimpact TEXT, /* first short-answer application question */
    applicant_other TEXT DEFAULT NULL, /* any additional info, optional field */
    PRIMARY KEY (applicant_id));
    
/* create stored procedure for adding new applications to database */
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
    
    
    
    