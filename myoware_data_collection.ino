/*
  MyoWare Example_01_analogRead_SINGLE
  SparkFun Electronics
  Pete Lewis
  3/24/2022
  License: This code is public domain but you buy me a beverage if you use this and we meet someday.
  This code was adapted from the MyoWare analogReadValue.ino example found here:
  https://github.com/AdvancerTechnologies/MyoWare_MuscleSensor

  This example streams the data from a single MyoWare sensor attached to ADC A0.
  Graphical representation is available using Serial Plotter (Tools > Serial Plotter menu).

  *Only run on a laptop using its battery. Do not plug in laptop charger/dock/monitor.
  
  *Do not touch your laptop trackpad or keyboard while the MyoWare sensor is powered.

  Hardware:
  SparkFun RedBoard Artemis (or Arduino of choice)
  USB from Artemis to Computer.
  Output from sensor connected to your Arduino pin A0
  
  This example code is in the public domain.
*/

void setup() 
{
  Serial.begin(115200);
  while (!Serial);
  Serial.println("timestamp,emg"); // CSV header
}

void loop() 
{  
  Serial.print(millis());
  Serial.print(",");
  //Make sure the analog pin matches to what you have connected too
  Serial.println(analogRead(A0));
  delay(50);
}