from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import date, timedelta
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError
from sqlalchemy import update,desc
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity


app = Flask(__name__)

app.config['JSON_SORT_KEYS'] = False
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
    pharm_rel = db.relationship(
        'PurchaseOrder', backref='purchaseorder', cascade='all, delete-orphan', lazy='dynamic')


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
    med_rel = db.relationship(
        'MedicineStock', backref='medicinelist', cascade='all, delete-orphan', lazy='dynamic')


class MedicineListSchema(ma.Schema):
    class Meta:
        fields = ('med_id', 'med_name', 'med_type', 'med_dose', 'description')


class MedicineStock(db.Model):
    __tablename__ = 'medicinestock'

    med_stockid = db.Column(db.Integer, primary_key=True)
    med_id = db.Column(db.Integer, db.ForeignKey(
        'medicinelist.med_id'), unique=True, nullable=False)
    quantity = db.Column(db.Numeric, nullable=False)
    price_per_unit = db.Column(db.Numeric, nullable=False)
    description = db.Column(db.String)
    medstock_rel = db.relationship(
        'PurchaseOrder', backref='purchaseorder1', cascade='all, delete-orphan', lazy='dynamic')


class MedicineStockSchema(ma.Schema):
    class Meta:
        fields = ('med_stockid', 'med_id', 'quantity',
                  'price_per_unit', 'description')


class PurchaseOrder(db.Model):
    __tablename__ = 'purchaseorder'

    purchaseorder_id = db.Column(db.Integer, primary_key=True)
    med_stockid = db.Column(db.Integer, db.ForeignKey(
        'medicinestock.med_stockid'), nullable=False)
    pharmacist_id = db.Column(db.Integer, db.ForeignKey(
        'pharmacist.pharmacist_id'), nullable=False)
    price = db.Column(db.Numeric, nullable=False)
    quantity = db.Column(db.Numeric, nullable=False)


class PurchaseOrderSchema(ma.Schema):
    class Meta:
        fields = ('purchaseorder_id', 'med_stockid',
                  'pharmacist_id', 'price', 'meddose', 'quantity')

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
            pharmacist_id=1,
            name='admin',
            emailid='admin@pharm.com',
            password=bcrypt.generate_password_hash('abcd').decode('utf-8')
        ),
        Pharmacist(
            pharmacist_id=2,
            name='steffy',
            emailid='steffy@pharm.com',
            password=bcrypt.generate_password_hash('abcd').decode('utf-8')
        )
    ]

    medicinelist = [
        MedicineList(
            med_id=1,
            med_name='PANADOL STRIP 10',
            med_type='Paracetamol',
            med_dose='500Mg',
            description='Paracetamol'
        ),
        MedicineList(
            med_id=2,
            med_name='NUROFEN STRIP 15',
            med_type='IBUPROFEN',
            med_dose='100Mg',
            description='IBUPROFEN'
        ),
        MedicineList(
            med_id=3,
            med_name='METFORMIN SZ 500mg TAB 100',
            med_type='Generic',
            med_dose='100Mg',
            description='METFORMIN'
        ),
        MedicineList(
            med_id=4,
            med_name='TADALAFIL SDZ 20MG 8 TABLETS',
            med_type='Generic',
            med_dose='100Mg',
            description='TADALAFIL'
        )
    ]

    medicinestock = [
        MedicineStock(
            med_stockid=1,
            med_id=1,
            quantity=100,
            price_per_unit=15,
            description='Paracetamol'
        ),
        MedicineStock(
            med_stockid=2,
            med_id=2,
            quantity=100,
            price_per_unit=10,
            description='IBUPROFEN'
        ),
        MedicineStock(
            med_stockid=3,
            med_id=3,
            quantity=100,
            price_per_unit=10,
            description='METFORMIN'
        ),
        MedicineStock(
            med_stockid=4,
            med_id=4,
            quantity=100,
            price_per_unit=15,
            description='TADALAFIL'
        )
    ]

    purchaseorder = [
        PurchaseOrder(
            med_stockid=1,
            pharmacist_id=2,
            price=30,
            quantity=2
        ),
        PurchaseOrder(
            med_stockid=1,
            pharmacist_id=2,
            price=45,
            quantity=3
        )

    ]

    db.session.add_all(pharmacists)
    db.session.add_all(medicinelist)
    db.session.add_all(medicinestock)
    db.session.add_all(purchaseorder)
    db.session.commit()
    print('Tables seeded')

    ################################################################

