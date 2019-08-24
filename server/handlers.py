from protocol import make_response
from actions import actionnames


def default_handler(request):

    action_target = request.url
    response = make_response(404, 'not found', 'ooops')

    for action in actionnames:  # Поиск контроллера
        if action['actions'] == action_target:
            return action['controller'](request)

    return response  # Контроллер не найдет
