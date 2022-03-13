import logging
from websocket_server import WebsocketServer



class socketServer:

    def __init__(self, port=8081):
        self.port = port
        self.clients = []
        self.server = WebsocketServer(host='127.0.0.1', port=self.port, loglevel=logging.DEBUG)
        self.server.set_fn_message_received(self.new_message)
        self.server.set_fn_new_client(self.new_client)
        self.server.set_fn_client_left(self.client_left)
        self.server.run_forever(threaded=True)


    def client_left(self, client, server):
        for i in range(len(self.clients)):
            if self.clients[i]['client'] == client:
                self.clients.pop(i)
                break


    def new_client(self, client, server):
        print('new client:', client['id'])


    def new_message(self, client, server, message):
        print('dasdasdasdas')
        self.clients.append({'user_id': int(message), 'client': client})
        print('new user:', message)


    def send_message(self, user_id, message):
        for user in self.clients:
            if user['user_id'] == user_id:
                self.server.send_message(user['client'], message)
                break



# import threading
# import asyncio
# import websockets




# class socketServer:

#     def __init__(self, port=8081):
#         self.port = port
#         self.sockets = []
#         x = threading.Thread(target=self.run)
#         x.start()
#         print('dasd1111as')



#     async def handler(self, websocket):
#         while True:
#             message = await websocket.recv()
#             print(message, 'dasdasdas')
#             self.sockets.append({'user_id': int(message), 'socket': websocket})


#     async def main(self):
#         async with websockets.serve(self.handler, "localhost", self.port):
#             await asyncio.Future()

#     def run(self):
#         asyncio.run(self.main())


#     def send_message(self, user_id, message):
#         for s in self.sockets:
#             if s['user_id'] == user_id:
#                 s['socket'].send(bytes(message, encoding = 'UTF-8'))
#                 break









# class socketServer:
#     def __init__(self, ip=8081):
#         self.ip = ip
#         self.sockets = []
#         self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.sock.bind(('', 8081))
#         self.sock.listen(10)
#         x = threading.Thread(target=self.server, daemon=True)
#         x.start()
#         print('Socket Server is running')


#     def server(self):
#         while True:
#             conn, addr = self.sock.accept()
#             print('connected:', addr)
#             response = conn.recv(100000)
#             print(str(response))
#             response = conn.recv(100000)
#             #user_id = int.from_bytes(response, "big")
#             print(str(response))
#             user_id = int(str(response))
#             self.sockets.append({'user_id': user_id, 'socket': conn})

#     def send_message(self, user_id, message):
#         for s in self.sockets:
#             if s['user_id'] == user_id:
#                 s['socket'].send(bytes(message, encoding = 'UTF-8'))
#                 break

# conn.close()
