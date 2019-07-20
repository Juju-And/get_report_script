CREATE DATABASE costs_db;

CREATE TABLE Costs (
    id serial,
    purpose varchar(255),
    description text,
    amount decimal(10,2)
);


INSERT INTO costs(purpose, description, amount) VALUES ('szkolenia', 'bootcamp', 10);
INSERT INTO costs(purpose, description, amount) VALUES ('rozrywka', 'kursy tańca', 50);
INSERT INTO costs(purpose, description, amount) VALUES ('wypoczynek', 'lot w kosmos', 90);
INSERT INTO costs(purpose, description, amount) VALUES ('remont', 'szpachla i farba', 80);