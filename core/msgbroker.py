#import asyncio
import uasyncio as asyncio
#import time
from queue import Queue
#from asyncio import Queue
import json
#import math
import gc
from globals import Globals
from client import WebsocketClient
import messages
#import motor
import logtask

class MsgBroker():
    def __init__(self):
        self.topicTable = []
        self.topics = []
        self.parmTypes = []
        self.subscribed = []
        self.advertised = []
        self.numTopics = 0
        self.connection = None
        
    async def websocket_advertise(self, topic, parmType):
        advertise = {
                        "op" : "advertise",
                        "topic" : topic,
                        "type" : parmType
                    }
        if topic in self.advertised:
            print('Topic ', topic, ' already advertised')
        else:
            advertise_str = json.dumps(advertise)
            self.advertised.append( topic )
            await self.connection.send( advertise_str.encode())
            print("Advertise Sent: ", advertise_str)
        
    async def websocket_subscribe( self, topic, parmType):
        subscribe = {
                        "op" : "subscribe",
                        "topic" : topic
                    }
        if topic in self.subscribed:
            print('Topic ', topic, ' already subscribed')
        else:
            self.subscribed.append( topic )
        
        subscribe_str = json.dumps(subscribe)
        await self.connection.send( subscribe_str.encode() )
        print("Subscribe Sent: ", subscribe_str)

    async def websocket_unsubscribe( self, topic, parmType):
        unsubscribe = {
                        "op" : "unsubscribe",
                        "topic" : topic,
                        "type" : parmType
                    }
       
        unsubscribe_str = json.dumps(unsubscribe)
        await self.connection.send( unsubscribe_str.encode())
        print("Unsubscribe Sent: ", unsubscribe_str)

    async def websocket_unadvertise( self, topic, parmType):
        subscribe = {
                        "op" : "unadvertise",
                        "topic" : topic
                    }
       
        unadvertise_str = json.dumps()
        await self.connection.send( unadvertise_str.encode())
        print("Unadvertise Sent: ", unadvertise_str)

    async def websocket_end( self ):
        for topic in self.subscribed:
            topicID = self.topicToIndex( topic )
            await self.websocket_unsubscribe( topic, self.parmTypes[ topicID ] )
        
        for topic in self.advertised:
            await self.websocket_unadvertise( topic )
        #await Globals.webserver.websocket.close()    

    def topicToIndex(self, topic):
        if topic in self.topics:
            return self.topics.index(topic)
        else:
            return -1

    def indexToTopic(self, index):
        if index < len(self.topics):
            return self.topics[index]
        else:
            return None

    def printTopicTable(self):
        index = 0
        print('\nTopic Table')
        for tc in self.topicTable:
            print( 'Topic ', self.indexToTopic( index) )
            tq = self.topicTable[index]
            if len(tq) > 0:
                qs = 0
                for t in tq[0]:
                    print('    Task ', t, ' Msgs = ', tq[1][qs].qsize())
                    qs += 1
            else:
                print('    No Subs' )
            index += 1

    def makeMsg(self, inMsg):
        if inMsg[messages.Msg.cmd] == messages.MotorMsg.cmd_motorMsg:
            msg = messages.MotorMsg(inMsg[messages.Msg.topicID])
        elif inMsg[messages.Msg.cmd] == messages.SensorMsg.cmd_sensorMsg:
            msg = messages.SensorMsg(inMsg[messages.Msg.topicID])
        elif inMsg[messages.Msg.cmd] == messages.LogMsg.cmd_loggingMsg:
            msg = messages.LogMsg(inMsg[messages.Msg.topicID])
        msg.msg = inMsg
        return msg

    async def registerPub(self, topic, parmType):
        index = self.topicToIndex( topic )
        if index > -1:
            print('Topic ', topic, ' already exists')
            return index
        else:
            self.topics.append( topic )
            self.parmTypes.append( parmType )
            index = len(self.topics) - 1
            self.topicTable.append( [[],[]] )
            
        await self.websocket_advertise( topic, parmType)
        print('Topic ', topic, ' added with index = ', index)
        
        return index

    async def registerSub(self, topic, parmType, extern) :
        q = Queue()
        index = self.topicToIndex( topic )
        if index < 0:
            self.topics.append( topic )
            self.parmTypes.append( parmType )
            index = len(self.topics) - 1
            self.topicTable.append( [[],[]] )

        tq = self.topicTable[index]    
        tq[0].append(index)
        tq[1].append(q)
        print('Task ', index, 'subscribed to ', topic)

        if extern:    
            await self.websocket_subscribe( topic, parmType)
            print( 'subscribed to ', topic )
            await asyncio.sleep(0)
        
        return q
    
    async def createTopics(self, topics, topicsTypes):
        for topic in topics:
            index = self.topicToIndex( topic )
            print('creating topic ', topic, ', with type ', topicsTypes[index] )
            await self.registerPub(topic, topicsTypes[index])
    
    async def publishMsg( self, topicID, type, msg ):
        
        def buildPubMsg(topic, msg):    
            pubMsg = {
                        'op': 'publish',
                        'topic': topic,
                        'type': type,
                        'msg': {'data': ''} 
                    }
            pubMsg['msg']['data'] = str(msg)
            omsg = json.dumps(pubMsg)
            #print('pubmsg ', msg, ' ', omsg )
            return( omsg ) 

        topic = self.indexToTopic( topicID )
        pubMsg = buildPubMsg( topic, msg )
        
        await self.connection.send( pubMsg.encode() )

    async def putMsg( self, topicID, msg ):
        if topicID > len(self.topics)-1:
            print('Topic ', topicID, ' does not exists')
        else:
            # check if this msg if for external comsumption
            # for sobotrimulator
            #if msg.external:
                #print('External Msg')
                
                # for sobotrimulator
            #    await self.publishMsg( topicID, msg ) 
                
                #for teleop
                #await Globals.webserver.writeq.put( msg )
            #   return
            
            tq = self.topicTable[topicID]
            for q in tq[1]:
                #print('Put msg on task q ', tq[0], ' ', msg)
                await q.put( msg )
    
    async def run( self ):
        #uri = "ws://192.168.68.103:9090"
        uri = "ws://192.168.68.89:9090"
        Globals.webserver = WebsocketClient( uri )
        self.connection = await Globals.webserver.connect()
        Globals.connected = True
        print('connected')
        try:
            while True:
                msg = await self.connection.recv()
                #print( 'Recv: ', msg )
                msgdata = json.loads( msg )
                topicID = self.topicToIndex( msgdata['topic'] )
                #print('Recv topicID ', topicID, msgdata['msg'])
                await self.putMsg( topicID, msgdata['msg'] )
                #await asyncio.sleep(0.1)
            
        except asyncio.CancelledError:
            print('\nWebServer Cancelled')  # This mechanism doesn't work on Unix build.
        finally:
            await self.connection.close()
            print('Websocket closed')

