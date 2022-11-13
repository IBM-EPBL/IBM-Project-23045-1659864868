from flask import *
from datetime import date
import ibm_db
app=Flask(__name__)
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=3883e7e4-18f5-4afe-be8c-fa31c41761d2.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;SECURITY=SSL;PORT=31498;PROTOCOL=TCPIP;UID=nnm68033;PWD=DUTMGiDWgJy5zlS8",'','')
# conn=None
retailer_id=0


@app.route("/", methods=['GET','POST'])
def login():
    if request.method=='GET':
        return render_template("Login/index.html",status="",colour="red")
    elif request.method=='POST':
        global retailer_id
        email=request.form["email"]
        password=request.form["password"]
        query = '''select * from retailers where email = \'{}\''''.format(email)
        exec_query = ibm_db.exec_immediate(conn, query)
        row = ibm_db.fetch_both(exec_query)
        if(row is not False):
            if(row['PASSWORD'] != password):
                return render_template("Login/index.html",status="Invalid Password",colour="red")
            else:
                temp='''select RETAILER_ID from retailers where email = \'{}\''''.format(email)
                exec_query = ibm_db.exec_immediate(conn, temp)
                dict= ibm_db.fetch_both(exec_query)
                retailer_id=dict["RETAILER_ID"]
                return render_template("Dashboard/index.html")

        return render_template("Login/index.html",status="Invalid Email",colour="red")

@app.route("/signup", methods=['GET','POST'])
def signup():
    
    if request.method=='GET':
        return render_template("Login/signup.html",status="",colour="red")
    elif request.method=='POST':
        email=request.form["email"]
        password=request.form["password"]
        first_name=request.form["first_name"]
        last_name=request.form["last_name"]
        store_name=request.form["store_name"]
        address=request.form["address"]
        phone_number=request.form["phone_number"]
        query = '''select * from retailers where email = \'{}\''''.format(email)
        exec_query = ibm_db.exec_immediate(conn, query)
        row = ibm_db.fetch_both(exec_query)
        if(row is False):
            query = '''insert into retailers(email, password, first_name, last_name, store_name, address, phone_number) values('{}', '{}', '{}', '{}', '{}', '{}', '{}')'''.format(email, password, first_name, last_name, store_name, address, phone_number)
            exec_query = ibm_db.exec_immediate(conn, query)
            return render_template("Login/signup.html",status="Signup Success",colour="green")
        else:
            return render_template("Login/signup.html",status="User Already Exists",colour="red")

@app.route("/dashboard", methods=['GET','POST'])
def dashboard():
    if request.method=="GET":
        return render_template("Dashboard/index.html")


@app.route("/add_customer", methods=['GET','POST'])
def add_customer():
    if request.method=="GET":
        return render_template("Dashboard/add_customer.html")
    elif request.method=="POST":
        name=request.form["name"]
        id=int(request.form["id"])
        query = '''select * from customer where customer_id = \'{}\''''.format(id)
        exec_query = ibm_db.exec_immediate(conn, query)
        row = ibm_db.fetch_both(exec_query)
        if(row is False):
            query = '''insert into customer(customer_id,retailer_id,customer_name) values('{}', '{}', '{}')'''.format(id,retailer_id,name)
            exec_query = ibm_db.exec_immediate(conn, query)
            return render_template("Dashboard/add_customer.html",status="Customer Added",colour="green")
        else:
            return render_template("Dashboard/add_customer.html",status="Customer Already Exists",colour="red")

@app.route("/view_customer", methods=['GET','POST'])
def view_customer():
    if request.method=="GET":
        query = '''select * from customer'''
        exec_query = ibm_db.exec_immediate(conn, query)
        row = ibm_db.fetch_both(exec_query)
        name=[]
        id=[]
        while(row):
            name.append(row["CUSTOMER_NAME"])
            id.append(row["CUSTOMER_ID"])
            row = ibm_db.fetch_both(exec_query)
        return render_template("Dashboard/view_customer.html",name=name,id=id,len=len(name))
        
