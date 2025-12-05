from flask import Flask, render_template, request, jsonify
import connect_database
import json
import chatbot


app = Flask(__name__)


user = None
products_list = []
conversations = []
total_price = 0





@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/')
def start():
    return render_template('login-register.html')

@app.route('/login', methods = ['GET' , 'POST'])
def login():
    global user
    error_message = None
    if request.method == 'POST':
        email = request.form['email'].strip()
        password = request.form['password'].strip()
        user = connect_database.get_name(email)
        result = connect_database.login(email=email , password=password)
        if result:
            return render_template("index.html")
        else:
            error_message = "Password Incorrect!"
            return render_template("login-register.html")

    return render_template('login-register.html',error = error_message)

@app.route('/register', methods=['GET', 'POST'])
def register():
    error_message = None

    if request.method == 'POST':
        first_name = request.form['first_name'].strip()
        last_name = request.form['last_name'].strip()
        email = request.form['email'].strip()
        password = request.form['password'].strip()
        confirm_password = request.form['cpassword'].strip()

        if password != confirm_password:
            error_message = "Passwords do not match. Please try again."
        else:
            print(f"Register - First Name: {first_name}, Last Name: {last_name}, Email: {email},Password: {password}")
            success_message = "Registered successfully! Login to continue shopping."
            connect_database.register_account(fname= first_name , lname= last_name , email= email ,
                                               password=password)
            return render_template('login-register.html', success=success_message)

    return render_template('login-register.html', error=error_message)
@app.route('/aboutus')
def aboutus():
    return render_template('about-us.html')
    
@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/shop')
def shop():
    return render_template('shop-3-column.html')

@app.route('/cart')
def cart():
    return render_template('shopping-cart.html')

@app.route('/product')
def product():
    return render_template('single-product.html')

@app.route('/wishlist')
def wishlist():
    return render_template('wishlist.html')


# Product prices list
product_prices = [
    ('Samsung Galaxy S9 | S9+', '₹ 34,999'),
    ('Apple Watch Series 1', '₹ 25,999'),
    ('Apple iPhone 7', '₹ 20,999'),
    ('iPad Air 2', '₹ 68,999'),
    ('Bang & Olufsen BeoPlay Speakers', '₹ 9,999'),
    ('Beats Solo3 Bluetooth Headset', '₹ 999'),
    ('Bose SoundLink Revolve', '₹ 2,999'),
    ('DELL LED Desktop', '₹ 12,999'),
    ('Xbox Wireless Controller', '₹ 7,999'),
    ('Samsung Gear 360', '₹ 1,05,999'),
    ('Samsung Curved Desktop', '₹ 48,999')
]

# Convert prices list to a dictionary
price_dict = {product: int(price.split('₹')[1].replace(',', '')) for product, price in product_prices}


