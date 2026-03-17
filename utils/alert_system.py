from collections import Counter

class AlertSystem:

    def __init__(self):
        self.buffer = []

    def update(self, issue, sentiment):

        if "1" in sentiment or "2" in sentiment:
            self.buffer.append(issue)

        if len(self.buffer) > 20:
            self.buffer.pop(0)

    def check_alert(self):

        if not self.buffer:
            return None

        issue, freq = Counter(self.buffer).most_common(1)[0]

        if freq >= 5:
            return f"🚨 High complaints about {issue}"

        return None