@app.route('/auth/register/', methods=['POST'])
@jwt_required()
def auth_register():
    try:
        # Register new pharmacist user
        user = Pharmacist(
            emailid = request.json['emailid'],
            password = bcrypt.generate_password_hash(request.json['password']).decode('utf8'),
            name = request.json['name']
        )
        # Add and commit user to DB
        db.session.add(user)
        db.session.commit()
        # Respond to client
        return UserSchema(exclude=['password']).dump(user), 201
    except IntegrityError:
        return {'error': 'Email address already in use'}, 409    

#User login and authentication
@app.route('/auth/login/', methods=['POST'])
def auth_login():
    # Find a user by email address
    stmt = db.select(Pharmacist).filter_by(emailid=request.json['emailid'])
    user = db.session.scalar(stmt)
    # If user exists and password is correct
    if user and bcrypt.check_password_hash(user.password, request.json['password']):        
        token = create_access_token(identity=str(user.pharmacist_id), expires_delta=timedelta(days=1))
        return {'email': user.emailid, 'token': token}
    else:
        return {'error': 'Invalid email or password'}, 401
        
# Display medicine stock
@app.route('/medstock/')
def display_stock():
    medicine_stock_schema = MedicineStockSchema(many=True)
    # Fetch all records for medicine stock
    med_stock = MedicineStock.query.order_by(MedicineStock.med_stockid).all()
    # Convert the nedicine stock data from database into a JSON format and store them in result variable.
    result = medicine_stock_schema.dump(med_stock)
    # return the data in JSON format
    return jsonify(result)

# Display List of medicines and its details
@app.route('/medlist/')
def display_medlist():
    medicine_list_schema = MedicineListSchema(many=True)
    # Fetch all the records of the medicines
    med_list = MedicineList.query.order_by(MedicineList.med_id).all()
    # convert the medicine list data from db into JSON format and store them in result variable
    result = medicine_list_schema.dump(med_list)
    # Retun the data in JSON format
    return jsonify(result)

# Display purchase orders
@app.route('/po/')
def display_po():
    if not authorize():
        return {'error': 'You must be a user'},401
    po_schema = PurchaseOrderSchema(many=True)
    # Fetch all the records of the medicines
    po_list = PurchaseOrder.query.order_by(desc(PurchaseOrder.purchaseorder_id)).all()
    # convert the medicine list data from db into JSON format and store them in result variable
    result = po_schema.dump(po_list)
    # Retun the data in JSON format
    return jsonify(result)


# Update Pharmacist information
@app.route('/updatepharmacistinfo/', methods=['POST'])
@jwt_required()
def update_pharm():
    try:
        pharm = Pharmacist(
            pharmacist_id=request.json['pharmacist_id'],
            name=request.json['name'],
            emailid=request.json['email']
        )
        if db.session.query(Pharmacist).filter(Pharmacist.pharmacist_id == pharm.pharmacist_id).count() > 0:
            db.session.query(Pharmacist).filter(Pharmacist.pharmacist_id == pharm.pharmacist_id).update(
                {Pharmacist.name: pharm.name, Pharmacist.emailid: pharm.emailid}, synchronize_session=False)
        else:
            return {'Not_found': 'Matching Pharmacist record was not found'}, 400
        db.session.commit()
        # Respond to client
        return {'Success': 'Successfully committed'}, 201
    except IntegrityError:
        return {'error': ' The email id is already in use. Please enter a different email id'}, 400


