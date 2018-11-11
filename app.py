from flask import Flask, flash, redirect, render_template, request, session, abort,url_for,Response
from datetime import datetime
import PyPDF2
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tabledef import *
from reportlab.pdfgen import canvas
from billgeneratorfunction import makeBill

engine = create_engine('sqlite:///app.db')
 
app = Flask(__name__)

############################## Landing Page #########################################
@app.route('/')
def landingPage():
    global billItems
    if len(billItems) != 0:
        billItems = []
    return render_template('homepage.html')

############################ Add New Item #############################################
@app.route('/add', methods=['GET','POST'])
def addItem():
    global items
    if request.method == 'POST':
        POST_NAME = str(request.form['name'])
        POST_PRICE = str(request.form['price'])   
        Session = sessionmaker(bind=engine)
        s = Session()
        newItem = FoodItem(POST_NAME,POST_PRICE)
        s.add(newItem)
        s.commit()
        items = s.query(FoodItem).order_by(FoodItem.name).all()
        return render_template('addItem.html',items=items)
    return render_template('addItem.html',items=items)

############################ Add New MRP Item #########################################
@app.route('/addNewMrpItem', methods=['GET','POST'])
def addAnewMrpItem():
    if request.method == 'POST':
        global MrpItems
        POST_NAME = str(request.form['name'])
        Session = sessionmaker(bind=engine)
        s = Session()
        newItem = MrpFoodItem(POST_NAME)
        s.add(newItem)
        s.commit()
        MrpItems = s.query(MrpFoodItem).order_by(MrpFoodItem.name).all()
        return render_template('addNewMrpItem.html',MrpItems=MrpItems)
    return render_template('addNewMrpItem.html',MrpItems=MrpItems)

################ Add a Custom Item #####################################
@app.route('/addCustomItem', methods=['GET','POST'])
def addCustomItem():
    if request.method=='POST':
        POST_NAME = str(request.form['item'])
        POST_UNITS = str(request.form['units'])
        POST_PRICE = str(request.form['price'])
        NEWITEM=BillItem(POST_NAME,POST_UNITS,POST_PRICE)
        billItems.append(NEWITEM)
        return redirect(url_for('billing'))
    else:
        return render_template('AddCustomItem.html')


#################### Billing types ######################################################
@app.route('/billing', methods=['GET','POST'])
def billing():
    if request.method == 'GET':
        return render_template('billing.html',items=items,billItems=billItems)

@app.route('/billing1', methods=['GET','POST'])
def billing1():
    if request.method == 'GET':
        global TYPE
        TYPE = 1
        return render_template('billing.html',items=items,billItems=billItems)

@app.route('/billing2', methods=['GET','POST'])
def billing2():
    if request.method == 'GET':
        global TYPE
        TYPE = 2
        return render_template('billing.html',items=items,billItems=billItems)

@app.route('/billing3', methods=['GET','POST'])
def billing3():
    if request.method == 'GET':
        global TYPE
        TYPE = 3
        return render_template('selfBilling.html',items=items,billItems=billItems)

################ Adding Items to Bill and price retrieval of existing #####################
@app.route('/addMore', methods=['GET','POST'])
def addMore():
    if request.method=='POST':
        POST_NAME = str(request.form['item'])
        POST_UNITS = str(request.form['units'])
        Session = sessionmaker(bind=engine)
        s = Session()
        query = s.query(FoodItem).filter(FoodItem.name==POST_NAME)
        query=query.first()
        NEWITEM=BillItem(query.name,POST_UNITS,query.price)
        billItems.append(NEWITEM)
        return redirect(url_for('billing'))

@app.route('/removeItem/<id>', methods=['GET','POST'])
def remove(id):
    if request.method=='GET':
        indx = int(id)
        global billItems
        billItems.pop(indx)
        if TYPE == 3:
            return redirect(url_for('billing3'))
        else:
            return redirect(url_for('billing'))            

################ Self Assigned Price ##########################################
@app.route('/addSelfPriced', methods=['GET','POST'])
def addSelfPrice():
    if request.method=='POST':
        POST_NAME = str(request.form['item'])
        POST_UNITS = str(request.form['units'])
        POST_PRICE = str(request.form['price'])
        NEWITEM=BillItem(POST_NAME,POST_UNITS,POST_PRICE)
        billItems.append(NEWITEM)
        return redirect(url_for('billing3'))

################ Add an Item priced as per MRP #####################################
@app.route('/mrpItem', methods=['GET','POST'])
def addMRPitem():
    if request.method=='POST':
        POST_NAME = str(request.form['item'])
        POST_UNITS = str(request.form['units'])
        POST_PRICE = str(request.form['price'])
        NEWITEM=BillItem(POST_NAME,POST_UNITS,POST_PRICE)
        billItems.append(NEWITEM)
        return redirect(url_for('billing'))
    else:
        return render_template('AddMrpItem.html',MrpItems=MrpItems)



############### Give Discount #################################################
@app.route('/discount', methods=['GET','POST'])
def addDiscount():
    if request.method == 'POST':
        global Discount
        Discount = float(request.form['discount'])
        return redirect(url_for('getPDF'))

################## Finally Make Bill ####################################################
@app.route("/invoice")
def getPDF():
    global billItems , DiscountAdded , TYPE , billName , orderNumber
    if DiscountAdded == 0 and TYPE == 2 :
        DiscountAdded = 1
        return render_template('Discount.html',billItems=billItems)
    txtFile = open( "myfile.txt",'r')
    orderNumber = txtFile.read()
    billName = str("./Bills/" + orderNumber + ".pdf")
    makeBill(billItems,Discount,TYPE)
    billItems = []
    DiscountAdded = 0
    with open( billName, 'rb') as fp:
        pdf = fp.read()
    response = Response(
        pdf,
        mimetype="application/pdf",
        headers={"Content-disposition":
                 "inline; filename=" + billName })
    return response

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    Session = sessionmaker(bind=engine)
    s = Session()
    MrpItems = s.query(MrpFoodItem).order_by(MrpFoodItem.name).all()
    items = s.query(FoodItem).order_by(FoodItem.name).all()
    billItems=[]
    TYPE = 1
    DiscountAdded = 0
    Discount = 0
    txtFile = open( "myfile.txt",'r')
    orderNumber = txtFile.read()
    billName = str("./Bills/" + orderNumber + ".pdf")
    app.run(debug=True)
