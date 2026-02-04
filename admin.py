import streamlit as st
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="complaint_db"
    )

st.title("🛠 Admin Dashboard")

menu = st.sidebar.selectbox(
    "Admin Menu",
    ["View Complaints", "Search Complaint", "Update Status"]
)

if menu == "View Complaints":
    con = get_connection()
    cur = con.cursor(dictionary=True)
    cur.execute("SELECT * FROM complaints")
    data = cur.fetchall()
    con.close()

    for d in data:
        with st.expander(f"Complaint ID: {d['id']}"):
            st.write(d)

elif menu == "Search Complaint":
    cid = st.text_input("Enter Complaint ID")
    if st.button("Search"):
        con = get_connection()
        cur = con.cursor(dictionary=True)
        cur.execute("SELECT * FROM complaints WHERE id=%s", (cid,))
        d = cur.fetchone()
        con.close()

        if d:
            st.success("Complaint Found")
            st.write(d)
        else:
            st.error("Complaint Not Found")

elif menu == "Update Status":
    cid = st.text_input("Complaint ID")
    status = st.selectbox("Update Status", ["Open", "In Progress", "Closed"])

    if st.button("Update"):
        con = get_connection()
        cur = con.cursor()
        cur.execute(
            "UPDATE complaints SET status=%s WHERE id=%s",
            (status, cid)
        )
        con.commit()
        con.close()
        st.success("Status Updated Successfully")
