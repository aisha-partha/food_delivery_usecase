import mysql.connector
import itertools
import requests

#from delivery_time_model import __version__ as ml_version
#from delivery_time_model.predict import make_prediction
import pandas as pd
import json

import requests
import os 
import holidays
import smtplib

GOOGLE_MAPS_API_KEY = os.environ['GOOGLE_MAPS_API_KEY']
WEATHER_API_KEY = os.environ['WEATHER_API_KEY']
TRAFFIC_API_KEY = os.environ['TRAFFIC_API_KEY']
GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json'
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"

hostname = os.environ['HOSTNAME']
user = os.environ['USER']
password = os.environ['PASSWORD']
database = os.environ['DATABASE']



db = mysql.connector.connect(
    host=hostname,
    user=user,
    password=password,
    database=database
)

mc = db.cursor() 

def login(email, password):
    mc.execute(f"SELECT password FROM users WHERE email = '{email}'")
    detail = mc.fetchall()
    # for i in detail:
    try :
        passw = detail[0][0]
        if passw == password:
            return True
        else:
            return False
    except:
        return False
    
    
def signup(email, name, address ,city, phnumber, sign_password):
    pz = ''
    lat, long = fetch_google_coords(address)
    mc.execute(f"INSERT INTO users (user_id,email, name, password, address,city, phonenumber, delivery_location_latitude, delivery_location_longitude) VALUES (DEFAULT, '{email}','{name}', '{sign_password}', '{address}', '{city}', '{phnumber}', '{lat}', '{long}')")
    # mc.execute(f"INSERT INTO USER (USER_ID, USER_NAME, PASSWORD) VALUES ('{id}', '{name}','{password}') ")
    db.commit()
    return True

def get_details(email):
    mc.execute(f"SELECT user_id, name, address, phonenumber, email, city, delivery_location_latitude, delivery_location_longitude FROM users WHERE email = '{email}'")
    details = mc.fetchall()
    return [details[0][0], details[0][1], details[0][2], details[0][3], details[0][4], details[0][5], details[0][6], details[0][7]]
    
def place_order(user_id, total_amt, paymentmethod ,food_list, qty_list):
    try :
        mc.execute(f"INSERT INTO orders( user_id, ordertotal, paymentmethod, order_date, time_ordered, time_order_picked) VALUES ( '{user_id}', '{total_amt}', '{paymentmethod}', CURDATE(), CURTIME(), ADDTIME(CURTIME(),'00:15:00'))" )
        mc.execute("SELECT LAST_INSERT_ID()")     
        order_idd= mc.fetchone()[0]
        print('order_idd', order_idd)
        for (food, qty) in zip(food_list, qty_list):
            mc.execute(f"INSERT INTO orderitems ( order_id, item_name, quantity ) VALUES ('{order_idd}', '{food}', '{qty}')")
        db.commit()
        return True
    except:
        return False
    
def user_feedback(user_id, delivery_rating):
    print('user feedback')
    try :
        mc.execute("SELECT LAST_INSERT_ID()")     
        order_idd= mc.fetchone()[0]
        print('order_idd_feedback', order_idd)
        mc.execute(f"INSERT INTO feedback ( order_id, user_id, delivery_rating, food_rating ) VALUES ('{order_idd}', '{user_id}', '{delivery_rating}', '{delivery_rating}')")
        db.commit()
        return True
    except:
        return False
    
def get_user_data():
    mc.execute("SELECT user_id, email, name, address, phonenumber FROM users")
    details = mc.fetchall() 
    detail_dict = {'User Id': [i[0] for i in details ],
                   'Email Id' : [i[1] for i in details],
                   'Name' :[i[2] for i in details],
                   'Address':[i[3] for i in details],
                   'Phone Number' : [i[4] for i in details]}
    return detail_dict

    
