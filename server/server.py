from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

@app.route("/lineChartData")
def getLineChartData():
  return {"label":['January', 'February', 'March', 'April', 'May', 'June'],
          "attribute1":[12, 19, 3, 5, 2, 3],
          "attribute2":[10, 14, 6, 8, 3, 7]}

@app.route("/pieChartData")
def getPieChartData():
  return {"label":['January', 'February', 'March', 'April', 'May'],
          "attribute":[12, 19, 3, 5, 2, 13],
          "colors":['red', 'orange', 'yellow', 'green', 'blue', 'purple']}


if __name__ == "__main__":
  app.run(debug=True)
