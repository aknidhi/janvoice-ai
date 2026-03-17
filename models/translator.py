from googletrans import Translator

translator = Translator()

def translate_text(text):
    try:
        return translator.translate(text, dest='en').text
    except:
        return text