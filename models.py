from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    phone_number = db.Column(db.String(15), nullable=True)
    address = db.Column(db.String(200), nullable=True)
    district = db.Column(db.String(100), nullable=True)
    state = db.Column(db.String(100), nullable=True)
    role = db.Column(db.String(20), default="Farmer")  # Farmer, Buyer, Transporter
    company_name = db.Column(db.String(120), nullable=True)
    gst_number = db.Column(db.String(30), nullable=True)
    vehicle_type = db.Column(db.String(50), nullable=True)
    vehicle_number = db.Column(db.String(30), nullable=True)

    produces = db.relationship('Produce', backref='seller', lazy=True)

class Produce(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    crop_name = db.Column(db.String(100), nullable=False)
    quantity_kg = db.Column(db.Float, nullable=False)
    expected_price = db.Column(db.Float, nullable=True)
    quality_grade = db.Column(db.String(20), default="A Grade")
    location = db.Column(db.String(100), default="Mandi Central")
    seller_name = db.Column(db.String(100), default="Trader/Farmer")
    seller_role = db.Column(db.String(30), default="Farmer")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    
    offers = db.relationship('BuyerOffer', backref='produce', lazy=True)

class BuyerOffer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    buyer_name = db.Column(db.String(100), nullable=False)
    offered_price = db.Column(db.Float, nullable=False)
    produce_id = db.Column(db.Integer, db.ForeignKey('produce.id'), nullable=False)

class MandiPrice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    crop_name = db.Column(db.String(100), nullable=False)
    mandi_name = db.Column(db.String(100), nullable=False)
    min_price = db.Column(db.Float, nullable=False)
    max_price = db.Column(db.Float, nullable=False)
    modal_price = db.Column(db.Float, nullable=False)
    date = db.Column(db.String(20), nullable=False)