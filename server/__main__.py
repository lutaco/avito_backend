import socket
import os.path
from settings import HOST, PORT, BUFFERSIZE, ENCODING, DB_NAME
from protocol import get_request
from handlers import default_handler
from database import create

if not os.path.exists(DB_NAME):
    create(DB_NAME)

try:
    sock = socket.socket()
    sock.bind((HOST, PORT))
    sock.listen(0)
    print('server started')

    while True:

        client, address = sock.accept()

        print(f'client with address {address} was detected')
        b_data = client.recv(BUFFERSIZE)

        # Подразумевается, что испльзуется HTTP/1.1 валидный запрос с \n\r в качестве разделителя
        request = get_request(b_data.decode(ENCODING))
        response = default_handler(request)

        client.send(response.encode(ENCODING))
        client.close()

except KeyboardInterrupt:
    print('server closed')
