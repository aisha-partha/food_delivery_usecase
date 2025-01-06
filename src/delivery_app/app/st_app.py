import streamlit as st 
from userdata import login, signup, get_details, place_order, update_details, update_password, delete_user, predict_delivery_time, user_feedback
import pandas as pd 
import time 

st.set_page_config(page_title='Order Food Now !', page_icon=None, layout="centered", initial_sidebar_state="auto", menu_items=None)

headerSection = st.container()
mainSection = st.container()
loginSection = st.container()
logOutSection = st.container()
checkoutSection = st.container()
chatSection = st.container()
   
food_list=[None, None, None, None, None, None, None, None, None ]
qty_list=[None, None, None , None, None, None, None, None, None]
amt_list=[None, None, None, None, None, None, None, None, None]

rest_id = 1

order = {
    'Food Name':food_list,
    'Qty' : qty_list,
    'Amount':amt_list
}

cart = pd.DataFrame(order)


def show_chat_page(name):
    with chatSection:  
        #with st.form("my_form"):
        st.text(f"Rate Delivery") 
        sentiment_mapping = ["one", "two", "three", "four", "five"]
        selected = st.feedback("stars")
        #submitted = st.form_submit_button("Submit")
        #if submitted:
        time.sleep(2)
        selected = 3
        print(selected)
        if selected is not None:
            delivery_rating = sentiment_mapping[selected]
            submit_user_feedback(st.session_state['details'][0], delivery_rating)
        else:
            delivery_rating = 0
        submit_user_feedback(st.session_state['details'][0], 3)
            
        
        
def order_pressed(user_id, total_amt, paymentmethod ,food_list, qty_list, rest_id):
    if place_order(user_id, total_amt, paymentmethod, food_list, qty_list):
        st.session_state['checkout'] = True
        st.session_state['loggedIn'] = False
        st.session_state['predicted_delivery_time'] = predict_delivery_time(
            rest_id, 
            st.session_state['details'][5], 
            st.session_state['details'][6], 
            st.session_state['details'][7], 
        )
        
                

def show_checkout_page():
    with checkoutSection:
        my_bar = st.progress(0)
        for percent_complete in range(100):
            time.sleep(0.01)
            my_bar.progress(percent_complete + 1)
        st.success(f"Hey {st.session_state['details'][1]}, Your Order has been placed Successfully")
        st.balloons()
        #st.subheader(f"Your Order will arrive to your address {st.session_state['details'][2]}" )
        st.subheader(f"Your Order will arrive to your address in {st.session_state['predicted_delivery_time']} minutes") 
        st.subheader(f"and our rider will contact you on = {st.session_state['details'][3]}")
        
        st.button ("Feedback", on_click=show_chat_page, args= (st.session_state['details'][1],))

def update_user_details(user_id, email, name ,address, number, city):
    if update_details(user_id, email, name ,address, number, city):
        st.info("User Information Updated Successfully, you will be logged out now")
        LoggedOut_Clicked()
    else:
        st.info("Error Detected while updating")


def update_user_password(user_id, password):
    if update_password(user_id, password):
        st.info("Password updated successfully, you will be logged out now")
        LoggedOut_Clicked()
    else:
        st.info("Error Detected while updating password")
    
def submit_user_feedback(user_id, delivery_rating):
    if user_feedback(user_id, delivery_rating):
        st.info("Feedback submitted successfully!")
    else:
        st.info("Error Detected while submitting feedback")
        
