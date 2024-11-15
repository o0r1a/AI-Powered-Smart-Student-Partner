from flask import Flask, render_template, request, jsonify
from helpers.pdf_processor import process_pdf
from helpers.yt_processor import process_yt
from helpers.analytics import generate_progress_chart

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # File or YouTube link handling
        return render_template('results.html', notes="Notes here", quizzes="Quiz here")
    return render_template('upload.html')


@app.route('/progress/<int:user_id>')
def progress(user_id):
    # Example of user data (this would typically be retrieved from a database)
    completed_topics = 12  # Example value, replace with real data
    completed_quizzes = 8  # Example value
    completed_goals = 5  # Example value

    # Example progress data (topic progress as a dictionary)
    progress_data = {
        "Math": 80,
        "Science": 60,
        "History": 90,
        "Literature": 70,
    }

    # Generate the progress chart (base64-encoded)
    img_b64 = generate_progress_chart(progress_data)

    return render_template('progress.html',
                           completed_topics=completed_topics,
                           completed_quizzes=completed_quizzes,
                           completed_goals=completed_goals,
                           img_b64=img_b64)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/community')
def community():
    return render_template('community.html')

@app.route('/contactus', methods=['GET', 'POST'])
def contactus():
    if request.method == 'POST':
        # Handle form submission
        pass
    return render_template('contactus.html')

if __name__ == '__main__':
    app.run(debug=True)
