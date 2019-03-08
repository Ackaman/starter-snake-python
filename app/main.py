import json
import os
import random
import bottle

from api import ping_response, start_response, move_response, end_response


# Moving towards a tail is safe as long as that snake does not have food witihn reach.
# If it is te only possible move, that move should be made anyway


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

    foodposition = []

    for food in data['food']['data']:
        foodposition.append((food['x'], food['y']))

    my_head = (data['you']['body']['data'][0]['x'], data['you']['body']['data'][0]['y'])

    snakePositions = []
    myPositions = []

    for pos in data['you']['body']['data']:
        myPositions.append((pos['x'], pos['y']))

    for snakes in data['snakes']['data']:
        for pos in snakes['body']['data']:
            snakePositions.append((pos['x'], pos['y']))

    # for pos in data['snakes']['data'][0]['body']['data']:
    #    snakePositions.append((pos['x'], pos['y']))

    walls = []
    width = data['height']
    for i in range(width):
        walls.append((0, i))
        walls.append((i, 0))
        walls.append((width, i))
        walls.append((i, width))

    stuffToAvoid = []

    for position in myPositions:
        stuffToAvoid.append(position)

    for position in walls:
        stuffToAvoid.append(position)

    for position in snakePositions:
        stuffToAvoid.append(position)

    xhead = my_head[0]
    yhead = my_head[1]

    possiblemoves = []

    if (xhead + 1, yhead) not in stuffToAvoid:
        possiblemoves.append('right')
    if (xhead, yhead + 1) not in stuffToAvoid:
        possiblemoves.append('down')
    if (xhead - 1, yhead) not in stuffToAvoid:
        possiblemoves.append('left')
    if (xhead, yhead - 1) not in stuffToAvoid:
        possiblemoves.append('up')

    foodDistances = []
    ##Find closest food
    currentDist = 1000000

    for i in foodposition:
        xfood = i[0]
        yfood = i[1]
        dist = ((abs(my_head[0] - xfood)) + (abs((my_head[1]) - yfood)))
        if (dist < currentDist):
            closestFoodPos = (xfood, yfood)
            currentDist = dist

    xdistancetofood = xhead - closestFoodPos[0]
    ydistancetofood = yhead - closestFoodPos[1]

    if (xdistancetofood >= ydistancetofood) and xhead - xdistancetofood < 0 and 'right' in possiblemoves:
        direction = 'right'
    else:
        direction = random.choice(possiblemoves)


    # direction = random.choice(possiblemoves)

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
