import mysql.connector

def login():

    print("""MENU
    1)Login as Warehouse manager
    2)Miscellaneous queries
    3)Login as Store manager
    4)Exit""")


def warehouse_menu():
    print("""MENU
    1)Display Warehouse details
    2)Display list of suppliers to warehouse
    3)Display products availabe at warehouse
    4)Add product to warehouse
    5)Restock product
    6)Exit""")


def store_menu():
    print("""MENU
    1)Display store details
    2)Display list of warehouse delivering store
    3)Display products availabe at store
    4)Add product to store
    5)Restock product
    6)Exit""")


def menu2():

    print("""MENU
    1)Print total stock of product availabe in warehouse and stores
    2)Print the total cost by product and by store in all deliveries
    3)Number of minimum products in all store
    4)Number of maximum products in all stores
    5)Exit""")



#checks if wid is valid
def valid_wid(wid):
    mycursor.execute("select WID from warehouse")
    result = mycursor.fetchall()
    for x in result:
        if(int(x[0]) == wid):
            return True
    return False


#checks if store id is valid
def valid_sid(sid):
    mycursor.execute("select ST_ID from store")
    result = mycursor.fetchall()
    for x in result:
        if(int(x[0]) == sid):
            return True
    return False


def avail_w(wid , stock , pid):
    mycursor.execute("select Stock from stores1 where Prd_ID=%s and Wh_ID=%s" , (wid , pid))
    result = mycursor.fetchall()
    if(result.__len__() > 0):
        if(stock - result[0] < 0) :
            return False
        else :
            return True
    else : 
        return False

#connecting to database
mydb = mysql.connector.connect(
    host="siddhant-Inspiron-15-5518",
    user="root",
    password="@Karnal122112",
    database="MoMilk"
)


#The cursor object acts as a handle or pointer to the result set of a query, 
# allowing to perform operations on the database
mycursor = mydb.cursor()
choice_main=1
choice_warehouse=1


