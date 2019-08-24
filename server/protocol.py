from collections import namedtuple
import json

Request = namedtuple('Request', 'method, url, version, headers, data')


# Создает объект request по строковому представлению
def get_request(raw_request):

    headers, body = raw_request.split('\r\n\r\n')  # Разделяем тело и заговки
    headers = headers.split('\r\n')  # разделяем заголовки по строкам

    return Request(
        *headers.pop(0).split(' '),  # Удалем первую строку заголовка и разделяем на метод, url, и версию http
        dict(map(lambda x: x.split(': '), headers)),  # Сохраняем остальные строки заголовка в виде словаря
        body
    )


def make_response(code, message, data=''):
    return f'HTTP/1.1 {code} {message}\r\n\r\n{data}'


def get_json(request):

    if request.headers['Content-Type'] != 'application/json':
        return None

    try:
        res = json.loads(request.data)
    except json.decoder.JSONDecodeError:
        res = None

    return res
