from controllers import (
    list_users_chat, create_chat, create_user, get_messages_from_chat, send_message
)


actionnames = [
    {'actions': '/chats/get', 'controller': list_users_chat},
    {'actions': '/users/add', 'controller': create_user},
    {'actions': '/chats/add', 'controller': create_chat},
    {'actions': '/messages/get', 'controller': get_messages_from_chat},
    {'actions': '/messages/add', 'controller': send_message},
]
