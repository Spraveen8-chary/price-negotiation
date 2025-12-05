
def get_price(percent, original_price):
    print(percent)
    print(type(percent))
    percent = 100 - percent
    result = original_price * (percent / 100)
    return result


with open('iter.txt', 'w') as file:
        file.write(str(1))



def perform_negotiation(user_amount, actual_price):

    try:
        with open('iter.txt', 'r') as file:
            discount_index = int(file.read())
    except FileNotFoundError:
        discount_index = 1


    last_price = int(actual_price - (actual_price * (15 / 100)))
    print("Last price:", last_price)

    discount_prices = [(actual_price - int(actual_price * (percent / 100))) for percent in range(2, 15)]
    print("Discount prices:", discount_prices)

    response = ""

    while discount_index < len(discount_prices):
        current_price = discount_prices[discount_index]
        if user_amount >= last_price:
            response = f"Offer accepted! Please pay ₹{user_amount}. Thank you! Visit again 😊"
            print(response)
            with open('iter.txt', 'w') as file:
                file.write(str(1))
            break
        else:
            response = f"Sorry 😢, I can't offer a lower price. My last offer is ₹{current_price}."
            print(response)
            break

    while discount_index > len(discount_prices):
        current_price = discount_prices
        if user_amount >= last_price:
            response = f"Offer accepted! Please pay ₹{user_amount}. Thank you! Visit again 😊"
            print(response)
            with open('iter.txt', 'w') as file:
                file.write(str(1))
            break
        else:
            response = f"Sorry 😢, I can't offer a lower price. My last offer is ₹{last_price}." 
            print(response)
            
            break
    
    discount_index += 1
    try:
        with open('iter.txt', 'w') as file:
            file.write(str(discount_index))
    except FileNotFoundError:
        discount_index = 1

    return response



if __name__ == '__main__':
    perform_negotiation(actual_price = 195403, user_amount = 123004)
    perform_negotiation(actual_price = 195403, user_amount = 134004)
    perform_negotiation(actual_price = 195403, user_amount = 132004)
    perform_negotiation(actual_price = 195403, user_amount = 135004)
    perform_negotiation(actual_price = 195403, user_amount = 145004)
    perform_negotiation(actual_price = 195403, user_amount = 148004)