@app.route("/add_item", methods=['GET','POST'])
def add_item():
    if request.method=="GET":
        return render_template("Dashboard/add_item.html")
    elif request.method=="POST":
        name=request.form["name"]
        price=float(request.form["price"])
        query = '''select * from items where item_name = \'{}\''''.format(name)
        exec_query = ibm_db.exec_immediate(conn, query)
        row = ibm_db.fetch_both(exec_query)
        if(row is False):
            query = '''insert into items(retailer_id,item_name,price,left_out) values('{}', '{}', '{}', '{}')'''.format(retailer_id,name,price,0)
            exec_query = ibm_db.exec_immediate(conn, query)
            return render_template("Dashboard/add_item.html",status="Item Added",colour="green")
        else:
            return render_template("Dashboard/add_item.html",status="Item Already Exists",colour="red")

@app.route("/view_item", methods=['GET','POST'])
def view_item():
    if request.method=="GET":
        query = '''select * from items'''
        exec_query = ibm_db.exec_immediate(conn, query)
        row = ibm_db.fetch_both(exec_query)
        name=[]
        id=[]
        price=[]
        left_out=[]
        while(row):
            name.append(row["ITEM_NAME"])
            id.append(row["ITEM_ID"])
            price.append(row["PRICE"])
            left_out.append(row["LEFT_OUT"])
            row = ibm_db.fetch_both(exec_query)
        return render_template("Dashboard/view_item.html",name=name,id=id,price=price,left_out=left_out,len=len(name))

@app.route("/add_inventory", methods=['GET','POST'])
def add_inventory():
    name=[]
    query = '''select * from items'''
    exec_query = ibm_db.exec_immediate(conn, query)
    row = ibm_db.fetch_both(exec_query)
    while(row):
        name.append(row["ITEM_NAME"])
        row = ibm_db.fetch_both(exec_query)
    if request.method=="GET":
        return render_template("Dashboard/add_inventory.html",name=name,len=len(name),status=" ")
    elif request.method=="POST":
        fname=request.form["name"]
        quantity=request.form["quantity"]
        date=request.form["date"]
        
        # Finding ITEM ID
        query = '''select item_id from items where item_name = \'{}\''''.format(fname)
        exec_query = ibm_db.exec_immediate(conn, query)
        row = ibm_db.fetch_both(exec_query)
        id=row["ITEM_ID"]
        # INSERTION
        query = '''insert into inventory(item_id,quantity,stock_date) values('{}', '{}', '{}')'''.format(id,quantity,date)
        exec_query = ibm_db.exec_immediate(conn, query)
        #UPDATION
        query = '''update items set left_out=left_out+\'{}\' where item_id=\'{}\''''.format(quantity,id)
        exec_query = ibm_db.exec_immediate(conn, query)
        return render_template("Dashboard/add_inventory.html",name=name,len=len(name),status="Inventory added")

@app.route("/view_inventory", methods=['GET','POST'])
def view_inventory():
    name=[]
    query = '''select * from items'''
    exec_query = ibm_db.exec_immediate(conn, query)
    row = ibm_db.fetch_both(exec_query)
    while(row):
        name.append(row["ITEM_NAME"])
        row = ibm_db.fetch_both(exec_query)
    items=list()
    if request.method=="GET":
        return render_template("Dashboard/view_inventory.html",name=name,items=items)
    elif request.method=="POST":
        item_name=request.form["name"]
        start=request.form["start_date"]
        end=request.form["end_date"]
        query = '''select item_id from items where item_name = \'{}\''''.format(item_name)
        exec_query = ibm_db.exec_immediate(conn, query)
        row = ibm_db.fetch_both(exec_query)
        id=row["ITEM_ID"]
        query = '''select stock_date,quantity from inventory where item_id=\'{}\' and stock_date<=\'{}\' and stock_date>=\'{}\''''.format(id,end,start)
        exec_query = ibm_db.exec_immediate(conn, query)
        row = ibm_db.fetch_both(exec_query)
        while(row):
            items.append({"item_name":item_name,"quantity":row[1],"stock_date":row[0]})
            row = ibm_db.fetch_both(exec_query)
        return render_template("Dashboard/view_inventory.html",name=name,items=items)

