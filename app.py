#create Flask app
from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mission_to_mars"
mongo = PyMongo(app)

@app.route('/')
def index():

    mars_data = mongo.db.mars.find_one()
    print(mars_data)
    return render_template("index.html", mars_data=mars_data)

@app.route("/scrape")
def scrape():
    mission_to_mars = scrape_mars.scrape()
    mars_data = mongo.db.mars
    mars_data.update(
        {}, 
        mission_to_mars,
        upsert=True
       )

    return redirect("http://localhost:5000/", code=302)
    
if __name__ == "__main__":
    app.run(debug=True)

