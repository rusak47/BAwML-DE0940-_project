\copy ads(site_id, district, street, nr_of_rooms,area_m2,floor,floor_max,series,building_type,extra,price,price_m2,site,description) FROM '/var/lib/postgresql/output.csv' DELIMITER ',' CSV HEADER

CREATE TABLE ad_scores (
    ad_id INT REFERENCES ads(id) ON DELETE CASCADE,
    lon FLOAT DEFAULT NULL,
    lat FLOAT DEFAULT NULL,
    score FLOAT NOT NULL,
    PRIMARY KEY (ad_id)
);

SELECT COUNT(*) AS record_count FROM ads;

SELECT COUNT(distinct ad_id) AS record_count FROM ad_scores;