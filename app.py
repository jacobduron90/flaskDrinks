#!venv/bin/python

from flask import Flask
from flask import make_response, jsonify, abort

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
 #### Error Handlers ####
########################


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( {'error': 'Not found'} ), 404)

  ######################
 #### GET Requests ####
######################


@app.route('/presidrinks/api/v1.0/drinks', methods = ['GET'])
def get_drinks():
    return jsonify( {'drinks': drinks} )


# URL encoding for the space is %20 -- will the http request handle this?
@app.route('/presidrinks/api/v1.0/drinks/<president>', methods = ['GET'])
def get_drink(president):
    p = president.lower()
    drink = filter(lambda d: d['president'] == p, drinks)
    if len(drink) == 0:
        abort(404)
    return jsonify( {'drink': drink[0]} )


if __name__ == '__main__':
    app.run(debug=True)
