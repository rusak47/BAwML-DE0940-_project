from BaseDatabaseConnector import BaseDatabaseConnector
from Range import Range
from Ad import Ad
from Scorer import Scorer

class Searcher(BaseDatabaseConnector):
    """
    Specialized class for searching ads in the database.
    Extends BaseDatabaseConnector to inherit connection management functionality.
    """

    def __init__(self):
        super().__init__()
        self.db_config = self.config.get_database_config()
        self.limits_config = self.config.get_limits_config()
        self.scoring_enabled = self.limits_config.get('scoring_enabled', True)
        self.max_scored_items = self.limits_config.get('max_scored_items', 2000)
        self.score_threshold = self.limits_config.get('score_threshold', 0.0)
        self.scorer = Scorer() if self.scoring_enabled else None

    """
    Search for ads in the database with optional filters
    Args:
        filters (dict): Dictionary of column names and values to filter by
                      e.g. {'district': 'Centrs', 'nr_of_rooms': 2}
    Returns:
        list: List of Ad objects containing the matching records
    """
    def search_ads(self, filters=None, max_scored_items=None, score_threshold=None, calculate_scores=None):
        """
        Search for ads in the database with optional filters.

        Args:
            filters (dict): Dictionary of column names and values to filter by
                          e.g. {'district': 'Centrs', 'nr_of_rooms': 2}
            max_scored_items (int): Maximum number of items to calculate scores for
                                  (to limit processing time for large result sets)
                                  If None, uses the value from config
            score_threshold (float): Threshold value below which we should stop scoring
                                   If None, uses the value from config
            calculate_scores (bool): Whether to calculate scores for the ads
                                   If None, uses the value from config (scoring_enabled)
        Returns:
            list: List of Ad objects containing the matching records
        """
        # Use config values if parameters are not provided
        if max_scored_items is None:
            max_scored_items = self.max_scored_items

        if score_threshold is None:
            score_threshold = self.score_threshold

        if calculate_scores is None:
            calculate_scores = self.scoring_enabled
        try:
            if not self.connection and not self.connect():
                return []

            query = "SELECT id, site_id, district, street, nr_of_rooms, area_m2, floor, floor_max, series, building_type, extra, price, price_m2, site, description FROM ads"
            params = []
            conditions = []

            if filters:
                for key, value in filters.items():
                    if key == "search_text":
                        # Search across multiple text fields
                        search_conditions = [
                            "LOWER(district) LIKE %s",
                            "LOWER(street) LIKE %s",
                            "LOWER(series) LIKE %s",
                            "LOWER(building_type) LIKE %s",
                            "LOWER(extra) LIKE %s",
                            "LOWER(description) LIKE %s"
                        ]
                        search_param = f"%{value.lower()}%"
                        conditions.append(f"({' OR '.join(search_conditions)})")
                        params.extend([search_param] * len(search_conditions))
                    elif isinstance(value, Range):
                        range_condition, range_params = value.get_condition_and_params()
                        if range_condition:
                            conditions.append(range_condition)
                            params.extend(range_params)
                    else:
                        conditions.append(f"LOWER({key}) = %s")
                        params.append(value.lower())

                if conditions:
                    query += " WHERE " + " AND ".join(conditions)

            self.debug(f"query: {query}")
            self.debug(f"params: {params}")

            self.cursor.execute(query, params)
            results = self.cursor.fetchall()

            self.debug(f"fetched results: {len(results)}")

            # Convert database rows to Ad objects
            ads = []
            for row in results:
                try:
                    ad = Ad.from_db_row(row)
                    ads.append(ad)
                except Exception as e:
                    self.error(f"Error creating Ad from row: {e}")

            # Calculate scores if requested
            if calculate_scores:
                ads = self.calculate_scores_for_ads(ads, max_scored_items, score_threshold)

            return ads

        except Exception as error:
            self.error(f"Error while searching ads: {error}")
            return []

    def getBuildingTypeUnique(self):
        try:
            if not self.connection:
                if not self.connect():
                    return []

            query = "SELECT DISTINCT building_type FROM ads WHERE building_type IS NOT NULL ORDER BY building_type"
            self.cursor.execute(query)
            results = self.cursor.fetchall()

            # Extract building types from results
            building_types = [row[0] for row in results]
            return building_types

        except (Exception) as error:
            self.error(f"Error while getting unique building types: {error}")
            return []

    def getBuildingSeriesUnique(self):
        try:
            if not self.connection:
                if not self.connect():
                    return []

            query = "SELECT DISTINCT series FROM ads WHERE series IS NOT NULL ORDER BY series"
            self.cursor.execute(query)
            results = self.cursor.fetchall()

            # Extract building types from results
            series = [row[0] for row in results]
            return series

        except (Exception) as error:
            self.error(f"Error while getting unique series: {error}")
            return []

    def calculate_scores_for_ads(self, ads, max_scored_items=None, score_threshold=None):
        """
        Calculate scores for a list of ads.

        Args:
            ads (list): List of Ad objects to calculate scores for
            max_scored_items (int): Maximum number of items to calculate scores for
                                  If None, uses the value from config
            score_threshold (float): Threshold value below which we should stop scoring
                                   If None, uses the value from config

        Returns:
            list: The same list of Ad objects with scores calculated
        """
        # Use config values if parameters are not provided
        if max_scored_items is None:
            max_scored_items = self.max_scored_items

        if score_threshold is None:
            score_threshold = self.score_threshold

        # If scoring is disabled in config, return ads without scoring
        if not self.scoring_enabled:
            return ads
        try:
            if not self.scorer or not ads:
                return ads

            # Limit the number of ads to score
            items_to_score = min(len(ads), max_scored_items)
            self.debug(f"Calculating scores for {items_to_score} items out of {len(ads)}")

            # Calculate scores for the limited set
            for i in range(items_to_score):
                try:
                    # Get score for the current ad
                    score = self.scorer.get_score_for_ad(ads[i], score_threshold)
                    ads[i].score = score

                    # Check if we should continue scoring based on the current score
                    if not self.scorer.should_continue_scoring(score, score_threshold):
                        self.debug(f"Stopping score calculation at item {i+1} because score {score} is below threshold {score_threshold}")
                        break
                except Exception as e:
                    self.warning(f"Could not calculate score for ad {ads[i].id}: {e}")
                    ads[i].score = None

            # Sort by score in descending order (highest score first)
            try:
                # First sort by score (if available)
                scored_ads = [ad for ad in ads if hasattr(ad, 'score') and ad.score is not None]
                unscored_ads = [ad for ad in ads if not hasattr(ad, 'score') or ad.score is None]

                scored_ads.sort(key=lambda ad: ad.score, reverse=True)

                # Combine sorted scored ads with unscored ads
                return scored_ads + unscored_ads
            except Exception as e:
                self.error(f"Error sorting ads by score: {e}")
                return ads

        except Exception as error:
            self.error(f"Error while calculating scores for ads: {error}")
            return ads

