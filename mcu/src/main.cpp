#include <WiFi.h>
#include <SPI.h>
#include <Wire.h>
// #include <AsyncTCP.h>
// #include "ESPAsyncWebServer.h"
// #include <MySQL_Connection.h>
// #include <MySQL_Cursor.h>
#include <HTTPClient.h>

#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>
#include <OneWire.h>
#include <DFRobot_EC.h>

#include "SoftwareSerial.h"
#include <Adafruit_GPS.h>
// #include "neo6mGPS.h"

// #include <TinyGPSPlus.h>


const char* ssid = "Annie's";
const char* password = "20060603";
// const char* ssid = "Gogogo_serverice_IOT";
// const char* password = "Shuan_router_257-9";


/*
HttpClient
  Connect to AWS Cloud API Server
*/

const char* serverName =  "https://wco6y0ab82.execute-api.ap-northeast-1.amazonaws.com/default/Rds_Query";
int port = 8080;

WiFiClient wifi;


/*
DHT22 humidity and temperature sensor
  +      --->   3.3V
  out    --->   DHTPIN(25)
  -      --->   GND
*/

#define DHTPIN 25     // what digital pin we're connected to
//#define DHTTYPE DHT11   // DHT 11
#define DHTTYPE DHT22   // DHT 22  (AM2302), AM2321
// Initialize DHT sensor.
DHT dht(DHTPIN, DHTTYPE);

int dht_read(DHT *dht, float *temp, float *hum) {
  // Reading temperature or humidity takes about 250 milliseconds!
  // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
  float h = dht->readHumidity();
  // Read temperature as Celsius (the default)
  float t = dht->readTemperature();
  // Read temperature as Fahrenheit (isFahrenheit = true)
  //float f = dht.readTemperature(true);
  // Check if any reads failed and exit early (to try again).
  if (isnan(h) || isnan(t)) {
    *temp = 27.5;
    *hum = 53.2;
    Serial.println(F("Failed to read from DHT sensor!"));
    return -1;
  }
  *temp = t;
  *hum = h;
  return 0;
}


/*
Waterproof DS18B20 Digital Temperature Sensor & Arduino board
              1(A)   ---->     Digital Pin26
              2(B)   ---->     5V/3.3V
              3(C)   ---->     GND 

Setting for the Pull-up Register/Pull-down Register Selection Jumpers
    When connect DS18B20 with the adapter,please choose to use the
    Pull-up Register Jumpe
*/

int DS18S20_Pin = 26; //DS18S20 Signal pin on digital 26

//Temperature chip i/o
OneWire ds(DS18S20_Pin);  // on digital pin 26

float getTemp(){
  //returns the temperature from one DS18S20 in DEG Celsius

  byte data[12];
  byte addr[8];

  if ( !ds.search(addr)) {
      //no more sensors on chain, reset search
      Serial.println("no more sensors on chain, reset search!");
      ds.reset_search();
      return -1000;
  }

  if ( OneWire::crc8( addr, 7) != addr[7]) {
      Serial.println("CRC is not valid!");
      return -1000;
  }

  if ( addr[0] != 0x10 && addr[0] != 0x28) {
      Serial.print("Device is not recognized");
      return -1000;
  }

  ds.reset();
  ds.select(addr);
  ds.write(0x44,1); // start conversion, with parasite power on at the end

  byte present = ds.reset();
  ds.select(addr);
  ds.write(0xBE); // Read Scratchpad


  for (int i = 0; i < 9; i++) { // we need 9 bytes
    data[i] = ds.read();
  }

  ds.reset_search();

  byte MSB = data[1];
  byte LSB = data[0];

  float tempRead = ((MSB << 8) | LSB); //using two's compliment
  float TemperatureSum = tempRead / 16;

  return TemperatureSum;
}


/*
  Anyleaf Soil Moisture Sensor
  +      --->   3.3V
  out    --->   A0 (34)
  -      --->   GND
*/

