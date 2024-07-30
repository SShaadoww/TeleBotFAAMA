from mysql.connector import connect, Error



def CheckCustomer(userId):
    try:
        with connect(
                host="localhost",
                user="Shadow",
                password="Evropa18",
                database="faama"
        ) as connection:
            check = "select TelegramID from сustomerсard where TelegramID = '" + userId + "'"
            with connection.cursor(buffered = True) as cursor:
                cursor.execute(check)
                if cursor.rowcount <1:
                    insert = """
                                        INSERT INTO сustomerсard
                                        (TelegramID)
                                        VALUES ( %s )
                                        """
                    
                    with connection.cursor() as cursor:
                        cursor.execute(insert, [userId])
                        connection.commit()
                        return False
                else:
                    return True
    except Error as e:
        print(e)
        return(e)

def OrderCreator(userId, ProductName):
    try:
        with connect(
                host="localhost",
                user="Shadow",
                password="Evropa18",
                database="faama"
        ) as connection:

            getClientId = "select ID from сustomerсard where TelegramID = '" + userId + "'"
            with connection.cursor(buffered = True) as cursor:
                cursor.execute(getClientId)
                ClientId = cursor.fetchone()[0]
                check = "select IDCustomer from orders where IDCustomer = %s"
                cursor.execute(check, [ClientId])
                if cursor.rowcount<1:
                        insert = """
                                        insert into orders
                                        (IDCustomer)
                                        Values ( %s )
                                        """

                        cursor.execute(insert,[ClientId])
                        connection.commit()
                        OrderId = cursor.lastrowid
                else:
                    getOrderId = "select ID from orders where IDCustomer = %s"
                    cursor.execute(getOrderId, [ClientId])
                    OrderId = cursor.fetchone()[0]
                    getCost = "select cost from products where product = %s"
                    cursor.execute(getCost,[ProductName])
                    Cost = cursor.fetchone()[0]

                    getProductId = "select ID from products where product = %s"
                    cursor.execute(getProductId, [ProductName])
                    ProductId = cursor.fetchone()[0]
                    check2 = "select IDProduct from compositionorders where IDProduct = %s and IDOrder = %s"
                    cursor.execute(check2, [ProductId, OrderId])
                    if cursor.rowcount > 0:
                        check3 = "select Quantity from compositionorders where IDProduct = %s and IDOrder = %s"
                        cursor.execute(check3,[ProductId, OrderId])
                        quantity = cursor.fetchone()[0]
                        result = quantity+1
                        update = """
                                    update compositionorders
                                    set 
                                        Quantity = "%s",
                                        Cost = %s
                                    where IDProduct = "%s" and IDOrder = "%s"
                                    """
                        cursor.execute(update,[result, Cost*result, ProductId, OrderId])
                        connection.commit()
                    else:


                        insert = """
                                        insert into compositionorders
                                        (IDOrder, IDProduct, Quantity, Cost)
                                        values ( %s, %s, 1, %s )
                                        """
                        with connection.cursor() as cursor:
                            cursor.execute(insert,[OrderId, ProductId, Cost])
                        connection.commit()
                        return True
    except Error as e:
        print(e)
        return(e)
                            
def GetCart(userId):
    try:
        with connect(
                host="localhost",
                user="Shadow",
                password="Evropa18",
                database="faama"
        ) as connection:
            with connection.cursor(buffered=True) as cursor:

                getClietnId = "select ID from сustomerсard where TelegramID = %s"
                cursor.execute(getClietnId,[userId])
                ClientId = cursor.fetchone()[0]

                getOrderId = "select ID from orders where IDCustomer = %s"
                cursor.execute(getOrderId,[ClientId])
                OrderId = cursor.fetchone()[0]

                getProductsId = "select IDProduct from compositionorders where IDOrder = %s"
                cursor.execute(getProductsId,[OrderId])
                ProductsId = cursor.fetchall()
                ProductsId = [i[0] for i in ProductsId]


                for i in ProductsId:
                    getDataCart = "select IDProduct, Quantity, Cost from compositionorders where IDOrder = %s"
                    cursor.execute(getDataCart,[OrderId])
                    Cart = cursor.fetchall()

                FnlCart = [list(t) for t in Cart]



                for i in range(len(ProductsId)):
                    getProducts = "select product from products where ID = %s"
                    cursor.execute(getProducts,[ProductsId[i]])
                    FnlCart[i][0] = cursor.fetchone()[0]
                return FnlCart
    except Error as e:
        print(e)
        return e


def Plus(userId, ProductData):
    ProductName = ProductData.replace("plus","")
    try:
        with connect(
                host="localhost",
                user="Shadow",
                password="Evropa18",
                database="faama"
        ) as connection:
            with connection.cursor(buffered=True) as cursor:

                getClietnId = "select ID from сustomerсard where TelegramID = %s"
                cursor.execute(getClietnId,[userId])
                ClientId = cursor.fetchone()[0]

                getOrderId = "select ID from orders where IDCustomer = %s"
                cursor.execute(getOrderId,[ClientId])
                OrderId = cursor.fetchone()[0]

                getProductId = "select ID from products where product = %s"
                cursor.execute(getProductId,[ProductName])
                ProductId = cursor.fetchone()[0]

                return True
    except Error as e:
        print(e)
        return e

Plus("Artemk4_Z","plusDot Aio mini")

def FirstLastName(name):
    try:
        with connect(
                host="localhost",
                user="Shadow",
                password="Evropa18",
                database="faama"
        ) as connection:
            insert = """
            insert into сustomerсard
            (LastNameFirstName)
            values (%s)
            """
            with connection.cursor() as cursor:
                cursor.executemany(insert,name)
                connection.commit()
                
    except Error as e:
        return print(e)


def TelephonNum(telephone):
    try:
        with connect(
                host="localhost",
                user="Shadow",
                password="Evropa18",
                database="faama"
        ) as connection:
            insert = """
            insert into сustomerсard
            (Telefone)
            values (%s)
            """
            with connection.cursor() as cursor:
                cursor.executemany(insert,telephone)
                connection.commit()

    except Error as e:
        return print(e)
