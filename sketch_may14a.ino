#include "HX711.h"                                     // Код для считывания с тензодачика и записи на порт                              
                                            
    
HX711 scale;                                                  
uint8_t DOUT_PIN = A1;                                                                                   
uint8_t SCK_PIN  = A0;  
float calibration_factor = 5;                          // калибровачный фактор определяется методом сравнения для более точных данных
float units;                                                 
float ounces;   
int count;                                             // задаём переменную для измерений в унциях

void setup() {
  Serial.begin(9600);                                        
  scale.begin(DOUT_PIN, SCK_PIN);                                         
  scale.set_scale();                                          
  scale.tare();                                             
  scale.set_scale(calibration_factor);                       
}

void loop() {
  //Serial.print("Reading: ");                                  
  for (int i = 0; i < 100; i ++) {                             
    units = + scale.get_units(), 100;                          
  }
  units = units/10000;                                         
  ounces = units * 0.035274;                       
  count = ounces / 50;
  delay(100);
 Serial.println(ounces,3);                            // выводим данные в порт
    
 // Serial.println(count);
}
