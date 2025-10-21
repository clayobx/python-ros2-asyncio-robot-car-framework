from machine import Pin, I2C
import constants
import messages

class Globals():
    statusMsg = messages.StatusMsg(1)
    broker = None
    brokerT = None
    webserver = None
    statusTask = None
    connection = None
    connected = False
    loggerTopicID = -1
    
    i2cbus = I2C(0, scl=Pin(constants.i2cSclPin), sda=Pin(constants.i2cSdaPin), freq=constants.i2cFreq)
    print( 'Globals Init i2c Scan ', i2cbus.scan() )

if __name__ == '__main__':
    print('Globals Lib')