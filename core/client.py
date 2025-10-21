"""
Websockets client for micropython

Based very heavily off
https://github.com/aaugustin/websockets/blob/master/websockets/client.py
"""

'''
import ubinascii as binascii
import urandom as random
from ucollections import namedtuple

import uasyncio as asyncio
'''
import binascii
import random
from collections import namedtuple

import asyncio

#import ulogging as logging
from protocol import Websocket

#LOGGER = logging.getLogger(__name__)


class WebsocketClient(Websocket):
    """
    Connect a websocket.
    """
    
    is_client = True

    def parse_endpoint(self, endpoint):
        endpoint = endpoint.lower()
        port_map = {'ws': 80, 'wss': 443}
        schema, location = endpoint.split('://')
        host = location.split('/')[0]
        port = int(host.split(':')[1] if ':' in host else port_map[schema])
        host = host if ':' not in location else location.split('/')[0].split(':')[0]
        path = '/' + '/'.join(location.split('/')[1:]) if '/' in location else '/'
        URI = namedtuple('URI', ('scheme', 'hostname', 'port', 'path'))
        return URI(schema, host, port, path)

    def __init__(self, uri):
        self.uri = self.parse_endpoint(uri)  # urllib.parse.urlparse(uri)

    #async def __iter__(self):
    #    """This is a hack to allow the websocket = connect() format."""
    #    print('hack')
    #    return await self.connect()

    async def connect(self):
        print('Connect')
        assert self.uri.scheme == 'ws'

        if __debug__: print("open connection %s:%s",
                                self.uri.hostname, self.uri.port)
        self.reader, self.writer = await asyncio.open_connection(self.uri.hostname,
                                                    self.uri.port)

        async def send_header(header, *args):
            #if __debug__: print(str(header), *args)
            headerStr = header % args + '\r\n'

            byte_data = headerStr.encode('utf-8')
            self.writer.write( byte_data )

        # Sec-WebSocket-Key is 16 bytes of random base64 encoded
        key = binascii.b2a_base64(bytes(random.getrandbits(8)
                                        for _ in range(16))).rstrip()

        await send_header('GET %s HTTP/1.1', self.uri.path or '/')
        await send_header('Host: %s:%s', self.uri.hostname, self.uri.port)
        await send_header('Connection: Upgrade')
        await send_header('Upgrade: websocket')
        await send_header('Sec-WebSocket-Key: %s', key)
        # await send_header(b'Sec-WebSocket-Protocol: chat')
        await send_header('Sec-WebSocket-Version: 13')
        await send_header('Origin: http://localhost')
        await send_header('')

        header = await self.reader.readline()
        print( header )
        #assert header in ['HTTP/1.1 101 Switching Protocols\r\n',
        #                'HTTP/1.1 101 Web Socket Protocol Handshake\r\n'],\
        #    header

        # We don't (currently) need these headers
        # FIXME: should we check the return key?
        while header.rstrip():
            #if __debug__: print(str(header))
            header = await self.reader.readline()

        return Websocket(self.reader, self.writer)

    async def __aenter__(self):
        self._websocket = await self._connect()
        return self._websocket

    async def __aexit__(self, exc_type, exc, tb):
        await self._websocket.close()