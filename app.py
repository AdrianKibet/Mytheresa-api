from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy.exc

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///product.db'
db = SQLAlchemy(app)


# database was more convenient for keeping records
class Product(db.Model):
    '''Product model'''
    sku = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    currency = db.Column(db.String(8), default=False)
    original_price = db.Column(db.Integer, nullable=False)
    discount_percentage = db.Column(db.Integer, default=False)
    final_price = db.Column(db.Integer, nullable=False)


@app.route('/product', methods=['GET', 'POST'])
def product():
    '''processes GET and POST data'''
    if request.method == 'GET':
        # without parameters specified
        products = Product.query.order_by(Product.sku).limit(5).all()
        if 'category' in request.args:
            # parameter 'category' is specified
            category = request.args.get('category')
            products = Product.query.filter_by(category=category).limit(5)
        if 'priceLessThan' in request.args:
            # parameter 'priceLessThan' is specified
            priceLessThan = request.args.get('priceLessThan')
            products = Product.query.filter(Product.original_price<=priceLessThan).limit(5)

        json_list = []
        for product in products:
            x = {
                'sku': product.sku,
                'name': product.name,
                'category': product.category,
                'price': {
                    'original': product.original_price,
                    'final': product.final_price,
                    'discount_percentage': None if product.discount_percentage == 0 else '%s%%'%(product.discount_percentage),
                    'currency': product.currency
                    }}
            json_list.append(x)
        return jsonify(json_list)

    if request.method == 'POST':
        # convenient method for adding records
        content = request.get_json(silent=True)
        products = content['products']
        product_list = []
        for product in products:
            if Product.query.filter_by(sku=product["sku"]).first():
                continue
            product_sku = product["sku"]
            product_name = product["name"]
            product_category = product["category"]
            product_currency = "EUR"
            product_original_price = product["price"]
            # what happens when we change our discount strategy?
            # implementing function to apply discount seemed unnecessary given time and goals
            if product_sku == "000003" and product_category != "boots":
                product_discount_percentage = 15
            if product_category == "boots":
                product_discount_percentage = 30
            else:
                product_discount_percentage = 0
            product_final_price = product["price"] 
            if product_discount_percentage != 0:
                product_final_price =  int(product_original_price * ((100 - product_discount_percentage)/100))
            discount = None 
            if product_discount_percentage != 0:
                discount = '%s%%'%(product_discount_percentage)

            create_product = Product(
                sku=product_sku, name=product_name, category=product_category,
                currency=product_currency, original_price=product_original_price,
                discount_percentage=product_discount_percentage, final_price=product_final_price)
            

            try:
                db.session.add(create_product)
                # If there are 20000 products, you'll create 20000 transactions.
                # On the flip side if a product fails to save here, all the preceding products will have
                # saved successfully.
                db.session.commit()
                product_list.append({
                    'sku': product_sku,
                    'name': product_name,
                    'category': product_category,
                    'price': {
                        'original': product_original_price,
                        'final': product_final_price,
                        'discount_percentage': discount,
                        'currency': product_currency
                    }
                })
            except Exception as e:
                return jsonify('An issue occurred saving the product: ' + str(e), status=500)
        return jsonify(product_list)


def create_products():
    '''create products for test'''
    Product1 = Product(sku='000001', name='BV Lean leather ankle boots', category="boots", currency="EUR", original_price=89000, discount_percentage=30, final_price=62299)
    Product2 = Product(sku='000002', name='BV Lean leather ankle boots', category="boots", currency="EUR", original_price=99000, discount_percentage=30, final_price=69300)
    Product3 = Product(sku='000003', name='Ashlington leather ankle boots', category="boots", currency="EUR", original_price=71000, discount_percentage=30, final_price=49700)
    Product4 = Product(sku='000004', name='Naima embellished suede sandals', category="sandals", currency="EUR", original_price=79500, discount_percentage=None, final_price=79500)
    Product5 = Product(sku='000005', name='Nathane leather sneakers', category="sneakers", currency="EUR", original_price=59000, discount_percentage=None, final_price=59000)
    Product6 = Product(sku='000006', name='Gucci leather sneakers', category="sneakers", currency="EUR", original_price=89000, discount_percentage=None, final_price=89000)

    try:
        db.session.add(Product1)
        db.session.add(Product2)
        db.session.add(Product3)
        db.session.add(Product4)
        db.session.add(Product5)
        db.session.add(Product6)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        print('Products already created')

if __name__ == "__main__":
    #()
    db.create_all()
    create_products()
    app.run(debug=True, port=5000)