def show_main_page():
    with mainSection:
        st.header(f" Welcome {st.session_state['details'][1]} :sunglasses:")
        
        
        menu, cart, myaccount = st.tabs(['Menu', 'Cart', 'My Account'])
        
        
        with menu:
            
            st.subheader('Select the food you want to order') 
            
            rest1 = st.radio("Select the Restaurant",
                [" ","The Sizzling Spoon"])
        
            col1, col2, col3 = st.columns(3)
            col1.image('food_images/pizza.jpg')
            col1.text("Pizza 🍕")
            if col1.checkbox(label ='Order Pizza @ ₹199',key =1):
                col1.text('Enter QTY. -')
                c_pizza = col1.number_input(label="", min_value=1, key = 11)
                food_list[0] = 'pizza'
                qty_list[0] = int(c_pizza)
                amt_list[0] = int(c_pizza)*199
                      
            col2.image('food_images/burger.jpg')
            col2.text("Burger 🍔")
            if col2.checkbox('Order Buger @ ₹99',key =2):
                col2.text('Enter QTY. -')
                c_burger = col2.number_input(label="", min_value=1, key = 12)
                
                food_list[1] = 'burger'
                qty_list[1] = int(c_burger)
                amt_list[1] = int(c_burger)*99             
                       
            col3.image('food_images/noodles.jpg')
            col3.text("Noodles 🍜")
            if col3.checkbox('Order noodles @ ₹149',key =3):
                col3.text('Enter QTY. -')
                c_noodles = col3.number_input(label="", min_value=1, key = 13)
                food_list[2] = 'noodles'
                qty_list[2] = int(c_noodles)
                amt_list[2] = int(c_noodles)*149                
              
            rest2 = st.radio("Select the Restaurant",
                [" ","Tea Time Treats",])
         
            col1, col2, col3 = st.columns(3)
            col1.image('food_images/coffee.png')
            col1.text("Coffee")
            if col1.checkbox(label ='Order Coffee @ ₹79',key =4):
                col1.text('Enter QTY. -')
                c_coffee = col1.number_input(label="", min_value=1, key = 14)
                food_list[3] = 'Coffee'
                qty_list[3] = int(c_coffee)
                amt_list[3] = int(c_coffee)*79
                      
            col2.image('food_images/tea.png')
            col2.text("Tea")
            if col2.checkbox('Order Tea @ ₹79',key =5):
                col2.text('Enter QTY. -')
                c_tea = col2.number_input(label="", min_value=1, key = 15)
                
                food_list[4] = 'Tea'
                qty_list[4] = int(c_tea)
                amt_list[4] = int(c_tea)*79             
                       
            col3.image('food_images/latte.png')
            col3.text("Latte")
            if col3.checkbox('Order Latte @ ₹149',key =6):
                col3.text('Enter QTY. -')
                c_latte = col3.number_input(label="", min_value=1, key = 16)
                food_list[5] = 'Latte'
                qty_list[5] = int(c_latte)
                amt_list[5] = int(c_latte)*149    
                
            
            rest3 = st.radio("Select the Restaurant",
                [" ","Sip & Snack Cafe"])
            
            col1, col2, col3 = st.columns(3)
            col1.image('food_images/juice.png')
            col1.text("Fruit Juice")
            if col1.checkbox(label ='Order Juice @ ₹100',key =7):
                col1.text('Enter QTY. -')
                c_juice = col1.number_input(label="", min_value=1, key = 17)
                food_list[6] = 'Juice'
                qty_list[6] = int(c_juice)
                amt_list[6] = int(c_juice)*100
                      
            col2.image('food_images/sandwich.png')
            col2.text("Sandwich")
            if col2.checkbox('Order Sandwich @ ₹120',key =8):
                col2.text('Enter QTY. -')
                c_sandwich = col2.number_input(label="", min_value=1, key = 18)
                
                food_list[7] = 'Sandwich'
                qty_list[7] = int(c_sandwich)
                amt_list[7] = int(c_sandwich)*120             
                       
            col3.image('food_images/fries.png')
            col3.text("Fries")
            if col3.checkbox('Order fries @ ₹149',key =9):
                col3.text('Enter QTY. -')
                c_fries = col3.number_input(label="", min_value=1, key = 19)
                food_list[8] = 'Fries'
                qty_list[8] = int(c_fries)
                amt_list[8] = int(c_fries)*149     
                
            with cart:
                hide_table_row_index = """
                <style>
                thead tr th:first-child {display:none}
                tbody th {display:none}
                </style>
                 """
                st.markdown(hide_table_row_index, unsafe_allow_html=True)
                
                order = {
                        'Food Name':food_list,
                        'Qty' : qty_list,
                        'Amount':amt_list
                    }
                
                cart = pd.DataFrame(order)
                cart_final = cart.dropna()
                cart_final['Qty'].astype(int)
                st.table(cart_final)
                total_amt = [ amt for amt in amt_list if amt!=None]
                total_item = [food for food in food_list if food !=None]
                total_qty = [qty for qty in qty_list if qty!=None]
                total_sum = sum(total_amt)
                st.subheader("Your Total Amout to be paid" + ' --  Rs.'+ str(total_sum) )
                
                payment = st.selectbox('How would you like to Pay',('Cash','UPI', 'Net Banking', 'Credit Card', 'Debit Card'))
                
                if rest1 != "":
                    rest_id = 1
                elif rest2 != "":
                    rest_id = 2
                else:
                    rest_id = 3
                    
                
                st.button ("Order Now", on_click=order_pressed, args= (st.session_state['details'][0], total_sum, payment ,total_item, total_qty, rest_id))
            
            with myaccount:
                st.header('Update your details here')
                st.subheader("Enter updated email")
                up_email = st.text_input(label="", value = str(st.session_state['details'][4]))
                st.subheader("Enter updated name")
                up_name = st.text_input(label="", value=str(st.session_state['details'][1]))
                st.subheader("Enter updated address")
                up_address = st.text_input(label="", value=str(st.session_state['details'][2]))
                up_city = st.selectbox('Choose City',('Agra','Aurangabad','Bangalore','Bhopal','Chennai','Coimbatore','Delhi','Goa',
                        'Hyderabad','Indore','Jaipur','Kanpur','Kochi','Kolkata','Ludhiana','Mumbai','Mysore','Prayagraj','Pune','Ranchi','Surat','Vadodra'))
                st.subheader("Enter updated phone number")
                up_number = st.text_input(label="", value=str(st.session_state['details'][3]))
                
                st.button('Update User Details', on_click = update_user_details , args=(st.session_state['details'][0], up_email, up_name, up_address, up_number, up_city))

                if st.checkbox("Do you want to change the password ?"):
                    st.subheader('Write Updated Password :')
                    up_passw =st.text_input (label="", value="",placeholder="Enter updated password", type="password", key = 256)
                    up_conf_passw = st.text_input (label="", value="",placeholder="Enter updated password", type="password", key =257)
                    if up_passw == up_conf_passw:
                        st.button('Update Password', on_click=update_user_password, args=(st.session_state['details'][0], up_passw))
                    else :
                        st.info('Password does not match ')
                        
                if st.checkbox("Do you want to Delete your account ? "):
                    st.subheader("Are you sure you want to delete your account ?")
                    st.text(st.session_state['details'][0])
                    st.button('DELETE MY ACCOUNT', on_click = delete_user_show, args =(st.session_state['details'][0],))
            
            
                   
