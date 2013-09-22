#!venv/bin/python

from flask import Flask
from flask import make_response, jsonify, abort, request
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://president:housesecret@127.0.0.1/presiDrinks"

from models import db, Drink

db.init_app(app)



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
    #return jsonify( {'drinks': drinks} )
    drinks = Drink.query.all()
    
    json_list = alchemy_json(drinks, Drink)
    return jsonify({'drinks': json_list})






# URL encoding for the space is %20 -- will the http request handle this?
@app.route('/presidrinks/api/v1.0/drinks/<president>', methods = ['GET'])
def get_drink(president):
    p = president.lower()
    drink = filter(lambda d: d['president'] == p, drinks)
    if len(drink) == 0:
        abort(404)
    return jsonify( {'drink': drink[0]} )


@app.route('/testdb')
def testdb():
  #if db.session.query("1").from_statement("SELECT 1").all():
  #  return 'It works.'
  #else:
  #  return 'Something is broken.'   

  db.create_all()
  return "i got here"

  #######################
 #### POST Requests ####
#######################

'''
Need to figure out how to handle object creation for
these nested objects (ingredients, steps). How will 
this work with the MySQL database?
'''


@app.route('/presidrinks/api/v1.0/drinks', methods = ['POST'])
def create_drink():
    if not request.json or not 'president' in request.json:
        abort(400)
    else:
        newdrink = Drink(request.json.get('drinkName', ""), request.json['president'])
        db.session.add(newdrink)
        db.session.commt()


    #drink = {
    #    'id': drinks[-1]['id'] + 1,
    #    'president': request.json['president'],
    #    'drinkName': request.json.get('drinkName', ""),
    #    'ingredients': {},
    #    'steps': {},
    #}
    #drinks.append(drink)
    #return jsonify( {'drink': drink} ), 201
    drinks = Drink.query.all()
    return drink

# Add an ingredient to the ingredients object for a given president
@app.route('/presidrinks/api/v1.0/drinks/ingredients/<president>', methods = ['POST'])
def add_ingredient(president):
    if not request.json:
        abort(400)
    p = president.lower()
    drink = filter(lambda d: d['president'] == p, drinks)

    for key, value in request.json.items():
        drink[0]['ingredients'][key] = value

    return jsonify( {'drink': drink} ), 201


# Add a step to the steps object for a given president
@app.route('/presidrinks/api/v1.0/drinks/steps/<president>', methods = ['POST'])
def add_step(president):
    if not request.json:
        abort(400)
    p = president.lower()
    drink = filter(lambda d: d['president'] == p, drinks)

    for key, value in request.json.items():
        drink[0]['steps'][key] = value

    return jsonify( {'drink': drink} ), 201



def alchemy_json(Mycollection, Mytable):
    output = []
    for i in Mycollection:
        print i
        row = {}
        for field in Mytable.__table__.columns:
            v = getattr(i, str(field.name), None)
            if v is not None:
                row[field.name] = v

        output.append(row)
        return output





if __name__ == '__main__':
    app.run(debug=True)