class msgPublisher():
    def __init__(self):
        return
    
    def mem(self):
        gc.collect()
        F = gc.mem_free()
        A = gc.mem_alloc()
        T = F+A
        #P = '{0:.2f}%'.format(F/T*100)
        #P = '{0:.2f}'.format(F/T*100)
        P = round( F/T*100, 2 )
        return P
    
    async def sendMotorMsg(self, topicID, msgData ):
        #print( 'sendMotorMsg: topicID ', topicID, ' msgData ', msgData )
        
        msg = { 'data': '' }
        msg['data'] = msgData
        
        #strMsg = json.dumps( msg )
        print( 'msg ', msg )
        
        #await Globals.broker.publishMsg( topicID, 'std_msgs/String', strMsg )
        await Globals.broker.putMsg( topicID, msg  )
                
    async def run(self):
        #print('msgPublisher ', Globals.connected)
        
        while Globals.broker.connection == None:
            print('not connected')
            await asyncio.sleep( 0.5 )
        
        topicID = await Globals.broker.registerPub( '/status', 'std_msgs/String' )
        #topicID = await Globals.broker.registerPub( '/motor', 'std_msgs/String' )
        #topicID = await Globals.broker.registerPub( '/drive/response', 'std_msgs/String' )
        print( 'chatter topicID ', topicID )
        #i = 0
        self.logger = logtask.logPublisher()

        try:
            while True:
                #print('sent msg ', topicID, ' ', i )
                M = self.mem()
                Globals.statusMsg.setMem( M )
                await Globals.statusTask.sendStatus()
                
                #await self.logger.log( f'MEM {M}')
        
                Globals.statusMsg.setLog( f'MEM {M}' )
                await Globals.statusTask.sendStatus()
                
                #await Globals.broker.publishMsg( topicID, 'std_msgs/String', self.mem() )
                #i += 1
                await asyncio.sleep(5)
                
                '''
                await self.sendMotorMsg( topicID, '[0.55, 0.5]' )
                await asyncio.sleep(0.25)
                
                await self.sendMotorMsg( topicID, '[-0.55, 1.0]' )
                await asyncio.sleep(0.25)
                i += 1
                #self.mem()    
                #gc.collect()
                #self.mem()
                if i > 2:
                    break
                '''
        except asyncio.CancelledError:
            print('\nmsgPublisher Cancelled')  # This mechanism doesn't work on Unix build.
        finally:
            return
        

'''
class CreateTasks():
    def __init__(self):
        self.tasks = []

    async def create_tasks(self):
        print('Starting Tasks...')

        Globals.broker = MsgBroker()

        motorTask = motor.MotorTask()
        publisher = msgPublisher()

        asyncio.create_task(publisher.run())
        asyncio.create_task(motorTask.run())
        asyncio.run(Globals.broker.run())
    
    async def closeWebSocket(self):
        if Globals.broker.connection == None:
            print('No connection object')
            return
        await Globals.broker.connection.close()
'''

if __name__ == '__main__':
    print('MsgBroker Lib')
    '''
    try:
        ct = CreateTasks()
        asyncio.run(ct.create_tasks())
    except KeyboardInterrupt:
        print('\nMain Loop Interrupted')  # This mechanism doesn't work on Unix build.
    finally:
        asyncio.run(ct.closeWebSocket())
        _ = asyncio.new_event_loop()
    '''    
