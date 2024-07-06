from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
from PIL import Image
import pytesseract
import pypdfium2 as pdfium
from Model import SpellCheckerModule
spell_checker_module = SpellCheckerModule()
import openai
import requests
import sys
from gemini_utility import *
from feedback_and_grade import *
import whisper
app = Flask(__name__)
from main1 import plagiarism
from Backend import *
# Set the upload folder
UPLOAD_FOLDER = r'C:\Users\satwi\Downloads\Essay_grade\test flask\test_flask\static\uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

######################################################################################################################
#Function implentations


# Function to extract text from a PDF
def extract_text_from_pdf(file_path):
    final_text = ""
    pdf = pdfium.PdfDocument(file_path)
    for i in range(len(pdf)):
        page = pdf[i]
        image = page.render(scale=4).to_pil()
        extracted_text = pytesseract.image_to_string(image)
        final_text += extracted_text
    return final_text

# Function to extract text from an image
def extract_text_from_image(file_path):
    text = pytesseract.image_to_string(Image.open(file_path))
    return text

# Function to calculate the score
def calculate_score(text):
    # Your scoring logic goes here
    # For example, count the number of words
    words = text.split()
    score = len(words)
    return score


openai.api_key = 'Your api'

def get_feedback_and_grade(essay):
    URL = "https://api.openai.com/v1/chat/completions"
    text = essay.encode('utf-8')
    #print(text)
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": text.decode('utf-8')},
            {"role": "assistant", "content": "Please provide feedback on how the writer can improve the essay"}
        ],
        "temperature": 0.7,
        "max_tokens": 100,
        "n": 1,
        "stream": False,
        "presence_penalty": 0,
        "frequency_penalty": 0,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai.api_key}"
    }

    response = requests.post(URL, headers=headers, json=payload)
    print(response)
    if response.status_code == 200:
        data = response.json()
        feedback = data['choices'][0]['message']['content']
        return feedback
    else:
        return None




def audio_text(path):
    model = whisper.load_model("base")  # Options: "tiny", "base", "small", "medium", "large"
    audio_file = path
    result = model.transcribe(audio_file)

    text = result["text"]
    return text


##########################################################################################################
#routes

@app.route('/feedback', methods=['GET', 'POST'])
def display_feedback():
    if request.method == 'POST':
        text = request.form['text']
        #lang=request.form['language']
        #print(text)
        score = calculate_score(text)
        feedback = get_feedback_and_grade(text)
        #print(feedback)
        x=r"C:\Users\satwi\Downloads\Essay_grade\test flask\test_flask\plagiarism\yourself\temp.txt"
        with open(x, "w",encoding='utf-8') as f:
            f.write(text)
        f.close()
        if 'a' not in text:
            feedback=gemini_pro_response(text+'Please provide feedback in hindi on how the writer can improve the essay')
        plagiarism(r'C:\Users\satwi\Downloads\Essay_grade\test flask\test_flask\plagiarism')
        return render_template('feedback.html', text=text, score=score, feedback=feedback)
    return redirect(url_for('upload_file'))


def check_spelling1(t):
    # Call your function to check for spelling mistakes
    # and return the result as a string
    result = mainfunc(t)

    return result

@app.route('/score', methods=['POST'])
def display_score():
    text = request.form['text']
    score = mainfunc(text)
    score['Overall Score']=grade1(text)
    
    return render_template('score.html', text=text, score=score)

@app.route('/spelling', methods=['POST', 'GET'])
def spelling():
    if request.method == 'POST':
        text = request.form['text']
        corrected_text, corrected_words = spell_checker_module.correct_spell(text)
        corrected_grammar, _ = spell_checker_module.correct_grammar(text)
        original_words = text.split()
        word_pairs = zip(original_words, corrected_words)
        return render_template('spell.html', corrected_words=word_pairs, original_text=text)
    
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        text = ''
        #selected_language = request.form['language']
        
        # Check if a file was uploaded
        if 'file' in request.files:
            file = request.files['file']

            # Check if the file has a name
            if file.filename != '':
                # Save the file to the upload folder
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)

                # Extract text from the file
                if file.content_type == 'application/pdf':
                    text = extract_text_from_pdf(file_path)
                elif file.content_type.startswith('image/'):
                    text = extract_text_from_image(file_path)
                elif file.content_type == 'text/plain':
                    with open(file_path, 'r') as f:
                        text = f.read()
                elif file.content_type == 'audio/wav':
                    text=audio_text(file_path)
                else:
                    with open(file_path, 'r') as f:
                        text = f.read()

        # If no file was uploaded, get the text from the text box
        if text == '':
            text = request.form['text']
        #print(text)
        # Calculate the score
        score = "calculate_score(text)"
        t=grade1(text)
        # Generate feedback
        
        feedback =" get_feedback_and_grade(text)"
        insert_feedback("3", 'student'+str(3), text, score,t, feedback)
        # Render the result template with the extracted text, t,feedback
        return render_template('result.html', text=text, score=score, feedback=feedback)

    # Render the initial template with the file uploader and text box
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)