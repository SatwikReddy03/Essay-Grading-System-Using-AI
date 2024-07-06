import pymongo
import pandas as pd
import matplotlib.pyplot as plt
import mpld3
# Connect to MongoDB

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["Feedback"]  # Replace "Feedback" with your database name
collection = db["feedback"]  # Replace "feedback_data" with your collection name

# Insert data into MongoDB
def insert_feedback(id, name, text, score,overallscore, suggestions):
    
    feedback = {
        "id": id,
        "name": name,
        "text": text,
        "score": {
            "Overall Score": overallscore,
            "detailed": score
        },
        "suggestions": suggestions
        }
    print("inserted")
    collection.insert_one(feedback)

# Get top 3 scores from MongoDB
def get_top3_scores():
    top3_scores = collection.find().sort("score", pymongo.DESCENDING).limit(3)
    return list(top3_scores)
def getstatistics():
    # Query to retrieve scores
    query = {}  # You can add filters to the query if needed
    projection = {"_id": 0, "score": 1}  # Include only the score field

    # Retrieve scores from MongoDB and convert to pandas DataFrame
    cursor = collection.find(query, projection)
    df = pd.DataFrame(list(cursor))

    # Categorize scores into low, medium, and high categories using the categorize_score function from the previous example
    def categorize_score(score):
        if score >= 1 and score <= 6:
            return 'Low'
        elif score >= 7 and score <= 8:
            return 'Medium'
        elif score >= 9 and score <= 10:
            return 'High'
        elif score>10:
            return 'Invalid'

    df['category'] = df['score'].apply(categorize_score)

    # Calculate the count of scores in each category
    category_counts = df['category'].value_counts()

    # Plotting a pie chart
    plt.figure(figsize=(8, 6))
    plt.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%', startangle=140)
    plt.title('Score Categories Distribution')
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    html_plot = mpld3.fig_to_html(plt.gcf())
    return html_plot
    # Display the plot
    plt.show()
# def read_text_file(file_path):
#     with open(file_path, 'r') as file:
#         text = file.read()
#     return text
# text=read_text_file("Text.txt")
# Example usage:
if __name__ == "__main__":
    # Insert feedback data
    # Get and print top 3 scores
    # insert_feedback("1",'Harish',text,8,"Strengthen the introduction: Provide a clear thesis statement that outlines the key points and arguments of the essay. Include specific examples: Incorporate real-life examples or case studies to support your arguments and provide concrete evidence.")
    # insert_feedback("1",'Harish',text,9,"Strengthen the introduction: Provide a clear thesis statement that outlines the key points and arguments of the essay. Include specific examples: Incorporate real-life examples or case studies to support your arguments and provide concrete evidence.")
    # insert_feedback("1",'Harish',text,10,"Strengthen the introduction: Provide a clear thesis statement that outlines the key points and arguments of the essay. Include specific examples: Incorporate real-life examples or case studies to support your arguments and provide concrete evidence.")
    # top3_feedback = get_top3_scores()
    # print("Top 3 Scores:")
    # for feedback in top3_feedback:
    #     print(f"ID: {feedback['id']}")
    #     prompt=f"Get the Summary of the {text}  given"
    #     print("summary",gemini_pro_response(prompt))
    html_pie_chart = getstatistics()

# Now you can save the HTML content to a file or use it in a web page
    with open('pie_chart.html', 'w') as f:
        f.write(html_pie_chart)

