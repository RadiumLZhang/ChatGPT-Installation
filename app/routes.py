from app import app, db, prodia_config
from flask import request, jsonify, render_template
from app.models import User, Question, Image, Theme, Answer, Post
from flask import render_template
from sqlalchemy.sql.expression import func
import subprocess
import shlex, os
import requests


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
    print("generate_image called")
    prompt = request.json.get('prompt')
    print("prompt:", prompt)

    num_of_images = 4
    image_urls = []
    job_ids = []
    try:
        for _ in range(num_of_images):  # Generate 4 images
            for key in prodia_config.api_keys:

                #model = random.choice(prodia_config.sd_models)
                #model = prodia_config.sd_models[51]  # Realistic_Vision_V5.0.safetensors [614d1063]
                model = prodia_config.sd_models[3]  # redshift_diffusion-V10.safetensors [1400e684]
                payload = {
                    "model": model,
                    "style_preset": "cinematic",
                    "prompt": prompt
                }
                headers = {
                    "accept": "application/json",
                    "content-type": "application/json",
                    "X-Prodia-Key": key
                }

                url = prodia_config.model_urls["sd"]
                response = requests.post(url, json=payload, headers=headers)
                print(response.text)

                if response.status_code == 200:
                    # {'job': '2015bd00-ba88-41ca-8912-7d818cae3155', 'status': 'queued'}
                    if response.json().get('status') != 'succeeded':
                        job_id = response.json().get('job')
                        job_ids.append(job_id)
                    else :
                    # {
                    #   "job": "xxxx-xxxx-xxxx-xxxx",
                    #   "params": "{}",
                    #   "imageUrl": "string"
                    # }
                        image_url = response.json().get('imageUrl')
                        image_urls.append(image_url)
                    break  # Move to the next image generation
                elif response.status_code == 400:
                    return jsonify({'error': 'Invalid Generation Parameters'}), 400
                elif response.status_code == 401:
                    continue  # Try the next API key
                elif response.status_code == 402:
                    return jsonify({'error': 'API Access Not Enabled'}), 402

        # Process all job_ids until the list is empty
        while job_ids:
            print("Job IDs:", job_ids)
            for job_id in job_ids:
                url = f"https://api.prodia.com/v1/job/{job_id}"
                headers = {
                    "accept": "application/json",
                    "X-Prodia-Key": prodia_config.api_keys[0]  # Use the first API key for status check
                }

                response = requests.get(url, headers=headers)
                print(response.text)

                if response.status_code == 200:
                    if response.json().get('status') == 'succeeded':
                        image_url = response.json().get('imageUrl')
                        image_urls.append(image_url)
                        job_ids.remove(job_id)

        if len(image_urls) == num_of_images:
            print("All images generated successfully")
            print("Image URLs:", image_urls)
            return jsonify({'images': image_urls}), 200
        else:
            return jsonify({'error': 'All API keys exhausted, not all images generated successfully.'}), 500

    except Exception as e:
        print("Error executing script:", e)
        return jsonify({'error': str(e)}), 500



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

    local_image_path = '/' + save_image_locally(image_path)

    insert_into_database(prompt, content, local_image_path, creator.id, theme_id)

    return jsonify({'message': 'Question saved successfully'}), 200


def save_image_locally(image_url, save_dir='app/static/generated'):
    # Ensure the save directory exists
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Get the image content
    response = requests.get(image_url)
    if response.status_code == 200:
        # Extract the image name from the URL
        image_name = os.path.basename(image_url)
        local_path = os.path.join(save_dir, image_name)

        # Save the image to the local path
        with open(local_path, 'wb') as f:
            f.write(response.content)

        return local_path
    else:
        raise Exception(f"Failed to download image: {response.status_code}")


def insert_into_database(prompt, content, image_path, creator_id, theme_id=1):
    # Create a new Image object
    new_image = Image(image_path=image_path, is_generated=True)

    # Add the new image to the session
    db.session.add(new_image)
    db.session.flush()  # This is needed to generate the id for new_image

    # Create a new Question object with the id of the new image
    new_question = Question(content=content, prompt=prompt, generated_image_id=new_image.id, creator_id=creator_id,
                            theme_id=theme_id)

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
    # calculate the question difficulties
    return render_template('guesser.html', question_cards=None)

