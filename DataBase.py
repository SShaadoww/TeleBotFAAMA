from mysql.connector import connect, Error
import aiomysql
from requests import delete

from Config import DataSql



async def CheckCustomer(userId):
    try:
        connection = await aiomysql.connect(
                host=DataSql["Host"],
                user=DataSql["User"],
                password=DataSql["Password"],
                db=DataSql["DataBase"]
        )
        async with connection.cursor() as cursor:
            check = "select TelegramID from сustomerсard where TelegramID = %s"
            await cursor.execute(check, [userId])

            if cursor.rowcount <1:
                insert = """
                                    INSERT INTO сustomerсard
                                    (TelegramID)
                                    VALUES ( %s )
                                    """

                async with connection.cursor() as cursor:
                    await cursor.execute(insert, [userId])
                    await connection.commit()
                    await cursor.close()
                    connection.close()
                    return False
            else:
                await cursor.close()
                connection.close()
                return True
    except Error as e:
        print(e)
        return(e)

async def OrderCreator(userId, ProductName):
    try:
        connection = await aiomysql.connect(
                host=DataSql["Host"],
                user=DataSql["User"],
                password=DataSql["Password"],
                db=DataSql["DataBase"]
        )

        async with connection.cursor() as cursor:

            getClientId = "select ID from сustomerсard where TelegramID = %s"

            await cursor.execute(getClientId, [userId])
            # ClientId = await cursor.fetchone()[0]

            result = await cursor.fetchone()
            ClientId = result[0] if result else None

            check = "select IDCustomer from orders where IDCustomer = %s"
            await cursor.execute(check, [ClientId])
            if cursor.rowcount<1:
                    insert = """
                                    insert into orders
                                    (IDCustomer)
                                    Values ( %s )
                                    """

                    await cursor.execute(insert,[ClientId])
                    await connection.commit()
                    OrderId = cursor.lastrowid

            else:
                getOrderId = "select ID from orders where IDCustomer = %s"
                await cursor.execute(getOrderId, [ClientId])
                # OrderId = await cursor.fetchone()[0]

                result = await cursor.fetchone()
                OrderId = result[0] if result else None

            getCost = "select cost from products where product = %s"
            await cursor.execute(getCost,[ProductName])
            # Cost = await cursor.fetchone()[0]

            result = await cursor.fetchone()
            Cost = result[0] if result else None


            getProductId = "select ID from products where product = %s"
            await cursor.execute(getProductId, [ProductName])
            # ProductId = await cursor.fetchone()[0]

            result = await cursor.fetchone()
            ProductId = result[0] if result else None

            check2 = "select IDProduct from compositionorders where IDProduct = %s and IDOrder = %s"
            await cursor.execute(check2, [ProductId, OrderId])
            if cursor.rowcount > 0:
                check3 = "select Quantity from compositionorders where IDProduct = %s and IDOrder = %s"
                await cursor.execute(check3,[ProductId, OrderId])
                # quantity = await cursor.fetchone()[0]

                result = await cursor.fetchone()
                quantity = result[0] if result else None

                result = quantity+1
                update = """
                            update compositionorders
                            set 
                                Quantity = "%s",
                                Cost = %s
                            where IDProduct = "%s" and IDOrder = "%s"
                            """
                await cursor.execute(update,[result, Cost*result, ProductId, OrderId])
            else:


                insert = """
                            insert into compositionorders
                            (IDOrder, IDProduct, Quantity, Cost)
                            values ( %s, %s, 1, %s )
                            """
                async with connection.cursor() as cursor:

                    await cursor.execute(insert,[OrderId, ProductId, Cost])

            await connection.commit()


    except Error as e:
        print(e)
        return(e)
    finally:
        connection.close()
                            
async def GetCart(userId):
    try:
        connection = await aiomysql.connect(
            host=DataSql["Host"],
            user=DataSql["User"],
            password=DataSql["Password"],
            db=DataSql["DataBase"]
        )

        async with connection.cursor() as cursor:

            getClietnId = "select ID from сustomerсard where TelegramID = %s"
            await cursor.execute(getClietnId,[userId])
            # ClientId = await cursor.fetchone()[0]
            result = await cursor.fetchone()
            ClientId = result[0] if result else None

            getOrderId = "select ID from orders where IDCustomer = %s"
            await cursor.execute(getOrderId,[ClientId])
            # OrderId = await cursor.fetchone()[0]
            result = await cursor.fetchone()
            OrderId = result[0] if result else None

            getProductsId = "select IDProduct from compositionorders where IDOrder = %s"
            await cursor.execute(getProductsId,[OrderId])
            ProductsId = await cursor.fetchall()
            ProductsId = [i[0] for i in ProductsId]

            if len(ProductsId) == 0 :
                return False
            else:

                for i in ProductsId:
                    getDataCart = "select IDProduct, Quantity, Cost from compositionorders where IDOrder = %s"
                    await cursor.execute(getDataCart,[OrderId])
                    Cart = await cursor.fetchall()

                FnlCart = [list(t) for t in Cart]



                for i in range(len(ProductsId)):
                    getProducts = "select product from products where ID = %s"
                    await cursor.execute(getProducts,[ProductsId[i]])
                    # FnlCart[i][0] = await cursor.fetchone()[0]
                    row = await cursor.fetchone()
                    if row:
                        FnlCart[i][0] = row[0]


                return FnlCart

            await connection.commit()
            await cursor.close()
            connection.close()
    except Error as e:
        print(e)
        return e

