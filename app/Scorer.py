import os
import requests
from dotenv import load_dotenv

from BaseDatabaseConnector import BaseDatabaseConnector
from Ad import Ad
from Utils import simplify_address

class Scorer(BaseDatabaseConnector):
    """
    Specialized class for scoring locations based on coordinates.
    Extends BaseDatabaseConnector to inherit connection management functionality.
    """
    def __init__(self):
        super().__init__()
        self.db_config = self.config.get_osgi_scorer_database_config()
        self.limits_config = self.config.get_limits_config()
        self.scoring_enabled = self.limits_config.get('scoring_enabled', True)
        self.score_threshold = self.limits_config.get('score_threshold', 0.0)

        # Get the URL for the geocoding service
        self.url = self.db_config.get('url', 'http://localhost:8080/search?q=')

    def get_lat_lon(self, street: str) -> tuple[float, float]:
        city = "Riga"

        # Expand street abbreviations to their full forms
        expanded_street = simplify_address(street)

        # Replace spaces with plus signs for URL encoding
        street_url = expanded_street.replace(" ", "+")

        url = self.url + street_url + f",+{city}&format=json"

        try:
            r = requests.get(url).json()[0]
        except IndexError:
            print(f"An invalid or non-existing street name: {street}->{street_url}")
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

    def get_score_for_ad(self, ad: Ad, threshold: float = None) -> float:
        """
        Get a score for an ad based on its coordinates.

        Args:
            ad (Ad): Ad object
            threshold (float): Threshold value below which we should stop scoring
                              If None, uses the value from config
                              This parameter is not used in this method but is included for API consistency

        Returns:
            float: Score value or -1 if an error occurred
        """
        # Use config value if parameter is not provided
        if threshold is None:
            threshold = self.score_threshold

        # If scoring is disabled in config, return 0
        if not self.scoring_enabled:
            return 0
        try:
            # Get coordinates for the address
            lat, lon = self.get_lat_lon(ad.street)

            # Calculate score based on coordinates
            score = self.get_score(lat, lon)
            return score
        except Exception as e:
            self.error(f"Error while getting score for ad: {e}")
            return -1

    def should_continue_scoring(self, score: float, threshold: float = None) -> bool:
        """
        Determine if we should continue scoring more ads based on the current score.

        Args:
            score (float): The current ad's score
            threshold (float): Threshold value below which we should stop scoring
                              If None, uses the value from config

        Returns:
            bool: True if we should continue scoring, False otherwise
        """
        # Use config value if parameter is not provided
        if threshold is None:
            threshold = self.score_threshold

        # If scoring is disabled in config, return False to stop scoring
        if not self.scoring_enabled:
            return False
        # If score is -1, it means there was an error, so we should continue
        if score == -1:
            return True

        # If score is below threshold, we should stop scoring
        return score >= threshold

if __name__ == "__main__":
    scorer = Scorer()
    print("coordinates:")
    print(scorer.get_lat_lon("J. Vācieša 6"))
    print("score:")
    print(scorer.get_score(56.9519, 24.1171))

    print("score for ad:")
    ad = Ad(
        id=1,
        site_id=1,
        district="Centrs",
        street="Čiekurkalna 4. šķ l. 12 k-2",
        nr_of_rooms=2,
        area_m2=50,
        floor=2,
        floor_max=2,
        price=50000,
        site="http://example.com",
        description="description",
        building_type="building_type",
        series="series"
    )
    score = scorer.get_score_for_ad(ad)
    print(f"Score: {score}")

    # Test threshold functionality
    threshold = 0.7
    should_continue = scorer.should_continue_scoring(score, threshold)
    print(f"Should continue scoring (threshold={threshold})? {should_continue}")

    threshold = 0.3
    should_continue = scorer.should_continue_scoring(score, threshold)
    print(f"Should continue scoring (threshold={threshold})? {should_continue}")
