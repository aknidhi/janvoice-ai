import pandas as pd
import time
from src.analyzer import analyze_text

def stream_data():

    df = pd.read_csv("data/sample_live_feed.csv")

    for text in df['text']:

        result = analyze_text(text)

        yield result

        time.sleep(2)