while(1):
    login()
    choice_main=int(input("Enter choice:"))
    if(choice_main==1):
        wid=int(input("Enter Warehouse ID:"))
        if(valid_wid(wid)):
            while(1):
                warehouse_menu()
                choice_warehouse=int(input("Enter warehouse menu choice:"))
                if(choice_warehouse==1):
                    #print warehouse details 
                    mycursor.execute("select* from warehouse where WID=%s",(wid,))
                    result = mycursor.fetchall()
                    print("Warehouse ID:%s \nWarehouse Name:%s \nWarehouse Address:%s " %(result[0][0],result[0][1],result[0][2]))
                    #getting warehouse phone number form w_phone table which contains all warehouse phone number
                    mycursor.execute("select WPh from w_phone where Whr_ID=%s",(wid,))
                    result = mycursor.fetchall()
                    print("Phone Number:",end="")
                    for x in result:
                        print(int(x[0]))
                        print(" ")
                    
                if(choice_warehouse==2):

                    #getting list of all the suppliers
                    mycursor.execute("select supplierID from supplies where warehouseID=%s", (wid,))
                    result = mycursor.fetchall()
                    for x in result: #iterating over the list of supplierIds
                        mycursor.execute("select * from supplier where sid=%s",(x[0],))
                        result2=mycursor.fetchall()
                        for y in result2: # printing all details for each supplier
                            print("Supplier ID:%s \nSupplier Name:%s \nSupplier Address:%s \n "%(y[0],y[1],y[2]))

                elif(choice_warehouse==3):
                    
                    mycursor.execute("select * from stores1 where Wh_ID=%s",(wid,))
                    result=mycursor.fetchall() #list of all products
                    for x in result:
                        mycursor.execute("select * from product where pid=%s",(x[1],)) #searching for the particular pid 
                        result2=mycursor.fetchall()
                        for y in result2: 
                            print("PID:%s \nProduct Name:%s \nPrice:%s \nCategory ID:%s \nStock:%s "%(y[0],y[1],y[2],y[3],x[0]))

                elif(choice_warehouse==4):
                    pid=input("Enter pid:")
                    stock=input("Enter stock:")
                    mycursor.execute("Select pid from product")
                    result=mycursor.fetchall()
                    for x in result:
                        if(x[0]==int(pid)):
                            mycursor.execute("select * from stores1 where prd_id=%s and wh_id=%s",(pid,wid))
                            result2=mycursor.fetchall()
                            if(result2.__len__()>0):
                                print("Product already exists in wharehouse.")
                                break
                            else:
                                mycursor.execute("insert into stores1 values(%s,%s,%s)",(stock,pid,wid))
                                mydb.commit()
                                print("Product added to warehouse!")
                        
                    
                elif(choice_warehouse==5):
                    pid = int(input("Enter pid:"))
                    stock = int(input("Enter updated stock:"))
                    mycursor.execute("Select pid from product")
                    result = mycursor.fetchall()
                    for x in result:
                        if(x[0] == int(pid)):
                            mycursor.execute("select * from stores1 where Prd_id=%s and Wh_id=%s", (pid, wid))
                            result2 = mycursor.fetchall()
                            if(result2.__len__() > 0):
                                mycursor.execute("update stores1 set Stock=%s where Prd_id=%s and Wh_id=%s",(stock,pid,wid))
                                mydb.commit()
                                break
                    
                elif(choice_warehouse==6):
                    break
                else:
                    print("Enter a valid choice")
        else:
            print("Invalid Warehouse ID")
    elif(choice_main==2):
        while(1):
            menu2()
            choice_m = int(input("Enter choice:"))
            if(choice_m==1):
                mycursor.execute("select PID,count(Pname) as total  from product join stores1 on product.pid=stores1.Prd_ID join stores2 on product.pid=stores2.Prd_ID group by PID with rollup")
                result=mycursor.fetchall()
                for x in result:
                    print(x[0],x[1])          
            elif(choice_m==2):
                mycursor.execute("SELECT prodID, storeID, SUM(Price) FROM delivers_to GROUP BY prodID, storeID WITH ROLLUP order by prodID")
                result = mycursor.fetchall()
                for x in result:
                    print(x[0], x[1],x[2])
            elif(choice_m==3):
                mycursor.execute("SELECT storeID, COUNT(prodID) FROM delivers_to GROUP BY storeID WITH ROLLUP ORDER BY COUNT(prodID) ")
                result = mycursor.fetchall()
                m=result[0][1]
                for x in result:
                    if(x[1]==m):
                        print(x[0], x[1])
            elif(choice_m==4):
                mycursor.execute("SELECT storeID, COUNT(prodID) FROM delivers_to GROUP BY storeID WITH ROLLUP ORDER BY COUNT(prodID) desc ")
                result = mycursor.fetchall()
                m = result[1][1]
                for x in result:
                    if(x[1] == m):
                        print(x[0], x[1])
            elif(choice_m==5):
                break
            else:
                print("Enter a valid choice")
    elif(choice_main==3):
        sid = int(input("Enter store id : "))
        if(valid_sid(sid)): 
            while(1) : 
                store_menu()
                choice_store = int(input("Enter store menu choice : "))
                if(choice_store == 1):
                    mycursor.execute("select * from store where ST_ID=%s",(sid,))
                    result = mycursor.fetchall()
                    print("Store ID:%s \nStore Name:%s \nStore Address:%s " %(result[0][0],result[0][1],result[0][2]))

                elif(choice_store == 2):
                    mycursor.execute("select wareID from delivers_to where storeID=%s" , (sid,))
                    result = mycursor.fetchall()
                    for x in result : 
                        mycursor.execute("select * from warehouse where WID=%s" , (x[0],))
                        result2 = mycursor.fetchall()
                        print("yo")
                        for y in result2:
                            print("Warehouse ID:%s \nWarehouse Name:%s \nWarehouse Address:%s "%(y[0],y[1],y[2]))

                elif(choice_store == 3):
                    mycursor.execute("select * from stores2 where Store_ID=%s",(sid,))
                    result=mycursor.fetchall() #list of all products
                    for x in result:
                        mycursor.execute("select * from product where pid=%s",(x[1],)) #searching for the particular pid 
                        result2=mycursor.fetchall()
                        for y in result2: 
                            print("PID:%s \nProduct Name:%s \nPrice:%s \nCategory ID:%s \nStock:%s "%(y[0],y[1],y[2],y[3],x[0]))

                elif(choice_store == 4):

                    pid=int(input("Enter pid:"))
                    stock=int(input("Enter stock:"))
                    wh_id = int(input("Enter warehouse id"))
                    if(avail_w(wh_id , stock , pid)) :
                        mycursor.execute("Select pid from product")
                        result=mycursor.fetchall()
                        print(result)
                        for x in result:
                            if(x[0]==int(pid)):
                                mycursor.execute("select * from stores2 where Prd_ID=%s and Store_ID=%s",(pid,sid))
                                result2=mycursor.fetchall()
                                if(result2.__len__()>0):
                                    print("Product already exists in store.")
                                    break
                                else:
                                    mycursor.execute("insert into stores2 values(%s,%s,%s)",(stock,sid,pid))
                                    mydb.commit()
                                    print("Product added to store!")

                elif(choice_store == 5):

                    pid = int(input("Enter pid:"))
                    stock = int(input("Enter updated stock:"))
                    wh_id = int(input("Enter warehouse id"))
                    if(avail_w(wh_id , stock , pid)) :
                        mycursor.execute("Select pid from product")
                        result = mycursor.fetchall()
                        for x in result:
                            if(x[0] == int(pid)):
                                mycursor.execute("select * from stores2 where Prd_ID=%s and Store_ID=%s", (pid, sid))
                                result2 = mycursor.fetchall()
                                if(result2.__len__() > 0):
                                    mycursor.execute("update stores2 set Stock=%s where Prd_ID=%s and Store_ID=%s",(stock,pid,sid))
                                    mydb.commit()
                                    break
                elif(choice_store == 6):
                    break
                
        else: 
            print("Invalid store Id ")
        
    else:
        print("Enter a valid choice")        
