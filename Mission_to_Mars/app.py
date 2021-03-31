# Import Dependencies and pymongo library - lets us connect our Flask app to our Mongo database.
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars


app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


@app.route("/")
def index():
    mars_info = mongo.db.mars_info.find_one()
    return render_template("index.html", mars=mars_info)


@app.route("/scrape_mars")
def scrape():
    mars_info = mongo.db.mars_info
    mars_scrape = scrape_mars.scrape()
    # Update the Mongo database using update and upsert=True
    mars_info.update({}, mars_scrape, upsert=True)    
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True, port = 5000)
