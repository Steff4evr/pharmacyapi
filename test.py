from re import A
from flask import Flask
import json

app = Flask(__name__)

# Need to have some data to return.
# For a production app this information would be stored in a database of course...
art_dict = {
    "composition 8": {
        "When": "1923",
        "Artist": "Vasily Kandinsky",
        "Medium": "Oil Painting",
        "Place": "Moscow",
        "Periods": ["Suprematism", "Abstract art"]
    },
    "Royal Red and Blue": {
        "When": "1954–1954",
        "Artist": "Mark Rothko",
        "Medium": "Oil Paint",
        "Place": "Litvak Descent",
        "Periods": ["Washington Color School"]
    },
    "Starry Night": {
        "When": "1889",
        "Artist": "Vincent van Gogh",
        "Medium": "Oil Painting",
        "Place": "Netherlands",
        "Periods": ["Post-Impressionism", "Modern art"]
    }
}

# Now for some routes:
@app.route("/composition_8")
def homepage():
    return json.dumps(art_dict["composition 8"])

@app.route("/composition_1")
def homepage1():
    return json.dumps(art_dict["Royal Red and Blue"])


app.