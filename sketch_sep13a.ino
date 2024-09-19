#include <ArdusatSDK.h>

Luminosity lum;
Temperature temp;

void setup(void) {
  Serial.begin(9600);
  lum.begin();
  temp.begin();
}


void loop(void) {
  delay(6000);
  //Serial.println(lum.readToJSON("Luminosity")); // >> ~{"sensorName": "Luminosity", "unit": "lux", "value": 123.5, "cs": 43}|
  //Serial.println(lum.readToJSON("lum2"));       // >> ~{"sensorName": "lum2", "unit": "lux", "value": 121.9, "cs": 30}|
  //Serial.println(lum.readToCSV("Luminosity"));  // >> 243,Luminosity,128.2,49
  //Serial.println(lum.readToCSV("lum4"));        // >> 311,lum4,124.6,29
  //Serial.println(lum.lux);                      // >> 124.6
  //Serial.println(lum.lux);                      // >> 124.6
  lum.read();
  Serial.println(lum.lux);                      // >> 127.5

  Serial.println(temp.readToJSON("Temperature"));
  temp.read();
  //Serial.println(temp.temperature);
}