def delete_user_show(urd_id):
    delete_user(urd_id)
    LoggedOut_Clicked()
    st.success("Account Deleted Successfuly")

def LoggedOut_Clicked():
    st.session_state['loggedIn'] = False
    st.session_state['details'] = None
    st.session_state['checkout'] = False
    
def show_logout_page():
    loginSection.empty();
    with logOutSection:
        st.button ("Log Out", key="logout", on_click=LoggedOut_Clicked)
        

def LoggedIn_Clicked(email_id, password):
    if login(email_id, password):
        st.session_state['loggedIn'] = True
        st.session_state['details'] = get_details(email_id)
        
    else:
        st.session_state['loggedIn'] = False;
        st.session_state['details'] = None
        st.error("Invalid user name or password")
        
def signup_clicked(email, name, address ,city, phnumber, sign_password):
    try :
        if signup(email, name, address ,city, phnumber,sign_password):
            st.success("Signup successful ")
            st.balloons()
    except:
        st.warning('Invalid User ID or user ID already taken')
    
        
def show_login_page():
    with loginSection:
        if st.session_state['loggedIn'] == False:
            
            login, signup = st.tabs(["Login ✨", "Signup ❤️"])
            with login:
                st.subheader('Login Here 🎉')         
                email_id = st.text_input (label="", value="", placeholder="Enter your Email")
                password = st.text_input (label="", value="",placeholder="Enter password", type="password")
                st.button ("Login", on_click=LoggedIn_Clicked, args= (email_id, password))
            with signup:
                st.subheader('Signup 🫶')
                email = st.text_input(label="", value="", placeholder = "Enter your Email-ID", key = 10)
                name = st.text_input (label="", value="", placeholder="Enter your Name", key =9)
                
                address = st.text_input(label="", value="", placeholder ="Enter your Address:", key = 13)
                city = st.selectbox('Choose City',('Agra','Aurangabad','Bangalore','Bhopal','Chennai','Coimbatore','Delhi','Goa',
                        'Hyderabad','Indore','Jaipur','Kanpur','Kochi','Kolkata','Ludhiana','Mumbai','Mysore','Prayagraj','Pune','Ranchi','Surat','Vadodra'))
                phnumber = st.text_input(label= "", value="+91 ", placeholder ='Enter you Phone Number', key =14)
                
                sign_password =  st.text_input (label="", value="",placeholder="Enter password", type="password", key = 11)
                cnf_password =  st.text_input (label="", value="",placeholder="confirm your password", type="password", key = 12)
                st.button ("Sign UP", on_click=signup_clicked, args= (email, name, address ,city, phnumber,sign_password))
                if sign_password != cnf_password:
                    st.warning('Password does not match')


with headerSection:
    st.title("Online Food Ordering System 😋")
    if 'loggedIn' not in st.session_state:
        st.session_state['loggedIn'] = False
        show_login_page() 
    if 'checkout' not in st.session_state:
        st.session_state['checkout'] = False
    else:
        if st.session_state['loggedIn']:
            show_logout_page()    
            show_main_page()
        elif st.session_state['checkout']:
            show_logout_page()
            show_checkout_page()
        else:
            show_login_page()

            
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)