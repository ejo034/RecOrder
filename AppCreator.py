from flask import Flask,request, render_template
from flask.ext.mysql import MySQL


class App:

	def __init__(self):
		self.app = Flask(__name__)
		self.mysql = MySQL()

		# mysql config
		self.app.config['MYSQL_DATABASE_USER'] = "root"
		self.app.config['MYSQL_DATABASE_PASSWORD'] = ""
		self.app.config['MYSQL_DATABASE_DB'] = "mastertestv2"
		self.app.config['MYSQL_DATABASE_HOST'] = "localhost"
		self.mysql.init_app(self.app)