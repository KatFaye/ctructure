DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_createUser`(
IN _firstname VARCHAR(30),
IN _lastname VARCHAR(30),
IN _username VARCHAR(30),
IN _email VARCHAR(30),
IN _password VARCHAR(30)
)
BEGIN
  insert into users
  (
   firstname,
   lastname,
   username,
   email,
   password
)
values
   (
   _firstname,
   _lastname,
   _username,
   _email,
   _password
);

END$$
DELIMITER ;