# Insert medicine to stock
@app.route('/addmedtostock/', methods=['POST'])
@jwt_required()
def add_med():
    try:
        med = MedicineStock(            
            med_id=request.json['medid'],
            price_per_unit=request.json['price'],
            med_dose=request.json['meddose'],
            description=request.json['description']
        )
        if db.session.query(MedicineList).filter(MedicineList.med_id == med.med_id).count() == 0:
            return {'Not_found': 'Medicine id is invalid, Please enter a valid medicine that is present in the medicine list'}, 400        
        # Add and command the medicine to DB
        db.session.add(med)
        db.session.commit()
        # Respond to client
        return {'Success': 'Successfully committed'}, 201
    except IntegrityError:
        return {'error': 'The medicine that you are trying to add is already present in stock. Try updating the quantity of the existing item in stock'}, 400



# Update medicine  stock
@app.route('/updatemedicinestock/', methods=['POST'])
#@jwt_required()
def update_medicine():
    try:
        med = MedicineStock(
            med_stockid=request.json['stockid'],
            price_per_unit=request.json['price_per_unit'],
            quantity=request.json['quantity']
        )
        # Check if quantity or price is correct.
        if med.quantity < 0 or med.price_per_unit < 0:
            return {'Value error': 'The quantity or price has to be valid positve numbers'}, 400
        # Check if the stock record is already present.
        elif db.session.query(MedicineStock).filter(MedicineStock.med_stockid == med.med_stockid).count() > 0 :
            db.session.query(MedicineStock).filter(MedicineStock.med_stockid == med.med_stockid).update(
                {MedicineStock.price_per_unit: med.price_per_unit, MedicineStock.quantity: med.quantity}, synchronize_session=False)
        else:
            return {'Not_found': 'There are no matching medicine to  update in stock'}, 400        
        db.session.commit()
        # Respond to client
        return {'Success': 'Successfully Updated the stock'}, 201
    except IntegrityError:
        return {'error': 'The values provided is not satifying the integrity constraints'}, 400
    except:
        return {'error': 'Invalid Input'}, 400

# Add to PurchaseOrder - This endpoint is used to handle customer purchase orders. 
@app.route('/purchaseorder/', methods=['POST'])
@jwt_required()
def purchaseorder():
    try:
        med = PurchaseOrder(
            med_stockid=0,
            pharmacist_id=request.json['pharmacist_id'],
            price=0,
            quantity=request.json['quantity']
        )
        med_id = request.json['medid']
        # Verify if the Medicine is a valid one. Else return the error message
        if db.session.query(MedicineList).filter(MedicineList.med_id == med_id).count() == 0:
            return {'Not_found': 'Medicine id is invalid. Please enter correct medicine id'}, 400
        # Verify if Quantity is available in stock . Else return the error message
        if db.session.query(MedicineStock).filter(MedicineStock.med_id == med_id and MedicineStock.quantity == 0).count() == 0:
            return {'Not_found': 'Medicine is currently not available in stock'}, 400
        else:
            med_stockid = db.session.query(MedicineStock.med_stockid).filter(
                MedicineStock.med_id == med_id).scalar()
            # Fetch the quantity currently available in stock
            available_quantity = db.session.query(MedicineStock.quantity).filter(
                MedicineStock.med_id == med_id).scalar()
            # If sufficient quantity is not available then return error message
            if available_quantity < med.quantity:
                return {'Quantity_error': ' There is insufficient quantity in stock'}, 400
            # Get the price
            price = db.session.query(MedicineStock.price_per_unit).filter(
                MedicineStock.med_id == med_id).scalar()
            med.med_stockid = med_stockid
            # Calculate the price for the purchased quantity
            med.price = price * med.quantity
            # Update the Medicine stock with the updated quantity
            db.session.query(MedicineStock).filter(MedicineStock.med_stockid == med_stockid).update(
                {MedicineStock.quantity:  MedicineStock.quantity - med.quantity}, synchronize_session=False)
        # Add and command the medicine to DB
        db.session.add(med)
        db.session.commit()
        # Respond to client
        return {'Success': 'Successfully committed'}, 201
    except IntegrityError:
        return {'error': ' The Pharmacist ID is incorrect'}, 400


@app.route('/')
def index():
    return "WELCOME TO STEFFS PHARMACY!"
