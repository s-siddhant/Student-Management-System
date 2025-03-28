import streamlit as st
import requests
import pandas as pd

# Configuration
FLASK_API_URL = "http://127.0.0.1:5000"  # Update if your Flask app runs on a different URL

# Helper functions
def get_all_students():
    response = requests.get(f"{FLASK_API_URL}/students")
    if response.status_code == 200:
        return response.json()
    return []

def get_student(student_id):
    response = requests.get(f"{FLASK_API_URL}/students/{student_id}")
    if response.status_code == 200:
        return response.json()
    return None

def create_student(data):
    response = requests.post(f"{FLASK_API_URL}/students", json=data)
    return response

def update_student(student_id, data):
    response = requests.put(f"{FLASK_API_URL}/students/{student_id}", json=data)
    return response

def delete_student(student_id):
    response = requests.delete(f"{FLASK_API_URL}/students/{student_id}")
    return response

# Streamlit UI
st.title("Student Management System")
st.write("A simple interface for managing student records")

# Navigation
menu = st.sidebar.selectbox("Menu", ["View All Students", "Add Student", "Edit Student", "Delete Student"])

if menu == "View All Students":
    st.header("All Students")
    students = get_all_students()
    if students:
        df = pd.DataFrame(students)
        st.dataframe(df)
    else:
        st.info("No students found in the database")

elif menu == "Add Student":
    st.header("Add New Student")
    with st.form("add_student"):
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        dob = st.date_input("Date of Birth")
        amount_due = st.number_input("Amount Due", min_value=0.0, step=0.01)
        
        submitted = st.form_submit_button("Add Student")
        if submitted:
            student_data = {
                "first_name": first_name,
                "last_name": last_name,
                "dob": str(dob),
                "amount_due": amount_due
            }
            response = create_student(student_data)
            if response.status_code == 201:
                st.success("Student added successfully!")
            else:
                st.error(f"Error adding student: {response.json().get('error', 'Unknown error')}")

elif menu == "Edit Student":
    st.header("Edit Student")
    students = get_all_students()
    if students:
        student_options = {f"{s['student_id']} - {s['first_name']} {s['last_name']}": s['student_id'] for s in students}
        selected_student = st.selectbox("Select Student", options=list(student_options.keys()))
        student_id = student_options[selected_student]
        
        student = get_student(student_id)
        if student:
            with st.form("edit_student"):
                first_name = st.text_input("First Name", value=student['first_name'])
                last_name = st.text_input("Last Name", value=student['last_name'])
                dob = st.date_input("Date of Birth", value=pd.to_datetime(student['dob']))
                amount_due = st.number_input("Amount Due", min_value=0.0, step=0.01, value=float(student['amount_due']))
                
                submitted = st.form_submit_button("Update Student")
                if submitted:
                    update_data = {
                        "first_name": first_name,
                        "last_name": last_name,
                        "dob": str(dob),
                        "amount_due": amount_due
                    }
                    response = update_student(student_id, update_data)
                    if response.status_code == 200:
                        st.success("Student updated successfully!")
                    else:
                        st.error(f"Error updating student: {response.json().get('error', 'Unknown error')}")
        else:
            st.error("Student not found")
    else:
        st.info("No students found in the database")

elif menu == "Delete Student":
    st.header("Delete Student")
    students = get_all_students()
    if students:
        student_options = {f"{s['student_id']} - {s['first_name']} {s['last_name']}": s['student_id'] for s in students}
        selected_student = st.selectbox("Select Student to Delete", options=list(student_options.keys()))
        student_id = student_options[selected_student]
        
        if st.button("Delete Student"):
            response = delete_student(student_id)
            if response.status_code == 200:
                st.success("Student deleted successfully!")
            else:
                st.error(f"Error deleting student: {response.json().get('error', 'Unknown error')}")
    else:
        st.info("No students found in the database")