async def DeleteCart(userId):
    try:
        connection = await aiomysql.connect(
            host=DataSql["Host"],
            user=DataSql["User"],
            password=DataSql["Password"],
            db=DataSql["DataBase"]
        )

        async with connection.cursor() as cursor:
            getClietnId = "select ID from сustomerсard where TelegramID = %s"
            await cursor.execute(getClietnId, [userId])
            result = await cursor.fetchone()
            ClientId = result[0] if result else None

            getOrderId = "select ID from orders where IDCustomer = %s"
            await cursor.execute(getOrderId, [ClientId])
            result = await cursor.fetchone()
            OrderId = result[0] if result else None

            deleteCart = "delete from compositionorders where IDOrder = %s"
            await cursor.execute(deleteCart, [OrderId])
        await connection.commit()
        connection.close()

    except Error as e:
        print(e)
        return e


async def Plus(userId, ProductData):
    ProductName = ProductData.replace("plus","")
    try:
        connection = await aiomysql.connect(
            host=DataSql["Host"],
            user=DataSql["User"],
            password=DataSql["Password"],
            db=DataSql["DataBase"]
        )

        async with connection.cursor() as cursor:

            getClietnId = "select ID from сustomerсard where TelegramID = %s"
            await cursor.execute(getClietnId,[userId])
            # ClientId = await cursor.fetchone()[0]
            result = await cursor.fetchone()
            ClientId = result[0] if result else None

            getOrderId = "select ID from orders where IDCustomer = %s"
            await cursor.execute(getOrderId,[ClientId])
            # OrderId = await cursor.fetchone()[0]
            result = await cursor.fetchone()
            OrderId = result[0] if result else None

            getProductId = "select ID from products where product = %s"
            await cursor.execute(getProductId,[ProductName])
            # ProductId = await cursor.fetchone()[0]
            result = await cursor.fetchone()
            ProductId = result[0] if result else None

            getQuantityId = "select Quantity from compositionorders where IDOrder = %s and IDProduct = %s"
            await cursor.execute(getQuantityId, [OrderId, ProductId])
            # QuantityId = await cursor.fetchone()[0]
            result = await cursor.fetchone()
            QuantityId = result[0] if result else None

            getCost = "select cost from products where product = %s"
            await cursor.execute(getCost, [ProductName])
            # Cost = await cursor.fetchone()[0]
            result = await cursor.fetchone()
            Cost = result[0] if result else None

            fnlQuantityId = QuantityId+1
            fnlCost = Cost * fnlQuantityId

            update = """
                        update compositionorders
                                set 
                                    Quantity = "%s",
                                    Cost = %s
                                where IDOrder = "%s" and IDProduct = "%s"
                        """
            await cursor.execute(update, [fnlQuantityId, fnlCost, OrderId, ProductId])
            await connection.commit()
            await cursor.close()
            connection.close()

            return True
    except Error as e:
        print(e)
        return e

async def Minus(userId, ProductData):
    ProductName = ProductData.replace("minus", "")
    try:
        connection = await aiomysql.connect(
            host=DataSql["Host"],
            user=DataSql["User"],
            password=DataSql["Password"],
            db=DataSql["DataBase"]
        )

        async with connection.cursor() as cursor:

            getClietnId = "select ID from сustomerсard where TelegramID = %s"
            await cursor.execute(getClietnId, [userId])
            # ClientId = await cursor.fetchone()[0]
            result = await cursor.fetchone()
            ClientId = result[0] if result else None

            getOrderId = "select ID from orders where IDCustomer = %s"
            await cursor.execute(getOrderId, [ClientId])
            # OrderId = await cursor.fetchone()[0]
            result = await cursor.fetchone()
            OrderId = result[0] if result else None

            getProductId = "select ID from products where product = %s"
            await cursor.execute(getProductId, [ProductName])
            # ProductId = await cursor.fetchone()[0]
            result = await cursor.fetchone()
            ProductId = result[0] if result else None

            getCompositionordersId = "select ID from compositionorders where IDOrder = %s and IDProduct = %s"
            await cursor.execute(getCompositionordersId, [OrderId, ProductId])
            # CompositionordersId = await cursor.fetchone()[0]
            result = await cursor.fetchone()
            CompositionordersId = result[0] if result else None

            getQuantityId = "select Quantity from compositionorders where IDOrder = %s and IDProduct = %s"
            await cursor.execute(getQuantityId, [OrderId, ProductId])
            # QuantityId = await cursor.fetchone()[0]
            result = await cursor.fetchone()
            QuantityId = result[0] if result else None

            getCost = "select cost from products where product = %s"
            await cursor.execute(getCost, [ProductName])
            # Cost = await cursor.fetchone()[0]
            result = await cursor.fetchone()
            Cost = result[0] if result else None

            fnlQuantityId = QuantityId - 1
            fnlCost = Cost * fnlQuantityId

            if fnlQuantityId == 0:
                delete = """
                            Delete from compositionorders 
                            where 
                                ID = %s
                            """
                await cursor.execute(delete,[CompositionordersId])
            else:

                update = """
                                update compositionorders
                                        set 
                                            Quantity = "%s",
                                            Cost = %s
                                        where ID = "%s"
                                """
                await cursor.execute(update, [fnlQuantityId, fnlCost, CompositionordersId])
            await connection.commit()
            await cursor.close()
            connection.close()

            return True
    except Error as e:
        print(e)
        return e



def FirstLastName(name):
    try:
        with connect(
                host=DataSql["Host"],
                user=DataSql["User"],
                password=DataSql["Password"],
                db=DataSql["DataBase"]
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
                host=DataSql["Host"],
                user=DataSql["User"],
                password=DataSql["Password"],
                database=DataSql["DataBase"]
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
