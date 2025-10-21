class Msg():
    topicID = 0
    cmd = 1
    external = False
    

class StatusMsg(Msg):
    cmd = 1
    data = 2
    
    # cmd codes
    encoders = 0
    targets = 1
    current = 2
    mag = 3
    mem = 4
    log = 5
    
    def __init__(self, topicID):
        self.msg = [topicID, 0, [] ]
    
    def setEncoder(self, which, value ):
        self.msg[StatusMsg.cmd] = StatusMsg.encoders
        self.msg[StatusMsg.data][which] = value
        
    def setEncoders(self, value ):
        self.msg[StatusMsg.cmd] = StatusMsg.encoders
        self.msg[StatusMsg.data] = value

    #def incEncoder( self, which, value):
    #    self.msg[StatusMsg.encoders][which] += value
        
    def setTarget(self, which, value ):
        self.msg[StatusMsg.cmd] = StatusMsg.targets
        self.msg[StatusMsg.data] = value

    def setTargets(self, values):
        self.msg[StatusMsg.cmd] = StatusMsg.targets
        self.msg[StatusMsg.data] = values

    def setCurrent(self, which, value ):
        self.msg[StatusMsg.cmd] = StatusMsg.current
        self.msg[StatusMsg.data][which] = value

    def setCurrents(self, value):
        self.msg[StatusMsg.cmd] = StatusMsg.current
        self.msg[StatusMsg.data] = value

    def setMag(self, value ):
        self.msg[StatusMsg.cmd] = StatusMsg.mag
        self.msg[StatusMsg.data] = value

    def setMem(self, value ):
        self.msg[StatusMsg.cmd] = StatusMsg.mem
        self.msg[StatusMsg.data] = value
        
    def setLog( self, value ):
        self.msg[StatusMsg.cmd] = StatusMsg.log
        self.msg[StatusMsg.data] = value
        #print('Log Msg', self.msg )
        
    def getMsg( self ):
            return self.msg

'''
class StatusMsg(Msg):
    cmd_statusMsg = 1
 
    # sensor offsets
    encoders = 2
    target = 3
    current = 4
    mag = 5
    mem = 6
        #           topicID       cmd                 encoders      rpm     current    mag
    def __init__(self, topicID):
        self.msg = [topicID, StatusMsg.cmd_statusMsg,
                    [0,1,2,3], [4,5], [6,7,8,9], 10.0, 11.0 ]
    
    def getEncoder(self, which ):
        return self.msg[StatusMsg.encoders][which]
    
    def getEncoders(self):
        return self.msg[StatusMsg.encoders]

    def setEncoder(self, which, value ):
        self.msg[StatusMsg.encoders][which] = value
    
    def setEncoders(self, value ):
        self.msg[StatusMsg.encoders] = value

    def incEncoder( self, which, value):
        self.msg[StatusMsg.encoders][which] += value
        
    def getTarget(self, which ):
        return self.msg[StatusMsg.target][which]

    def getTargets(self):
        return self.msg[StatusMsg.target]

    def setTarget(self, which, value ):
        self.msg[StatusMsg.target][which] = value

    def setTargets(self, value):
        #print('Targets = ', value )
        self.msg[StatusMsg.target] = value

    def getCurrent(self, which ):
        return self.msg[StatusMsg.current][which]

    def getCurrents(self):
        return self.msg[StatusMsg.current]

    def setCurrent(self, which, value ):
        self.msg[StatusMsg.current][which] = value

    def setCurrents(self, value):
        self.msg[StatusMsg.current] = value

    def getMag(self):
        return self.msg[StatusMsg.mag]

    def setMag(self, value ):
        self.msg[StatusMsg.mem] = value

    def getMem(self):
        return self.msg[StatusMsg.mem]

    def setMem(self, value ):
        self.msg[StatusMsg.mem] = value

    def getMsg( self ):
            return self.msg
'''

if __name__ == '__main__':
    print('Messages Lib')
 