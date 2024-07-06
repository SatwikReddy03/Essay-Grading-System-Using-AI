import re

def extract_scores(text):
    """
    Extracts scores from the analysis results in the provided text.

    Args:
        text: The text containing the analysis results.

    Returns:
        A dictionary containing the extracted scores or None if no scores are found.
    """
    scores = {}
    pattern = r"\b(\w+)\s*:\s*(\d+)/\d+\b"  # Regex pattern to match category and score
    matches = re.findall(pattern, text)
    for match in matches:
        category, score_str = match
        score = int(score_str)
        scores[category.lower()] = score
    return scores if scores else None

# text = "Vocabulary: 8/10, Sentence formation: 9/10, Context: 9/10, Grammar: 9/10"
# scores = extract_scores(text)
# print(scores)

# Provided text with analysis results
# text = """Essay Analysis:
# Vocabulary (7/10):
# The essay uses a good range of vocabulary, including some strong academic terms like "interdependent" and "industrialization."
# There are a few minor errors, such as "birth to many pollutions" (should be "birth to many pollutants").
# Sentence Formation (6/10):
# The sentence structure is mostly simple, with some attempts at compound sentences.

