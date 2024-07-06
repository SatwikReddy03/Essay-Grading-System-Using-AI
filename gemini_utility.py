import os
import json
from PIL import Image
from app import *
import google.generativeai as genai
from extractedscore import * 
# working directory path
working_dir = os.path.dirname(os.path.abspath(__file__))

# path of config_data file
# config_file_path = f"{working_dir}/config.json"
#config_data = json.load(open("config.json"))

# loading the GOOGLE_API_KEY
GOOGLE_API_KEY =   "AIzaSyA0BEdgpLUDh1kup3gziioCBqLu97fijQg"

# configuring google.generativeai with API key
genai.configure(api_key=GOOGLE_API_KEY)


def load_gemini_pro_model():
    gemini_pro_model = genai.GenerativeModel("gemini-pro")
    return gemini_pro_model


# get response from Gemini-Pro-Vision model - image/text to text
def gemini_pro_vision_response(prompt, image):
    gemini_pro_vision_model = genai.GenerativeModel("gemini-pro-vision")
    response = gemini_pro_vision_model.generate_content([prompt, image])
    result = response.text
    return result


# get response from embeddings model - text to embeddings
def embeddings_model_response(input_text):
    embedding_model = "models/embedding-001"
    embedding = genai.embed_content(model=embedding_model,
                                    content=input_text,
                                    task_type="retrieval_document")
    embedding_list = embedding["embedding"]
    return embedding_list


# get response from Gemini-Pro model - text to text
def gemini_pro_response(user_prompt):
    gemini_pro_model = genai.GenerativeModel("gemini-pro")
    response = gemini_pro_model.generate_content(user_prompt)
    result = response.text
    return result


# result = gemini_pro_response("What is Machine Learning")
# print(result)
# print("-"*50)
#
#
# image = Image.open("test_image.png")
# result = gemini_pro_vision_response("Write a short caption for this image", image)
# print(result)
# print("-"*50)
#
#
# result = embeddings_model_response("Machine Learning is a subset of Artificial Intelligence")
# print(result)
def read_text_file(file_path):
    with open(file_path, 'r') as file:
        text = file.read()
    return text
def mainfunc(text):
    print(text)
    prompt = f"From the given essay: {text} can you provide the scores out of 10 for vocabulary, sentence formation, context, and grammar without any suggestions or feedback? Give me those values in single line in the fomat Vocabulary: Score/10, Sentence formation: Score/10, Context: Score/10, Grammar: Score/10"    
    scores=extract_scores(gemini_pro_response(prompt))
    print(gemini_pro_response(prompt))
    return scores
    #print("gemini response:",y)
    # print("hello scores")
    # print(scores)
    # if scores:
    #     print("Extracted Scores:")
    #     for category, score in scores.items():
    #         print(f"\t{category}: {score}")
    # else:
    #     print("No scores found in the text.")