from app import app, db  # Import your Flask application and your SQLAlchemy db object

def setup_database():
	"""Create database tables."""
	with app.app_context():
		db.create_all()

if __name__ == '__main__':
	setup_database()  # Make sure to call this within the application context
	app.run(debug=True, port=8080)
