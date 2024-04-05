import csv
from app import db  # Adjust this import path to match where you initialize your SQLAlchemy db instance
from app.models import Theme, Image, Post  # Adjust this import path to your models
from flask import Flask
from config import Config  # Adjust if your configuration setup differs

def create_app():
	app = Flask(__name__, template_folder='app/templates')
	app.config.from_object(Config)
	db.init_app(app)
	with app.app_context():
		db.create_all()  # Create database tables for our models
	return app

def import_themes_from_csv(csv_path):
	app = create_app()
	with app.app_context():
		with open(csv_path, newline='') as csvfile:
			reader = csv.DictReader(csvfile)
			for row in reader:
				# Assuming 'suggested_prompts' is a string like "keyword1, keyword2"
				suggested_prompts = [word.strip() for word in row['suggested_prompts'].split(',')]
				theme = Theme(name=row['name'], description=row['description'], suggested_prompts=suggested_prompts)
				db.session.add(theme)
			db.session.commit()
def import_images_from_csv(csv_path):
	app = create_app()
	with app.app_context():
		with open(csv_path, newline='') as csvfile:
			reader = csv.DictReader(csvfile)
			for row in reader:
				image = Image(image_path=row['image_path'], theme_id=int(row['theme_id']), is_generated=row['is_generated'] == 'True')
				db.session.add(image)
			db.session.commit()


def import_posts_from_csv(csv_path):
	app = create_app()
	with app.app_context():
		with open(csv_path, newline='') as csvfile:
			reader = csv.DictReader(csvfile)
			for row in reader:
				image = Image(image_path=row['image_path'], theme_id=row['theme_id'], is_generated=False)
				db.session.add(image)
				db.session.flush()  # This is to get the id of the newly created Image object

				# Create the Post object
				post = Post(content=row['post_content'], theme_id=row['theme_id'], image_id=image.id)
				db.session.add(post)
			db.session.commit()

if __name__ == '__main__':
	print('Importing themes and images from CSV')
	import_themes_from_csv('data/themes.csv')
	#import_images_from_csv('data/images.csv')
	import_posts_from_csv('data/posts.csv')