def get_order_data():
    mc.execute("SELECT * FROM orders")
    details = mc.fetchall()
    details_dict = {'Order Id':[i[0] for i in details],
                  'User Id': [i[1] for i in details],
                  'Total Amount' :[i[2] for i in details],
                  'Payment Method':[i[3] for i in details]}
    return details_dict

def get_order_details():
    mc.execute("SELECT LAST_INSERT_ID()")     
    order_idd= mc.fetchone()[0]
    print("order id", order_idd)
    if int(order_idd) > 0:
        mc.execute(f"SELECT DATE_FORMAT(order_date, '%d-%m-%Y'), DATE_FORMAT(time_ordered, '%H:%i:%s'), DATE_FORMAT(time_order_picked,'%H:%i:%s') FROM orders where order_id = {order_idd} ")
        details = mc.fetchall()
        print(details)
        details_dict = {'Order Date':[i[0] for i in details],
                  'Time Food Ordered': [i[1] for i in details],
                  'Time Food Picked Up' :[i[2] for i in details]}
    else:
        details_dict = {'Order Date':'2025-01-11','Time Food Ordered':'10:00:00','Time Food Picked Up':'10:15:00'}
        
    return details_dict

def get_orderitem_data():
    mc.execute("SELECT * FROM orderitems")
    details = mc.fetchall()
    details_dict = {'order_id' : [i[0] for i in details],
                    'Food Item' : [i[1] for i in details],
                    'QTY':[i[2] for i in details]}
    return details_dict

def update_details(user_id, email, name ,address, number, city):
    mc.execute(f"UPDATE users SET email = '{email}', name ='{name}', address ='{address}', phonenumber = '{number}' , city = '{city}' WHERE user_id ={user_id} ")
    db.commit()
    return True

def update_password(user_id, password):
    mc.execute(f"UPDATE users SET password ='{password}' WHERE user_id={user_id} ")
    db.commit()
    return True

def get_orderitem_detail(order_id):
    mc.execute(f"SELECT * FROM orderitems WHERE order_id = '{order_id}'")
    details = mc.fetchall()
    detail_dict = {'order_id' : [i[0] for i in details],
                    'Food Item' : [i[1] for i in details],
                    'QTY':[i[2] for i in details]}
    return detail_dict

def delete_user(user_id):
    mc.execute("SET FOREIGN_KEY_CHECKS=0")
    mc.execute(f"DELETE users, orders, orderitems FROM users INNER JOIN orders ON users.user_id = orders.user_id INNER JOIN orderitems on orders.order_id = orderitems.order_id  WHERE users.user_id ={user_id}")
    db.commit()
    

def fetch_rest_add(rest_id, rest_city):
    mc.execute(f"SELECT restaurant_longitude, restaurant_latitude, delivery_person_age, delivery_person_ratings, delivery_person_id FROM restaurants WHERE restaurant_id = '{rest_id}' AND city_name = '{rest_city}'")
    detail = mc.fetchall()
    # for i in detail:
    try :
        rest_lat = detail[0][0]
        rest_long = detail[0][1]
        delivery_person_age = detail[0][2]
        delivery_person_ratings = detail[0][3]
        delivery_person_id = detail[0][4]
        return rest_lat, rest_long, delivery_person_age, delivery_person_ratings, delivery_person_id
    except:
        return 12.9332, 77.6154, 22, 4.8, 'BANGRES01DEL02'
    
def fetch_google_coords(address):
    
    params = {
            'address': address,
            'sensor': 'false',
            'region': 'india',
            'key': GOOGLE_MAPS_API_KEY,
        }

    # Do the request and get the response data
    req = requests.get(GOOGLE_MAPS_API_URL, params=params)
    res = req.json()
    res
    # Use the first result
    result = res['results'][0]

    geodata = dict()
    geodata['lat'] = result['geometry']['location']['lat']
    geodata['lng'] = result['geometry']['location']['lng']
    geodata['address'] = result['formatted_address']

    print('{address}. (lat, lng) = ({lat}, {lng})'.format(**geodata))
    return geodata['lat'] , geodata['lng']

