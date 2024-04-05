from app import app, db
from flask import request, jsonify, render_template
from app.models import User, Question, Image, Theme, Answer, Post
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

@app.route('/save', methods=['POST'])
def save_question():
	data = request.get_json()
	prompt = data['prompt']
	image_path = data['image']
	creator_name = data['creator']
	theme_id = data['theme_id']
	content = data['content']

	creator = User.query.filter_by(username=creator_name).first()
	if not creator:
		creator = User(username=creator_name)
		db.session.add(creator)
		db.session.flush()

	insert_into_database(prompt, content, image_path, creator.id, theme_id)

	return jsonify({'message': 'Question saved successfully'}), 200


def insert_into_database(prompt, content, image_path, creator_id, theme_id=1):
    # Create a new Image object
    new_image = Image(image_path=image_path, is_generated=True)

    # Add the new image to the session
    db.session.add(new_image)
    db.session.flush()  # This is needed to generate the id for new_image

    # Create a new Question object with the id of the new image
    new_question = Question(content=content, prompt = prompt, generated_image_id=new_image.id, creator_id=creator_id, theme_id=theme_id)

    # Add the new question to the session
    db.session.add(new_question)

    # Commit the session to save the new image and question in the database
    db.session.commit()

# Answer Question

# List Questions
@app.route('/questions', methods=['GET'])
def list_questions():
    questions = Question.query.all()
    questions_data = [
        {
            'id': q.id,
            'prompt': q.prompt,
            'content': q.content,
            'theme_id': q.theme_id,
            'creator_id': q.creator_id,
            'create_time': q.create_time,
            'generated_image_id': q.generated_image_id
        }
        for q in questions
    ]
    return jsonify(questions_data)

from sqlalchemy.sql.expression import func

@app.route('/guesser')
def guesser():
    # Randomly select 4 questions
    questions = Question.query.order_by(func.random()).limit(4).all()
    question_cards = []
    for question in questions:
        # Simplify: Classify difficulty based on a placeholder function
        difficulty = question.difficulty
        # Fetch the image related to the question
        image = Image.query.get(question.generated_image_id)
        image_url = image.image_path if image else None
        question_cards.append({
			'id': question.id,
            'username': question.creator.username,  # Adjust based on your User model
            'difficulty': difficulty,
            'image_url': image_url
        })
    return render_template('guesser.html', question_cards=question_cards)


# def classify_difficulty(question):
# 	# Placeholder for your logic to determine question difficulty
# 	return "New"



# @app.route('/get_question_by_difficulty', methods=['POST'])
# def get_question_by_difficulty():
#     data = request.get_json()
#     difficulty = data.get('difficulty')
#
#     # Query the database for a question with the specified difficulty level
#     question = Question.query.filter_by(difficulty=difficulty).order_by(func.random()).first()
#
#     if question is None:
#         return jsonify({'message': 'No question found for the specified difficulty level'}), 404
#
#     # Return the question in the response
#     question_data = {
#         'id': question.id,
#         'content': question.content,
#         'difficulty': question.difficulty,
#         'theme_id': question.theme_id,
#         'creator_id': question.creator_id
#     }
#     return jsonify(question_data)



@app.route('/question/<int:question_id>/answer', methods=['POST'])
def answer_question(question_id):
    question = Question.query.get_or_404(question_id)
    data = request.get_json()
    user_id = data.get('user_id')
    content = data.get('content')
    is_correct = data.get('is_correct', False)  # This needs a method to evaluate correctness
    answer = Answer(content=content, user_id=user_id, question_id=question.id, is_correct=is_correct)
    db.session.add(answer)

    # Calculate the new difficulty level
    n_selected = Answer.query.filter_by(question_id=question.id, is_correct=True).count()
    n_appear = Answer.query.filter_by(question_id=question.id).count()
    ratio = n_selected / n_appear if n_appear > 0 else 0

    if ratio < 0.2:
        difficulty = 'Hard'
    elif ratio < 0.3:
        difficulty = 'Medium'
    else:
        difficulty = 'Easy'

    # Update the question's difficulty level
    question.difficulty = difficulty

    db.session.commit()
    return jsonify({'message': 'Answer submitted successfully'}), 201

@app.route('/get_question_by_difficulty', methods=['POST'])
def get_question_by_difficulty():
    data = request.get_json()
    # print the difficulty level
    print("Difficulty level:", data.get('difficulty'))
    difficulty = data.get('difficulty')

    # Query the database for a question with the specified difficulty level
    question = Question.query.filter_by(difficulty=difficulty).order_by(func.random()).first()

    if question is None:
        return jsonify({'message': 'No question found for the specified difficulty level'}), 404

    # Return the question in the response
    question_data = {
        'id': question.id,
        'content': question.content,
        'difficulty': question.difficulty,
        'theme_id': question.theme_id,
        'creator_id': question.creator_id
    }
    return jsonify(question_data)



@app.route('/get_post_by_theme', methods=['POST'])
def get_post_by_theme():
    data = request.get_json()
    theme = data.get('theme')

    # Query the database for a post with the specified theme
    post = Post.query.filter_by(theme_id=theme).order_by(func.random()).first()

    if post is None:
        return jsonify({'message': 'No post found for the specified theme'}), 404

    # Return the post in the response
    post_data = {
        'id': post.id,
        'content': post.content,
        'theme_id': post.theme_id,
        'image_id': post.image_id
    }
    return jsonify(post_data)


@app.route('/post')
def post_page():
    # Randomly select a post
    post = Post.query.order_by(func.random()).first()
    post_image = Image.query.get(post.image_id)
    post_data = {
        'id': post.id,
        'content': post.content,
        'theme_id': post.theme_id,
        'image_path': post_image.image_path
    }

    # Randomly select a question
    question = Question.query.order_by(func.random()).first()
    question_image = Image.query.get(question.generated_image_id)
    question_data = {
        'id': question.id,
        'content': question.content,
        'difficulty': question.difficulty,
        'theme_id': question.theme_id,
        'creator_id': question.creator_id,
        'image_path': question_image.image_path
    }

    # Render the post page with the selected post and question
    return render_template('post.html', post=post_data, question=question_data)
