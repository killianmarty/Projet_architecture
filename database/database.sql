BEGIN TRANSACTION;
DROP TABLE IF EXISTS "Disponibility";
CREATE TABLE IF NOT EXISTS "Disponibility" (
	"id"	INTEGER NOT NULL UNIQUE,
	"date"	INTEGER NOT NULL,
	"page_id"	INTEGER NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("page_id") REFERENCES "Page"("id")
);
DROP TABLE IF EXISTS "User";
CREATE TABLE IF NOT EXISTS "User" (
	"id"	INTEGER NOT NULL UNIQUE,
	"firstName"	TEXT NOT NULL,
	"lastName"	TEXT NOT NULL,
	"username"	TEXT NOT NULL,
	"password"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "Booking";
CREATE TABLE IF NOT EXISTS "Booking" (
	"disponibility_id"	INTEGER NOT NULL,
	"cancel_code"	TEXT NOT NULL,
	"mail"	TEXT NOT NULL,
	"name"	TEXT NOT NULL,
	FOREIGN KEY("disponibility_id") REFERENCES "Disponibility"("id"),
	PRIMARY KEY("disponibility_id")
);
DROP TABLE IF EXISTS "Page";
CREATE TABLE IF NOT EXISTS "Page" (
	"id"	INTEGER NOT NULL UNIQUE,
	"user_id"	INTEGER NOT NULL,
	"visible"	TEXT NOT NULL,
	"page_name"	TEXT,
	"description"	TEXT,
	"activity"	TEXT,
	FOREIGN KEY("user_id") REFERENCES "User"("id"),
	PRIMARY KEY("id" AUTOINCREMENT)
);
COMMIT;
