class Ad:
    def __init__(self, id, site_id, district, street, nr_of_rooms, area_m2, floor, 
                 floor_max, series, building_type, extra, price, price_m2, site, description):
        self.id = id
        self.site_id = site_id
        self.district = district
        self.street = street
        self.nr_of_rooms = nr_of_rooms
        self.area_m2 = area_m2
        self.floor = floor
        self.floor_max = floor_max
        self.series = series
        self.building_type = building_type
        self.extra = extra
        self.price = price
        self.price_m2 = price_m2
        self.site = site
        self.description = description

    def __str__(self):
        return f"Ad(id={self.id}, district={self.district}, street={self.street}, " \
               f"price={self.price}, area={self.area_m2}m², rooms={self.nr_of_rooms})"

    @classmethod
    def from_db_row(cls, row):
        """Create an Ad object from a database row tuple"""
        return cls(
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