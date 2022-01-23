import json

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from data_file import users_data, orders_data, offers_data


app = Flask("HW_16")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
db = SQLAlchemy(app)

#Step 1

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text(50))
    last_name = db.Column(db.Text(50))
    age = db.Column(db.Integer)
    email = db.Column(db.Text(30))
    role = db.Column(db.Text(50))
    phone = db.Column(db.Text(20))

    def dic_form(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "email": self.email,
            "role": self.role,
            "phone": self.phone,
        }


class Offer(db.Model):
    __tablename__ = 'offer'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # user = db.relationship("User")
    # order = db.relationship("Order")

    def dic_form(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "executor_id": self.executor_id,
        }


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(50))
    description = db.Column(db.Text(300))
    start_date = db.Column(db.Text(20))
    end_date = db.Column(db.Text(20))
    address = db.Column(db.Text(200))
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey('offer.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # offer = db.relationship("Offer")
    # order = db.relationship("Order")

    def dic_form(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "address": self.address,
            "price": self.price,
            "customer_id": self.customer_id,
            "executor_id": self.executor_id,
        }

db.create_all()

#Step 2

for user in users_data:
    new_entry = User(
        id = user['id'],
        first_name = user['first_name'],
        last_name = user['last_name'],
        age = user['age'],
        email = user['email'],
        role = user['role'],
        phone = user['phone'],
    )
    db.session.add(new_entry)
    db.session.commit()

for offer in offers_data:
    new_entry = Offer(
        id = offer['id'],
        order_id = offer['order_id'],
        executor_id = offer['executor_id'],
    )
    db.session.add(new_entry)
    db.session.commit()

for order in orders_data:
    new_entry = Order(
        id = order['id'],
        name = order['name'],
        description = order['description'],
        start_date = order['start_date'],
        end_date = order['end_date'],
        address = order['address'],
        price = order['price'],
        customer_id = order['customer_id'],
        executor_id = order['executor_id'],
    )
    db.session.add(new_entry)
    db.session.commit()

#Step 3 and 6

@app.route('/users', methods=['GET', 'POST'])
def all_users():
    '''function which loads the data of all users from the database if we used GET method and add new user by POST method'''
    if request.method == "GET":
        results = []
        for user in User.query.all():
            results.append(user.dic_form())
        return json.dumps(results), 200, {'Content-Type':'application/json; charset=utf-8'}
    elif request.method == "POST":
        user = json.load(request.data)
        new_user = User(
            first_name = user['first_name'],
            last_name = user['last_name'],
            age = user['age'],
            email = user['email'],
            role = user['role'],
            phone = user['phone'],
            )
        db.session.add(new_user)
        db.session.commit()
        return "user added"


@app.route('/users/<userid>', methods = ["GET", "PUT", "DELETE"])
def user_by_id(userid):
    '''function which loads the data of selected user from the database if we used GET method, delete selected user if we used DELETE method and update selected user if we used PUT method'''
    if request.method == "GET":
        return User.query.get(userid).dic_form(), 200, {'Content-Type':'application/json; charset=utf-8'}
    elif request.method == "DELETE":
        user = User.query.get(userid)
        db.session.delete(user)
        db.session.commit()
        return "user deleted"
    elif request.method == "PUT":
        upd_user = json.loads(request.data)
        user = User.query.get(userid)
        user.first_name = upd_user['first_name']
        user.last_name = upd_user['last_name']
        user.age = upd_user['age']
        user.email = upd_user['email']
        user.role = upd_user['role']
        user.phone = upd_user['phone']
        db.session.add(user)
        db.session.commit()
        return "user updated"


#Step 4 and 7

@app.route('/orders', methods=['GET', 'POST'])
def all_orders():
    '''function which loads the data of all orders from the database if we used GET method and add new order by POST method'''
    if request.method == "GET":
        results = []
        for order in Order.query.all():
            results.append(order.dic_form())
        return jsonify(results)
    elif request.method == "POST":
        order = json.load(request.data)
        new_order = Order(
            name = order['name'],
            description = order['description'],
            start_date = order['start_date'],
            end_date = order['end_date'],
            address = order['address'],
            price = order['price'],
            customer_id = order['customer_id'],
            executor_id = order['executor_id'],
            )
        db.session.add(new_order)
        db.session.commit()
        return "order added"


@app.route('/orders/<orderid>', methods = ["GET", "PUT", "DELETE"])
def order_by_id(orderid):
    '''function which loads the data of selected order from the database if we used GET method, delete selected order if we used DELETE method and update selected order if we used PUT method'''
    if request.method == "GET":
        return Order.query.get(orderid).dic_form(), 200, {'Content-Type':'application/json; charset=utf-8'}
    elif request.method == "DELETE":
        order = Order.query.get(orderid)
        db.session.delete(order)
        db.session.commit()
        return "order deleted"
    elif request.method == "PUT":
        upd_order = json.loads(request.data)
        order = Order.query.get(orderid)
        order.name = upd_order['name']
        order.description = upd_order['description']
        order.start_date = upd_order['start_date']
        order.end_date = upd_order['end_date']
        order.address = upd_order['address']
        order.price = upd_order['price']
        order.customer_id = upd_order['customer_id']
        order.executor_id = upd_order['executor_id']
        db.session.add(order)
        db.session.commit()
        return "order updated"


#Step 5 and 8

@app.route('/offers', methods=['GET', 'POST'])
def all_offers():
    '''function which loads the data of all offers from the database if we used GET method and add new offer by POST method'''
    if request.method == "GET":
        results = []
        for offer in Offer.query.all():
            results.append(offer.dic_form())
        return jsonify(results)
    elif request.method == "POST":
        offer = json.load(request.data)
        new_offer = Offer(
            id = offer['id'],
            order_id = offer['order_id'],
            executor_id = offer['executor_id'],
            )
        db.session.add(new_offer)
        db.session.commit()
        return "offer added"


@app.route('/offers/<offerid>', methods = ["GET", "PUT", "DELETE"])
def offer_by_id(offerid):
    '''function which loads the data of selected offer from the database if we used GET method, delete selected offer if we used DELETE method and update selected offer if we used PUT method'''
    if request.method == "GET":
        return Offer.query.get(offerid).dic_form(), 200, {'Content-Type':'application/json; charset=utf-8'}
    elif request.method == "DELETE":
        offer = Offer.query.get(offerid)
        db.session.delete(offer)
        db.session.commit()
        return "offer deleted"
    elif request.method == "PUT":
        upd_offer = json.loads(request.data)
        offer = Offer.query.get(offerid)
        offer.id = upd_offer['id']
        offer.order_id = upd_offer['order_id']
        offer.executor_id = upd_offer['executor_id']
        db.session.add(offer)
        db.session.commit()
        return "offer updated"


if __name__ == "__main__":
    app.run(debug=True)