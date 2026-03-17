def classify_issue(text):

    text = text.lower()

    if "traffic" in text or "jam" in text:
        return "Traffic"

    elif "water" in text or "pani" in text:
        return "Water"

    elif "electricity" in text or "light" in text:
        return "Electricity"

    elif "road" in text:
        return "Road"

    else:
        return "General"