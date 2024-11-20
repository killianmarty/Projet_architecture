BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "Appointment" (
	"disponibility_id"	INTEGER NOT NULL,
	"cancel_code"	TEXT NOT NULL,
	"mail"	TEXT NOT NULL,
	"name"	TEXT NOT NULL,
	PRIMARY KEY("disponibility_id"),
	FOREIGN KEY("disponibility_id") REFERENCES "Disponibility"("id")
);
CREATE TABLE IF NOT EXISTS "Disponibility" (
	"id"	INTEGER NOT NULL UNIQUE,
	"date"	INTEGER NOT NULL,
	"page_id"	INTEGER NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("page_id") REFERENCES "Page"("id")
);
CREATE TABLE IF NOT EXISTS "Page" (
	"id"	INTEGER NOT NULL UNIQUE,
	"user_id"	INTEGER NOT NULL,
	"visible"	INTEGER NOT NULL,
	"page_name"	TEXT,
	"description"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("user_id") REFERENCES "User"("id")
);
CREATE TABLE IF NOT EXISTS "User" (
	"id"	INTEGER NOT NULL UNIQUE,
	"firstName"	TEXT NOT NULL,
	"lastName"	TEXT NOT NULL,
	"username"	TEXT NOT NULL,
	"password"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
COMMIT;
