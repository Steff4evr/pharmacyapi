from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import date, timedelta
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity


app = Flask(__name__)

app.config ['JSON_SORT_KEYS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://steffy:password@127.0.0.1:5432/pharmacymanagement'
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
    pharm_rel = db.relationship('PurchaseOrder',backref='purchaseorder',cascade = 'all, delete-orphan', lazy = 'dynamic')

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
    medstock_rel = db.relationship('PurchaseOrder',backref='purchaseorder1',cascade = 'all, delete-orphan', lazy = 'dynamic')

class MedicineStockSchema(ma.Schema):
    class Meta:
        fields = ('med_StockId', 'med_id', 'Price_Per_Unit', 'Expiry', 'meddose','description')

class PurchaseOrder(db.Model):
    __tablename__ = 'purchaseorder'

    purchaseorder_id = db.Column(db.Integer, primary_key=True)
    med_stockid = db.Column(db.Integer, db.ForeignKey('medicinestock.med_StockId'),nullable=False)
    pharmacist_id = db.Column(db.Integer,db.ForeignKey('pharmacist.pharmacist_id'),nullable=False)
    price = db.Column(db.Numeric, nullable=False)
    quantity = db.Column(db.Numeric, nullable=False)
    
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
    pharmacists = [
        Pharmacist(
            pharmacist_id = 1,            
            name = 'admin',
            emailid = 'admin@pharm.com',
            password = bcrypt.generate_password_hash('abcd').decode('utf-8'),
            is_admin = True
        ),
        Pharmacist(
            pharmacist_id = 2,
            name = 'steffy',
            emailid = 'steffy@pharm.com',
            password = bcrypt.generate_password_hash('abcd').decode('utf-8'),
            is_admin = True
        )
    ]

    medicinelist = [
        MedicineList(
            med_id = 1,
            med_name = 'PANADOL STRIP 10',
            med_type = 'Paracetamol',
            med_dose = '500Mg',
            description = 'Paracetamol'
        ),
        MedicineList(
            med_id = 2,
            med_name = 'NUROFEN STRIP 15',
            med_type = 'IBUPROFEN',
            med_dose = '100Mg',
            description = 'IBUPROFEN'
        ),
        MedicineList(
            med_id = 3,
            med_name = 'METFORMIN SZ 500mg TAB 100',
            med_type = 'Generic',
            med_dose = '100Mg',
            description = 'METFORMIN'
        ),
        MedicineList(
            med_id = 4,
            med_name = 'TADALAFIL SDZ 20MG 8 TABLETS',
            med_type = 'Generic',
            med_dose = '100Mg',
            description = 'TADALAFIL'
        )
    ]

    medicinestock = [
        MedicineStock(
            med_StockId = 1,
            med_id = 1,
            Price_Per_Unit = 15,
            Expiry = '25-DEC-2022',
            meddose = '1 per day',
            description = 'Paracetamol'                
        ),
        MedicineStock(
            med_StockId = 2,
            med_id = 2,
            Price_Per_Unit = 10,
            Expiry = '1-DEC-2022',
            meddose = '2 per day',
            description = 'IBUPROFEN'   
        ),
        MedicineStock(
            med_StockId = 3,
            med_id = 3,
            Price_Per_Unit = 10,
            Expiry = '22-DEC-2022',
            meddose = '1 per day',
            description = 'METFORMIN'   
        ),
        MedicineStock(
            med_StockId = 4,
            med_id = 4,
            Price_Per_Unit = 15,
            Expiry = '31-DEC-2022',
            meddose = '3 per day',
            description = 'TADALAFIL'               
        )
    ]

    purchaseorder = [
        PurchaseOrder(            
            med_stockid = 1,
            pharmacist_id = 2,
            price = 30,
            quantity = 2
        ),
        PurchaseOrder(
            med_stockid = 1,
            pharmacist_id = 2,
            price = 45,
            quantity = 3
        )

    ]

    db.session.add_all(pharmacists)
    db.session.add_all(medicinelist)
    db.session.add_all(medicinestock)
    db.session.add_all(purchaseorder)
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