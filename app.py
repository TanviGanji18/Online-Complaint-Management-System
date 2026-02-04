import streamlit as st
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="complaint_db"
    )

def submit_complaint(name, email, category, description):
    con = get_connection()
    cur = con.cursor()
    cur.execute(
        "INSERT INTO complaints (name, email, category, description) VALUES (%s,%s,%s,%s)",
        (name, email, category, description)
    )
    con.commit()
    cid = cur.lastrowid
    con.close()
    return cid

st.title("📢 Online Complaint Management System")

name = st.text_input("Name")
email = st.text_input("Email")
category = st.selectbox("Category", ["Internet", "Electricity", "Water", "Other"])
description = st.text_area("Complaint Description")

if st.button("Submit Complaint"):
    if name == "" or email == "" or description == "":
        st.error("All fields are required")
    else:
        cid = submit_complaint(name, email, category, description)
        st.success(f"Complaint submitted successfully! Complaint ID: {cid}")
