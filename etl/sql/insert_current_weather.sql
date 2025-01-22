INSERT INTO student.mh_current_weather (
        local_time, location_name, region, country, lat, lon, tz_id, localtime_epoch,
        last_updated_epoch, last_updated, temp_c, temp_f, is_day,
        condition_text, condition_icon, condition_code,
        wind_mph, wind_kph, wind_degree, wind_dir,
        pressure_mb, pressure_in, precip_mm, precip_in, humidity, cloud,
        feelslike_c, feelslike_f, windchill_c, windchill_f, heatindex_c, heatindex_f, dewpoint_c, dewpoint_f,
        vis_km, vis_miles, uv, gust_mph, gust_kph,
        co, no2, o3, so2, pm2_5, pm10, us_epa_index, gb_defra_index
    ) VALUES (
        :local_time, :location_name, :region, :country, :lat, :lon, :tz_id, :localtime_epoch,
        :last_updated_epoch, :last_updated, :temp_c, :temp_f, :is_day,
        :condition_text, :condition_icon, :condition_code,
        :wind_mph, :wind_kph, :wind_degree, :wind_dir,
        :pressure_mb, :pressure_in, :precip_mm, :precip_in, :humidity, :cloud,
        :feelslike_c, :feelslike_f, :windchill_c, :windchill_f, :heatindex_c, :heatindex_f, :dewpoint_c, :dewpoint_f,
        :vis_km, :vis_miles, :uv, :gust_mph, :gust_kph,
        :co, :no2, :o3, :so2, :pm2_5, :pm10, :us_epa_index, :gb_defra_index
    ) ON CONFLICT (local_time) DO NOTHING;