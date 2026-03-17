from collections import Counter

class AlertSystem:

    def __init__(self):
        self.buffer = []

    def update(self, issue, sentiment):

        if sentiment == "Negative":
            self.buffer.append(issue)

        if len(self.buffer) > 20:
            self.buffer.pop(0)

    def check_alert(self):

        if not self.buffer:
            return None

        issue, freq = Counter(self.buffer).most_common(1)[0]

        if freq >= 4:
            return f"🚨 Rising complaints about {issue}"

        return None