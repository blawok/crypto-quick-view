select * from cryptoStats;
select * from cryptoStatsUser;
select * from cryptoDict;

drop table if exists cryptoStats;
drop table if exists cryptoStatsUser;
drop table if exists cryptoDict;

CREATE TABLE cryptoStats ("index" INTEGER, createdDate DEFAULT (datetime('now')), Date DATE, Open REAL, High REAL, Low REAL, Close REAL, Volume REAL, "Market Cap" REAL, Currency TEXT);
CREATE TABLE cryptoStatsUser ("index" INTEGER, createdDate DEFAULT (datetime('now')), Date DATE, Open REAL, High REAL, Low REAL, Close REAL, Volume REAL, "Market Cap" REAL, Currency TEXT);
CREATE TABLE cryptoDict ("index" INTEGER, CurrencyShort TEXT, Currency TEXT);

delete from cryptoStats where Currency = 'lisk';
delete from cryptoStatsUser where Currency = 'lisk';
delete from cryptoStatsTemp where Currency = 'lisk';
delete from cryptoStats where Currency = 'XRP';


select distinct Currency from cryptoStats;
select * from cryptoStats where Currency = 'lisk' and Date = '2017-09-01';
select * from cryptoStats where Currency = 'XRP';

select * from cryptoStats where Currency = 'ripple' and strftime('%Y', Date) = '2017';

PRAGMA foreign_keys=off;

BEGIN TRANSACTION;

ALTER TABLE cryptoStats RENAME TO old_cryptoStats;

CREATE TABLE cryptoStats (
 "index" INTEGER PRIMARY KEY, createdDate DEFAULT (datetime('now')), Date DATE, Open REAL, High REAL, Low REAL, Close REAL, Volume REAL, "Market Cap" REAL, Currency TEXT, foreign key(Date, Currency) REFERENCES cryptoStatsUser );

INSERT INTO cryptoStats SELECT * FROM old_cryptoStats;

DROP TABLE old_cryptoStats;

COMMIT;

PRAGMA foreign_keys=on;




PRAGMA foreign_keys=off;

BEGIN TRANSACTION;

ALTER TABLE cryptoDict RENAME TO old_cryptoDicts;

CREATE TABLE cryptoDict (
 CurrencyShort TEXT, Currency TEXT
);

INSERT INTO cryptoDict SELECT * FROM old_cryptoDicts;

DROP TABLE old_cryptoDicts;

COMMIT;

PRAGMA foreign_keys=on;




insert into cryptoDict
(Currency, CurrencyShort)
values
('lisk', 'LSK'),
('bitcoin', 'BTC'),
('ripple', 'XRP'),
('ethereum', 'ETH'),
('litecoin', 'LTC')


PRAGMA foreign_keys=off;

BEGIN TRANSACTION;

ALTER TABLE cryptoStatsUser RENAME TO old_cryptoStatsUser;

CREATE TABLE cryptoStatsUser (
 "index" INTEGER PRIMARY KEY, Date DATE, Open REAL, High REAL, Low REAL, Close REAL, Volume REAL, "Market Cap" REAL, Currency TEXT
);

INSERT INTO cryptoStatsUser SELECT * FROM old_cryptoStatsUser;

DROP TABLE old_cryptoStatsUser;

COMMIT;

PRAGMA foreign_keys=on;
