import os
import requests
from dotenv import load_dotenv

from BaseDatabaseConnector import BaseDatabaseConnector

class Scorer(BaseDatabaseConnector):
    """
    Specialized class for scoring locations based on coordinates.
    Extends BaseDatabaseConnector to inherit connection management functionality.
    """
    def __init__(self):
        super().__init__()
        self.db_config = self.config.get_osgi_scorer_database_config()

        # Get the URL for the geocoding service
        self.url = self.db_config.get('url', 'http://localhost:8080/search?q=')

    def get_lat_lon(self, street: str) -> tuple[float, float]:
        city = "R%C4%ABga"
        street = street.replace(" ", "+")

        url = self.url + street + f",+{city}&format=json"

        try:
            r = requests.get(url).json()[0]
        except IndexError:
            print(f"An invalid or non-existing street name: {street}")
            return (0, 0)

        latitude = r["lat"]
        longitude = r["lon"]

        return latitude, longitude

    def get_score(self, lat: float, lon: float) -> float:
        """
        Get a score for a location based on its coordinates.

        Args:
            lat (float): Latitude
            lon (float): Longitude

        Returns:
            float: Score value or -1 if an error occurred
        """
        try:
            # Ensure we have a connection
            if not self.connection and not self.connect():
                return -1

            query = "select score(%s, %s)"
            params = [lat, lon]

            self.cursor.execute(query, params)
            score = self.cursor.fetchone()[0]

            return score

        except Exception as e:
            self.error(f"Error while getting location score: {e}")
            return -1


if __name__ == "__main__":
    scorer = Scorer()
    print("coordinates:")
    print(scorer.get_lat_lon("Bruņinieku iela 45"))
    print("score:")
    print(scorer.get_score(56.9519, 24.1171))
