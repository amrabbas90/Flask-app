from flask import Flask, jsonify, request

CRapp = Flask(__name__)

TOKEN = 'hiring'

# Define a task list
tasks = [
    {
        'id': 1,
        'question': 'We have fair coin. What is the probability that all first 5 tosses are heads?',
        'correct_answer': 0.03125
    },
    {
    
        'id': 2,
        'question': 'We have fair coin. We tossed it 5 times and got following sequence: HTTHH. What is the probability that 6th toss will be H?',
        'correct_answer': 0.5
    },
    {
        'id': 3,
        'question': 'Two cards are drawn from a deck of 52 cards. Find the probability that they are both kings if the first card is REPLACED. Round to the third decimal place.',
        'correct_answer': 0.006
    },
    {
        'id': 4,
        'question': 'Two cards are drawn from a deck of 52 cards. Find the probability that they are both kings if the first card is NOT REPLACED. Round to the third decimal place.',
        'correct_answer': 0.005
    },
    {
        'id': 5,
        'question': 'We have dice. We roll it 100 times. What is the probability that out from 100 rollings a six will show up exactly 15 times? Round to the first decimal place.',
        'correct_answer': 0.1
    },
    {
        'id': 6,
        'question': 'For Careem there are 3 car providers: A, B, C. Provider A has 2000 cars, provider B has 3000 cars, provider C has 5000 cars. On average we know that 95% of cars A are not broken, for B 80% of cars are not broken, for C 90% of cars are not broken. One random car was chosen and it appeared that it was broken. Find the probability that the manufacturer was B.',
        'correct_answer': 0.5
    }
]

# Define a list to store submitted answers
answers = []

@CRapp.route('/describe', methods=['GET'])
def describe():
    return jsonify({
        'message': 'You have now 6 tasks. Send the answers to the /send_answers endpoint using the POST method with JSON in the request body. An example of the JSON format can be found at the following link: https://pastebin.com/TBGs4pRm'
    })

@CRapp.route('/get_task', methods=['GET'])
def get_task():
    # Check if the user is authorized to access the endpoint
    if request.headers.get('Authorization') != TOKEN:
        return jsonify({'message': 'Unauthorized access.'}), 401
    
    # Select a random task from the task list
    task = tasks.pop(0)

    # Return the task as JSON
    return jsonify({
        'id': task['id'],
        'question': task['question']
    })

@CRapp.route('/send_answers', methods=['POST'])
def send_answers():
    # Check if the user is authorized to access the endpoint
    if request.headers.get('Authorization') != TOKEN:
        return jsonify({'message': 'Unauthorized access.'}), 401
    
    # Get the user's answers from the request body
    user_answers = request.json

    # Check if the user has answered all tasks
    if len(user_answers) != len(tasks):
        return jsonify({'message': 'Please answer all tasks.'}), 400
    
    # Calculate the user's score
    score = 0
    for i, answer in enumerate(user_answers):
        if answer['answer'] == tasks[i]['correct_answer']:
            score += 1

    # Add the user's answers to the answers list
    answers.append(user_answers)

    # Return the user's score as JSON
    return jsonify({
        'message': 'Your score is {} out of {}.'.format(score, len(tasks))
    })

if __name__ == '__main__':
    CRapp.run(debug=True,host='0.0.0.0')