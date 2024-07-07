#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

@app.route("/restaurants")
def restaurants():
    restaurants = []
    for restaurant in Restaurant.query.all():
        rest_dict=restaurant.to_dict()
        restaurants.append(rest_dict)
    return make_response(restaurants,200)

@app.route("/restaurants/<int:id>", methods=['GET','DELETE'])
def restaurants_by_id(id):
    restaurant = Restaurant.query.filter(Restaurant.id==id).first()
    if request.method=='GET':
        if restaurant:
            rest_dic = restaurant.to_dict()
            return make_response(rest_dic,200)
        return {"error":"Restaurant not found"}
    elif request.method=='DELETE':
        if restaurant:
            db.session.delete(restaurant)
            db.session.commit()

            response_body = {"message":"Restaurant deleted successfully"}
            return make_response(response_body,200)
        return {"error":"Restaurant not found"}

@app.route("/pizzas")
def pizzas():
    pizzas = [pizza.to_dict() for pizza in Pizza.query.all()]
    return make_response(pizzas,200)

@app.route("/restaurant_pizzas", methods=['POST'])
def restaurant_pizzas():
    data = request.get_json()

    restaurant_pizza = RestaurantPizza(
    price = data['price'],
    pizza_id = data['pizza_id'],
    restaurant_id = data['restaurant_id']
)
    response_data = {
    'id': restaurant_pizza.id,
    'price': restaurant_pizza.price,
    'pizza_id': restaurant_pizza.pizza_id,
    'restaurant_id': restaurant_pizza.restaurant_id,
    'pizza': restaurant_pizza.pizza.to_dict() if restaurant_pizza.pizza else None,
    'restaurant': restaurant_pizza.restaurant.to_dict() if restaurant_pizza.restaurant else None,}

    print(response_data)
    try:

        db.session.add(restaurant_pizza)
        db.session.commit()
    except Exception as e:
        return make_response({"errors":[str(e)]},400)
    
    return make_response(response_data,200)


if __name__ == "__main__":
    app.run(port=5555, debug=True)
