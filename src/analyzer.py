from models.language_detector import detect_language
from models.translator import translate_text
from models.sentiment_model import get_sentiment
from models.issue_classifier import classify_issue

def analyze_text(text):

    lang = detect_language(text)

    translated = translate_text(text)

    sentiment = get_sentiment(translated)

    issue = classify_issue(translated)

    return {
        "text": text,
        "language": lang,
        "translated": translated,
        "sentiment": sentiment,
        "issue": issue
    }