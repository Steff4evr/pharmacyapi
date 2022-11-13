# SteffyJohnson_T2A2 - API Webserver Project

# MEDIA LINKS
[github repo](https://github.com/Steff4evr/pharmacyapi.git)

# R1 - Identification of the problem you are trying to solve by building this particular app
The pharmacy management system app is an app that is designed to manage a pharmacy inventory .
Pharmacy inventory management is fundamentally required to make the system profitable. By enhancing inventory management, we safeguard the system from becoming disorganized, we are able to understand the market trends better, and employ cost-minimizing strategies. Identifying key trends is essential because for a pharmacy the trend is usually local which may not be the same as that of larger geography. 

Furthermore, it helps in making accurate projections of what could be the demand for in the times to come. If historical inventory data is recorded and analyzed for a few years, the pharmacy could end up having a sales trend. It can give crucial insights into what will be sold in the future. A robust system of managing inventory helps to maintain accurate shelved stocks and prices. 

# R2 - Why is it a problem that needs solving
Poor inventory management systems fail to timely alert and replenish inventory.  Therefore it is important that inventories are managed well. 
In this way of managing a pharmacy inventory, the pharmacist or the designated person takes a visual survey of the inventory and counts in-hand stock against the product list and quantity. A purchasing order is raised when the stock number falls below the desired listed amount.

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



# R6	An ERD for your app
![MENU](./docs/Pharmacymanagement_ERD.png)

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

# R7	Detail any third party services that your app will use



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

## ERD Diagram
Create the ERD diagram as the first task. Activities includes Identifying the entities and its attributes. The relationships between the entities are defined. Followed by creation of the ERD diagram using any online app.

## Folder Structure 
Create appropirate folder structure for the project 

## Environment setup 
Setup the virtual environment and install the required libraries. Also install the chosen database. Here PostgreSQL database is the one used.

## Create Models and Schemas
Write code for model and schemas. Write CLI command for creating those tables. Execute those CLI commands to  create the tables in the database.

## Drop Tables
Write CLI command for drop tables. This is required in case the tables need to be dropped and recreated. 

## Seed the APP Tables
Write CLI command for seeding the tables with initial records. Execute the CLI commands for inserting the records to the table.

## Endpoints
Identify the the CRUD activities that the APP will perform and decide the endpoints for the APP. 

## Create route function for the endpoints.
Route functons for each CRUD activities identified. 

Display Medicine list
Display Medicine stock
Display Purchase order
User registration
User login
Add medicines to stock
Create purchase order
Update medicine stock
Update pharmacist info

## Documentation
Write README documentation and the ensure sufficient comments are presend for the code.

