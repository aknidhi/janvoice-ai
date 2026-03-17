from collections import Counter

class RiskMeter:

    def calculate(self, data):

        if len(data) == 0:
            return 0

        total = len(data)

        negative = [
            d for d in data
            if "1" in d['sentiment'] or "2" in d['sentiment']
        ]

        neg_score = (len(negative)/total) * 60

        if negative:
            freq = Counter([d['issue'] for d in negative]).most_common(1)[0][1]
            issue_score = (freq/total) * 40
        else:
            issue_score = 0

        return min(int(neg_score + issue_score), 100)