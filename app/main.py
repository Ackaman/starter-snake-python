import json
import os
import random
import bottle

from api import ping_response, start_response, move_response, end_response

@bottle.route('/')
def index():
    return '''
    Battlesnake documentation can be found at
       <a href="https://docs.battlesnake.io">https://docs.battlesnake.io</a>.
    '''

@bottle.route('/static/<path:path>')
def static(path):
    """
    Given a path, return the static file located relative
    to the static folder.

    This can be used to return the snake head URL in an API response.
    """
    return bottle.static_file(path, root='static/')

@bottle.post('/ping')
def ping():
    """
    A keep-alive endpoint used to prevent cloud application platforms,
    such as Heroku, from sleeping the application instance.
    """
    return ping_response()

@bottle.post('/start')
def start():
    data = bottle.request.json

    """
    TODO: If you intend to have a stateful snake AI,
            initialize your snake state here using the
            request's data if necessary.
    """
    print(json.dumps(data))

    color = "#00FF00"

    return start_response(color)


@bottle.post('/move')
def move():
    data = bottle.request.json

    """
    TODO: Using the data from the endpoint request object, your
            snake AI must choose a direction to move in.
    """

    directions = ['up', 'down', 'left', 'right']
    ## DATA
    myX = data['you']['body']['data'][0]['x']
    myY = data['you']['body']['data'][0]['y']

    foodX = data['food']['data'][0]['x']
    foodY = data['food']['data'][0]['y']

    xdistToFood = myX - foodX
    ydistToFood = myY - foodY

    mypostions = data['you']['body']['data']

    def getpriority():
        if abs(xdistToFood) > abs(ydistToFood):
            if xdistToFood > 0:
                ##direction = 'left'
                prioritizedMove = ['left', 'right', 'up', 'down']
            else:
                ##direction = 'right'
                prioritizedMove = ['right', 'left', 'up', 'down']

        else:
            if ydistToFood > 0:
                ##direction = 'up'
                prioritizedMove = ['up', 'down', 'right', 'left']

            else:
                ##direction = 'down'
                prioritizedMove = ['down', 'up', 'right', 'left']
        return prioritizedMove

    def checkmove(prioritizedMove):
        for possiblemove in prioritizedMove:
            if possiblemove in mypostions:
                direction = prioritizedMove[0]
                break
            else:
                direction = 'down'
        return direction


    prioritizedMove = getpriority()
    direction = checkmove(prioritizedMove)




    print(json.dumps(data))
    return move_response(direction)


@bottle.post('/end')
def end():
    data = bottle.request.json

    """
    TODO: If your snake AI was stateful,
        clean up any stateful objects here.
    """
    print(json.dumps(data))

    return end_response()

# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug=os.getenv('DEBUG', True)
    )


