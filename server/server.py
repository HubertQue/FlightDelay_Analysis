from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

@app.route("/data")
def getData():
  return {"datas":["data1", "data2"]}



if __name__ == "__main__":
  app.run(debug=True)
