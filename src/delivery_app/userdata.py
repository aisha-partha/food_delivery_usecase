import mysql.connector
import itertools

#from delivery_time_model import __version__ as ml_version
#from delivery_time_model.predict import make_prediction
import pandas as pd


db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='adminadmin',
    database="onlinerest"
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
    
    
def signup(email, name, address ,phnumber,sign_password):
    pz = ''
    mc.execute(f"INSERT INTO users (user_id,email, name, password, address, phonenumber) VALUES (DEFAULT, '{email}','{name}', '{sign_password}', '{address}', '{phnumber}')")
    # mc.execute(f"INSERT INTO USER (USER_ID, USER_NAME, PASSWORD) VALUES ('{id}', '{name}','{password}') ")
    db.commit()
    return True

def get_details(email):
    mc.execute(f"SELECT user_id, name, address, phonenumber, email FROM users WHERE email = '{email}'")
    details = mc.fetchall()
    return [details[0][0], details[0][1], details[0][2], details[0][3], details[0][4]]
    
def place_order(user_id, total_amt, paymentmethod ,food_list, qty_list):
    try :
        mc.execute(f"INSERT INTO orders( user_id, ordertotal, paymentmethod) VALUES ( '{user_id}', '{total_amt}', '{paymentmethod}') " )
        mc.execute("SELECT LAST_INSERT_ID()")
        order_idd= mc.fetchone()[0]
        
        for (food, qty) in zip(food_list, qty_list):
            mc.execute(f"INSERT INTO orderitems ( order_id, item_name, quantity ) VALUES ('{order_idd}', '{food}', '{qty}')")
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

def get_orderitem_data():
    mc.execute("SELECT * FROM orderitems")
    details = mc.fetchall()
    details_dict = {'order_id' : [i[0] for i in details],
                    'Food Item' : [i[1] for i in details],
                    'QTY':[i[2] for i in details]}
    return details_dict

def update_details(user_id, email, name ,address, number):
    mc.execute(f"UPDATE users SET email = '{email}', name ='{name}', address ='{address}', phonenumber = '{number}' WHERE user_id ={user_id} ")
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
    
    
def predict_delivery_time(ID,Delivery_person_ID,Delivery_person_Age,Delivery_person_Ratings,Restaurant_latitude,Restaurant_longitude,Delivery_location_latitude,Delivery_location_longitude,Order_Date,Time_Orderd,Time_Order_picked,Weatherconditions,Road_traffic_density,Vehicle_condition,Type_of_order,Type_of_vehicle,multiple_deliveries,Festival,City):
    ID=str(ID)
    Delivery_person_ID=str(Delivery_person_ID)
    Delivery_person_Age=str(Delivery_person_Age)
    Delivery_person_Ratings=str(Delivery_person_Ratings)
    Restaurant_latitude=str(Restaurant_latitude)
    Restaurant_longitude=str(Restaurant_longitude)
    Delivery_location_latitude=str(Delivery_location_latitude)
    Delivery_location_longitude=str(Delivery_location_longitude)
    Order_Date=str(Order_Date)
    Time_Orderd=str(Time_Orderd)
    Time_Order_picked=str(Time_Order_picked)
    Weatherconditions=str(Weatherconditions)
    Road_traffic_density=str(Road_traffic_density)
    Vehicle_condition=str(Vehicle_condition)
    Type_of_order=str(Type_of_order)
    Type_of_vehicle=str(Type_of_vehicle)
    multiple_deliveries=str(multiple_deliveries)
    Festival=str(Festival)
    City=str(City)
    
    input = [ID,Delivery_person_ID,Delivery_person_Age,Delivery_person_Ratings,Restaurant_latitude,Restaurant_longitude,Delivery_location_latitude,Delivery_location_longitude,Order_Date,Time_Orderd,Time_Order_picked,Weatherconditions,Road_traffic_density,Vehicle_condition,Type_of_order,Type_of_vehicle,multiple_deliveries,Festival,City]
    input_df = pd.DataFrame([input],columns = ['ID','Delivery_person_ID','Delivery_person_Age','Delivery_person_Ratings','Restaurant_latitude','Restaurant_longitude','Delivery_location_latitude','Delivery_location_longitude','Order_Date','Time_Orderd','Time_Order_picked','Weatherconditions','Road_traffic_density','Vehicle_condition','Type_of_order','Type_of_vehicle','multiple_deliveries','Festival','City'])
    print(input_df.head())
    #pred_results = make_prediction(input_data=input_df.replace({np.nan: None}))
    
    #return pred_results['predictions'][0]
    return '10'