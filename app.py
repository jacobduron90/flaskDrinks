#!venv/bin/python

from flask import Flask
from flask import make_response, jsonify, abort, request

app = Flask(__name__)

drinks = [
    {   'id': 1,
        'president': 'george washington',
        'drinkName': 'The Revolution',
        'ingredients': {
            "one": "1 Sugar Cube",
            "two": "Angostura Bitters",
            "three": "2.75 oz Bourbon or Rye Whiskey"
        },
        "steps":{
            "one": "1. Soak sugar cube in bitters in an Old Fashioned glass, then muddle.",
            "two": "2. Place large ice chunk in the glass.",
            "three": "3. Pour whiskey over ice and stir vigoriously",
            "four": "4. Garnish with lemon & orange twist, and maraschino cherry."
        }
    },
    {   'id': 2,
        'president': 'john adams',
        'drinkName': 'Samual Adams Boston Lager',
        'steps': {
            "one": "1. Remove bottle cap and pour into a chilled glass, Founding Father style."
        }
    }
]
  ########################
 #### Helper Methods ####
########################


  ########################
 #### Error Handlers ####
########################


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( {'error': 'Not found'} ), 404)

  ######################
 #### GET Requests ####
######################


@app.route('/presidrinks/api/v1.0/drinks', methods = ['GET'])
def getDrinks():
    return jsonify( {'drinks': drinks} )


# URL encoding for the space is %20 -- will the http request handle this?
@app.route('/presidrinks/api/v1.0/drinks/<president>', methods = ['GET'])
def getDrink(president):
    drink = filter(lambda d: d['president'] == president.lower(), drinks)
    if len(drink) == 0:
        abort(404)
    return jsonify( {'drink': drink[0]} )

  #######################
 #### POST Requests ####
#######################

'''
Need to figure out how to handle object creation for
these nested objects (ingredients, steps). How will 
this work with the MySQL database?
'''


# Create a new drink object
@app.route('/presidrinks/api/v1.0/drinks', methods = ['POST'])
def createDrink():
    if not request.json or not 'president' in request.json:
        abort(400)
    drink = {
        'id': drinks[-1]['id'] + 1,
        'president': request.json['president'],
        'drinkName': request.json.get('drinkName', ""),
        'ingredients': {},
        'steps': {},
    }
    drinks.append(drink)
    return jsonify( {'drink': drink} ), 201


# Add an ingredient to the ingredients object for a given president
@app.route('/presidrinks/api/v1.0/drinks/ingredients/<president>', methods = ['POST'])
def createIngredient(president):
    if not request.json:
        abort(400)
    drink = filter(lambda d: d['president'] == president.lower(), drinks)

    for key, value in request.json.items():
        drink[0]['ingredients'][key] = value

    return jsonify( {'drink': drink} ), 201


# Add a step to the steps object for a given president
@app.route('/presidrinks/api/v1.0/drinks/steps/<president>', methods = ['POST'])
def createStep(president):
    if not request.json:
        abort(400)
    drink = filter(lambda d: d['president'] == president.lower(), drinks)

    for key, value in request.json.items():
        drink[0]['steps'][key] = value

    return jsonify( {'drink': drink} ), 201


# Edit an existing drink object
@app.route('/presidrinks/api/v1.0/drinks/<president>', methods = ['POST'])
def editDrink(president):
    drink = filter(lambda d: d['president'] == president.lower(), drinks)

    # Error checking
    if len(drink) < 1:
        abort(404)
    if not request.json:
        abort(400)
    for key, value in request.json.items():
        if key == 'ingredients' or 'steps':
            abort(404)
        if key != 'ingredients' or 'steps':
            drink[0][key] = request.json.get(key, drink[0][key])
    return jsonify({ 'drink': drink[0]})


# Edit an existing ingredient object for a drink
@app.route('/presidrinks/api/v1.0/drinks/ingredients/edit/<president>', methods = ['POST'])
def editIngredient(president):
    pass

if __name__ == '__main__':
    app.run(debug=True)
