from BaseDatabaseConnector import BaseDatabaseConnector
from Scorer import Scorer
from Ad import Ad
from Utils import simplify_address

class SearcherScoreCacher(BaseDatabaseConnector):
    """
    Specialized class for calculating and caching ad scores in the database.
    Extends BaseDatabaseConnector to inherit connection management functionality.
    """

    def __init__(self):
        super().__init__()
        self.db_config = self.config.get_database_config()
        self.limits_config = self.config.get_limits_config()
        self.scorer = Scorer()

    def calculate_and_cache_scores(self, batch_size=100):
        """
        Reads all ads without cached scores, calculates their scores,
        and inserts them into the ad_scores table.
        
        Args:
            batch_size (int): Number of ads to process in each batch
            
        Returns:
            int: Number of ads processed
        """
        try:
            if not self.connection and not self.connect():
                self.error("Failed to connect to database")
                return 0
                
            # Find ads that don't have scores in the ad_scores table
            query = """
                SELECT ads.id, ads.site_id, ads.district, ads.street, ads.nr_of_rooms, 
                       ads.area_m2, ads.floor, ads.floor_max, ads.series, ads.building_type, 
                       ads.extra, ads.price, ads.price_m2, ads.site, ads.description
                FROM ads 
                LEFT JOIN ad_scores ON ads.id = ad_scores.ad_id
                WHERE ad_scores.ad_id IS NULL
                LIMIT %s
            """
            
            total_processed = 0
            
            while True:
                self.cursor.execute(query, [batch_size])
                results = self.cursor.fetchall()
                
                if not results:
                    break
                    
                self.debug(f"Processing batch of {len(results)} ads")
                
                # Process each ad
                for row in results:
                    try:
                        ad = Ad.from_db_row(row)
                        
                        # Calculate score
                        score = self.scorer.get_score_for_ad(ad, None)
                        
                        # Insert into ad_scores table
                        insert_query = """
                            INSERT INTO ad_scores (ad_id, lon, lat, score)
                            VALUES (%s, %s, %s, %s)
                            ON CONFLICT (ad_id) DO UPDATE 
                            SET lon = %s, lat = %s, score = %s
                        """
                        self.cursor.execute(
                            insert_query, 
                            [ad.id, ad.lon, ad.lat, score, ad.lon, ad.lat, score]
                        )
                        
                        total_processed += 1
                        
                    except Exception as e:
                        self.error(f"Error processing ad {row[0]}: {e}")
                
                # Commit after each batch
                self.connection.commit()
                
                if len(results) < batch_size:
                    break
                    
            self.debug(f"Total ads processed: {total_processed}")
            return total_processed
            
        except Exception as error:
            self.error(f"Error while calculating and caching scores: {error}")
            if self.connection:
                self.connection.rollback()
            return 0

if __name__ == "__main__":
    # Test the score calculator
    calculator = SearcherScoreCacher()
    print("Starting score calculation...")
    processed = calculator.calculate_and_cache_scores()
    print(f"Processed {processed} ads")