def weather_api(city):
    city_mappings = {
        "INDORE": 0,
        "BANGALORE": 1,
        "COIMBATORE": 2,
        "CHENNAI": 3,
        "HYDERABAD": 4,
        "RANCHI": 5,
        "MYSORE": 6,
        "DELHI": 7,
        "KOCHI": 8,
        "PUNE": 9,
        "LUDHIANA": 10,
        "KANPUR": 11,
        "MUMBAI": 12,
        "KOLKATTA": 13,
        "JAIPUR": 14,
        "SURAT": 15,
        "GOA": 16,
        "AURANGABAD": 17,
        "AGRA": 18,
        "VADODRA": 19,
        "ALLAHABAD": 20,
        "BHOPAL": 21
    }


    #def get_key_city(val_city):

    #    for key, value in city_mappings.items():
    #        if val_city == value:
    #            return key

    #    return "key doesn't exist"


    #CITY=get_key_city(city_map)
    CITY = city

    weather_mappings = {
        "clear sky": "Sunny", #Sunny
        "mist": "Fog",  #Cloudy
        "haze": "Fog",  #Fog
        "scattered clouds": "Cloudy",
        "few clouds": "Sunny",
        "Windy": "Windy",
        "Stormy": "Stormy",
        "Sandstorms": "Sandstorms",
        "Other" : "Sunny"
    }





# upadting the URL
    URL = BASE_URL + "q=" + CITY + "&appid=" + WEATHER_API_KEY
# HTTP request
    response = requests.get(URL)
    response
# checking the status code of the request
    if response.status_code == 200:
   # getting data in the json format
        data = response.json()
   # getting the main dict block
        main = data['main']
   # getting temperature
        temperature = main['temp']
   # getting the humidity
        humidity = main['humidity']
   # getting the pressure
        pressure = main['pressure']
   # weather report
        report = data['weather']
        weather=report[0]['description']
        print(f"{CITY:-^30}")
        print(f"Temperature: {temperature}")
        print(f"Humidity: {humidity}")
        print(f"Pressure: {pressure}")
        print(f"Weather Report: {report[0]['description']}")
    else:
   # showing the error message
        weather = 'Other'
        print("Error in the HTTP request")


    def get_key_weather(val_weather):

        for key, value in weather_mappings.items():
            if val_weather == key:
                return value

        return weather_mappings['Other']

    Value=get_key_weather(weather)
    return(Value)

def check_festival(order_date):
        print('-----',order_date)
        if str(order_date[0]) in holidays.India(years=[2025]):
            return 'Yes'
        else:
            return 'No'
        
def traffic_density(source,destination):
# API key
    print(source)
    print(destination)
    home=source
    work=destination
# base url
    url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&"

    try:
        r = requests.get(url + "origins=" + home + "&destinations=" + work + "&key=" + TRAFFIC_API_KEY)
        print(r.json())
        # return time as text and as seconds
        time = r.json()["rows"][0]["elements"][0]["duration"]["text"]
        seconds = r.json()["rows"][0]["elements"][0]["duration"]["value"]
        distance = r.json()["rows"][0]["elements"][0]["distance"]["text"]
    except Exception as E:
        time = '9'
        seconds = '30'
        distance = '7'


    time_hr=time.split()[0]
    time_hr=float(time_hr)
    time_hr=(time_hr/60)
    print('time in hr:',time_hr)
    distance_km=distance.split()[0]
    distance_km=float(distance_km)
    distance_km= int(distance_km*1.6)
    print('distance in km:',distance_km)
    speed=int(distance_km/time_hr)
    print('speed:',speed)

    if(speed > 14):
        road_traffic_density='Low' #Low
    elif(speed > 7):
        road_traffic_density='Medium' #Medium
    elif(speed > 2):
        road_traffic_density='High' #High
    else:
        road_traffic_density='Jam' #Jam

    return(road_traffic_density)
    
