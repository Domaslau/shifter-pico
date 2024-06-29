import board
import digitalio
import analogio
import usb_hid
from hid_gamepad import Gamepad


gamepad = Gamepad(usb_hid.devices)
xaxis = analogio.AnalogIn(board.A1) #pin 32 ADC1
yaxis = analogio.AnalogIn(board.A0) #pin 31 ADC0
reverse = digitalio.DigitalInOut(board.GP28) #pin 34 GP28
reverse.switch_to_input()

# For neutral only checking y axis as it's where the gear is engaged
# if y axis is within the treshold clear all buttons  
def checkNeutral():
    if(yaxis.value < 40000 and yaxis.value > 19000):
        gamepad.release_all_buttons()

#check if x is high position (right side)
def xHigh():
    if(xaxis.value > 40000):
        return True
    else: return False

#check if x is low position (left side)
def xLow():
    if(xaxis.value < 20000):
        return True
    else: return False

#check if y is in top position
def yHigh():
    if(yaxis.value > 40000):
        return True
    else: return False

#check if y is in bottom position
def yLow():
    if(yaxis.value < 19000):
        return True
    else: return False

#main loop
#repeated inputs are handled by hid_gamepad
while(1):
    #check if it's in neutral position and clear buttons
    checkNeutral()
    
    #x is not high or low just check if it's in 3rd or 4th gear
    if(yHigh()):
        gamepad.press_buttons(3)
    if(yLow()):
        gamepad.press_buttons(4)

    #loop here if x is low
    while(xLow()):

        #check for neutral
        checkNeutral()
        if(yHigh()):
            gamepad.press_buttons(1)
        if(yLow()):
            gamepad.press_buttons(2)

    #loop here if x is high
    while(xHigh()):

        #check for neutral
        checkNeutral()

        # if y is high send 5
        if(yHigh()):
            gamepad.press_buttons(5)
        
        # if y is low here we have reverse check as well because reverse is in
        # same position as 6th gear so if stick is not pressed down send 6
        if(yLow() and reverse.value == 0):
            gamepad.press_buttons(6)
        
        if(yLow() and reverse.value == 1):
            gamepad.press_buttons(7)