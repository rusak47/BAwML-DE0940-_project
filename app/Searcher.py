from BaseDatabaseConnector import BaseDatabaseConnector
from Range import Range
from Ad import Ad

class Searcher(BaseDatabaseConnector):
    """
    Specialized class for searching ads in the database.
    Extends BaseDatabaseConnector to inherit connection management functionality.
    """
    
    def __init__(self):
        super().__init__()

    """
    Search for ads in the database with optional filters
    Args:
        filters (dict): Dictionary of column names and values to filter by
                      e.g. {'district': 'Centrs', 'nr_of_rooms': 2}
    Returns:
        list: List of Ad objects containing the matching records
    """
    def search_ads(self, filters=None):
        try:
            if not self.connection:
                if not self.connect():
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
            return [Ad.from_db_row(row) for row in results]

        except (Exception) as error:
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


# For backward compatibility, create an alias
DatabaseConnector = Searcher

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
