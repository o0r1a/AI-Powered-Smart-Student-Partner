# import matplotlib.pyplot as plt
# import io
# import base64
#
# def generate_progress_chart(progress_data):
#     fig, ax = plt.subplots()
#     topics = list(progress_data.keys())
#     scores = list(progress_data.values())
#
#     ax.bar(topics, scores, color='skyblue')
#     ax.set_title('Progress Overview')
#     ax.set_ylabel('Score')
#     ax.set_xlabel('Topics')
#
#     # Save chart to a base64 image
#     buffer = io.BytesIO()
#     plt.savefig(buffer, format='png')
#     buffer.seek(0)
#     image = base64.b64encode(buffer.getvalue()).decode('utf-8')
#     buffer.close()
#     return image
import matplotlib.pyplot as plt
import io
import base64
from flask import Flask, render_template

app = Flask(__name__)

# Simulate user progress data
progress_data = {
    'Math': 80,
    'Science': 90,
    'History': 75,
    'English': 85
}

def generate_progress_chart(progress_data):
    # Create a plot
    fig, ax = plt.subplots()
    topics = list(progress_data.keys())
    scores = list(progress_data.values())

    # Create a bar chart
    ax.bar(topics, scores, color='skyblue')
    ax.set_title('Progress Overview')
    ax.set_ylabel('Score')
    ax.set_xlabel('Topics')

    # Save chart to a base64 image
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()

    return image

@app.route('/')
def index():
    # Generate chart and pass it to the template
    img_b64 = generate_progress_chart(progress_data)
    return render_template('index.html', img_b64=img_b64)

if __name__ == '__main__':
    app.run(debug=True)

