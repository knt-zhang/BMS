-- bank management system sql

-- paste below here

CREATE DATABASE bank_management_system;
USE bank_management_system;

### Creating tables ###
# -- bank
CREATE TABLE IF NOT EXISTS bank (idBank integer PRIMARY KEY NOT NULL DEFAULT 1,name text NOT NULL,address text NOT NULL);

# -- branch
CREATE TABLE IF NOT EXISTS branch (idBranch integer PRIMARY KEY NOT NULL AUTO_INCREMENT,name text NOT NULL,address text NOT NULL,idBank integer NOT NULL DEFAULT 1,FOREIGN KEY (idBank) REFERENCES bank (idBank));

# -- clients
CREATE TABLE IF NOT EXISTS clients (idClient integer PRIMARY KEY NOT NULL AUTO_INCREMENT,name text NOT NULL,address text NOT NULL,phone text NOT NULL,idBranch integer NOT NULL,FOREIGN KEY (idBranch) REFERENCES branch (idBranch));

# -- account
CREATE TABLE IF NOT EXISTS account (idAccount integer PRIMARY KEY NOT NULL AUTO_INCREMENT,account_type text NOT NULL, idBranch integer NOT NULL, idClient integer NOT NULL,FOREIGN KEY (idBranch) REFERENCES branch(idBranch),FOREIGN KEY (idClient) REFERENCES clients (idClient));

# -- checking
CREATE TABLE IF NOT EXISTS checking (idChecking integer PRIMARY KEY NOT NULL AUTO_INCREMENT, balance integer NOT NULL, idAccount integer NOT NULL, FOREIGN KEY (idAccount) REFERENCES account (idAccount));

# -- saving
CREATE TABLE IF NOT EXISTS saving (idSaving integer PRIMARY KEY NOT NULL AUTO_INCREMENT, balance integer NOT NULL, interest integer NOT NULL ,idAccount integer NOT NULL, FOREIGN KEY (idAccount) REFERENCES account (idAccount));

# -- credit_card
CREATE TABLE IF NOT EXISTS credit_card (idCredit_Card integer PRIMARY KEY NOT NULL AUTO_INCREMENT, balance integer NOT NULL, credit_limit integer NOT NULL, idAccount integer NOT NULL, FOREIGN KEY (idAccount) REFERENCES account (idAccount));

# -- loan
CREATE TABLE IF NOT EXISTS loan (idLoan integer PRIMARY KEY NOT NULL AUTO_INCREMENT, type_of_loan text NOT NULL, amount integer NOT NULL, idAccount integer NOT NULL, FOREIGN KEY (idAccount) REFERENCES account (idAccount));

# -- checking_records
CREATE TABLE checking_records (id INT AUTO_INCREMENT PRIMARY KEY,	idAccount INT, before_balance INT NOT NULL, after_balance INT NOT NULL);

# -- updated_client_records
CREATE TABLE updated_client_records (id INT AUTO_INCREMENT PRIMARY KEY, idClient INT, name TEXT, address TEXT, phone TEXT, idBranch INT);

### Inserting values ###
#-- bank
INSERT INTO bank (Name, Address) VALUES ('Cello Bank', '100 Fake Street, Newton NY 88888');

# -- branch
INSERT INTO branch (Name, Address) VALUES ('Broadway', '214 Broadway, New York, NY 10038'), ('23rd St', '333 E 23rd St, New York, NY 10010'), ('2nd Ave', '156 2nd Ave, New York, NY 10003');

# -- clients
INSERT INTO clients (Name, Address, Phone, idBranch) VALUES
('John Smith', '680 Cantebury Drive New York, NY 10018', "718-123-4567", 1),
('Robert T. Noble', '3865 Longview Avenue Forest Hills, NY 11375', '718-544-1466', 1),
('Wilma H. Luna', '2523 Irving Place Smithtown, NY 11787', '631-979-3610', 2),
('Margaret J. Thomas', '1550 Grove Street Selden, NY 11784', "757-596-0135", 2),
('Lawrence B. Jamerson', '173 Pallet Street West Nyack, NY 10994', "312-315-1195", 3),
('Frances L. Beardsley', '3344 Turkey Pen Road West Nyack, NY 10994', "319-472-4291", 3),
('Christopher T. Weathersby', '3638 Benedum Drive Garden City, NY 11530', '803-781-7654', 1),
('Charles R. Ohara', '2124 Patterson Road Bronx, NY 10461', '910-863-0788', 1),
('Pamela J. Scott', '4037 Feathers Hooves Drive New York, NY 10005', '765-447-7366', 1),
('Robyn D. Headley', '3541 Saint Marys Avenue Utica, NY 13502', '828-893-0846', 1),
('Stanley S. Jenkins', '2494 Angus Road New York, NY 10038', '850-437-3323', 2),
('Harry R. Hinds', '1830 Redbud Drive West Nyack, NY 10994', '410-575-5314', 2),
('Alice T. Laplant', '3355 Deans Lane White Plains, NY 10641', '858-586-2644', 2),
('Hong R. Loving', '2388 Turkey Pen Road New York, NY 10019', '214-923-7194', 2),
('Rebecca J. Haywood', '161 Dancing Dove Lane New York, NY 10013', '973-831-2790', 3),
('Patricia D. Swarey', '2904 Church Street New York, NY 10013', '903-678-3756', 3),
('Donna J. Garcia', '578 Settlers Lane New York, NY 10016', '608-274-2030', 3),
('Mara J. Miller', '2273 Church Street Queens, NY 11418', '931-346-6673', 3);

