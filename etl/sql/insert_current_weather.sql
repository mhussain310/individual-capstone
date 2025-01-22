INSERT INTO student.current_weather_mh_de11 (
        location_name, region, country, latitude, longitude, local_time,
        temp_c, temp_f, condition, wind_mph, wind_kph, wind_degree, wind_dir,
        pressure_mb, humidity, cloud, feelslike_c, feelslike_f,
        air_quality_co, air_quality_no2, air_quality_o3, air_quality_so2,
        air_quality_pm2_5, air_quality_pm10, air_quality_us_epa_index, air_quality_gb_defra_index
    )
    VALUES (
        :location_name, :region, :country, :latitude, :longitude, :local_time,
        :temp_c, :temp_f, :condition, :wind_mph, :wind_kph, :wind_degree, :wind_dir,
        :pressure_mb, :humidity, :cloud, :feelslike_c, :feelslike_f,
        :air_quality_co, :air_quality_no2, :air_quality_o3, :air_quality_so2,
        :air_quality_pm2_5, :air_quality_pm10, :air_quality_us_epa_index, :air_quality_gb_defra_index
    )
    ON CONFLICT (location_name, local_time)
    DO UPDATE SET
        temp_c = EXCLUDED.temp_c,
        temp_f = EXCLUDED.temp_f,
        condition = EXCLUDED.condition,
        wind_mph = EXCLUDED.wind_mph,
        wind_kph = EXCLUDED.wind_kph,
        wind_degree = EXCLUDED.wind_degree,
        wind_dir = EXCLUDED.wind_dir,
        pressure_mb = EXCLUDED.pressure_mb,
        humidity = EXCLUDED.humidity,
        cloud = EXCLUDED.cloud,
        feelslike_c = EXCLUDED.feelslike_c,
        feelslike_f = EXCLUDED.feelslike_f,
        air_quality_co = EXCLUDED.air_quality_co,
        air_quality_no2 = EXCLUDED.air_quality_no2,
        air_quality_o3 = EXCLUDED.air_quality_o3,
        air_quality_so2 = EXCLUDED.air_quality_so2,
        air_quality_pm2_5 = EXCLUDED.air_quality_pm2_5,
        air_quality_pm10 = EXCLUDED.air_quality_pm10,
        air_quality_us_epa_index = EXCLUDED.air_quality_us_epa_index,
        air_quality_gb_defra_index = EXCLUDED.air_quality_gb_defra_index;