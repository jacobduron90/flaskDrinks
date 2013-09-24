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
    #return jsonify( {'drinks': drinks} )
    drinks = Drink.query.all()
    json_list = alchemy_json(drinks, Drink)
    return jsonify({'drinks': json_list})






# URL encoding for the space is %20 -- will the http request handle this?
@app.route('/presidrinks/api/v1.0/drinks/<president>', methods = ['GET'])
def getDrink(president):
    query = Drink.query.filter_by(president=president).first();
    if query == None:
        abort(404)
    return jsonify( {'drink': {'name': query.name, 'president': query.president, 'uid':query.uid}} )


@app.route('/testdb')
def testdb():
  #if db.session.query("1").from_statement("SELECT 1").all():
  #  return 'It works.'
  #else:
  #  return 'Something is broken.'   
  db.drop_all()
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


# Create a new drink object
@app.route('/presidrinks/api/v1.0/drinks', methods = ['POST'])
def createDrink():
    if not request.json or not 'president' in request.json:
        abort(400)
    else:
        name = request.json.get('drinkName', "")
        president  = request.json['president']
        ingredient = request.json.get('ingredients', )
        print president
        newdrink = Drink(name, president)
        db.session.add(newdrink)
        db.session.commit()
        drinks = Drink.query.all()
        json_list = alchemy_json(drinks, Drink)
        return jsonify({'drinks': json_list})


    #drink = {
    #    'id': drinks[-1]['id'] + 1,
    #    'president': request.json['president'],
    #    'drinkName': request.json.get('drinkName', ""),
    #    'ingredients': {},
    #    'steps': {},
    #}
    #drinks.append(drink)
    #return jsonify( {'drink': drink} ), 201


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



def alchemy_json(Mycollection, Mytable):
    output = []
    for i in Mycollection:
        row = {}
        for field in Mytable.__table__.columns:
            v = getattr(i, str(field.name), None)
            if v is not None:
                row[field.name] = v

        output.append(row)
    return output






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
