class Config:
	"""Base configuration class with common settings."""
	SECRET_KEY = 'change_this_to_a_random_secret_key'
	SQLALCHEMY_DATABASE_URI = 'sqlite:///chatgpt_installation.db'
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	# Common configurations that are shared across all environments

class DevelopmentConfig(Config):
	"""Development environment specific configuration."""
	DEBUG = True
	# Additional configurations for development environment

class TestingConfig(Config):
	"""Testing environment specific configuration."""
	TESTING = True
	SQLALCHEMY_DATABASE_URI = 'sqlite:///testing.db'
	# Additional configurations for testing environment

class ProductionConfig(Config):
	"""Production environment specific configuration."""
	DEBUG = False
	# Here, you might want to use a production database
	SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:password@hostname/chatgpt_installation'
	# Additional configurations for production environment
