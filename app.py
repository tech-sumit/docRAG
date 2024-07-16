import os
import re
import json
from pinecone import Pinecone
from openai import OpenAI
from flask import Flask, flash, request, redirect, send_from_directory
from dotenv import load_dotenv
from flask.templating import render_template
from werkzeug.utils import secure_filename

from sentence_transformers import SentenceTransformer

from RAG import vector_store, extractor, agent

# Load environment variables
load_dotenv()

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'json', 'pdf'}

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize OpenAI Client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize Pinecone Database
pinecone = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))

# Initialize SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'json_file' not in request.files or 'data_file' not in request.files:
            flash("Sorry, the upload didn't send all of the data!")
            return redirect(request.url)
        json_file = request.files["json_file"]
        data_file = request.files["data_file"]
        json_data_file = request.files["json_data_file"]
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if json_file.filename == "" or data_file.filename == "" or json_data_file.filename == "":
            flash('You need to upload 2 files!')
            return redirect(request.url)
        if (json_file and allowed_file(json_file.filename)) and (data_file and allowed_file(data_file.filename)) and (
                json_data_file and allowed_file(json_data_file.filename)):
            # try:
            json_filename = secure_filename(json_file.filename)
            json_filepath = os.path.join(app.config['UPLOAD_FOLDER'], json_filename)
            json_file.save(json_filepath)

            data_filename = secure_filename(data_file.filename)
            data_filepath = os.path.join(app.config['UPLOAD_FOLDER'], data_filename)
            data_file.save(data_filepath)

            json_data_filename = secure_filename(json_data_file.filename)
            json_data_filepath = os.path.join(app.config['UPLOAD_FOLDER'], json_data_filename)
            json_data_file.save(json_data_filepath)

            # index name
            index_name = generate_valid_name(data_filename)

            # create the pinecone index
            vector_store.create_index(pinecone, index_name)

            # get the data from pdf
            pdf_data = extractor.get_text_from_pdf(data_filepath)

            # add the data to the vector store
            vector_store.add_text_to_vector_store(index_name, pdf_data, model, pinecone)

            # summarise data from json
            json_data = extractor.summarize_data_from_json(json_data_filepath, client)

            # add the data to the vector store
            vector_store.add_text_to_vector_store(index_name, json_data, model, pinecone)

            # Process files to find answers
            questions = read_questions_from_json(json_filepath)
            answers = agent.find_answers_in_pdf(index_name, questions, client, model, pinecone)

            # Clean up uploaded files
            os.remove(json_filepath)
            os.remove(data_filepath)
            os.remove(json_data_filepath)

            # Render results
            return render_template("results.html", answers=answers)
        # except Exception as e:
        #     flash(f"An error occurred: {str(e)}")
        #     return redirect(request.url)

    elif request.method == "GET":
        return render_template("template.html")


def read_questions_from_json(json_filepath):
    try:
        with open(json_filepath, 'r') as f:
            data = json.load(f)

        questions = []
        for item in data:
            questions.append(item.get('content'))

        return questions
    except json.JSONDecodeError:
        flash("Invalid JSON file")
        return []
    except Exception as e:
        flash(f"Error reading JSON file: {str(e)}")
        return []


def generate_valid_name(existing_name):
    # Convert the string to lowercase
    existing_name = existing_name.lower()

    # Replace all characters that are not lowercase alphanumeric or hyphen with an empty string
    valid_name = re.sub(r'[^a-z0-9-]', '', existing_name)

    return valid_name


if __name__ == '__main__':
    app.run(debug=True)