if __name__ == "__main__":
    # Test database connection
    searcher = Searcher()

    print("Testing database connection...")
    if searcher.connect():
        print("✓ Successfully connected to database")

        # Test cursor creation
        if searcher.cursor:
            print("✓ Successfully created database cursor")
        else:
            print("✗ Failed to create database cursor")

        # Test disconnection
        searcher.disconnect()
        if not searcher.connection:
            print("✓ Successfully disconnected from database")
        else:
            print("✗ Failed to disconnect from database")
    else:
        print("✗ Failed to connect to database")

    # Test context manager
    print("\nTesting context manager...")
    try:
        with Searcher() as db:
            if db.connection and db.cursor:
                print("✓ Context manager successfully connected")
            else:
                print("✗ Context manager failed to connect")
        if not db.connection:
            print("✓ Context manager successfully disconnected")
        else:
            print("✗ Context manager failed to disconnect")
    except Exception as e:
        print(f"✗ Context manager test failed with error: {e}")

    # Test search_ads functionality
    print("\nTesting search_ads with different parameters...")
    try:
        with Searcher() as db:
            # Test with no parameters (should return all ads)
            results = db.search_ads()
            print("✓ search_ads with no params returned", len(results), "results")

            # Test with district filter
            results = db.search_ads(filters={"district": "purvciems"})
            print("✓ search_ads with district filter returned", len(results), "results")

            # Test with price range
            price_range = Range("price", number_min=8000, number_max=None)
            results = db.search_ads(filters={"price": price_range})
            print(f"✓ search_ads with price range {price_range} returned", len(results), "results")

            # Test with rooms number range
            rooms_range = Range("nr_of_rooms", number_min=2, number_max=3)
            results = db.search_ads(filters={"nr_of_rooms": rooms_range})
            print(f"✓ search_ads with rooms number range {rooms_range} returned", len(results), "results")

            # Test with area range (only minimum)
            area_range = Range("area_m2", number_min=50)
            results = db.search_ads(filters={"area_m2": area_range})
            print(f"✓ search_ads with minimum area {area_range} returned", len(results), "results")

            # Test with multiple parameters including ranges
            results = db.search_ads(filters={
                "nr_of_rooms": Range("nr_of_rooms", 2, 3),
                "price": Range("price", number_max=150000),
                "district": "centrs"
            })
            print("✓ search_ads with multiple filters including ranges returned", len(results), "results")

            # Test with different score thresholds
            print("\nTesting search_ads with different score thresholds...")

            # Test with high threshold (should stop scoring early)
            results_high_threshold = db.search_ads(score_threshold=0.9)

            # Test with low threshold (should score more items)
            results_low_threshold = db.search_ads(score_threshold=0.1)

            print(f"✓ search_ads with high threshold (0.9) returned {len(results_high_threshold)} results")
            print(f"✓ search_ads with low threshold (0.1) returned {len(results_low_threshold)} results")

            building_types = db.getBuildingTypeUnique()
            print(building_types)
            assert len(building_types) >= 1, "Should return at least 1 unique building type"
            assert None not in building_types, "Should not contain NULL values"

            building_types = db.getBuildingSeriesUnique()
            print(building_types)
            assert len(building_types) >= 1, "Should return at least 1 unique building type"
            assert None not in building_types, "Should not contain NULL values"

    except Exception as e:
        print(f"✗ search_ads tests failed with error: {e}")
