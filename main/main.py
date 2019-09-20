
import os
from machine import Pin,Timer,PWM, I2C
from relay import setPin, getPinStatus
import machine, dht, ssd1306
from humcontrol import dewpoint_approximation

dhtSensor = dht.DHT22(machine.Pin(0))

i2c = I2C(scl=Pin(5), sda=Pin(4), freq=100000)  #Init i2c
oled=ssd1306.SSD1306_I2C(128,64,i2c)             #create LCD object,Specify col and row


# Setting global variables
pwmLED =PWM(Pin(2),100)            #create PWM object from a pin,and set frequency
polar = 0
duty = 0
cycles = 0



def setLed(t):                  #create a variate,and change it between 0 and 1008
  global duty,polar
  if(polar == 0):
    duty+=16
    if(duty >= 1008):
      polar = 1
  else:
    duty -= 16
    if(duty <= 0):
      polar = 0
  pwmLED.duty(duty)                #set duty of the PWM

timerLED = Timer(1)                  #create Timer object from Virtual timers with timer ID=1
timerLED.init(period=10,mode=Timer.PERIODIC, callback=setLed)     #init Timer,Call the callback function with per second




print("")
print("Breathing LED is started")

oled.fill(0)
oled.text("Welcome!",30,28)
oled.show()




def setPinAuto(t):
  if(getPinStatus() == 0):
    print(setPin(1))
    getPinStatus()
  else:
    print(setPin(0))
    getPinStatus()



#timerRelay = Timer(5)                  #create Timer object from Virtual timers with timer ID=2
#timerRelay.init(period=1000,mode=Timer.PERIODIC, callback=setPinAuto)     #period in millis, mode, callback
    
    
def getDHT(t):
  global cycles
  dhtSensor.measure()
  T = dhtSensor.temperature()
  H = dhtSensor.humidity()
  Td = round(dewpoint_approximation(dhtSensor.temperature(),dhtSensor.humidity()),2)
  tempcycles = cycles
  cycles = tempcycles + 1
  print("Temp: " + str(T))
  print("Hum:  " + str(H))
  print("TD :  " + str(Td))
  print("Run no of times: " + str(cycles))
  print()
  oled.fill(0)
  oled.text("Temp:",0,0)
  oled.text("Hum:",0,16)
  oled.text("Td:",0,32)
  oled.text(str(T),64,0)
  oled.text(str(H),64,16)
  oled.text(str(Td),64,32)
  oled.text(str(cycles),0,48)
  oled.show()
  
timerDHT = Timer(6)                  #create Timer object from Virtual timers with timer ID=2
timerDHT.init(period=5000,mode=Timer.PERIODIC, callback=getDHT)    #period in millis, mode, callback




try:                            #The catching
  while True:
    
    pass
except:                         #Capture anomaly, deinit Timer and PWM
  timerLED.deinit()
  pwmLED.deinit()
  timerDHT.deinit()
  