@app.route('/guesser_selection')
def guesser_selection():
    # Get the difficulty from the request parameters
    difficulty = request.args.get('difficulty')

    if difficulty is None:
        # If no difficulty was provided, return an error
        return jsonify({'message': 'Missing difficulty level'}), 400

    # Get the contents and fake index using the get_random_question_and_posts function
    contents, fake_index, question_id = get_random_question_and_posts(difficulty)

    print("Contents:", contents)
    print("Fake index:", fake_index)
    print("Question ID:", question_id)

    # Render the guesser_selection.html template and pass the difficulty level to it
    return render_template('guesser_selection.html', contents=contents, fake_index=fake_index, question_id=question_id)

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


import random
from sqlalchemy.sql.expression import func
from app.models import db, Question, Post


def get_random_question_and_posts(difficulty):
    # Get all questions with the selected difficulty
    questions = Question.query.filter_by(difficulty=difficulty).all()

    # if questions is less than 3, then random from all questions
    if len(questions) < 1:
        questions = Question.query.all()

    # Select a random question,
    # we would find the questions with the minimum number of num_appear
    # then random select the least answered question,
    # if there are multiple questions with the same number of answers then random select one
    min_num_appear = min([question.num_appear for question in questions])
    questions = [question for question in questions if question.num_appear == min_num_appear]

    question = random.choice(questions)


    # record the question id
    question_id = question.id

    # Get three random posts
    posts = Post.query.order_by(func.random()).limit(3).all()

    # Create a list with the contents of the question and posts
    contents = [question.content] + [post.content for post in posts]

    images = [question.generated_image_id] + [post.image_id for post in posts]

    # use image_ids in the images list to get the image_path
    images = [Image.query.get(image_id).image_path for image_id in images]

    # make pairs of content and image
    contents = list(zip(contents, images))

    # Randomize the order of the contents, and get the index of the question
    random.shuffle(contents)
    fake_index = contents.index((question.content, images[0]))

    return contents, fake_index, question_id


@app.route('/report_fake', methods=['POST'])
def report_fake():
    data = request.get_json()
    user_choice = data.get('user_choice')
    question_id = data.get('question_id')

    # Get the answers from the database for the specified question
    answers = Answer.query.filter_by(question_id=question_id).all()

    # Check if the user's choice matches the fake index
    is_correct = user_choice == 1

    # Create a new answer object for the user's choice
    answer_question(question_id, is_correct)

    # answer = Answer(question_id=question_id, is_correct=is_correct)
    # db.session.add(answer)
    # db.session.commit()

    # Get how many users have answered the question
    n_answers = Answer.query.filter_by(question_id=question_id).count()
    # Get how many users have answered correctly
    n_correct = Answer.query.filter_by(question_id=question_id, is_correct=True).count()
    # Calculate the percentage of correct answers
    percentage_correct = (n_correct / n_answers) * 100 if n_answers > 0 else 0
    # Tell the user if they were correct
    is_correct = user_choice == 1
    return jsonify({'is_correct': is_correct, 'percentage_correct': percentage_correct, 'n_answers': n_answers,
                    'n_correct': n_correct})




def answer_question(question_id, is_correct):
    answer = Answer(question_id=question_id, is_correct=is_correct)
    db.session.add(answer)
    db.session.commit()


@app.route('/ranking', methods=['GET'])
def ranking():
    # Query the database for all users
    users = User.query.all()

    # Initialize an empty list to store the user data
    user_data = []

    # Iterate over each user
    for user in users:
        # Get all questions created by the user
        questions = Question.query.filter_by(creator_id=user.id).all()

        # Initialize counters for the total number of answers and correct answers
        total_answers = 0
        correct_answers = 0

        # Iterate over each question
        for question in questions:
            # Get all answers for the question
            answers = Answer.query.filter_by(question_id=question.id).all()

            # Increment the total number of answers by the number of answers for the question
            total_answers += len(answers)

            # Get all correct answers for the question
            correct_answers += len([answer for answer in answers if answer.is_correct])

        # Calculate the difficulty of the questions created by the user
        difficulty = 100 * correct_answers / total_answers if total_answers > 0 else 0

        print("User:", user.username, "Difficulty:", difficulty)

        # Do rounding
        difficulty = round(difficulty, 2)

        # Append the user data to the list
        user_data.append({
            'username': user.username,
            'difficulty': difficulty
        })

    # Sort the user data by difficulty in descending order and get the top 5
    top_users = sorted(user_data, key=lambda x: x['difficulty'], reverse=True)[:5]
    print("Top users:", top_users)

    # Render the ranking.html template and pass the top users to it
    # pass the top users and their difficulty levels to the template
    return render_template('ranking.html', top_users=top_users)
