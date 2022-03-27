/* Create table Bqsket */

use Basket;

DROP TABLE IF EXISTS `Court`;
CREATE TABLE `Court` (
  `court_id` int(20) NOT NULL,
  `sport` varchar(20) NOT NULL,
  `city` varchar(20) NOT NULL,
  `adress` varchar(100) NOT NULL,
  `price` int(20) NOT NULL,
	PRIMARY KEY (`court_id`),
    UNIQUE KEY `id_UNIQUE` (`court_id`)
);

DROP TABLE IF EXISTS `Reservation`;
CREATE TABLE `Reservation` (
    `id` varchar(30) NOT NULL,
    `name` varchar(30) NOT NULL,
	`court_id` varchar(20) NOT NULL,
	`time` varchar(30) NOT NULL,
      PRIMARY KEY (`id`),
      UNIQUE KEY (`id`),
      KEY `FK_court_idx` (`court_id`)
);




