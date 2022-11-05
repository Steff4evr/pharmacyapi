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

    pharmacist_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    emailid = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

class PharmacistSchema(ma.Schema):
    class Meta:
        fields = ('pharmacist_id', 'name', 'emailid', 'password', 'is_admin')

class MedicineList(db.Model):
    __tablename__ = 'medicinelist'

    med_id = db.Column(db.Integer, primary_key=True)
    med_name = db.Column(db.String)
    med_type = db.Column(db.String, nullable=False)
    med_dose = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    med_rel = db.relationship('MedicineStock',backref='medicinelist',cascade = 'all, delete-orphan', lazy = 'dynamic')

class MedicineListSchema(ma.Schema):
    class Meta:
        fields = ('med_id', 'med_name', 'med_type', 'med_dose', 'description')

class MedicineStock(db.Model):
    __tablename__ = 'medicinestock'

    med_StockId = db.Column(db.Integer, primary_key=True)
    med_id = db.Column(db.Integer, db.ForeignKey('medicinelist.med_id'),nullable=False)
    Price_Per_Unit = db.Column(db.Numeric)
    Expiry = db.Column(db.String, nullable=False)
    meddose = db.Column(db.String, nullable=False)
    description = db.Column(db.String)

class MedicineStockSchema(ma.Schema):
    class Meta:
        fields = ('med_StockId', 'med_id', 'Price_Per_Unit', 'Expiry', 'meddose','description')

class PurchaseOrder(db.Model):
    __tablename__ = 'purchaseorder'

    purchaseorder_id = db.Column(db.Integer, primary_key=True)
    med_stockid = db.Column(db.Integer, primary_key=True)
    pharmacist_id = db.Column(db.Numeric)
    price = db.Column(db.String, nullable=False)
    quantity = db.Column(db.String, nullable=False)
    
class PurchaseOrderSchema(ma.Schema):
    class Meta:
        fields = ('purchaseorder_id', 'med_stockid', 'pharmacist_id', 'price', 'meddose','quantity')



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
        Pharmacist(            
            name = 'admin',
            emailid = 'admin@pharm.com',
            password = bcrypt.generate_password_hash('abcd').decode('utf-8'),
            is_admin = True
        ),
        Pharmacist(
            name = 'steffy',
            emailid = 'steffy@pharm.com',
            password = bcrypt.generate_password_hash('abcd').decode('utf-8'),
            is_admin = True
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
def display_stock():
    pass


#Display List of medicines and its details
@app.route('/medlist/')
def display_medlist():
    pass


#Insert medicine to stock
@app.route('/addmedtostock/')
def add_med():
    pass

#Update Pharmacist information
@app.route('/updatepharmacistinfo/')
def update_pharm():
    pass

#Delete medicine from stock
@app.route('/deletemedicinefromstock/')
def delete_medicine():
    pass