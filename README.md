##PresiDrinks API v1.0

PresiDrinks is a Python web API servicing a Knockout web application. PresiDrinks is built on top of the Flask framework, with a MySQL backend.

PresiDrinks API v1.0 is currently under development...

####Endpoints:

######/drinks

This endpoint returns a JSON object for each drink in the PresiDrink database

Example Query:

    curl -i http://127.0.0.1:5000/presidrinks/api/v1.0/drinks

Example Response:

    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 828
    Server: Werkzeug/0.9.4 Python/2.7.2
    Date: Sun, 22 Sep 2013 02:44:21 GMT

    {
      "drinks": [
        {
          "drinkName": "The Revolution", 
          "id": 1, 
          "ingredients": {
            "one": "1 Sugar Cube", 
            "three": "2.75 oz Bourbon or Rye Whiskey", 
            "two": "Angostura Bitters"
          }, 
          "president": "george washington", 
          "steps": {
            "four": "4. Garnish with lemon & orange twist, and maraschino cherry.", 
            "one": "1. Soak sugar cube in bitters in an Old Fashioned glass, then muddle.", 
            "three": "3. Pour whiskey over ice and stir vigoriously", 
            "two": "2. Place large ice chunk in the glass."
          }
        }, 
        {
          "drinkName": "Samual Adams Boston Lager", 
          "id": 2, 
          "president": "john adams", 
          "steps": {
            "one": "1. Remove bottle cap and pour into a chilled glass, Founding Father style."
          }
        }
      ]
    }

######/drinks/president

This endpoint return a drink for a specific president. Since this is a namespace, URL encoding needs to use %20 for spaces between first name and last name of a given president

Example Query:

    curl -i http://127.0.0.1:5000/presidrinks/api/v1.0/drinks/george%20washington

Example Response:

    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 557
    Server: Werkzeug/0.9.4 Python/2.7.2
    Date: Sun, 22 Sep 2013 02:45:10 GMT

    {
      "drink": {
        "drinkName": "The Revolution", 
        "id": 1, 
        "ingredients": {
          "one": "1 Sugar Cube", 
          "three": "2.75 oz Bourbon or Rye Whiskey", 
          "two": "Angostura Bitters"
        }, 
        "president": "george washington", 
        "steps": {
          "four": "4. Garnish with lemon & orange twist, and maraschino cherry.", 
          "one": "1. Soak sugar cube in bitters in an Old Fashioned glass, then muddle.", 
          "three": "3. Pour whiskey over ice and stir vigoriously", 
          "two": "2. Place large ice chunk in the glass."
        }
      }
    }
