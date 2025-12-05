from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import json
import hashlib
from datetime import datetime

# Establishing connection to Cassandra
cloud_config = {
    'secure_connect_bundle': 'secure-connect-limupa-database.zip'
}

with open("Limupa Database-token.json") as f:
    secrets = json.load(f)

CLIENT_ID = secrets["clientId"]
CLIENT_SECRET = secrets["secret"]

auth_provider = PlainTextAuthProvider(CLIENT_ID, CLIENT_SECRET)
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect()

keyspace_name = 'limupa_database'

# Using the specified keyspace
session.execute(f"USE {keyspace_name}")
# Function to create tables
def create_tables():
    create_register_table = """
    CREATE TABLE IF NOT EXISTS register (
        name text PRIMARY KEY,
        email text,
        password text
    )
    """

    create_customer_table = """
    CREATE TABLE IF NOT EXISTS customer (
        order_id int,
        name text,
        chat map<text, text>,
        PRIMARY KEY (order_id, name)
    )
    """

    create_product_table = """
    CREATE TABLE IF NOT EXISTS product (
        product_id int PRIMARY KEY,
        price text,
        product text,
        product_img text
    )
    """

    session.execute(create_register_table)
    session.execute(create_customer_table)
    session.execute(create_product_table)


    print("Tables created successfully")

# Function to insert data into the product table
def insert_product_data():
    product_data = [
        (401, "Samsung Galaxy S9 | S9+", "₹ 34,999", 'images/product/large-size/12.jpg'),
        (402, "Apple Watch Series 1", "₹ 25,999", 'images/product/large-size/11.jpg'),
        (403, "Apple iPhone 7", "₹ 20,999", 'images/product/large-size/9.jpg'),
        (404, "iPad Air 2", "₹ 68,999", 'images/product/large-size/8.jpg'),
        (405, "Bang & Olufsen BeoPlay Speakers", "₹ 9,999", 'images/product/large-size/7.jpg'),
        (406, "Beats Solo3 Bluetooth Headset", "₹ 999", 'images/product/large-size/6.jpg'),
        (407, "Bose SoundLink Revolve", "₹ 2,999", 'images/product/large-size/5.jpg'),
        (408, "DELL LED Desktop", "₹ 12,999", 'images/product/large-size/4.jpg'),
        (409, "Xbox Wireless Controller", "₹ 7,999", 'images/product/large-size/3.jpg'),
        (410, "Samsung Gear 360", "₹ 1,05,999", 'images/product/large-size/2.jpg'),
        (411, "Samsung Curved Desktop", "₹ 48,999", 'images/product/large-size/1.jpg')
    ]

    for product in product_data:
        session.execute(
            """
            INSERT INTO product (product_id, product, price, product_img)
            VALUES (%s, %s, %s, %s)
            """,
            (product[0], product[1], product[2], product[3])
        )

    print("Product data inserted successfully")



def register_account(fname, lname, email, password):
    name = f"{fname} {lname}" 
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    try:
        session.execute(
            "INSERT INTO register (name, email, password) VALUES (%s, %s, %s)",
            (name, email, hashed_password)
        )
        print("Account registered successfully!")
    except Exception as e:
        print(f"Failed to register account. Error: {e}")


def login(email, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    result = session.execute(
        "SELECT email, password FROM register WHERE email = %s",
        (email,)
    )
    for row in result:
  
        if row.password == hashed_password:
            return True 
    return False  



def customer_table(name, chat):
    chat_data = json.loads(chat)
    conversation = chat_data["conversation"]

    flat_conversation = ""
    for entry in conversation:
        for key, value in entry.items():
            flat_conversation += f"{key}: {value}\n"

    result = session.execute("SELECT MAX(order_id) FROM customer")
    max_order_id = result[0][0] if result and result[0] and result[0][0] is not None else 0

    order_id = max_order_id + 1
    date = datetime.now()

    session.execute(
        """
        INSERT INTO customer (order_id, name, date, chat)
        VALUES (%s, %s, %s, %s)
        """,
        (order_id, name, date, {flat_conversation: ""})
    )
    return order_id

def order_data(negotiated_price,product_id , product ):
    order_id = customer_table.order
    product_ids = []
    

def get_name(email):
    name = session.execute("""SELECT name,email FROM register WHERE email = %s """ , (email,))
    for i in name:
        return i.name
    


def get_product_id(product):
    result = session.execute("""SELECT product_id FROM product WHERE product = %s ALLOW FILTERING""", (product,))
    for i in result:
        return i.product_id

session.execute("CREATE INDEX IF NOT EXISTS ON register (email)")



if __name__ == '__main__':
    
    # Create tables
    # create_tables()

    # Insert product data
    # insert_product_data()



    # session.execute("""
    #     ALTER TABLE order_table ADD quantity timestamp
    # """)


    # # Adding 'date' column to the 'order_table' table
    # session.execute("""
    #     ALTER TABLE order_table ADD date timestamp
    # """)


    rows = session.execute("SELECT * FROM product")
    for row in rows:
        print(row)

    print("done...")

    rows = session.execute("SELECT * FROM register")
    for row in rows:
        print(row)

    # session.execute("DELETE FROM register WHERE name = 'praveen chary'")
    print('donee...')
    name = get_name('spchary21047cs012@gmail.com')
    print(name)
    print("done...")
    rows = session.execute("SELECT * FROM customer")
    for row in rows:
        print(row)
    session.execute("TRUNCATE TABLE customer")
    print("truncated....")


