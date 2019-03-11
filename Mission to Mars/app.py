from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of our Flask app.
app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Set route
@app.route('/')
def index():
    mars_data = mongo.db.mars_data.find_one()
    return render_template('index.html', mars_data = mars_data)


@app.route('/scrape')
def scrape_mongo():
   mars_data = mongo.db.mars_data
   mars_scraped = scrape_mars.scrape()
   mars_data.update({}, mars_scraped, upsert= True)
   return redirect("/", code=302)
   
if __name__ == "__main__":
    app.run(debug=True)