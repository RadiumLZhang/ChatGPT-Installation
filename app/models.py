from datetime import datetime
from app import db
import json


class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	questions_created = db.relationship('Question', backref='creator', lazy=True)
	answers = db.relationship('Answer', backref='player', lazy=True)


class Image(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	image_path = db.Column(db.String(100), nullable=False)
	theme_id = db.Column(db.Integer, db.ForeignKey('theme.id'), nullable=True)
	is_generated = db.Column(db.Boolean, default=False, nullable=False)


class Theme(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), nullable=False)
	description = db.Column(db.String(200), nullable=True)
	_suggested_prompts = db.Column('suggested_prompts', db.String, nullable=True)  # Store as a JSON string

	@property
	def suggested_prompts(self):
		if self._suggested_prompts:
			return json.loads(self._suggested_prompts)
		else:
			return []

	@suggested_prompts.setter
	def suggested_prompts(self, value):
		if value:
			self._suggested_prompts = json.dumps(value)
		else:
			self._suggested_prompts = json.dumps([])

	images = db.relationship('Image', backref='theme', lazy=True)


class Question(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	theme_id = db.Column(db.Integer, db.ForeignKey('theme.id'), nullable=False)
	creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	create_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	#origin_image_ids = db.Column(db.String, nullable=False)  # Comma-separated image IDs
	generated_image_id = db.Column(db.Integer, db.ForeignKey('image.id'), nullable=True)

	question_image_link = db.Table('question_image_link',
	                               db.Column('question_id', db.Integer, db.ForeignKey('question.id'), primary_key=True),
	                               db.Column('image_id', db.Integer, db.ForeignKey('image.id'), primary_key=True)
	                               )
class Answer(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
	answer_text = db.Column(db.String(200), nullable=False)
	score = db.Column(db.Integer, nullable=False)
	player_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	create_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