@app.route('/webhook', methods=['POST'])
def webhook():
    global user, products_list, conversations, total_price


    req = request.get_json(force=True)
    fulfillment_response = req.get('queryResult')
    intent_name = fulfillment_response.get('intent').get('displayName')

    user_message = fulfillment_response.get('queryText')
    bot_message = fulfillment_response.get('fulfillmentText')


    conversation_item = {user : user_message, 'Bot': bot_message}
    conversations.append(conversation_item)
    print(user)
    if intent_name == 'Default Welcome Intent':
        response = {
            "fulfillmentText": f"""Hii {user} 👋  How can I assist? You can say 'New Order'."""
        }
    if intent_name == 'new.order':
        response = {
            "fulfillmentText": """Sure, creating a new order for you!  select items from this
             ( PRODUCT ID : PRODUCT ) , ( 402 : Apple Watch Series 1 )           , ( 409 : Xbox Wireless Controller ) 
                       , ( 403 : Apple iPhone 7 )                , ( 411 : Samsung Curved Desktop )        , 
                       ( 410 : Samsung Gear 360 )              , ( 408 : DELL LED Desktop )              , 
                       ( 404 : iPad Air 2 )                    , ( 407 : Bose SoundLink Revolve )        , 
                       ( 405 : Bang & Olufsen BeoPlay Speakers ) , ( 406 : Beats Solo3 Bluetooth Headset ) ,
                         ( 401 : Samsung Galaxy S9 | S9+ ) Specify items and quantities. products or their ids 
                         For example, you can say, For example, you can say, : I'd like to order 1 (403) and two  
                         iPad Air 2 for a tech"""
        }

    # Other specific intent handling
    elif intent_name == 'Default Fallback Intent':
        response = {
            "fulfillmentText": "I'm sorry 😢, I didn't understand that. Can you please rephrase?"
        }

    elif intent_name == 'order.add-context: ongoing-order':
        parameters = fulfillment_response.get('parameters')
        products = parameters.get('product', [])
        quantities = parameters.get('number', [])

        # Ensure both products and quantities are lists
        if not isinstance(products, list):
            products = [products]
        if not isinstance(quantities, list):
            quantities = [quantities]

        products_list = []

        for product, quantity in zip(products, quantities):
            products_list.append({'product': product, 'quantity': int(quantity)})

        response = {
            "fulfillmentText": f"Added {', '.join([f'{int(q)} of {p}' for p, q in zip(products, quantities)])} to your order. Anything Else? 📝",
        }


    elif intent_name == 'order.remove-context: ongoing-order':
        parameters = fulfillment_response.get('parameters')
        product = parameters.get('product')

        updated_list = [item for item in products_list if item['product'] != product[0]]  
        removed_items = [item for item in products_list if item['product'] == product[0]]

        products_list = updated_list

        response = {
            "fulfillmentText": f"Removed {len(removed_items)} of {product[0]} from your order."
        }
    
    print(products_list)

    if intent_name == 'negotiation':
        req_data = request.get_json(force=True)
        parameters = req_data.get('queryResult').get('parameters')
        percentage = parameters.get('percentage')
        amount = parameters.get('unit-currency')
        actual_price = total_price
        negotiation_response = None
        print(amount)
        print("Total : " , actual_price)
                
        if percentage:
            price = int(percentage.strip('%'))
            print("Price : ", price)
            print(type(price))
            price = chatbot.get_price(percent=price, original_price=actual_price)
            print("User Discount amount : " , price)
            negotiation_response = chatbot.perform_negotiation(user_amount = price , actual_price= actual_price)

        if amount:
            price = int(amount['amount'])
            print("User Amount : ", price)
            negotiation_response = chatbot.perform_negotiation(user_amount = price , actual_price= actual_price)
            print("Negotiation : " , negotiation_response)
        if negotiation_response:
            response = {
                "fulfillmentText": f"{negotiation_response}"
            }
        else:
            response = {
                "fulfillmentText": "Negotiation response not found."
            }
        
        check = f"Offer accepted! Please pay ₹{price}. Thank you! Visit again 😊"
        print("Check" , check)
        if negotiation_response == check:
            negotiated_price = price
            user_products = [item['product'] for item in products_list]
            product_quan = [item['quantity'] for item in products_list]
            product_ids = [connect_database.get_product_id(i) for i in user_products]
            print(negotiated_price,user_products,product_quan,product_ids)

            products_list.clear()

        conversation_item = {user: user_message, 'Bot': negotiation_response }
        conversations.append(conversation_item)

        print("response : ", response) 

        

    if intent_name == 'order.complete-context: ongoing-order':

        total_price = sum(price_dict[item['product']] * item['quantity'] for item in products_list)
        products = '\n'.join([f"{item['quantity']} of {item['product']}" for item in products_list])
        response = {
            "fulfillmentText": f"Thank you ❤! \nTotal Price: ₹ {total_price}\nProducts:\n{products}."
        }

        
        
        conversation_json = {'conversation': conversations, 'total_price': total_price, 'products': products}
        
        with open('conversation_data.json', 'w') as file:
            json.dump(conversation_json, file)
        with open('conversation_data.json', 'r') as file:
            conversation_str = file.read()

        connect_database.customer_table(user, conversation_str)
        
        conversations = []
    return jsonify(response) 

    


if __name__ == '__main__':
    app.run(debug=True)