import json
import os
import csv

with open('Summary.csv', 'w') as c:
    c.write('CustomerID,NumberOfOrders,TotalPriceOfAllOrders,AvgPriceOfOrders\n')  # columns of csv file
info_csv = {}  # info to add to csv file

for folder in os.listdir(r'C:\Users\Rotem\Desktop\Orders\Orders'):  # access to outer folder
    order_sum = {}  # temp dictionary to convert into json file

    with open(fr'C:\Users\Rotem\Documents\שונות\עבודה ליאור\Orders\Orders\{folder}\Customer.json') as f:  # access data
        customer_dict = json.load(f)  # download data

        """save data to temporary dictionary"""
        order_sum['firstName'] = customer_dict['firstName']
        order_sum['lastName'] = customer_dict['lastName']

        customer_id = customer_dict['customerID']  # information for folder name

        """collect data for csv file"""
        if customer_id not in info_csv:  # data to insert into csv file
            info_csv[customer_id] = [0, 0, 0]  # data in the following order-> number of orders, total and avg

    with open(fr'C:\Users\Rotem\Documents\שונות\עבודה ליאור\Orders\Orders\{folder}\Order.json') as o:
        order_dict = json.load(o)  # download data

        """save data to temporary dictionary"""
        month = order_dict['orderMonth']
        year = order_dict['orderYear']

        order_sum['orderDate'] = f'{month}/{year}'
        order_sum['number_of_products'] = len(order_dict["products"])

        result = 0
        max_item = ''
        max_price = 0
        yellow = 0
        for item in order_dict["products"]:
            result += item['price']
            if item['price'] > max_price:
                max_price = item['price']
                max_item = item['name']
            yellow = yellow + 1 if 'yellow' in item['tags'] else yellow

        order_sum['totalPrice'] = result
        order_sum['max_price_item'] = max_item
        order_sum['yellow_in_order'] = True if yellow > 0 else False

        """collect data for csv file"""
        info_csv[customer_id][0] += 1  # number of orders
        info_csv[customer_id][1] += result  # total of order

        """add data to summary file"""
        try:
            os.makedirs(fr'C:\Users\Rotem\Desktop\{customer_id}\{folder}')
            with open(fr'C:\Users\Rotem\Desktop\{customer_id}\{folder}\OrderSummary.json', 'w') as w:
                json.dump(order_sum, w, indent=len(customer_dict))
        except:
            with open(fr'C:\Users\Rotem\Desktop\{customer_id}\{folder}\OrderSummary.json', 'w') as w:
                json.dump(order_sum, w, indent=len(customer_dict))

"""------------------------------------------------------------------------------------------------------------------"""
"""add info to csv file"""
with open('Summary.csv', 'a') as a:
    csv_writer = csv.writer(a, delimiter='\t')
    for customer in info_csv.items():
        temp_lst = [customer[0], customer[1][0], customer[1][1], customer[1][1] / customer[1][0]]
        csv_writer.writerow(temp_lst)
