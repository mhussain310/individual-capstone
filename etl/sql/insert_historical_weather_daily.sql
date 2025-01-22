INSERT INTO student.mh_historical_weather_daily (
        date, location_name, location_region, location_country, location_lat, location_lon,
        location_tz_id, location_localtime, date_epoch, maxtemp_c, maxtemp_f, mintemp_c,
        mintemp_f, avgtemp_c, avgtemp_f, maxwind_mph, maxwind_kph, totalprecip_mm, totalprecip_in,
        totalsnow_cm, avgvis_km, avgvis_miles, avghumidity, daily_will_it_rain,
        daily_chance_of_rain, daily_will_it_snow, daily_chance_of_snow, condition_text,
        condition_icon, condition_code, uv, sunrise, sunset, moonrise, moonset, moon_phase,
        moon_illumination
    ) VALUES (
        :date, :location_name, :location_region, :location_country, :location_lat, :location_lon,
        :location_tz_id, :location_localtime, :date_epoch, :maxtemp_c, :maxtemp_f, :mintemp_c,
        :mintemp_f, :avgtemp_c, :avgtemp_f, :maxwind_mph, :maxwind_kph, :totalprecip_mm,
        :totalprecip_in, :totalsnow_cm, :avgvis_km, :avgvis_miles, :avghumidity, :daily_will_it_rain,
        :daily_chance_of_rain, :daily_will_it_snow, :daily_chance_of_snow, :condition_text,
        :condition_icon, :condition_code, :uv, :sunrise, :sunset, :moonrise, :moonset, :moon_phase,
        :moon_illumination
    ) ON CONFLICT (date) DO NOTHING