# -- account
INSERT INTO account (account_type, idBranch, idClient) VALUES
('checking', 1, 1), ('credit_card', 1, 1), ('checking', 1, 2), ('loan', 1, 2),
('checking', 2, 3), ('checking', 2, 4), ('saving', 2, 4),
('checking', 3, 5), ('credit_card', 3, 5), ('credit_card', 3, 6),
('checking', 1, 7), ('credit_card', 1, 7), ('saving', 1, 7), ('loan', 1, 7),
('checking', 1, 8), ('credit_card', 1, 8), ('saving', 1, 8), ('loan', 1, 8),
('checking', 1, 9), ('credit_card', 1, 9), ('saving', 1, 9), ('loan', 1, 9),
('checking', 1, 10), ('credit_card', 1, 10), ('saving', 1, 10), ('loan', 1, 10),
('checking', 2, 11), ('credit_card', 2, 11), ('saving', 2, 11), ('loan', 2, 11),
('checking', 2, 12), ('credit_card', 2, 12), ('saving', 2, 12), ('loan', 2, 12),
('checking', 2, 13), ('credit_card', 2, 13), ('saving', 2, 13), ('loan', 2, 13),
('checking', 2, 14), ('credit_card', 2, 14), ('saving', 2, 14), ('loan', 2, 14),
('checking', 3, 15), ('credit_card', 3, 15), ('saving', 3, 15), ('loan', 3, 15),
('checking', 3, 16), ('credit_card', 3, 16), ('saving', 3, 16), ('loan', 3, 16),
('checking', 3, 17), ('credit_card', 3, 17), ('saving', 3, 17), ('loan', 3, 17),
('checking', 3, 18), ('credit_card', 3, 18), ('saving', 3, 18), ('loan', 3, 18);

# -- checking
INSERT INTO checking (Balance, idAccount) VALUES
(750, 1), (12000, 3), (3000, 5),
(2300, 6), (4500, 8), (35000 , 11),
(20000 , 15),(6455 , 19), (8002 , 23),
(10034 , 27), (2334 , 31), (9345 , 35),
(2125 , 39), (68748 , 43), (21353 , 47),
(15335 , 51), (1542 , 55);

# -- saving
INSERT INTO saving (Balance, interest, idAccount) VALUES
(38000, 0.55, 7), (10000, 0.55, 13), (10000, 0.55, 17),(10000, 0.55, 21),
(10000, 0.55, 25), (10000, 0.55, 29), (10000, 0.55, 33), (10000, 0.55, 37),
(10000, 0.55, 41), (10000, 0.55, 45), (10000, 0.55, 49), (10000, 0.55, 53), (10000, 0.55, 57);

# -- credit_card
INSERT INTO credit_card (balance, credit_limit, idAccount) VALUES
(700,5000,2), (570,7500,9), (2300,10000,10), (3222, 10000, 12), (5000, 25000, 16),
(2300, 10000, 20), (800, 10000, 24), (8633, 25000, 28), (14002, 50000, 32), (3698, 50000, 36),
(4558, 25000, 40), (989, 50000, 44), (32100, 100000, 48), (1355, 50000, 52), (6335, 50000, 56);

# -- loan
INSERT INTO loan (type_of_loan, amount, idAccount) VALUES
('student loans', 55000, 4), ('student loans', 55000, 14),
('personal loans', 22000, 18), ('auto loans', 15000, 22), ('mortgage loans', 150000, 26),
('mortgage loans', 550000, 30), ('auto loans', 60000, 34), ('student loans', 90000, 38),
('student loans', 155000, 42), ('personal loans', 10000, 46), ('personal loans', 8000, 50),
('auto loans', 32110, 54), ('mortgage loans', 25130, 58);
