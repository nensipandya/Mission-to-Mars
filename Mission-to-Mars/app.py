# Import  Dependencies

from flask import Flask, render_template, url_for, redirect
from flask_pymongo import PyMongo
import scraping

# set up flask app

app = Flask(__name__)
 
# Use flask_pymongo to  set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mission-to-mars-app"
mongo = PyMongo(app)

# Set the app route
@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)
                           
@app.route("/scrape")
def scarpe():
    mars = mongo.db.mars
    mars_data = scraping.scrape_all()
    mars.update_one({}, {"$set": mars_data}, upsert=True)
    return redirect('/', code=302)

if __name__ == "__main__":
    app.run()
                           
                           
                          





    
