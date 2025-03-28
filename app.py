from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Initialize database
def init_db():
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            dob TEXT NOT NULL,
            amount_due REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Helper function for database operations
def db_query(query, args=(), one=False):
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute(query, args)
    conn.commit()
    result = cursor.fetchall()
    conn.close()
    return (result[0] if result else None) if one else result

# Create a new student
@app.route('/students', methods=['POST'])
def create_student():
    data = request.get_json()
    required_fields = ['first_name', 'last_name', 'dob', 'amount_due']
    
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        # Validate date format
        datetime.strptime(data['dob'], '%Y-%m-%d')
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    
    query = '''
        INSERT INTO students (first_name, last_name, dob, amount_due)
        VALUES (?, ?, ?, ?)
    '''
    args = (data['first_name'], data['last_name'], data['dob'], data['amount_due'])
    db_query(query, args)
    
    return jsonify({'message': 'Student created successfully'}), 201

# Get all students
@app.route('/students', methods=['GET'])
def get_all_students():
    students = db_query('SELECT * FROM students')
    result = []
    for student in students:
        result.append({
            'student_id': student[0],
            'first_name': student[1],
            'last_name': student[2],
            'dob': student[3],
            'amount_due': student[4]
        })
    return jsonify(result)

# Get a specific student
@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    student = db_query('SELECT * FROM students WHERE student_id = ?', (student_id,), one=True)
    if student:
        return jsonify({
            'student_id': student[0],
            'first_name': student[1],
            'last_name': student[2],
            'dob': student[3],
            'amount_due': student[4]
        })
    return jsonify({'error': 'Student not found'}), 404

# Update a student
@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    data = request.get_json()
    
    # Check if student exists
    if not db_query('SELECT 1 FROM students WHERE student_id = ?', (student_id,), one=True):
        return jsonify({'error': 'Student not found'}), 404
    
    # Build update query based on provided fields
    updates = []
    args = []
    
    if 'first_name' in data:
        updates.append('first_name = ?')
        args.append(data['first_name'])
    if 'last_name' in data:
        updates.append('last_name = ?')
        args.append(data['last_name'])
    if 'dob' in data:
        try:
            datetime.strptime(data['dob'], '%Y-%m-%d')
            updates.append('dob = ?')
            args.append(data['dob'])
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    if 'amount_due' in data:
        updates.append('amount_due = ?')
        args.append(data['amount_due'])
    
    if not updates:
        return jsonify({'error': 'No fields to update'}), 400
    
    args.append(student_id)
    query = f'UPDATE students SET {", ".join(updates)} WHERE student_id = ?'
    db_query(query, args)
    
    return jsonify({'message': 'Student updated successfully'})

# Delete a student
@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    # Check if student exists
    if not db_query('SELECT 1 FROM students WHERE student_id = ?', (student_id,), one=True):
        return jsonify({'error': 'Student not found'}), 404
    
    db_query('DELETE FROM students WHERE student_id = ?', (student_id,))
    return jsonify({'message': 'Student deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)