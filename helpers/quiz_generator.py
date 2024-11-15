import random

def generate_quiz(text):
    words = text.split()
    quiz = []
    for i in range(min(5, len(words))):
        word = random.choice(words)
        quiz.append({'question': f"What is the meaning of '{word}'?", 'answer': word})
    return quiz

def find_external_sources(topic):
    # Mock example; integrate with APIs like Google or Bing
    return [
        {"title": "External Resource 1", "url": "http://example.com/resource1"},
        {"title": "External Resource 2", "url": "http://example.com/resource2"}
    ]
