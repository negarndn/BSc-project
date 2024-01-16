from flask import Flask, render_template, request

from RelationPrediction import RP
from request import request2

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_sentence', methods=['POST'])
def process_sentence():
    sentence = request.form['sentence']
    # Call your Python code with the input sentence
    # Replace the following line with your actual code to get Sparql response
    sparql_response = request2(sentence)
    return render_template('index.html', sentence=sentence, sparql_response=sparql_response)

if __name__ == '__main__':
    app.run(debug=True)
