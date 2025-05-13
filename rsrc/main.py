import os
import requests
from dotenv import load_dotenv
import psycopg2

URL = "http://localhost:8080/search?q="


def get_lat_lon(street: str) -> tuple[float, float]:
    city = "R%C4%ABga"
    street = street.replace(" ", "+")

    url = URL + street + f",+{city}&format=json"

    try:
        r = requests.get(url).json()[0]
    except IndexError:
        print(f"An invalid or non-existing street name: {street}")
        return (0, 0)

    latitude = r["lat"]
    longitude = r["lon"]

    return latitude, longitude


def get_score(lat: float, lon: float) -> float:
    conn = psycopg2.connect(
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        host="localhost",
        password=os.getenv("POSTGRES_PASSWORD"),
        port=5432,
    )
    cursor = conn.cursor()

    cursor.execute("select score(%(lat)s, %(lon)s)", {"lat": lat, "lon": lon})
    score = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return score


def main():
    load_dotenv("../.env")

    street = "Bruņinieku iela 45"

    latitude, longitude = get_lat_lon(street)

    print(f"lat: {latitude}, lon: {longitude}")

    score = get_score(latitude, longitude)

    print(f"Score = {score}")


if __name__ == "__main__":
    main()
