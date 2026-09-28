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
@app.route('/prices')
def prices():
    # Sample Mandi Data
    mandi_data = [
        {"crop": "Wheat (गेहूं)", "mandi": "Khagaria Mandi", "price": "₹2,250 / Qtl", "trend": "+₹50", "status": "up"},
        {"crop": "Paddy (धान)", "mandi": "Muzaffarpur Mandi", "price": "₹2,180 / Qtl", "trend": "-₹20", "status": "down"},
        {"crop": "Maize (मक्का)", "mandi": "Begusarai Mandi", "price": "₹1,950 / Qtl", "trend": "+₹30", "status": "up"},
        {"crop": "Potato (आलू)", "mandi": "Patna Mandi", "price": "₹1,400 / Qtl", "trend": "0", "status": "neutral"},
        {"crop": "Tomato (टमाटर)", "mandi": "Samastipur Mandi", "price": "₹2,800 / Qtl", "trend": "+₹100", "status": "up"}
    ]
    return render_template('prices.html', rates=mandi_data)
@app.route('/marketplace')
def marketplace():
    # Sample Marketplace Crops Data
    crops_list = [
        {"id": 1, "title": "Premium Organic Wheat", "seller": "Ramesh Kumar", "location": "Khagaria, Bihar", "quantity": "50 Quintals", "price": "₹2,300 / Qtl", "category": "Grains"},
        {"id": 2, "title": "Fresh Hybrid Maize", "seller": "Suresh Singh", "location": "Begusarai, Bihar", "quantity": "120 Quintals", "price": "₹1,980 / Qtl", "category": "Grains"},
        {"id": 3, "title": "Sharbati Basmati Rice", "seller": "Amit Patel", "location": "Muzaffarpur, Bihar", "quantity": "30 Quintals", "price": "₹3,800 / Qtl", "category": "Rice"},
        {"id": 4, "title": "Red Desi Potato", "seller": "Vikas Verma", "location": "Patna, Bihar", "quantity": "80 Quintals", "price": "₹1,450 / Qtl", "category": "Vegetables"}
    ]
    return render_template('marketplace.html', crops=crops_list)
@app.route('/logistics')
def logistics():
    vehicles_list = [
        {"id": 1, "driver": "Ramesh Express Logistics", "type": "Tata 407 (3.5 Ton)", "route": "Khagaria ➔ Patna", "rate": "₹18 / km", "contact": "+91 9876543210", "status": "Available"},
        {"id": 2, "driver": "Kisan Transport Services", "type": "Mahindra Pickup (1.5 Ton)", "route": "Begusarai Local / Inter-district", "rate": "₹14 / km", "contact": "+91 9812345678", "status": "Available"},
        {"id": 3, "driver": "Bihar Freight Carriers", "type": "10-Wheeler Truck (15 Ton)", "route": "Muzaffarpur ➔ Kolkata / Delhi", "rate": "₹32 / km", "contact": "+91 9765432109", "status": "On Route"}
    ]
    return render_template('logistics.html', vehicles=vehicles_list)