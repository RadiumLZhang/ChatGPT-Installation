import csv
from app import db  # Adjust this import path to match where you initialize your SQLAlchemy db instance
from app.models import Theme, Image, Post, Question, User  # Adjust this import path to your models
from flask import Flask
from config import Config  # Adjust if your configuration setup differs
import os
import shutil



def create_app():
    app = Flask(__name__, template_folder='app/templates')
    app.config.from_object(Config)
    db.init_app(app)
    with app.app_context():
        db.create_all()  # Create database tables for our models
    return app


def import_themes_from_csv(csv_path):
    app = create_app()
    # clear all the Theme in the database Theme

    with app.app_context():
        db.session.query(Theme).delete()
        with open(csv_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Assuming 'suggested_prompts' is a string like "keyword1, keyword2"
                suggested_prompts = [word.strip() for word in row['suggested_prompts'].split(',')]
                theme = Theme(name=row['name'], description=row['description'], suggested_prompts=suggested_prompts)
                db.session.add(theme)
            db.session.commit()


# image_path	post_content
def import_fake_questions_from_csv(csv_path):
    app = create_app()

    with app.app_context():
        # find the user "Fool Your Friend" and set the theme_id to 1, if user not exist, create a new user
        user = User.query.filter_by(username='Fool Your Friend').first()
        if user is None:
            user = User(username='Fool Your Friend')
            db.session.add(user)
            db.session.commit()
        with open(csv_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Create new image
                # [1] if the image_path is not exist in the database, create a new image
                # [2] if the image_path is exist in the database, get the image_id, and renew the question with the image_id
                image = Image.query.filter_by(image_path=row['image_path']).first()
                if image is not None:
                    question = Question.query.filter_by(generated_image_id=image.id).first()
                    if question is not None:
                        # renew the question with the image_id
                        question.prompt = row['prompt']
                        question.content = row['post_content']
                        db.session.add(question)
                        continue

                # [3] if the image_path is not exist in the database, create a new image
                image = Image(image_path=row['image_path'], theme_id=1, is_generated=True)
                db.session.add(image)
                db.session.flush()

                question = Question(prompt=row['prompt'], content=row['post_content'], theme_id=1, creator_id=user.id,
                                    generated_image_id=image.id, difficulty='New')
                db.session.add(question)
            db.session.commit()


def import_posts_from_csv(csv_path):
    app = create_app()
    with app.app_context():
        with open(csv_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # [1] if the image_path is not exist in the database, create a new image
                # [2] if the image_path is exist in the database, get the image_id, and renew the question with the image_id
                image = Image.query.filter_by(image_path=row['image_path']).first()
                if image is not None:
                    post = Post.query.filter_by(image_id=image.id).first()
                    if post is not None:
                        # renew the post with the image_id
                        post.content = row['post_content']
                        db.session.add(post)
                        continue
                image = Image(image_path=row['image_path'], theme_id=row['theme_id'], is_generated=False)
                db.session.add(image)
                db.session.flush()  # This is to get the id of the newly created Image object

                # Create the Post object
                post = Post(content=row['post_content'], theme_id=row['theme_id'], image_id=image.id)
                db.session.add(post)
            db.session.commit()



PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_ROOT = os.path.join(PROJECT_ROOT, 'app')
STATIC_FOLDER = os.path.join(PROJECT_ROOT, 'app/static')
IMAGE_FOLDER = os.path.join(STATIC_FOLDER, 'images')
GENERATED_FOLDER = os.path.join(STATIC_FOLDER, 'generated')

def clean_nonused_images():
    app = create_app()
    with app.app_context():
        # go through all images in /static/images and /static/generated and check if they are used in the database
        # if not, delete them
        images = Image.query.all()
        used_image_paths = set()
        for image in images:
            used_image_paths.add(image.image_path)  # used_image_path is under static/xxx
        print("used_image_paths: ", used_image_paths)

        recursive_remove_unused_images(IMAGE_FOLDER, used_image_paths)
        recursive_remove_unused_images(GENERATED_FOLDER, used_image_paths)




def recursive_remove_unused_images(image_folder, used_image_paths):
    for image_path in os.listdir(image_folder):
        if os.path.isdir(os.path.join(image_folder, image_path)):
            recursive_remove_unused_images(os.path.join(image_folder, image_path), used_image_paths)
        else:
            # make sure the image_path is under STATIC_FOLDER
            full_image_path = os.path.join(image_folder, image_path)
            # convert the full_image_path to the relative path under STATIC_FOLDER
            relative_image_path = '/' + os.path.relpath(full_image_path, APP_ROOT)
            print("relative_image_path: ", relative_image_path)
            if image_path not in used_image_paths:
                os.remove(os.path.join(image_folder, image_path))
                print("remove image: ", image_path)



if __name__ == '__main__':
    # print('Importing themes and images from CSV')
    # import_themes_from_csv('data/themes.csv')
    # import_fake_questions_from_csv('data/fake_posts.csv')
    # import_posts_from_csv('data/posts.csv')
    clean_nonused_images()
