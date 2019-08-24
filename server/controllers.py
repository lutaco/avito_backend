from database import connect
from protocol import make_response, get_json
import datetime
import json


def create_chat(request):

    def is_user_exist(user_id):
        return len(cursor.execute("SELECT id from users WHERE id = (?)", (user_id,)).fetchall()) == 1

    data = get_json(request)
    if data is None:
        return make_response(400, 'Bad request', 'json is not valid')

    conn = connect()
    cursor = conn.cursor()

    user_1, user_2 = data['users'][0], data['users'][1]

    if not (is_user_exist(user_1) and is_user_exist(user_2)):
        return make_response(400, 'Bad Request', 'users is not exits')

    chat_id = cursor.execute("INSERT INTO chat(`name`, `created_at`) VALUES (?,?)", (
        data['name'], datetime.datetime.now().timestamp())).lastrowid

    cursor.execute("INSERT INTO user_chat(`chat`, `user`) VALUES (?,?)", (chat_id, user_1))
    cursor.execute("INSERT INTO user_chat(`chat`, `user`) VALUES (?,?)", (chat_id, user_2))

    conn.commit()

    return make_response(201, 'Creates', chat_id)


def create_user(request):

    data = get_json(request)
    if data is None:
        return make_response(400, 'Bad request', 'json is not valid')

    conn = connect()
    cursor = conn.cursor()
    res_id = cursor.execute(
        "INSERT INTO users (`username`, `created_at`) VALUES (?,?)",
        (data['username'], datetime.datetime.now().timestamp())
    ).lastrowid
    conn.commit()

    return make_response(201, 'Created', res_id)


def send_message(request):

    data = get_json(request)
    if data is None:
        return make_response(400, 'Bad request', 'json is not valid')

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT id from user_chat WHERE user = (?) AND chat = (?)", (data['author'], data['chat']))
    if len(cursor.fetchall()) != 1:
        return make_response(400, 'Bad request', 'chat is not exist or user not in chat')

    mes_id = cursor.execute("INSERT INTO messages(`chat`, `author`, `text`, `created_at`) VALUES (?,?,?,?)", (
        data['chat'], data['author'], data['text'], datetime.datetime.now().timestamp())).lastrowid

    conn.commit()
    return make_response(201, 'Created', mes_id)


def list_users_chat(request):

    data = get_json(request)
    if data is None:
        return make_response(400, 'Bad request', 'json is not valid')

    conn = connect()
    cursor = conn.cursor()

    if len(cursor.execute("SELECT id from users WHERE id = (?)", (data['user'],)).fetchall()) != 1:
        return make_response(400, 'Bad request', 'user is not exist')

    cursor.execute("""
        SELECT m.* FROM chat
        JOIN (SELECT chat, user FROM user_chat WHERE user = (?)) as s ON chat.id = s.chat
        JOIN (SELECT * FROM messages ORDER BY -created_at) as m ON m.chat = chat.id
        GROUP BY chat.id
    """, (data['user'],))

    descriptions = list(zip(*cursor.description))[0]
    res = [dict(zip(descriptions, row)) for row in cursor.fetchall()]
    return make_response(200, 'OK', json.dumps(res))


def get_messages_from_chat(request):

    data = get_json(request)
    if data is None:
        return make_response(400, 'Bad request', 'json is not valid')

    conn = connect()
    cursor = conn.cursor()

    if len(cursor.execute("SELECT id from chat WHERE id = (?)", (data['chat'],)).fetchall()) != 1:
        return make_response(400, 'Bad request', 'chat is not exist')

    cursor.execute("""
        SELECT * FROM messages 
        WHERE chat = (?)
    """, (data['chat'],))

    descriptions = list(zip(*cursor.description))[0]
    res = [dict(zip(descriptions, row)) for row in cursor.fetchall()]

    return make_response(200, 'OK', json.dumps(res))
