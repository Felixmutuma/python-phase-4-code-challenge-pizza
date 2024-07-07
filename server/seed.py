#!/usr/bin/env python3

from app import app
from models import db, Restaurant, Pizza, RestaurantPizza

with app.app_context():

    # This will delete any existing rows
    # so you can run the seed file multiple times without having duplicate entries in your database
    print("Deleting data...")
    RestaurantPizza.query.delete()
    print("restaurant deleted")
    Restaurant.query.delete()
    Pizza.query.delete()
    

    print("Creating restaurants...")
    shack = Restaurant(name="Karen's Pizza Shack", address='address1')
    bistro = Restaurant(name="Sanjay's Pizza", address='address2')
    palace = Restaurant(name="Kiki's Pizza", address='address3')
    restaurants = [shack, bistro, palace]

    print("Creating pizzas...")

    cheese = Pizza(name="Emma", ingredients="Dough, Tomato Sauce, Cheese")
    pepperoni = Pizza(
        name="Geri", ingredients="Dough, Tomato Sauce, Cheese, Pepperoni")
    california = Pizza(
        name="Melanie", ingredients="Dough, Sauce, Ricotta, Red peppers, Mustard")
    pizzas = [cheese, pepperoni, california]

    print("Creating RestaurantPizza...")

    pr1 = RestaurantPizza(price=30,restaurant=shack, pizza=cheese)
    pr2 = RestaurantPizza(price=20,restaurant=bistro, pizza=pepperoni)
    pr3 = RestaurantPizza(price=24,restaurant=palace, pizza=california)
    restaurantPizzas = [pr1, pr2, pr3]
    db.session.add_all(restaurants)
    db.session.add_all(pizzas)
    db.session.add_all(restaurantPizzas)
    db.session.commit()

    print("Seeding done!")
