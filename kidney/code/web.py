import streamlit as st
import time
import numpy as np
from joblib import load 
import sqlite3
from passlib.hash import pbkdf2_sha256
import pandas as pd
import plotly.figure_factory as ff

st.set_page_config(
            page_title="Kidney Disease Identifier",
            page_icon="🔴",
            layout="wide",
            initial_sidebar_state="expanded",
        )



def result():
    name = st.text_input("Enter The Patient Name")
    age = st.text_input("Enter The Patient Age")
    gen = st.text_input("Enter The Patient Gender(Male/Female)")
            
    doc_name = st.text_input("Doctor Name")
    st.caption("Enter the Below Details Correctly, with your full knowledge")
    bp  = st.text_input("Enter The Blood Pressure value") 
    sg  = st.text_input("Enter The Specific gravity value")  
    al  = st.text_input("Enter The Albumin value")  
    
    su  = st.text_input("Enter The Sugar value")  
    rbc  = st.text_input("Enter The Red Blood Cells value")  
    bu  = st.text_input("Enter The Blood Urea value")  
    sc  = st.text_input("Enter The Serum Creatinine value")  
    sod  = st.text_input("Enter The Sodium value")  
    pot  = st.text_input("Enter The Potassium value")  
    hemo  = st.text_input("Enter The Hemoglobin value")  
    wbcc  = st.text_input("Enter The White Blood Cells Count")  
    rbcc  = st.text_input("Enter The Red Blood Cells Count")  
    htn  = st.selectbox('Is the Patient Suffering from Hypertension?',('yes', 'no'))
    st.write('You selected:', htn)
    if htn=='yes':
        htn = 1
    else:
        htn = 0
                
    agree = st.checkbox('I agree, the above data are correctly entered.')
    if agree:
        if(st.button("Submit")):
            progress_text = "Operation in progress. Please wait."
            my_bar = st.progress(0, text=progress_text)
            for percent_complete in range(10):
                time.sleep(0.01)
                my_bar.progress(percent_complete + 1, text=progress_text)
                time.sleep(1)
                my_bar.empty()
                    
                    
            st.header("Input Values")
                    # Bp - # Blood Pressure
                    # Sg - # Specific Gravity
                    # Al - # Albumin
                    # Su - # Sugar
                    # Rbc - # Red Blood Cell
                    # Bu - # Blood Urea
                    # Sc - # Serum Creatinine
                    # Sod - # Sodium
                    # Pot - # Pottasium
                    # Hemo - # Hemoglobin
                    # Wbcc - # White Blood Cell Count
                    # Rbcc - # Red Blood Cell Count
                    # Htn - # Hypertension
            # data_dict = {"Blood Pressure":float(bp),"Specific Gravity":float(sg),"Albumin":float(al),"Sugar":float(su),
            #              "Red Blood Cell":float(rbc),"Blood Urea":float(bu),"Serum Creatinine":float(sc),"Sodium":float(sod),
            #              "Potassium":float(pot),"HemoGlobin":float(hemo),"WBC count":float(wbcc),"RBC count":float(rbcc),
            #              "Hybertension":float(htn)}
            
            # data = pd.DataFrame(data_dict)
            
            col1, col2, col3,col4 = st.columns(4)
            col1.metric("Blood Pressure", str(bp), )
            col2.metric("Specific Gravity", str(sg), )
            col3.metric("Albumin", str(al), )
            col4.metric("Sugar",str(su),)
                    
            col5, col6, col7,col8 = st.columns(4)
            col5.metric("Red Blood Cell", str(rbc), )
            col6.metric("Blood Urea", str(bu), )
            col7.metric("Serum Creatinine", str(sc), )
            col8.metric("Sodium",str(sod),)
                    
            col9, col10, col11,col12,col13 = st.columns(5)
            col9.metric("Potassium", str(pot), )
            col10.metric("Hemoglobin", str(hemo), )
            col11.metric("WBC Count", str(wbcc), )
            col12.metric("RBC Count",str(rbcc),)
            col13.metric("Hypertension",str(htn),)
                    
            model = load('kidney/code/model.pkl')
                    # Model Testing
            x = np.array([[float(bp),float(sg),float(al),float(su),float(rbc),float(bu),float(sc),float(sod),float(pot),float(hemo),
                                float(wbcc),float(rbcc),float(htn)]])
            x = x.reshape(1,-1)
            p = model.predict(x)
            if p[0]==1:
                st.error("You're Chronic Disease is identified, kindly take rest and get good treatment.")
                        
            else:
                st.success("You are Perfectly Alright")
            

# Function to create a SQLite connection
def create_connection():
    conn = sqlite3.connect('users.db')
    return conn

# Function to create a table in the database
def create_table(conn):
    sql_create_table = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    );
    """
    try:
        c = conn.cursor()
        c.execute(sql_create_table)
    except sqlite3.Error as e:
        st.error(f"Error creating table: {e}")

# Function to check if a username already exists
def username_exists(username):
    conn = create_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    result = c.fetchone()
    conn.close()
    return result is not None

# Function to register a new user
def register_user(username, password):
    conn = create_connection()
    c = conn.cursor()
    hashed_password = pbkdf2_sha256.hash(password)
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
    conn.commit()
    conn.close()

# Function to authenticate a user
def authenticate_user(username, password):
    conn = create_connection()
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE username=?", (username,))
    result = c.fetchone()
    conn.close()
    if result:
        return pbkdf2_sha256.verify(password, result[0])
    return False

# Create the database connection and table
conn = create_connection()
create_table(conn)
conn.close()

# Streamlit UI
st.title("Kidney Chronic Disease Identifier")


tab1, tab2, tab3 = st.tabs(["Sign-Up", "Log-In", "Identifier"])

l=['.']

with tab2:
    st.subheader("Login")
    st.markdown("If you Don't have the account, kindly Sign-Up")
    username,password = '','' 
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        with st.spinner('Loading...'):
            time.sleep(1)
        st.success('Done!')
        if authenticate_user(username, password):
            st.success("Logged in successfully! Go to identifier Tab")
            l.append('+')
            
        else:
            st.error("Invalid username or password.")
    

with tab1:
    import streamlit as st1
    st.subheader("Sign-Up")
    st.markdown("If you Already have the account, kindly Log-in")
    st.subheader("Create an Account")
    new_username = st.text_area("Username")
    new_password = st.text_area("Password")
    if st.button("Sign-up"):
        if len(new_password)<8:
            st.warning("password must be of lenghth 8, kindly change it...")
        else:
            with st.spinner('Wait for it...'):
                time.sleep(1)
            st.success('Done!')
            if username_exists(new_username):
                st.error("Username already exists.")
            else:
                register_user(new_username, new_password)
                st.success("Account created successfully. Please log in.")
                
with tab3:
    st.caption("you have sucessfully entered.")
    result()                 
    # except Exception:
       # st.error("check the values again")

