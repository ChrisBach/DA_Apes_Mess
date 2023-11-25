USE da_my_mess;
DELETE FROM da_my_mess.apes_messages WHERE sender IN ("Unknown Sender", "Group photo");

SELECT * FROM da_my_mess.apes_messages;

ALTER TABLE da_my_mess.apes_messages
ADD COLUMN date DATE,
ADD COLUMN time TIME;

CREATE FUNCTION da_my_mess.to_date(timestamp VARCHAR(255), format VARCHAR(255))
RETURNS DATE
LANGUAGE SQL
BEGIN
  RETURN STR_TO_DATE(timestamp, format);
END;


USE da_my_mess;
UPDATE apes_messages
SET date = to_date(timestamp, '%b %d, %Y'),
time = to_time(timestamp);


INSERT INTO da_my_mess.apes_messages (date, time)
SELECT date, time FROM da_my_mess.apes_messages;



