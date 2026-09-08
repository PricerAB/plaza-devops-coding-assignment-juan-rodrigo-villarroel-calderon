import os
import requests
from fastapi import FastAPI, HTTPException, Query

app = FastAPI()

HELLO_MESSAGE = os.getenv("HELLO_MESSAGE", "Hello, World!")

@app.get("/")
def hello():
    return {"message": HELLO_MESSAGE}

@app.get("/data")
def get_star_wars_data(id: int = Query(1, description="Star Wars person ID")):
    try:
        response = requests.get(f"https://swapi.info/api/people/{id}", timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        raise HTTPException(status_code=500, detail="API Error")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=503, detail="Service Unavailable")
    except (KeyError, ValueError) as e:
        raise HTTPException(status_code=500, detail="Data Processing Error")

@app.get("/top-people-by-bmi")
def top_people_by_bmi():
    try:
        response = requests.get("https://swapi.info/api/people", timeout=10)
        response.raise_for_status()
        people = response.json()

        results = []
        for person in people:
            try:
                mass = float(person["mass"].replace(",", ""))
                height = float(person["height"])
                if height > 0:
                    bmi = mass / ((height / 100) ** 2)
                    results.append({"name": person["name"], "bmi": round(bmi, 2)})
            except (ValueError, KeyError):
                continue

        results.sort(key=lambda x: x["bmi"], reverse=True)
        return results[:20]

    except requests.exceptions.HTTPError:
        raise HTTPException(status_code=500, detail="API Error")
    except requests.exceptions.RequestException:
        raise HTTPException(status_code=503, detail="Service Unavailable")