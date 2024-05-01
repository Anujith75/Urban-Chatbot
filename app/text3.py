import streamlit as st
import psycopg2
import time
# Function to connect to the database
def connect_db():
    try:
        conn = psycopg2.connect(database="postgres", user="postgres.cidsbhqdqcupmmfgovdb",
                                password="brainalyst@123", host="aws-0-ap-south-1.pooler.supabase.com", port="5432")
        cursor = conn.cursor()
        st.success("Welcome")
        return conn, cursor
    except Exception as error:
        st.error("Unable to connect to DB")
        return None, None

# Function to login
def login(username: str, password: str, cursor):
    cursor.execute("SELECT id FROM customers WHERE username = %s AND password = %s", (username, password))
    user_id = cursor.fetchone()
    if not user_id:
        st.error("Wrong username or password")
    else:
        st.success("Login Successful")
        time.sleep(2)  # Consider using a loading indicator instead of sleep for a better UX
        return user_id[0]  # Return the actual user ID

# Function to display property details
def display_property_details(user_id, cursor):
    cursor.execute("SELECT * FROM properties WHERE customer_id = %s", (user_id,))
    properties = cursor.fetchall()
    if not properties:
        st.info("No properties found for this user.")
    else:
        for i in properties:
            st.write(f"Name: {i[1]}")
            st.write(f"Address: {i[2]}, {i[3]}, {i[4]}")
            st.write("")

# Function to add property (placeholders for input widgets)
def add_property(user_id, cursor, conn):
    # Replace placeholders with actual input widgets (text boxes, dropdowns, etc.)
    name = st.text_input("Property Name")
    street = st.text_input("Street")
    district = st.text_input("District")
    state = st.text_input("State")

    cursor.execute("INSERT INTO properties (property_name, street, district, state, customer_id) VALUES (%s,%s,%s,%s,%s) RETURNING property_id",
                   (name, street, district, state, user_id))
    property_id = cursor.fetchone()[0]
    conn.commit()
    st.success(f"Property added successfully with ID: {property_id}")

# Function to update property (placeholders for input widgets)
def update_property(property_id, cursor, conn):
    # Replace placeholders with actual input widgets (text boxes, dropdowns, etc.)
    name = st.text_input("Property Name")
    street = st.text_input("Street")
    district = st.text_input("District")
    state = st.text_input("State")

    cursor.execute("UPDATE properties SET property_name = %s, street = %s, district = %s, state = %s WHERE property_id = %s",
                   (name, street, district, state, property_id))
    conn.commit()
    st.success("Property updated successfully")

# Streamlit UI
def main():
    st.title("Property Management System")

    # Database connection
    conn, cursor = connect_db()

    # Login Section
    st.sidebar.subheader("Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    login_button = st.sidebar.button("Login")

    if login_button:
        user_id = login(username, password, cursor)
        if user_id:
            st.sidebar.session_state.logged_in = True

    # Property Management Section (visible only if logged in)
            if st.session_state.get("logged_in", True):
                st.subheader("Property Management")
            option = st.radio("Choose an option:", ["Property Details", "Add Property", "Update Property"])
            if st.session_state.get("logged_in", True):
                if option == "Property Details":
                    st.subheader("Property Details")
                    if user_id:  # Use the captured user_id from the login function
                        cursor.execute("SELECT * FROM properties WHERE customer_id = %s",(user_id,))
                        properties = cursor.fetchall()
                        if not properties:
                            st.info("No properties found for this user.")
                        else:
                            for i in properties:
                                st.write(f"Name: {i[1]}")
                                st.write(f"Address: {i[2]}, {i[3]}, {i[4]}")
                                st.write("")
                elif option == "Add Property":
                    
                    st.subheader("Input Property Details")
                    name = st.text_input("Property Name",default_value="NA", key=None, type="default")
                    street = st.text_input("Street",default_value="NA", key=None, type="default")
                    district = st.text_input("District",default_value="NA", key=None, type="default")
                    state = st.text_input("State",default_value="NA", key=None, type="default")

                    cursor.execute("INSERT INTO properties (property_name, street, district, state, customer_id) VALUES (%s,%s,%s,%s,%s) RETURNING property_id",(name, street, district, state, user_id))
                    property_id = cursor.fetchone()[0]
                    conn.commit()
                    st.success(f"Property added successfully with ID: {property_id}")                
            
if __name__ == "__main__":
    main()
