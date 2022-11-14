#include <WiFi.h>
#include <SPI.h>
#include <Wire.h>
// #include <AsyncTCP.h>
// #include "ESPAsyncWebServer.h"

#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>
#include <OneWire.h>
#include <DFRobot_EC.h>

#include <TinyGPSPlus.h>

const char* ssid = "Gogogo_serverice_IOT";
const char* password = "Shuan_router_257-9";


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

// GPS sensor
TinyGPSPlus gps;


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

}

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
  // get temperature from DS18B20
  float temperature = getTemp();
  Serial.println(temperature);
  // get pH value form phSensor 
  
  // float voltage = analogRead(PH_PIN) / 1024.0*5000;
  // float phValue = 3.5 * voltage + 0.5;
  // Serial.print("pH Value: ");
  // Serial.println(phValue);

  // get EC value form EC sensor
  voltageEC = analogRead(EC_PIN)/1024.0*5000;
  ecValue    = ec.readEC(voltageEC,temperature);       // convert voltage to EC with temperature compensation
  Serial.print(", EC:");
  Serial.print(ecValue,2);
  Serial.println("ms/cm");

  delay(2000);

}