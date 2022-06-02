import logging
from websocket_server import WebsocketServer



class socketServer:

    def __init__(self, host, port=8081):
        self.port = port
        self.host = host
        self.clients = []
        self.server = WebsocketServer(host=self.host, port=self.port)
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
        return


    def new_message(self, client, server, message):
        data = message.split('&')
        self.clients.append({'chat_id': int(data[0]), 'user_id': int(data[1]), 'client': client})


    def send_message(self, chat_id, user_id, message):
        for user in self.clients:
            if user['chat_id'] == chat_id and user['user_id'] == user_id:
                self.server.send_message(user['client'], message)
