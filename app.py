from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, User, Produce, BuyerOffer, MandiPrice

app = Flask(__name__)
app.config['SECRET_KEY'] = 'parakram-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///parakram.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    produces = Produce.query.all()
    farmers = User.query.filter_by(role='Farmer').all()
    buyers = User.query.filter_by(role='Buyer').all()
    transporters = User.query.filter_by(role='Transporter').all()
    return render_template('index.html', produces=produces, farmers=farmers, buyers=buyers, transporters=transporters)

@app.route('/register-farmer', methods=['POST'])
def register_farmer():
    username = request.form.get('username')
    phone_number = request.form.get('phone_number')
    district = request.form.get('district')
    state = request.form.get('state')

    if username and phone_number:
        new_farmer = User(
            username=username,
            phone_number=phone_number,
            district=district,
            state=state,
            role='Farmer'
        )
        db.session.add(new_farmer)
        db.session.commit()
        flash(f'Farmer Profile created for {username}!', 'success')

    return redirect(url_for('home'))

@app.route('/register-buyer', methods=['POST'])
def register_buyer():
    username = request.form.get('username')
    phone_number = request.form.get('phone_number')
    company_name = request.form.get('company_name')
    gst_number = request.form.get('gst_number')

    if username:
        new_buyer = User(
            username=username,
            phone_number=phone_number,
            company_name=company_name,
            gst_number=gst_number,
            role='Buyer'
        )
        db.session.add(new_buyer)
        db.session.commit()
        flash(f'Buyer Profile created for {username}!', 'success')

    return redirect(url_for('home'))

@app.route('/register-transporter', methods=['POST'])
def register_transporter():
    username = request.form.get('username')
    phone_number = request.form.get('phone_number')
    vehicle_type = request.form.get('vehicle_type')
    vehicle_number = request.form.get('vehicle_number')

    if username:
        new_transporter = User(
            username=username,
            phone_number=phone_number,
            vehicle_type=vehicle_type,
            vehicle_number=vehicle_number,
            role='Transporter'
        )
        db.session.add(new_transporter)
        db.session.commit()

    return redirect(url_for('home'))

@app.route('/add-produce', methods=['POST'])
def add_produce():
    seller_name = request.form.get('seller_name')
    seller_role = request.form.get('seller_role', 'Farmer')
    crop_name = request.form.get('crop_name')
    quantity = request.form.get('quantity')
    price = request.form.get('price')

    if crop_name and quantity and price:
        new_produce = Produce(
            seller_name=seller_name,
            seller_role=seller_role,
            crop_name=crop_name,
            quantity_kg=float(quantity),
            expected_price=float(price)
        )
        db.session.add(new_produce)
        db.session.commit()

    return redirect(url_for('home'))

@app.route('/place-bid', methods=['POST'])
def place_bid():
    buyer_name = request.form.get('buyer_name')
    produce_id = request.form.get('produce_id')
    bid_price = request.form.get('bid_price')

    if buyer_name and produce_id and bid_price:
        offer = BuyerOffer(
            buyer_name=buyer_name,
            produce_id=int(produce_id),
            offered_price=float(bid_price)
        )
        db.session.add(offer)
        db.session.commit()

    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)