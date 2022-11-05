from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import date, timedelta
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity


app = Flask(__name__)

app.config ['JSON_SORT_KEYS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://steffy:password@127.0.0.1:5432/trello_dev'
app.config['JWT_SECRET_KEY'] = 'hello there'


db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)   


class Pharmacist(db.Model):
    __tablename__ = 'pharmacist'

    pharmacistid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    emailid = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

class PharmacistSchema(ma.Schema):
    class Meta:
        fields = ('pharmacistid', 'name', 'emailid', 'password', 'is_admin')

class MedicineList(db.Model):
    __tablename__ = 'medicinelist'

    medid = db.Column(db.Integer, primary_key=True)
    medname = db.Column(db.String)
    medtype = db.Column(db.String, nullable=False)
    meddose = db.Column(db.String, nullable=False)
    description = db.Column(db.String)

class MedicineListSchema(ma.Schema):
    class Meta:
        fields = ('medid', 'medname', 'medtype', 'meddose', 'description')

class MedicineStock(db.Model):
    __tablename__ = 'medicinestock'

    medStockId = db.Column(db.Integer, primary_key=True)
    medid = db.Column(db.Integer, primary_key=True)
    PricePerUnit = db.Column(db.Numeric)
    Expiry = db.Column(db.String, nullable=False)
    meddose = db.Column(db.String, nullable=False)
    description = db.Column(db.String)

class MedicineStockSchema(ma.Schema):
    class Meta:
        fields = ('medStockId', 'medid', 'PricePerUnit', 'Expiry', 'meddose','description')

class PurchaseOrder(db.Model):
    __tablename__ = 'purchaseorder'

    purchaseorderid = db.Column(db.Integer, primary_key=True)
    medstockid = db.Column(db.Integer, primary_key=True)
    pharmacistid = db.Column(db.Numeric)
    price = db.Column(db.String, nullable=False)
    quantity = db.Column(db.String, nullable=False)
    
class PurchaseOrderSchema(ma.Schema):
    class Meta:
        fields = ('purchaseorderid', 'medstockid', 'pharmacistid', 'price', 'meddose','quantity')



################################################################


# Define a custom CLI (terminal) command
@app.cli.command('createpharmtables')
def create_db():
    db.create_all()
    print("Pharmacy Management Tables created")

@app.cli.command('droppharmtables')
def drop_db():
    db.drop_all()
    print("Pharmacy Management Tables dropped")

@app.cli.command('seedpharmtables')
def seed_db():
    users = [
        User(
            email='admin@spam.com',
            password=bcrypt.generate_password_hash('eggs').decode('utf-8'),
            is_admin=True
        ),
        User(
            name='John Cleese',
            email='someone@spam.com',
            password=bcrypt.generate_password_hash('12345').decode('utf-8')
        )
    ]

    cards = [
        Card(
            title = 'Start the project',
            description = 'Stage 1 - Create the database',
            status = 'To Do',
            priority = 'High',
            date = date.today()
        ),
        Card(
            title = "SQLAlchemy",
            description = "Stage 2 - Integrate ORM",
            status = "Ongoing",
            priority = "High",
            date = date.today()
        ),
        Card(
            title = "ORM Queries",
            description = "Stage 3 - Implement several queries",
            status = "Ongoing",
            priority = "Medium",
            date = date.today()
        ),
        Card(
            title = "Marshmallow",
            description = "Stage 4 - Implement Marshmallow to jsonify models",
            status = "Ongoing",
            priority = "Medium",
            date = date.today()
        )
    ]

    db.session.add_all(cards)
    db.session.add_all(users)
    db.session.commit()
    print('Tables seeded')


    ################################################################




#Display medicine stock
@app.route('/medstock/')

#Display List of medicines and its details
@app.route('/medlist/')


#Insert medicine to stock
@app.route('/addmedtostock/')


#Update Pharmacist information
@app.route('/updatepharmacistinfo/')

#Delete medicine from stock
@app.route('/deletemedicinefromstock/')