def predict_delivery_time(rest_id, city, delivery_lat, delivery_long):
    Restaurant_latitude,Restaurant_longitude, Delivery_person_Age, Delivery_person_Ratings, Delivery_person_ID = fetch_rest_add(rest_id, city)
    Delivery_location_latitude = delivery_lat
    Delivery_location_longitude = delivery_long
    
    order_details = get_order_details()
    Order_Date = order_details['Order Date']
    Time_Orderd = order_details['Time Food Ordered']
    Time_Order_picked = order_details['Time Food Picked Up']
    Weatherconditions = weather_api(city)
    source = str(Restaurant_latitude) + ","+ str(Restaurant_longitude)
    destination = str(Delivery_location_latitude) + ","+ str(Delivery_location_longitude)
    Road_traffic_density = traffic_density(source, destination)
    Festival = check_festival(Order_Date)
    
    ID=str("0x4607")
    Delivery_person_ID=str(Delivery_person_ID)
    Delivery_person_Age=str(Delivery_person_Age)
    Delivery_person_Ratings=str(Delivery_person_Ratings)
    Restaurant_latitude=str(Restaurant_latitude)
    Restaurant_longitude=str(Restaurant_longitude)
    Delivery_location_latitude=str(Delivery_location_latitude)
    Delivery_location_longitude=str(Delivery_location_longitude)
    Order_Date=str(Order_Date[0])
    Time_Orderd=str(Time_Orderd[0])
    Time_Order_picked=str(Time_Order_picked[0])
    print('Time_Orderd', Time_Orderd)
    print('Time_Order_picked',Time_Order_picked)
    Weatherconditions= 'conditions ' + str(Weatherconditions)
    Road_traffic_density=str(Road_traffic_density)
    #Vehicle_condition=str(Vehicle_condition)
    #Type_of_order=str(Type_of_order)
    #Type_of_vehicle=str(Type_of_vehicle)
    #multiple_deliveries=str(multiple_deliveries)
    Festival=str(Festival)
    #City=str(city)
    
    #data_in = [{"ID": "0x4607",'Delivery_person_ID': 'INDORES13DEL02', 'Delivery_person_Age': '37', 'Delivery_person_Ratings': '4.9', 'Restaurant_latitude': '22.745049',
    #           'Restaurant_longitude': '75.892471', 'Delivery_location_latitude': '22.765049', 'Delivery_location_longitude': '75.912471', 'Order_Date': '19-03-2022', 
    #           'Time_Orderd': '11:30:00', 'Time_Order_picked': '11:45:00',
    #           'Weatherconditions' :'conditions Sunny','Road_traffic_density' :'High','Vehicle_condition' :'2','Type_of_order' :'Snack',
    #           'Type_of_vehicle':'motorcycle','multiple_deliveries':'0','Festival' :'No','City' :'Urban'}]
    
    data_in = [{"ID": "0x4607",'Delivery_person_ID': Delivery_person_ID, 'Delivery_person_Age': Delivery_person_Age, 'Delivery_person_Ratings': Delivery_person_Ratings, 
                'Restaurant_latitude': Restaurant_latitude, 'Restaurant_longitude': Restaurant_longitude, 'Delivery_location_latitude': Delivery_location_latitude, 
                'Delivery_location_longitude': Delivery_location_longitude, 'Order_Date': Order_Date, 
                'Time_Orderd': Time_Orderd, 'Time_Order_picked': Time_Order_picked,
                'Weatherconditions' :Weatherconditions,'Road_traffic_density' :Road_traffic_density,'Festival' : Festival,
                'Vehicle_condition' :'2','Type_of_order' :'Snack', 'Type_of_vehicle':'motorcycle','multiple_deliveries':'0','City' :'Urban'}]
																		
    data = { "inputs" : data_in } 
    try:
        r = requests.post(url = "http://localhost:8001/api/v1/predict", data = json.dumps(data))
        r = r.json()
        print(r)
        return r['predictions']
        

    except Exception as e:
        return 'Failed to get prediction.' + str(e)