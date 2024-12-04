DROP TABLE IF EXISTS `Booking`;
DROP TABLE IF EXISTS `Disponibility`;
DROP TABLE IF EXISTS `Page`;
DROP TABLE IF EXISTS `User`;

CREATE TABLE IF NOT EXISTS `User` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `firstName` VARCHAR(255) NOT NULL,
  `lastName` VARCHAR(255) NOT NULL,
  `username` VARCHAR(255) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `Page` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `visible` ENUM('true', 'false') NOT NULL,
  `page_name` VARCHAR(255),
  `description` TEXT,
  `activity` TEXT,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`user_id`) REFERENCES `User`(`id`) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `Disponibility` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `date` DATETIME NULL,
  `page_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`page_id`) REFERENCES `Page`(`id`) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `Booking` (
  `disponibility_id` INT NOT NULL,
  `cancel_code` VARCHAR(255) NOT NULL,
  `mail` VARCHAR(255) NOT NULL,
  `name` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`disponibility_id`),
  FOREIGN KEY (`disponibility_id`) REFERENCES `Disponibility`(`id`) ON DELETE CASCADE
);
