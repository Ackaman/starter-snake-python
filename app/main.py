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


    ##directions = ['up', 'down', 'left', 'right']


    foodposition = []

    for food in data['food']['data']:
        foodposition.add(food['x'], food['y'])

    my_head = (data['you']['body']['data'][0]['x'], data['you']['body']['data'][0]['y'])


    myPositions = []

    for pos in data['you']['body']['data']:
        myPositions.add(pos['x'], pos['y'])

    walls = []
    width = 10
    for i in width:
        walls.add(0,i)
        walls.add(i,0)
        walls.add(width,i)
        walls.add(i,width)


    def closestFood():
        foodDistances = []
        ##Find closest food
        currentDist = 1000000
        for i in foodposition:
            x = fst(i)
            y = snd(i)
            dist = ((abs(fst(my_head) - x)) + (abs(snd(my_head) - y)))
            if (dist < currentDist):
                closestFoodPos = (x,y)
                currentDist = dist



        return closestFoodPos

    closestFoodPos = closestFood()

    def listOfCol():
        completeList = []
        completeList.append(myPositions)
        completeList.append(kanter)
        ## add all other snakes
        return completeList

    stuffToAvoid = listOfCol()

    def possibleMoves():
        x = fst(my_head)
        y = snd(my_head)
        possibleMove = []

        if (x+1, y) not in stuffToAvoid:
            possibleMove.add('right')
        if (x, y+1) not in stuffToAvoid:
            possibleMove.add('down')
        if(x-1, y) not in stuffToAvoid:
            possibleMove.add('left')
        if(x, y-1) not in stuffToAvoid:
            possibleMove.add('up')
    return possibleMove



    WHERETOGO = possibleMoves()
    direction = random.choice(WHERETOGO)









    ##foodX = data['food']['data'][0]['x']
    ##foodY = data['food']['data'][0]['y']

    ##xdistToFood = myX - foodX
    ##ydistToFood = myY - foodY

    ##mypostions = data['you']['body']['data']










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


