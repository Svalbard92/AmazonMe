import os
import mysql.connector
from scrapers.scraper import Amazon
from dotenv import load_dotenv
load_dotenv(f"{os.getcwd()}//environmentVariables//.env")


cnx = mysql.connector.connect(
        host = os.getenv('DB_HOST'),
        port = os.getenv('PORT'),
        user = os.getenv('DB_USERNAME'),
        password = os.getenv('DB_PASSWORD'),
        database = os.getenv('DATABASE'),
    )



async def verifyASIN(amazon_asin):
    cnx = mysql.connector.connect(
        host = os.getenv('DB_HOST'),
        port = os.getenv('PORT'),
        user = os.getenv('DB_USERNAME'),
        password = os.getenv('DB_PASSWORD'),
        database = os.getenv('DATABASE'),
    )
    cursor = cnx.cursor()
    sql_check_query = """SELECT * FROM asin_collections WHERE ASIN = %s"""
    params = (amazon_asin,)
    cursor.execute(sql_check_query, params)

    if cursor.fetchone():
        return True
    else:
        return
    

async def export_to_db(amazon_asin): 
    cnx = mysql.connector.connect(
        host = os.getenv('DB_HOST'),
        port = os.getenv('PORT'),
        user = os.getenv('DB_USERNAME'),
        password = os.getenv('DB_PASSWORD'),
        database = os.getenv('DATABASE'),
    )
    select_query = f"""SELECT * FROM asin_collections WHERE ASIN = '{amazon_asin}'"""
    cursor = cnx.cursor()  
    if await verifyASIN(amazon_asin):        
        cursor.execute(select_query)
        row = cursor.fetchone()

        columns = [col[0] for col in cursor.description]

        result_dict = dict(zip(columns, row))
        return result_dict
    else:        
        amazon_datas = await Amazon().dataByAsin(amazon_asin)   
        # return amazon_datas

        insert_query = f"""INSERT INTO `asin_collections` (`ASIN`, `Name`, `Price`, `Rating`, `Rating count`, `Availability`, `Hyperlink`, `Image`, `Store`, `Store link`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        values = (amazon_asin, amazon_datas['Name'], amazon_datas['Price'], amazon_datas['Rating'], amazon_datas['Rating count'], amazon_datas['Availability'], amazon_datas['Hyperlink'], amazon_datas['Image'], amazon_datas['Store'], amazon_datas['Store link'])

        cursor.execute(insert_query, values)
        cnx.commit()

        cursor.execute(select_query)
        row = cursor.fetchone()

        columns = [col[0] for col in cursor.description]

        result_dict = dict(zip(columns, row))
        return result_dict

    cursor.close()
    cnx.close()
    print(f"{amazon_asin} added to database.")


async def show_details(amazon_asin):
    mysql_pwd = os.getenv('MYSQL_PWD')
    cnx = mysql.connector.connect(
        host = '127.0.0.1',
        port = 2000,
        user = 'sus',
        password = mysql_pwd,
        database = 'asinDB',
    ) 
    cursor = cnx.cursor() 