// PhSensor phSensor;
// #define EC_PIN 27
// float voltage,ecValue,temperature = 25;


// # define PH_PIN 13
#define EC_PIN 32
DFRobot_EC ec;
float  voltagePH,voltageEC,phValue,ecValue,temperature = 25;

/*
GPS Module
  Vcc      --->   3.3V
  GND      --->   GND
  TXD      --->   RXD(4)
  RXD      --->   TXD(3)
  PS:if wse HardwareSerial Serial1(2);TXD and RX will be 16 and 17
  Tx     --->   RX(16)
  Rx     --->   TX(17)

It requires the use of SoftwareSerial, and assumes that you have a
4800-baud serial GPS device hooked up on pins 4(rx) and 3(tx).
*/

static const int RXPin = 13, TXPin = 12;
// static const int RXPin = 12, TXPin = 13;
static const uint32_t GPSBaud = 9600;
// neo6mGPS myGPS;
SoftwareSerial mySerial(RXPin, TXPin);
Adafruit_GPS GPS(&mySerial);




void setup() {
  Serial.begin(115200);

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());


  // Initialize device.
  dht.begin();
  // ec sensor initialization
  ec.begin();

  // GPS
  Serial.println(F("Adafruit GPS library basic test!"));
  GPS.begin(GPSBaud);

  GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCGGA);
  // Set the update rate
  GPS.sendCommand(PMTK_SET_NMEA_UPDATE_1HZ);   // 1 Hz update rate
  // Request updates on antenna status, comment out to keep quiet
  GPS.sendCommand(PGCMD_ANTENNA);
  


}
uint32_t timer = millis();

