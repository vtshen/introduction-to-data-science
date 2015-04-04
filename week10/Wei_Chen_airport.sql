
-- Problem 1

CREATE TABLE flights (
    year INT,
    month INT,
    dayOfMonth INT,
    dayOfWeek INT,
    actualDepartureTime INT,
    scheduledDepartureTime INT,
    arrivalArrivalTime INT,
    scheduledArrivalTime INT,
    uniqueCarrierCode TEXT,
    flightNumber INT,
    tailNumber TEXT,
    actualElapsedTime INT,
    scheduledElapsedTime INT,
    airTime INT,
    arrivalDelay INT,
    departureDelay INT,
    originCode TEXT,
    destinationCode TEXT,
    distance INT,
    taxiIn INT,
    taxiOut INT,
    cancelled INT,
    cancellationCode TEXT,
    diverted TEXT,
    carrierDelay INT,
    weatherDelay INT,
    nasDelay INT,
    securityDelay INT,
    lateAircraftDelay INT
);

.separator ","
.import /data/airline/2001.csv flights


DELETE FROM flights WHERE YEAR = 'Year';

SELECT COUNT(*) FROM flights;

CREATE TABLE iata(
    airportID INT,
    name TEXT,
    city TEXT, 
    country TEXT, 
    iata TEXT, 
    icao TEXT, 
    latitude REAL, 
    longitude REAL, 
    altitude INT, 
    timeZone INT, 
    dst TEXT, 
    tzDatabaseTimeZone TEXT
);

.separator ","
.import iata.csv iata

SELECT COUNT(*) FROM iata;

-- Problem 2


CREATE TABLE myTable AS
SELECT 
month, dayOfMonth, uniqueCarrierCode, flightNumber, scheduledDepartureTime, diverted, originCity, i.city AS destinationCity
FROM
(SELECT 
f.month, f.dayOfMonth, f.uniqueCarrierCode, f.flightNumber, f.scheduledDepartureTime, f.diverted, i.city AS originCity, f.destinationCode
FROM 
flights AS f LEFT OUTER JOIN iata AS i 
ON f.originCode = i.iata 
) LEFT OUTER JOIN iata AS i
ON destinationCode = i.iata
;


SELECT COUNT(*) FROM myTable;

INSERT INTO myTable
VALUES(9, 9, "INFO", 490, 0800, "1", "Champaign", "Chicago");

SELECT COUNT(*) FROM myTable;


-- Problem 3


SELECT AVG(departureDelay) FROM flights WHERE departureDelay <> "NA";
SELECT MAX(departureDelay) FROM flights WHERE departureDelay <> "NA";
SELECT MIN(departureDelay) FROM flights WHERE departureDelay <> "NA";

SELECT month, dayOfMonth, uniqueCarrierCode, flightNumber FROM flights
WHERE (scheduledDepartureTime < 0815) AND (scheduledDepartureTime > 0745) AND (diverted == "1") 
AND (destinationCode = (SELECT iata.iata FROM iata WHERE iata.city = "San Francisco"))
AND (originCode = (SELECT iata.iata FROM iata WHERE iata.city = "Newark"))
;