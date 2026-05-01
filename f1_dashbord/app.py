import requests
from flask import Flask, render_template

app = Flask(__name__)
BASE_URL = "https://api.jolpi.ca/ergast/f1/current"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/drivers")
def drivers():
    try:
        url = f"{BASE_URL}/driverStandings.json"
        data = requests.get(url).json()

        standings = data["MRData"]["StandingsTable"]["StandingsLists"][0]["DriverStandings"]

        drivers_list = []
        for d in standings:
            drivers_list.append({
                "position": d["position"],
                "name": d["Driver"]["givenName"] + " " + d["Driver"]["familyName"],
                "team": d["Constructors"][0]["name"],
                "points": d["points"]
            })

        return render_template("drivers.html", drivers=drivers_list)

    except:
        return "Error fetching driver data"


@app.route("/constructors")
def constructors():
    try:
        url = f"{BASE_URL}/constructorStandings.json"
        data = requests.get(url).json()

        standings = data["MRData"]["StandingsTable"]["StandingsLists"][0]["ConstructorStandings"]

        teams = []
        for t in standings:
            teams.append({
                "position": t["position"],
                "name": t["Constructor"]["name"],
                "points": t["points"]
            })

        return render_template("constructors.html", teams=teams)

    except:
        return "Error fetching constructor data"


@app.route("/results")
def results():
    try:
        url = f"{BASE_URL}/last/results.json"
        data = requests.get(url).json()

        results_data = data["MRData"]["RaceTable"]["Races"][0]["Results"]

        race_results = []
        for r in results_data:
            race_results.append({
                "position": r["position"],
                "name": r["Driver"]["givenName"] + " " + r["Driver"]["familyName"],
                "team": r["Constructor"]["name"],
                "time": r.get("Time", {}).get("time", "N/A")
            })

        return render_template("results.html", results=race_results)

    except:
        return "Error fetching race results"


if __name__ == "__main__":
    app.run(debug=True)