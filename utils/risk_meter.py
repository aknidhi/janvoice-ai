from collections import Counter

class RiskMeter:

    def calculate(self, data):

        if len(data) == 0:
            return 0

        total = len(data)

        negatives = [d for d in data if d["sentiment"]=="Negative"]

        neg_score = (len(negatives)/total)*60

        if negatives:
            freq = Counter([d["issue"] for d in negatives]).most_common(1)[0][1]
            issue_score = (freq/total)*40
        else:
            issue_score = 0

        return min(int(neg_score + issue_score),100)