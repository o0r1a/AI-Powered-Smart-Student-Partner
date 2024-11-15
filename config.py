from flask import Flask, render_template, request, redirect, url_for
import os
import PyPDF2
import matplotlib.pyplot as plt
import io
import base64
import mysql.connector

# Initialize the Flask app
app = Flask(__name__)

# MySQL Database connection configuration
DATABASE_CONFIG = {
    'user': 'root',  # Replace with your MySQL username
    'password': 'password',  # Replace with your MySQL password
    'host': 'localhost',  # 'localhost' for local MySQL server
    'database': 'your_database',  # Replace with your MySQL database name
    'raise_on_warnings': True
}


# Function to get a connection to the MySQL database
def get_db_connection():
    conn = mysql.connector.connect(**DATABASE_CONFIG)
    return conn


# Ensure the upload directory exists
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text


# Function to log user progress (adjust this to your actual table structure)
def log_progress(user_id, topic_id, quiz_id, goal_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO user_progress (user_id, topic_id, quiz_id, goal_id)
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (user_id, topic_id, quiz_id, goal_id))
    conn.commit()
    conn.close()


# Function to fetch and return user progress data
def fetch_progress(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(DISTINCT topic_id) FROM user_progress WHERE user_id = %s", (user_id,))
    completed_topics = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(DISTINCT quiz_id) FROM user_progress WHERE user_id = %s", (user_id,))
    completed_quizzes = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(DISTINCT goal_id) FROM user_progress WHERE user_id = %s", (user_id,))
    completed_goals = cursor.fetchone()[0]

    conn.close()
    return completed_topics, completed_quizzes, completed_goals


# Function to generate the progress chart as a base64 image
def generate_progress_chart(user_id):
    completed_topics, completed_quizzes, completed_goals = fetch_progress(user_id)

    labels = ['Completed Topics', 'Completed Quizzes', 'Completed Goals']
    values = [completed_topics, completed_quizzes, completed_goals]

    # Create a bar chart
    fig, ax = plt.subplots()
    ax.bar(labels, values, color=['skyblue', 'orange', 'green'])
    ax.set_title(f'User {user_id} Progress Tracking')
    ax.set_ylabel('Number of Completed Activities')

    # Save the chart to a BytesIO object and convert it to base64 for embedding in HTML
    img_io = io.BytesIO()
    plt.savefig(img_io, format='png')
    img_io.seek(0)
    img_b64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
    plt.close(fig)

    return img_b64


# Route for the home page
@app.route('/')
def home():
    return render_template('homepage.html')


# Route for the upload page (where users can upload PDFs)
@app.route('/upload', methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        # Handle PDF file upload
        file = request.files['pdf_file']
        if file:
            pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(pdf_path)
            # Extract text from the uploaded PDF
            text = extract_text_from_pdf(pdf_path)
            return render_template('upload.html', text=text)  # Display extracted text
    return render_template('upload.html')


# Route for the progress page
@app.route('/progress/<int:user_id>')
def progress(user_id):
    completed_topics, completed_quizzes, completed_goals = fetch_progress(user_id)
    img_b64 = generate_progress_chart(user_id)
    return render_template('progress.html',
                           user_id=user_id,
                           completed_topics=completed_topics,
                           completed_quizzes=completed_quizzes,
                           completed_goals=completed_goals,
                           img_b64=img_b64)


if __name__ == "__main__":
    app.run(debug=True)
