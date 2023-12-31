from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_wtf import FlaskForm # file upload
from wtforms import FileField, SubmitField, IntegerField # file upload
from werkzeug.utils import secure_filename # file upload
from wtforms.validators import InputRequired # file upload
import os
from model_logic import local_tokens # LLM stuff
from langchain.llms import OpenAI # LLM stuff
from langchain import PromptTemplate # LLM stuff
import time # LLM stuff


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' # /// relative path, //// absolute path
db = SQLAlchemy(app)

app.config['SECRET_KEY'] = 'youknownothingjonsnow' # file upload (would advise to change before production :/)
app.config['UPLOAD_FOLDER'] = 'static/uploads' # file upload


class Todo(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	content = db.Column(db.String(200), nullable=False) # added to display
	completed = db.Column(db.Integer, default=0)
	date_created = db.Column(db.DateTime, default=datetime.utcnow) # added to display
	output = db.Column(db.String(500), nullable=False) # added to display
	timetaken = db.Column(db.Float, nullable=False) # added to display
	numques = db.Column(db.Integer, nullable=False) # added to display

	def __repr__(self):
		return '<Task %r>' % self.id

class UploadFileForm(FlaskForm):
	file = FileField("File", validators=[InputRequired()])
	numques = IntegerField("Number of Questions", validators=[InputRequired()])
	submit = SubmitField("Upload File")

class LLM_output():
	def __init__(self, filename, numques=3):
		self.filename = filename # req at init
		self.numques = numques
		self.timetaken = None # seconds. None is a placeholder until eval() is executed.
		self.modelname = "text-davinci-003"

	def eval(self):
		oai_key = local_tokens.api_keys()["OAI"]["CMN"] # fetching keys

		# initializing the model
		openai = OpenAI(
			model_name= self.modelname,
			openai_api_key=oai_key
		)

		prompt = self.get_prompt()

		start = time.time()
		output = openai(prompt)
		end = time.time()

		self.timetaken = end - start # seconds

		return output, self.timetaken

	def get_prompt(self):
		with open("model_logic/prompt_template.txt", "r") as f:
			template = f.read()

		with open(self.filename, "r") as f:
			blog_txt = f.read()

		prompt_template = PromptTemplate(
			input_variables=[
				"blog_txt", 
				"num_ques",
				"ques_type"
			],
			template=template
		)

		prompt = prompt_template.format(
			blog_txt = blog_txt,
			num_ques = self.numques,
			ques_type = "coding or logical"
		)

		return prompt

def process_output(input):
	list_of_ques = input.split("@")
	list_of_ques = [ques.strip() for ques in list_of_ques]
	list_of_ques = [ques for ques in list_of_ques if ques != '']
	return list_of_ques
		

@app.route('/', methods=['POST', 'GET'])
def index():
	form = UploadFileForm()
	if request.method == 'POST' or form.validate_on_submit():
		file = form.file.data # grabbing the file
		filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
		file.save(filepath) # saving the file

		task_content = file.filename
		numques = form.numques.data
		if int(numques) > 10:
			return 'Too many questions!\nPlease enter a number less than 10'
		task_response, timetaken = LLM_output(filename=filepath, numques=numques).eval()
		task_response = process_output(task_response)
		new_task = Todo(
			content=task_content,
			output="\n".join(task_response),
			timetaken = round(timetaken,2),
			numques = int(numques),
		)

		try:
			db.session.add(new_task)
			db.session.commit()
			return redirect('/')
		except:
			return 'There was an issue adding your task'
		
	else:
		tasks = Todo.query.order_by(Todo.date_created).all()
		# tasks = Todo.query.order_by(Todo.date_created.desc()).first()
		return render_template('index.html', tasks=tasks, form=form)

@app.route('/delete/<int:id>')
def delete(id):
	task_to_delete = Todo.query.get_or_404(id)

	try:
		db.session.delete(task_to_delete)
		db.session.commit()
		return redirect('/')
	except:
		return 'There was a problem deleting that task'

if __name__ == '__main__':
	app.run(debug=True)