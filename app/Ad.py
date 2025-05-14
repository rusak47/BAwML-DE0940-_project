class Ad:
    def __init__(self, **kwargs):
        """
        Initialize an Ad object with the given attributes.

        Args:
            **kwargs: Arbitrary keyword arguments that will be set as attributes.
                     Common attributes include:
                     - id: Unique identifier
                     - site_id: Site identifier
                     - district: District name
                     - street: Street address
                     - nr_of_rooms: Number of rooms
                     - area_m2: Area in square meters
                     - floor: Floor number
                     - floor_max: Maximum floor in the building
                     - series: Building series
                     - building_type: Type of building
                     - extra: Additional information
                     - price: Price in currency units
                     - price_m2: Price per square meter
                     - site: Website source
                     - description: Full description
                     - score: Location score
        """
        # Set default values for common attributes
        self.id = None
        self.site_id = None
        self.district = None
        self.street = None
        self.nr_of_rooms = None
        self.area_m2 = None
        self.floor = None
        self.floor_max = None
        self.series = None
        self.building_type = None
        self.extra = None
        self.price = None
        self.price_m2 = None
        self.site = None
        self.description = None
        self.score = None

        # Update with provided values
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self):
        return f"Ad(id={self.id}, district={self.district}, street={self.street}, " \
               f"price={self.price}, area={self.area_m2}m², rooms={self.nr_of_rooms})"

    @classmethod
    def from_db_row(cls, row, scorer=None):
        """
        Create an Ad object from a database row tuple

        Args:
            row: Database row tuple
            scorer: Optional Scorer instance to calculate location score

        Returns:
            Ad: New Ad instance
        """
        # Create a new Ad instance with attributes from the database row
        ad = cls(
            id=row[0],
            site_id=row[1],
            district=row[2],
            street=row[3],
            nr_of_rooms=row[4],
            area_m2=row[5],
            floor=row[6],
            floor_max=row[7],
            series=row[8],
            building_type=row[9],
            extra=row[10],
            price=row[11],
            price_m2=row[12],
            site=row[13],
            description=row[14]
        )

        return ad