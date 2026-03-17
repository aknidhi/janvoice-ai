def classify_issue(text):

    t = text.lower()

    if any(k in t for k in ["traffic","jam","congestion"]):
        return "Traffic"

    if any(k in t for k in ["water","pani","supply"]):
        return "Water"

    if any(k in t for k in ["electricity","power","light"]):
        return "Electricity"

    if any(k in t for k in ["road","pothole","street"]):
        return "Road"

    return "General"