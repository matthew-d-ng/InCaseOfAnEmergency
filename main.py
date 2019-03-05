from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    earthQuakeList = ["USGSted: Prelim M5.5 Earthquake central Mid-Atlantic Ridge Feb-25 15:05 UTC",
                    "USGSted: Prelim M5.5 Earthquake Macquarie Island region Feb-24 06:00 UTC",
                    "USGSted: Prelim M5.5 Earthquake southern Mid-Atlantic Ridge Feb-22 21:15 UTC",
                    "USGSted: Prelim M5.5 Earthquake near the coast of Ecuador Feb-22 10:40 UTC",
                    "USGSted: Prelim M7.5 Earthquake Peru-Ecuador border region Feb-22 10:17 UTC"]
    APIKEY = "AIzaSyD1XIdaoi1PCBfttZe85pPnRBw25ZSADuU"
    return render_template('home.html', earthQuakeList = earthQuakeList, APIKEY = APIKEY)

if __name__ == '__main__':
   app.run(debug = True)
