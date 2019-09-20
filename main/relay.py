
import machine
import ure

RELAY = machine.Pin(14, machine.Pin.OUT)
 
def getPinStatus():
  return RELAY.value()
 
def setPin(value):
  RELAY.value(int(value))  
  return "PIN set to %s" % (value)



