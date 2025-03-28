# Student-Management-System
A Flask RESTful API with Streamlit Frontend

A simple CRUD (Create, Read, Update, Delete) application for managing student records, built with:
  -  Backend: Flask (Python)
  -  Database: SQLite
  -  Frontend: Streamlit

## Features
  -  Create new student records
  -  Read all students or a single student
  -  Update existing student details
  -  Delete students
  -  User-friendly Streamlit UI

## Endpoints
  - `POST /students`: Create a new student
  - `GET /students`: Get all students
  - `GET /students/<student_id>`: Get a specific student
  - `PUT /students/<student_id>`: Update a student
  - `DELETE /students/<student_id>`: Delete a student

##  Streamlit UI Preview
  -  View All Students → Displays a table of all records.
  -  Add Student → Fill the form to add a new student.
  -  Edit Student → Select a student and modify details.
  -  Delete Student → Remove a student with confirmation.
