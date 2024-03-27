from app import app, db
from flask import request, jsonify, render_template
from app.models import User, Question, Image, Theme, Answer
from flask import render_template
from sqlalchemy.sql.expression import func
import subprocess
import shlex, os

# Home Page
@app.route('/')
def home():
	return render_template('home.html')

# Create User
@app.route('/user', methods=['POST'])
def create_user():
	data = request.get_json()
	username = data.get('username')
	if username is None or username == '':
		return jsonify({'message': 'Username is required'}), 400
	user = User(username=username)
	db.session.add(user)
	db.session.commit()
	return jsonify({'message': f'User {username} created successfully'}), 201

# Submit Question
@app.route('/submit-question', methods=['GET'])
def display_submit_question():
	# Select a random theme
	random_theme = Theme.query.order_by(func.random()).first()
	# Fetch 5 images associated with the theme
	images = Image.query.filter_by(theme_id=random_theme.id).limit(5).all()
	return render_template('submit_question.html', images=images, theme=random_theme)



@app.route('/generate', methods=['POST'])
def generate_image():
	# print the flag to check if the function is called
	print("generate_image called")
	# Retrieve the prompt from the request
	prompt = request.json.get('prompt')

	print("Prompt:", prompt)
	# Activate the 'ssh-env' Conda environment
	# TODO: Replace with the path to conda executable

	# Activate the 'ssh-env' Conda environment
	conda_activate_command = 'source /opt/homebrew/anaconda3/bin/activate ssh-env'

	# Construct the command to activate the Conda environment and execute the Python script
	conda_activate_command = 'source /opt/homebrew/anaconda3/bin/activate ssh-env && python3 generate_image.py ' + shlex.quote(prompt)

	# Execute the command
	try:
		result = subprocess.run(conda_activate_command, shell=True, capture_output=True, text=True)
		output = result.stdout
		error = result.stderr
		print("Script output:", output)

		if error:
			print("Script error:", error)
			return jsonify({'error': error}), 500

		# Get the list of generated image files
		base_dir = os.path.dirname(os.path.abspath(__file__))
		image_dir = os.path.join(base_dir, 'static', 'generated', 'samples')
		image_files = [f for f in os.listdir(image_dir) if f.endswith('.png')]

		# Sort the image files based on their filenames (assuming they are numbered)
		sorted_images = sorted(image_files, key=lambda x: int(x.split('.')[0]))

		# Get only the four largest-numbered images
		largest_images = sorted_images[-4:]

		# Construct URLs for the largest images
		image_urls = [f'/static/generated/samples/{filename}' for filename in largest_images]

		print("Image URLs:", image_urls)
		# Return response with output, error, and list of generated images
		return jsonify({'output': output, 'error': error, 'images': image_urls}), 200

	except Exception as e:
			print("Error executing script:", e)
			# Handle error response
			return jsonify({'error': str(e)}), 500

'''
@app.route('/question', methods=['POST'])
def submit_question():
	data = request.get_json()
	content = data.get('content')
	creator_id = data.get('creator_id')
	theme_id = data.get('theme_id')
	if not content or not creator_id or not theme_id:
		return jsonify({'message': 'Missing data'}), 400
	question = Question(content=content, creator_id=creator_id, theme_id=theme_id)
	db.session.add(question)
	db.session.commit()
	return jsonify({'message': 'Question submitted successfully'}), 201
'''

# Answer Question
@app.route('/question/<int:question_id>/answer', methods=['POST'])
def answer_question(question_id):
	question = Question.query.get_or_404(question_id)
	data = request.get_json()
	user_id = data.get('user_id')
	content = data.get('content')
	is_correct = data.get('is_correct', False)  # This needs a method to evaluate correctness
	answer = Answer(content=content, user_id=user_id, question_id=question.id, is_correct=is_correct)
	db.session.add(answer)
	db.session.commit()
	return jsonify({'message': 'Answer submitted successfully'}), 201

# List Questions
@app.route('/questions', methods=['GET'])
def list_questions():
	questions = Question.query.all()
	questions_data = [{'id': q.id, 'content': q.content} for q in questions]
	return jsonify(questions_data)

@app.route('/guesser')
def guesser():
	questions = Question.query.all()  # Simplified; you might want to add filters or ordering
	question_cards = []
	for question in questions:
		# Simplify: Classify difficulty based on a placeholder function
		difficulty = classify_difficulty(question)
		# Placeholder for fetching one image; adjust based on your model relationships
		image_url = question.images[0].image_path if question.images else None
		question_cards.append({
			'username': question.creator.username,  # Adjust based on your User model
			'difficulty': difficulty,
			'image_url': image_url
		})
	return render_template('guesser.html', question_cards=question_cards)

def classify_difficulty(question):
	# Placeholder for your logic to determine question difficulty
	return "medium"