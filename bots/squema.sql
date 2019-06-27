DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;

CREATE TABLE wakeUpTime (
groupId text ,
channelName TEXT,
wakeUpTime TIMESTAMP NOT NULL
);