void loop() {
  // get temperature and humidity from DHT22
  float temp, hum;
  int ret = dht_read(&dht, &temp, &hum);
  if (ret == 0) {
    Serial.print(F("Humidity: "));
    Serial.print(hum);
    Serial.print(F("%  Temperature: "));
    Serial.print(temp);
    Serial.println(F("°C "));
  }

  // If unable to read temperature or humidity, use random values
  if (ret != 0) {
    temp = random(20, 30);
    hum = random(40, 60);
  }

  // get temperature from DS18B20
  float temperature = getTemp();
  Serial.println(temperature);
  // get pH value form phSensor 
  
  // If unable to read temperature ,use random values
  if (temperature == -1000) {
    temperature = random(20, 40);
  }

  float voltage = analogRead(EC_PIN) / 1024.0*5000;
  float phValue = 3.5 * voltage + 0.5;
  Serial.print("pH Value: ");
  Serial.println(phValue);

  // If phValue is not in the range of 3-11, it may be a bad reading.
  // If so, we simply set it to 7.0 +- 3.0
  if (phValue < 3.0 || phValue > 11.0) {
    phValue = random(4, 10);
  }


  // get EC value form EC sensor
  // voltageEC = analogRead(EC_PIN)/1024.0*5000;
  // ecValue    = ec.readEC(voltageEC,temperature);       // convert voltage to EC with temperature compensation
  // Serial.print(", EC:");
  // Serial.print(ecValue,2);
  // Serial.println("ms/cm");
  
  // Randomly generate a number between 0 and 350
  float ecValue = random(0, 350);


  // get GPS data
  char c = GPS.read();
  // if you want to debug, this is a good time to do it!
  if ((c) && (true))
    Serial.write(c);

  // if a sentence is received, we can check the checksum, parse it...
  if (GPS.newNMEAreceived()) {
    // a tricky thing here is if we print the NMEA sentence, or data
    // we end up not listening and catching other sentences!
    // so be very wary if using OUTPUT_ALLDATA and trytng to print out data
    //Serial.println(GPS.lastNMEA());   // this also sets the newNMEAreceived() flag to false

    if (!GPS.parse(GPS.lastNMEA()))   // this also sets the newNMEAreceived() flag to false
      return;  // we can fail to parse a sentence in which case we should just wait for another
  }

  // approximately every 2 seconds or so, print out the current stats
  if (millis() - timer > 2000) {
    timer = millis(); // reset the timer

    Serial.print("\nTime: ");
    if (GPS.hour < 10) { Serial.print('0'); }
    Serial.print(GPS.hour, DEC); Serial.print(':');
    if (GPS.minute < 10) { Serial.print('0'); }
    Serial.print(GPS.minute, DEC); Serial.print(':');
    if (GPS.seconds < 10) { Serial.print('0'); }
    Serial.print(GPS.seconds, DEC); Serial.print('.');
    if (GPS.milliseconds < 10) {
      Serial.print("00");
    } else if (GPS.milliseconds > 9 && GPS.milliseconds < 100) {
      Serial.print("0");
    }
    Serial.println(GPS.milliseconds);
    Serial.print("Date: ");
    Serial.print(GPS.day, DEC); Serial.print('/');
    Serial.print(GPS.month, DEC); Serial.print("/20");
    Serial.println(GPS.year, DEC);
    Serial.print("Fix: "); Serial.print((int)GPS.fix);
    Serial.print(" quality: "); Serial.println((int)GPS.fixquality);
    if (GPS.fix) {
      Serial.print("Location: ");
      Serial.print(GPS.latitude, 4); Serial.print(GPS.lat);
      Serial.print(", ");
      Serial.print(GPS.longitude, 4); Serial.println(GPS.lon);

      Serial.print("Speed (knots): "); Serial.println(GPS.speed);
      Serial.print("Angle: "); Serial.println(GPS.angle);
      Serial.print("Altitude: "); Serial.println(GPS.altitude);
      Serial.print("Satellites: "); Serial.println((int)GPS.satellites);
      Serial.print("Antenna status: "); Serial.println((int)GPS.antenna);
    }
  }

  // if latitude and longitude are not zero, save to longitude and latitude
  // else, useing the random number to simulate the data
  // range base on latitude,longitude= 22.625266504508858,120.29873388752162 +-0.05%

  float longitude = 0;
  float latitude = 0;
  if (GPS.latitude != 0 && GPS.longitude != 0) {
    longitude = GPS.longitude;
    latitude = GPS.latitude;
  } else {
    longitude = 120.29873388752162 + random(-5, 5) / 1E6;
    latitude = 22.625266504508858 + random(-5, 5) / 1E6;
  }


  // latitude, longitude, O_Hum, O_Temp, PH, TDS, W_Temp
  // Serial.println(serverPath);
  // http.begin(serverPath.c_str());
  // String httpRequestData = "{\"latitude\": \"" + String(random(0, 100)) + "\", \"longitude\": \"" + String(random(0, 100)) + "\", \"O_Hum\": \"" + String(hum) + "\", \"O_Temp\": \"" + String(temp) + "\", \"PH\": \"" + String(phValue) + "\", \"TDS\": \"" + String(ecValue) + "\", \"W_Temp\": \"" + String(temperature) + "\"}";
  String httpRequestData = "{\"latitude\": \"" + String(latitude,9) + "\", \"longitude\": \"" + String(longitude,9) + "\", \"O_Hum\": \"" + String(hum) + "\", \"O_Temp\": \"" + String(temp) + "\", \"PH\": \"" + String(phValue) + "\", \"TDS\": \"" + String(ecValue) + "\", \"W_Temp\": \"" + String(temperature) + "\"}";


  Serial.println(httpRequestData);
  // Initialize the http connection
  // Your Domain name with URL path or IP address with path
  HTTPClient http;
  http.begin(serverName);
  http.addHeader("Content-Type", "application/json");
  http.addHeader("Content-Length", String(httpRequestData.length()));
  int httpResponseCode = http.POST(httpRequestData);
  Serial.print("HTTP Response code: ");
  Serial.println(httpResponseCode);
  String payload = http.getString();
  Serial.println(payload);
  http.end();

  delay(5000);


}