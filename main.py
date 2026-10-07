import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt


# ---------- DATABASE SETUP ----------
conn = sqlite3.connect("customers.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT UNIQUE,
    phone TEXT,
    address TEXT,
    joined_date TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    product TEXT,
    amount REAL,
    order_date TEXT,
    FOREIGN KEY(customer_id) REFERENCES customers(id)
)
""")
conn.commit()


#--------- FUNCTION SETUP-----------

def add_cust(name,email,phone,address):
    c.execute("INSERT INTO customers (name,email,phone,address,joined_date) values (?, ?, ?, ?, ?)",
              (name, email, phone, address, datetime.now().strftime("%Y-%m-%d")))
    conn.commit()

def del_cust(customer_id):
    c.execute("DELETE FROM orders WHERE customer_id=?", (int(customer_id),))
    c.execute("DELETE FROM customers WHERE id=?", (int(customer_id),))
    conn.commit()

def view_cust():
    return pd.read_sql("select * from customers",conn)

def add_order(customer_id,product,amount):
    c.execute("INSERT INTO orders (customer_id,product,amount,order_date) values (?, ?, ?, ?)",
              (customer_id, product, amount, datetime.now().strftime("%Y-%m-%d")))
    conn.commit()

def view_orders():
    return pd.read_sql("SELECT o.order_id, c.name, o.product, o.amount, o.order_date \
                        FROM orders o JOIN customers c ON o.customer_id=c.id", conn)

#----------STREAMLIT UI------------
st.set_page_config(page_title="CUSTOMER MANAGEMENT SYSTEM",page_icon="https://cdn-icons-png.flaticon.com/512/1478/1478890.png",layout="wide")
st.title("CUSTOMER MANAGEMENT SYSTEM")
st.image("https://cdn-icons-png.flaticon.com/512/10397/10397542.png")

menu = ["ADD CUSTOMER","VIEW CUSTOMER","ADD ORDER","VIEW ORDERS","REPORTS"]
choice=st.sidebar.selectbox("MENU", menu)

if choice == "ADD CUSTOMER":
    st.subheader("Add Customer")
    name = st.text_input("Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone")
    address = st.text_input("Address")
    if st.button("Save Customer Profile"):
        add_cust(name,email,phone,address)
        st.success(f"Customer {name} added succesfully!")

elif choice == "VIEW CUSTOMER":
    st.subheader("All Customer")
    df = view_cust()
    st.dataframe(df)
    if not df.empty:
        delete_id = st.selectbox("Select Customer ID to Delete", df["id"])
        if st.button("Delete Customer"):
            del_cust(delete_id)
            st.warning("Customer deleted!")

elif choice == "ADD ORDER":
    st.subheader("Add New Order")
    customers = view_cust()
    if not customers.empty:
        customer_id = st.selectbox("select customer", customers["id"].astype(str) + " - " + customers["name"].astype(str))
        product = st.text_input("Product")
        amount = st.number_input("Amount", min_value=0.0, step=100.0)
        if st.button("Save Order"):
            add_order(int(customer_id.split(" - ")[0]), product, amount)
            st.success("Order added successfully!")
    else:
        st.warning("No customers available. Please add customers first.")

elif choice == "VIEW ORDERS":
    st.subheader("All Orders")
    df =  view_orders()
    st.dataframe(df)

elif choice == "REPORTS":
    st.subheader("Reports & Analytics")
    cust_count = pd.read_sql("SELECT COUNT(*) as total_customers FROM customers", conn)["total_customers"][0]
    order_count = pd.read_sql("SELECT COUNT(*) as total_orders FROM orders", conn)["total_orders"][0]
    revenue = pd.read_sql("SELECT SUM(amount) as total_revenue FROM orders", conn)["total_revenue"][0]

    st.metric("Total Customers", cust_count)
    st.metric("Total Orders", order_count)
    st.metric("Total Revenue", revenue if revenue else 0)


    #------------Pir Chart---------------
    st.subheader("Order Distribution (Pie Chart)")
    orders_data = pd.read_sql("SELECT c.name, COUNT(o.order_id) as total_orders \
                               FROM orders o JOIN customers c ON o.customer_id=c.id \
                               GROUP BY c.name", conn)



    if not orders_data.empty:
        fig1, ax1 = plt.subplots()
        ax1.pie(orders_data["total_orders"], labels=orders_data["name"], autopct="%1.1f%%", startangle=90)
        ax1.axis("equal")  
        st.pyplot(fig1)
    else:
        st.info("No orders available to display pie chart.")

    #------------Bar chart-------------------------
    st.subheader("Revenue per customer (Bar chart)")
    revenue_data = pd.read_sql("SELECT c.name, SUM(o.amount) as total_revenue \
                                FROM orders o JOIN customers c ON o.customer_id=c.id \
                                GROUP BY c.name", conn)
    
    if not revenue_data.empty:
        fig2, ax2 = plt.subplots()
        ax2.bar(revenue_data["name"], revenue_data["total_revenue"], color="skyblue")
        ax2.set_xlabel("Customer")
        ax2.set_ylabel("Revenue")
        ax2.set_title("Revenue per Customer")
        plt.xticks(rotation=30, ha="right")
        st.pyplot(fig2)
    else:
        st.info("No revenue data available to display bar chart.")
    
