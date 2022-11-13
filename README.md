# SteffyJohnson_T2A2 - API Webserver Project

# MEDIA LINKS
[github repo](https://github.com/Steff4evr/pharmacyapi.git)

# R1 - Identification of the problem you are trying to solve by building this particular app
The pharmacy management system app is an app that is designed to manage a pharmacy inventory .
Pharmacy inventory management is fundamentally required to make the system profitable. By enhancing inventory management, we safeguard the system from becoming disorganized, we are able to understand the market trends better, and employ strategies to minimize costs. Identifying key trends is essential because for a pharmacy the trend is usually local which may not be the same as that of larger geography. 

Furthermore, it helps in making accurate projections of what could be the future demand. If historical inventory data is recorded and analyzed for a few years, the pharmacy could end up having a sales trend. It can give crucial insights into what will be sold in the future. A robust system of managing inventory helps to maintain accurate shelved stocks and prices. 

# R2 - Why is it a problem that needs solving
Poor inventory management systems fail to timely alert and replenish inventory.  Therefore it is important that inventories are managed well. 
In this way of managing a pharmacy inventory, the pharmacist or the designated person takes a visual survey of the inventory and counts in-hand stock against the product list and quantity. A purchasing order is raised when the stock number falls below the desired listed amount. In this way we can safe gaurd the business from failing altogether. 

# R3 - Why have you chosen this database system. What are the drawbacks compared to others?
PostgreSQL is cross-platform, so you can run a database server on all major operating systems such as Linux, Windows, and macOS.
The software is open-source and is distributed free of charge. It is built and maintained by a worldwide community of contributors and volunteers.
Since it is open-source, PostgreSQL is also highly extensible. It is possible to augment the database’s operation with your own custom plugins, functions, and data types.Another great advantage is that PostgreSQL is highly scalable. Postgres database can be run on a single computer for small projects and also on a cluster of servers for enterprise-grade applications. PostgreSQL is powerful, yet easy to learn.It is highly scalable and also benefits from relatively low maintenance costs. Each Postgres database utilizes write-ahead logging which makes it very fault-tolerant, further reducing maintenance and troubleshooting costs.

## Drawbacks
It is common for applications to lack support for PostgreSQL. This lack of support is mainly due to the fact that Postgres is an open-source project that is not being developed and marketed by an enterprise-level company.
Postgres databases often show worse performance when compared to other database management systems like MySQL.It is also more difficult to optimize the performance of a Postgres database when compared to others. The increased difficulty comes from the fact that PostgreSQL is built with a focus on features and compatibility rather than performance. PostgreSQL conforms to the SQL standard. Unfortunately, some commands may have a somewhat different syntax and/or function. So even if you know how to write SQL queries, you might still run into a roadblock every now and then.

# R4	Identify and discuss the key functionalities and benefits of an ORM
An object-relational mapper provides an object-oriented layer between relational databases and object-oriented programming languages without having to write SQL queries. It standardizes interfaces reducing any overhead and speeding development time.

Some of the functionalities of ORMs are -
- ORMs translate data and create a structured map to help developers understand the underlying database structure.
- The mapping explains how objects are related to different tables. 
- ORMs use this information to convert data between tables and generate the SQL code for a relational database to insert, update, create and delete data in response to changes the application makes to the data object.This enables the implementation of CRUD operation in the database through web API. 
- The ORM mapping will manage the application’s data needs and you will not need to write any more low-level code.

# R5	Document all endpoints for your API

### /auth/register/
### Method: POST
- Arguments: emailid (String,Email ID of pharmacist), password (Sting, Password of the user),name (String,Name of the user)
- Description: Inserts the new pharmacist.
- Authentication: @jwt_required()
- Headers-Authorization: Bearer {Token} - only existing pharmacist can access this route.
- Request Body: (can include one or all the fields shown below:)

{
    "emailid": "abcdefghi@gmail.com",
    "password": "1234abcd",    
    "name": "steff"    
}

{
    "pharmacist_id": 3,
    "emailid": "abcdefghi@gmail.com",
    "name": "steff"
}

### /auth/login/
### Method: POST
- Arguments: emailid (String,Email ID of pharmacist), password (Sting, Password of the user),name (String,Name of the user)
- Description: Inserts the new pharmacist.
- Authentication: @jwt_required()
- Headers-Authorization: Bearer {Token} - only existing pharmacist can access this route.
- Request Body: (can include one or all the fields shown below:)

{
    "emailid":"steffy@pharm.com",
    "password":"abcd"    
}
- Request response:
- 
{
    "email": "steffy@pharm.com",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2ODMzMTk5NSwianRpIjoiNzhmZjZkYzgtZGM1OC00YzQ4LTk5ZGEtODc4MWYyYjkxZGNkIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjIiLCJuYmYiOjE2NjgzMzE5OTUsImV4cCI6MTY2ODQxODM5NX0.NwadCylZME_uNAIyZjpDorU9ycwne7i1YlFWftW1Df8"
}

### /medstock/
### Method: GET
- Arguments: None
- Description: Fetch the medicine stock and display.
- Authentication: None required
- Headers-Authorization: None
- Response :

    {
        "description": "Paracetamol",
        "price_per_unit": "1000",
        "med_stockid": 1,
        "med_id": 1,
        "quantity": "1000"
    },

### /medlist/
### Method: GET
- Arguments: None
- Description: Fetch the medicine master list and display.
- Authentication: None required
- Headers-Authorization: None
- Response :

    {
        "description": "Paracetamol",
        "med_id": 1,
        "med_name": "PANADOL STRIP 10",
        "med_type": "Paracetamol",
        "med_dose": "500Mg"
    }

### /purchaseorder/
### Method: GET
- Arguments: None
- Description: Fetch the purchase order and display.
- Authentication: None required
- Headers-Authorization: None
- Response :

    {
        "price": "60",
        "med_stockid": 2,
        "purchaseorder_id": 18,
        "quantity": "6",
        "pharmacist_id": 1
    }

### /pharmacist/
### Method: GET
- Arguments: None
- Description: Fetch the pharmacist users and display.
- Authentication: @jwt_required()
- Headers-Authorization: Bearer {Token} - only existing pharmacist can access this route.
- Response :

    {
        "emailid": "steffy@pharm.com",
        "name": "steffy",
        "pharmacist_id": 2,
        "password": "$2b$12$76Bo3eRxvjjtFOuHzG8csey1ksAZhjkygcmKHUqKj0EHEGU/dwSnO"
    }
### /updatepharmacistinfo/
### Method: POST
- Arguments: pharmacist_id (Numeric, Pharmacist id of the pharmacist ),name (String, Name of the user)
- Description: Update the Name and email id of the user based on the pharmacist id
- Authentication: @jwt_required()
- Headers-Authorization: Bearer {Token} - only existing pharmacist can access this route.
- Request Body: 

{
    "pharmacist_id": 1,
    "name": "Steff"    
}

- Response
{
    "Success": "Successfully committed"
}

### /addmedtostock/
### Method: POST
- Arguments: medid (Numeric, Stockid of the stock ),price_per_unit (Numeric, price per unit of medicine ),quantity (Numeric, quantity of medicine ), discrption (String, desctiption of medicine)
- Description: Add medicines to stock
- Authentication: @jwt_required()
- Headers-Authorization: Bearer {Token} - only existing pharmacist can access this route.
- Request Body: 

{
    "medid": "2",
    "price": 20,    
    "quantity": "10",
    "description":"Generic"    
}

{'Success': 'Stock successfully added'}
- Request Body
{
    "medid": "2",
    "price": 20,    
    "quantity": "10",
    "description":"Generic"    
}

{
    "error": "The medicine that you are trying to add is already present in stock. Try updating the quantity of the existing item in stock"
}


### /updatemedicinestock/
### Method: POST
- Arguments: stockid (Numeric, Stockid of the stock ),price_per_unit (Numeric, price per unit of medicine ),quantity (Numeric, quantity of medicine )
- Description: Update the stock information.
- Authentication: @jwt_required()
- Headers-Authorization: Bearer {Token} - only existing pharmacist can access this route.
- Request Body: 

{
    "stockid": 2,
    "price_per_unit": 25,    
    "quantity": 13    
}

Response:

{
    "Success": "Successfully Updated the stock"
}


### /createpurchaseorder/
### Method: POST
- Arguments: pharmacist_id (Numeric, Pharmacist id of the pharmacist ),quantity (Numeric, quantity of medicine ),medid (Numeric, medicine id)
- Description: Create purchase order
- Authentication: @jwt_required()
- Headers-Authorization: Bearer {Token} - only existing pharmacist can access this route.
- Request Body: 

    {
        "medid": 1,
        "pharmacist_id": "1",
        "quantity": 10
    }
Response :
    {
        "pharmacist_id": 1,
        "price": "10000",
        "med_stockid": 1,
        "purchaseorder_id": 26,
        "quantity": "10"
    },

# R6	An ERD for your app
![MENU](./docs/Pharmacymanagement_ERD-5.png)

The pharmacy management application is mostly about inventory management. The ERD focusses mainly on the medicine stock and how is it managed. 
Below are the list of entities and the description :
## MedicineList:
Contains the list of the medicines that are associated with the pharmacy. This is the master list if medicines and contains the more information about the medicines.
The Med_Id or medicine identifier is the primary key of Integer type. Other fields include, information on the medicines like the medicine name, medicine type , dosage and description of the medicine. 
## MedicineStock:
The table represents the medicines that are currently available for sale. Medicince stock id is the primary key for this table. There is a foreign key reference to the MedicineList table which ensures that all the medicines that are available for sale are part of the MedicineList.Other important fields include, expiry date of the medicine, price of the medicine per unit, quantity of the units available in the inventory.
## Pharmacist:
The table pharmacist, contains the users who will be using the application for managing the pharmacy inventory. Here the pharmacist id is the primary key. It also contains the the fields to store the name of the user along with the emailid and password. Emailid is a unique key that is used for authentication purposes along with the password. The password is encrypted with bcrypt.
## PurchaseOrder:
The table PurchaseOrder contains the purchase order information of each purchase made by customers. Purchaseorder id is the primary key for this table. There is a foreign key reference to the Medicinestock table using the key medicine stockid. This ensures that all medicines that are purchased by customers are part of the inventory. Other fields include, price of the purchased product and the quantity. Price is the price of the item in relation with the quantity.  

# R8	Describe your projects models in terms of the relationships they have with each other

'Pharmacist' model is defined for modelling pharmacist users. Pharmacy id is set as the primary key.
A backref is also set for setting up foerign key relationship with the purchase order. 
'MedicineList' model is defined for defining the master list of medicines. Here Med_id is the primary key.
A backreference is set for enabling foreign key relationship with the medicinelist. 
'MedicineStock' model is defined for medicine stock. Here stockid is the primary key. Foreign key reference on the medicinelist tables primary key, which is medid. This is ensure that the stock does not have any medicine that is not part of the master list. There is a backref set for the purchaseorder.
'PurchaseOrder' model is defined for creating customer purchaseorders. Here purchase orderid is the primary key. Foreign key reference on the stockid in the medicine stock table. This is to ensure that the medicine that is in purchase order is from stock. There is foreign key reference on the pharmacisty id to ensure that the pharmacist user is a registered user.

# R9	Discuss the database relations to be implemented in your application

Medicinelist table master table contains the list of the  medicines and their details. The primary key is defined on the med_id. The table MedicineStock has the med_stockid as the primary key. The table has med_id which has a foreign key relationship with the Machinelist table. Any stock added to the MedicineStock table will have to satisfy the constraint with the medicinelist , which means that only those medicine that are part of master list can be added to the stock.Pharmacist table contains the list of users of the application. Pharmacy Id is the primary key here.  Finally, the purchase order table contains the customer purchase orders. Here purchaseorderid is the primary key. There is foreign key constraints for the med_stockid and pharmacist_id .This is to ensure that any purchase order created should be part of the stock. Also the pharmacist who create the purchase order has to be a registered user of the application.

# R10	Describe the way tasks are allocated and tracked in your project
[Trello](https://trello.com/b/MbLQeqVp/pharmacymanagement)

### 1 ERD Diagram
Create the ERD diagram as the first task. Activities includes Identifying the entities and its attributes. The relationships between the entities are defined. Followed by creation of the ERD diagram using any online app.

### 2 Folder Structure 
Create appropirate folder structure for the project 

### 3 Environment setup 
Setup the virtual environment and install the required libraries. Also install the chosen database. Here PostgreSQL database is the one used.

### 4 Create Models and Schemas
Write code for model and schemas. Write CLI command for creating those tables. Execute those CLI commands to  create the tables in the database.

### 5 Drop Tables
Write CLI command for drop tables. This is required in case the tables need to be dropped and recreated. 

### 6 Seed the APP Tables
Write CLI command for seeding the tables with initial records. Execute the CLI commands for inserting the records to the table.

### 7 Endpoints
Identify the the CRUD activities that the APP will perform and decide the endpoints for the APP. 

### 8 Create route function for the endpoints.
Route functons for each CRUD activities identified. 

Display Medicine list, 
Display Medicine stock,
Display Purchase order,
User registration,
User login,
Add medicines to stock,
Create purchase order,
Update medicine stock,
Update pharmacist info

### 9 Documentation
Write README documentation and the ensure sufficient comments are presend for the code.

