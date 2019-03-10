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
    my_length = len((data['you']['body']['data']))

    snakePositions = []
    myPositions = []

    for pos in data['you']['body']['data']:
        myPositions.append((pos['x'], pos['y']))

    listofsnakelists = [] #[[] for i in range(data['snakes']['data'])]

    for snakes in data['snakes']['data']: ## alla ormar
        for pos in snakes['body']['data']: ## alla ormens positioner
            snakePositions.append((pos['x'], pos['y']))
        #    listofsnakelists[snake].append((pos['x'], pos['y']))
        #listofsnakelists.insert(snakes,snakePositions)


    #(x,y)
    #for snakes in listofsnakelists:
    #if listofsnakelists[snake].contains(x,y):
    #if len(listofsnakelists[snake] < my.lenght:
    #   kill

    walls = []
    width = data['height']
    for i in range(width + 1):
        walls.append((0 - 1, i))
        walls.append((i, 0 - 1))
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

    if (xhead + 1, yhead) not in stuffToAvoid and safe_path(xhead + 1, yhead, stuffToAvoid):
        possiblemoves.append('right')
    if (xhead, yhead + 1) not in stuffToAvoid and safe_path(xhead, yhead + 1, stuffToAvoid):
        possiblemoves.append('down')
    if (xhead - 1, yhead) not in stuffToAvoid and safe_path(xhead - 1, yhead, stuffToAvoid):
        possiblemoves.append('left')
    if (xhead, yhead - 1) not in stuffToAvoid and safe_path(xhead, yhead - 1, stuffToAvoid):
        possiblemoves.append('up')

    ##Find closest food
    currentDist = 1000000

    for i in foodposition:
        xfood = i[0]
        yfood = i[1]
        dist = ((abs(xhead - xfood)) + (abs(yhead - yfood)))
        if (dist < currentDist):
            closestFoodPos = (xfood, yfood)
            currentDist = dist

    xdistancetofood = abs(xhead - closestFoodPos[0])
    ydistancetofood = abs(yhead - closestFoodPos[1])

    foodtotheright = ((xhead - closestFoodPos[0]) < 0)
    foodtothetop = ((yhead - closestFoodPos[1]) > 0)

    prioritymoves = []

    if (xdistancetofood >= ydistancetofood) and ((xhead - closestFoodPos[0]) < 0) and 'right' in possiblemoves:
        prioritymoves.append('right')

    if (xdistancetofood >= ydistancetofood) and ((xhead - closestFoodPos[0]) > 0) and 'left' in possiblemoves:
        prioritymoves.append('left')

    if (ydistancetofood >= xdistancetofood) and ((yhead - closestFoodPos[1]) > 0) and 'up' in possiblemoves:
        prioritymoves.append('up')

    if (ydistancetofood >= xdistancetofood) and ((yhead - closestFoodPos[1]) < 0) and 'down' in possiblemoves:
        prioritymoves.append('down')

    # Look if neigbour squares are safe

    #

    prioritymoves.append(random.choice(possiblemoves))
    direction = prioritymoves[0]

    # direction = random.choice(possiblemoves)

    return move_response(direction)


# int x,y or tuple (NEXT STEP)

def safe_path(x, y, stuffToAvoid):

    right = (x+1, y)
    left = (x-1, y)
    down = (x, y+1)
    up = (x, y-1)

    if right in stuffToAvoid and left in stuffToAvoid and down in stuffToAvoid and up in stuffToAvoid:
        safe = False
    else:
        safe = True

    return safe

#Check if an other snakes head is in range. If it's a bigger snake, do not go there.
#def safe_head():



# def safetyLevel(x,y, stuffToAvoid):


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