@app.route("/add_sale", methods=['GET','POST'])
def add_sale():
    # ITEMS
    items=list()
    query = '''select * from items'''
    exec_query = ibm_db.exec_immediate(conn, query)
    row = ibm_db.fetch_both(exec_query)
    while(row):
        items.append({"name": row["ITEM_NAME"], "quantity": row["LEFT_OUT"], "price": row["PRICE"]})
        row = ibm_db.fetch_both(exec_query)
    # CUSTOMERS
    custname=[]
    query = '''select * from customer'''
    exec_query = ibm_db.exec_immediate(conn, query)
    row = ibm_db.fetch_both(exec_query)
    while(row):
        custname.append(row["CUSTOMER_NAME"])
        row = ibm_db.fetch_both(exec_query)
    if request.method=="GET":
        return render_template("Dashboard/add_sale.html",items=items,cname=custname,clen=len(custname),status="")
    elif request.method=="POST":
        i_array=request.form["item_array"]
        q_array=request.form["quantity_array"]
        item_list=i_array.split(",")
        quantity_list=q_array.split(",")
        cname=request.form["cname"]
        today = date.today()
        # FINDING CUSTOMER ID
        query = '''select customer_id from customer where customer_name = \'{}\''''.format(cname)
        exec_query = ibm_db.exec_immediate(conn, query)
        row = ibm_db.fetch_both(exec_query)
        id=row["CUSTOMER_ID"]
        #SALE TABLE
        query = '''insert into sale(sale_date,customer_id) values('{}', '{}')'''.format(today,id)
        exec_query = ibm_db.exec_immediate(conn, query)
        #GET SALE ID
        query = '''select sale_id from sale where sale_date = \'{}\' and customer_id=\'{}\''''.format(today,id)
        exec_query = ibm_db.exec_immediate(conn, query)
        row = ibm_db.fetch_both(exec_query)
        sale_id=row["SALE_ID"]
        #SALE ITEM TABLE
        n=len(item_list)
        for i in range(n):
            query = '''select item_id from items where item_name = \'{}\''''.format(item_list[i])
            exec_query = ibm_db.exec_immediate(conn, query)
            row = ibm_db.fetch_both(exec_query)
            item_id=row["ITEM_ID"]
            #UPDATION
            query = '''update items set left_out=left_out-\'{}\' where item_id=\'{}\''''.format(quantity_list[i],item_id)
            exec_query = ibm_db.exec_immediate(conn, query)
            # INSERTION
            query = '''insert into sale_items(sale_id,quantity,item_id) values('{}', '{}', '{}')'''.format(sale_id,quantity_list[i],item_id)
            exec_query = ibm_db.exec_immediate(conn, query)
        return render_template("Dashboard/add_sale.html",items=items,cname=custname,clen=len(custname),status="Sale Success")


@app.route("/view_sale", methods=['GET','POST'])
def view_sale():
    items=list()
    if request.method=="GET":
        return render_template("Dashboard/view_sale.html",items=items)
    elif request.method=="POST":
        start=request.form["start_date"]
        end=request.form["end_date"]
        query = '''select item_id,count(quantity) from sale_items where sale_id in (select sale_id from sale where sale_date<= \'{}\' and sale_date>=\'{}\') group by(item_id)'''.format(end,start)
        exec_query = ibm_db.exec_immediate(conn, query)
        row = ibm_db.fetch_both(exec_query)
        while(row):
            query = '''select item_name,price from items where item_id=\'{}\''''.format(row[0])
            exec_query1 = ibm_db.exec_immediate(conn, query)
            row1 = ibm_db.fetch_both(exec_query1)
            items.append({"item_id":row[0],"item_name":row1[0],"quantity":row[1],"amount":(row1[1]*row[1])})
            row = ibm_db.fetch_both(exec_query)
        # Item Name and Price
        return render_template("Dashboard/view_sale.html",items=items)
if __name__=="__main__":
    app.run(debug=True)
