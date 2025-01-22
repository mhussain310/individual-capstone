CREATE TABLE IF NOT EXISTS student.mh_current_weather (
        local_time TIMESTAMP PRIMARY KEY,
        location_name TEXT NOT NULL,
        region TEXT,
        country TEXT,
        lat FLOAT,
        lon FLOAT,
        tz_id TEXT,
        localtime_epoch INT UNIQUE,
        last_updated_epoch INT,
        last_updated TIMESTAMP,
        temp_c FLOAT,
        temp_f FLOAT,
        is_day INT,
        condition_text TEXT,
        condition_icon TEXT,
        condition_code INT,
        wind_mph FLOAT,
        wind_kph FLOAT,
        wind_degree INT,
        wind_dir TEXT,
        pressure_mb FLOAT,
        pressure_in FLOAT,
        precip_mm FLOAT,
        precip_in FLOAT,
        humidity INT,
        cloud INT,
        feelslike_c FLOAT,
        feelslike_f FLOAT,
        windchill_c FLOAT,
        windchill_f FLOAT,
        heatindex_c FLOAT,
        heatindex_f FLOAT,
        dewpoint_c FLOAT,
        dewpoint_f FLOAT,
        vis_km FLOAT,
        vis_miles FLOAT,
        uv FLOAT,
        gust_mph FLOAT,
        gust_kph FLOAT,
        co FLOAT,
        no2 FLOAT,
        o3 FLOAT,
        so2 FLOAT,
        pm2_5 FLOAT,
        pm10 FLOAT,
        us_epa_index INT,
        gb_defra_index INT
    );