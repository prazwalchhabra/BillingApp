# -*- coding: utf-8 -*-
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import datetime

def makeBill(items,discount,type):

    if type != 2:
        discount = 0
    
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    import datetime
    
    ##################### Date And Time For Bill #########################
    now = datetime.datetime.today()
    CurrentDate = str(now.strftime('%Y-%m-%d'))
    CurrentTime = str(now.strftime("%I:%M:%S %p"))
    ##### Read from text file the order number and the bill name #########
    txtFile = open("myfile.txt",'r')
    orderNumber = txtFile.read()
    billName = str("./Bills/"+orderNumber+".pdf")
    # orderNumber = int(orderNumber)
    ######################################################################
    canvas = canvas.Canvas(billName, pagesize=letter)
    canvas.setPageSize((58,270))
    canvas.setLineWidth(.3)
    canvas.setFont('Helvetica', 6)
    # canvas.drawString(1.9,107,'卐')
    canvas.line(0,262,58,262) 
    canvas.line(0,263,58,263) 
    canvas.line(0,264,58,264) 
    canvas.line(0,265,58,265) 
    ########################## Address And Details ##############################
    canvas.drawString(1.9,254,'Chhabra Restaurant')
    canvas.setFont('Helvetica', 2.5)
    canvas.drawString(9.5,250,' Adjoining S.B.I. Grain Market Branch ')
    canvas.setFont('Helvetica', 2)
    canvas.drawString(11.9,247.7,'Near Durga Mandir Gate , Rajpura Town')
    canvas.setFont('Helvetica', 2.5)
    canvas.drawString(12.4,245.3,'Phone Number : 01762-225854')
    canvas.drawString(5,240,'Date : '+ CurrentDate)
    canvas.drawString(33,240,'Time : '+ CurrentTime)
    canvas.setFont('Helvetica', 3)
    canvas.drawString(20,235,'ORDER NO.: '+ orderNumber)
    canvas.line(0,233,58,232) # 3 ka difference

    ##### Write to text file next order number #########
    a = int(orderNumber) + 1
    a = str(a)
    txtFile = open("myfile.txt",'w')
    orderNumber = txtFile.write(a)
    
    ################################################################################
    canvas.setFont('Helvetica', 3.5) # 4 ka difference
    canvas.drawString(4,228,'Item')
    canvas.drawString(17,228,'Units')
    canvas.drawString(30,228,'Price')
    canvas.drawString(42,228,'Subtotal')
    canvas.line(0,226,58,226)
    ######################## Now Dynamic Billing Starts ##############################

    y_cord=221

    canvas.setFont('Helvetica', 3)

    subtotal=0

    for item in items:
        canvas.drawString(4,y_cord,item.name[0:8])
        canvas.drawString(20, y_cord,item.units)
        canvas.drawString(30,y_cord,str(item.price))
        canvas.drawString(42,y_cord,str(item.total))
        subtotal = subtotal + float(item.total)
        y_cord=y_cord-4

    ###################################################################################

    canvas.line(24,y_cord-5,55,y_cord-5)
    y_cord=y_cord-10
    canvas.drawString(26,y_cord,'Sub Total :')
    canvas.drawString(43,y_cord,str(subtotal))
    
    if type == 2:        
        canvas.drawString(23,y_cord-4,'-   Discount  :')
        canvas.drawString(43,y_cord-4,str(discount))
        y_cord=y_cord-4
        subtotal = float(subtotal) - float(discount)        
    
    if subtotal%1 >= 0.5:
        subtotal=subtotal-(subtotal%1)+1
    else:
        subtotal = subtotal-(subtotal%1)
    canvas.drawString(23,y_cord-4,'Round OFF :')
    canvas.drawString(43,y_cord-4,str(subtotal))
    
    y_cord=y_cord-8
    canvas.line(0,y_cord,58,y_cord) 
    canvas.setFont('Helvetica', 1.5)
    y_cord=y_cord-5
    canvas.drawString(5,y_cord,'E. & O.E.')
    canvas.setFont('Helvetica', 5)
    canvas.drawString(26,y_cord-1,'Total')
    canvas.drawString(40,y_cord-1,str(subtotal))
    y_cord=y_cord-4
    canvas.line(0,y_cord,58,y_cord) 
    canvas.setFont('Helvetica', 2)
    y_cord=y_cord-5
    canvas.drawString(20,y_cord,'Thanks Visit Again!')
    y_cord=y_cord-4
    canvas.drawString(21,y_cord,'Have A Nice Day!')
    y_cord=y_cord-4
    canvas.line(0,y_cord,58,y_cord) 
    canvas.line(0,y_cord-1,58,y_cord-1) 
    canvas.line(0,y_cord-1,58,y_cord-1) 
    canvas.line(0,y_cord-1,58,y_cord-1) 
    canvas.save()
