Create table boat_data(
ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
latitude float  DEFAULT 22.625266504508858,
longitude float  DEFAULT 120.29873388752162,
O_Hum float DEFAULT 47,
O_Temp float DEFAULT 28,
PH float DEFAULT 7.8,
TDS float DEFAULT 120,
W_Temp float DEFAULT 30,
PRIMARY KEY (ts)
);
 
-- INSERT INTO boat_data(latitude,longitude,O_Hum,O_Temp,PH,TDS,W_Temp) VALUES (22.625266504508858,120.29873388752162,47,28,7.8,120,30);
INSERT INTO boat_data(latitude,longitude,O_Hum,O_Temp,PH,TDS,W_Temp) VALUES (22.625266504508858,120.29873388752162,47,28,7.8,120,30);

-- SELECT * FROM boat_data;
SELECT * FROM boat_data;

Drop Table boat_data ;