CREATE DATABASE flightsDatabase;
use flightsDatabase;

CREATE TABLE flights (
  source VARCHAR(20),
  dest VARCHAR(20),
  departureDay INT,
  departureHour INT,
  duration INT,
  numberOfSeats INT,
  flightId INT,
  books INT,
  boughtTickets INT
);

INSERT INTO flights (source, dest, departureDay, departureHour, duration, numberOfSeats, flightId, books, boughtTickets) VALUES ('Bucuresti', 'Timisoara', 122, 12, 2, 140, 5004, 0, 0);

INSERT INTO flights (source, dest, departureDay, departureHour, duration, numberOfSeats, flightId, books, boughtTickets) VALUES ('Bucuresti', 'Londra', 126, 16, 4, 140, 5006, 0, 0);

INSERT INTO flights (source, dest, departureDay, departureHour, duration, numberOfSeats, flightId, books, boughtTickets) VALUES ('Londra', 'Paris', 129, 2, 3, 140, 5007, 0, 0);

INSERT INTO flights (source, dest, departureDay, departureHour, duration, numberOfSeats, flightId, books, boughtTickets) VALUES ('Londra', 'Paris', 129, 4, 7, 140, 5008, 0, 0);

INSERT INTO flights (source, dest, departureDay, departureHour, duration, numberOfSeats, flightId, books, boughtTickets) VALUES ('Paris', 'Madrid', 129, 6, 2, 140, 5009, 0, 0);

INSERT INTO flights (source, dest, departureDay, departureHour, duration, numberOfSeats, flightId, books, boughtTickets) VALUES ('Paris', 'Madrid', 129, 4, 1, 140, 5010, 0, 0);
