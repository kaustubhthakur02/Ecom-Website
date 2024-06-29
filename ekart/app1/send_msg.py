# from app1.models import *
# import os
# from twilio.rest import Client

# account_sid = 'ACbfed8c1c91885dd1d48676eefeb41fa2'
# auth_token = 'd5a830829dae4f195475e38c30ce699d'
# client = Client(account_sid, auth_token)


# def sendmsg(product_id):
#     print(f"Product ID: {product_id}")

#     # Query orders based on the product ID
#     orders = Order.objects.filter(cid = product_id)
#     print(f"Orders count: {len(orders)}")

#     product_details = []
#     for order in orders:
#         print(f"Order: {order.cid.pid.name}, {order.cid.pid.price}")
#         product_details.append((order.cid.pid.name, order.cid.pid.price))

#     message_body = '\n\nOrder placed successfully!\n\nProduct Details:\n'
#     for name, price in product_details:
#         message_body += f"Name: {name}, Price: {price}\n"

#     print(message_body)

#     message = client.messages.create(
#         from_='+12567279802',
#         body=message_body,
#         to='+919156748282'
#     )

#     return message

# def sendmsg():
#     message_body = 'Order placed Successfully, Check mail for more details.😊'
#     print(message_body)
    
#     message = client.messages.create(
#         from_='+12567279802',
#         body=message_body,
#         to='+919156748282'
#     )
#     return message





