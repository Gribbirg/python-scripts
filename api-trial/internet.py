import time

import requests

from apikey import OPEN_WEATHER_API, TIME_API


class FullPlaceInfo:
    def __init__(self, name):
        self.name = name
        self.now_weather = Weather().get_now(name)
        self.future_weather = Weather().get_future(name)
        self.coords = Geo().get_lat_and_lon_by_name(name)
        self.time = Time().get_time(name)

    def __str__(self):
        return f'\nИнформация о городе: {self.name}\n\n' \
               f'{self.now_weather}' \
               f'{self.future_weather}' \
               f'{self.coords}' \
               f'{self.time}'


class Weather:

    def get_future(self, city):
        res = requests.get(
            f"http://api.openweathermap.org/data/2.5/forecast?id=524901&appid={OPEN_WEATHER_API}&q={city}&lang=ru&units"
            f"=metric"
        )
        data = res.json()
        if data['cod'] != '200':
            raise Exception(data['message'])
        data_city = data['city']
        ans = self.ListOfWeatherInfo(
            self.PlaceInfo(
                data_city['name'],
                data_city['country'],
                data_city['sunrise'],
                data_city['sunset']
            )
        )
        for data_weather in data['list']:
            ans.append(self.WeatherInfo(
                data_weather['dt_txt'],
                data_weather['main']['temp'],
                data_weather['main']['feels_like'],
                self.Clouds(
                    data_weather['weather'][0]['main'],
                    data_weather['weather'][0]['description']
                ),
                self.WindInfo(
                    data_weather['wind']['speed'],
                    data_weather['wind']['deg']
                ),
                data_weather['main']['pressure'],
                data_weather['visibility']
            ))
        return ans

    def get_now(self, city):
        res = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?id=524901&appid={OPEN_WEATHER_API}&q={city}&lang=ru"
            f"&units=metric"
        )
        data = res.json()
        if data['cod'] != 200:
            raise Exception(data['message'])

        ans = self.ListOfWeatherInfo(
            self.PlaceInfo(
                data['name'],
                data['sys']['country'],
                data['sys']['sunrise'],
                data['sys']['sunset']
            )
        )
        ans.append(
            self.WeatherInfo(
                Time().get_time(data['name']).current_time,
                data['main']['temp'],
                data['main']['feels_like'],
                self.Clouds(
                    data['weather'][0]['main'],
                    data['weather'][0]['description']
                ),
                self.WindInfo(
                    data['wind']['speed'],
                    data['wind']['deg']
                ),
                data['main']['pressure'],
                data['visibility']
            )
        )
        return ans

    class ListOfWeatherInfo:
        def __init__(self, place):
            self.place = place
            self.list = list()

        def __str__(self):
            res = f'{self.place}\n\n'
            for data in self.list:
                res += f'{data}\n\n'
            return res

        def append(self, data):
            self.list.append(data)

    class WeatherInfo:
        def __init__(self, date_str, temp, temp_feels_like, clouds, wind, pressure, visibility):
            self.date_str = date_str
            self.temp = temp
            self.temp_feels_like = temp_feels_like
            self.clouds = clouds
            self.wind = wind
            self.pressure = pressure
            self.visibility = visibility

        def __str__(self):
            return f'Дата: {self.date_str}\n' \
                   f'Температура: {self.temp} °C, ощущается как {self.temp_feels_like} °C\n' \
                   f'{self.clouds}\n' \
                   f'{self.wind}\n' \
                   f'Давление: {self.pressure} гектопаскалей\n' \
                   f'Видимость: {self.visibility} метров'

    class WindInfo:
        def __init__(self, speed, direction):
            self.speed = speed
            self.direction = int(direction)

        def __str__(self):
            return f'Ветер со скоростью {self.speed} м/с, направлен на {self.str_direction()}'

        def str_direction(self):
            sides = ['север', 'северо-восток', 'восток', 'юго-восток', 'юг', 'юго-запад', 'запад', 'северо-запад']
            deg = 22
            i = 0
            while deg <= self.direction:
                deg += 45
                i += 1
            return sides[i % 8]

    class Clouds:
        def __init__(self, name, description):
            self.name = name
            self.description = description

        def __str__(self):
            return f'Погода: {self.description}'

    class PlaceInfo:
        def __init__(self, city, country, unix_sun_rise, unix_sun_set):
            self.city = city
            self.country = country
            self.gmt = Time().get_time(city).gmt_offset
            self.sun_rise = Time.from_unix_to_str(int(unix_sun_rise), self.gmt)
            self.sun_set = Time.from_unix_to_str(int(unix_sun_set), self.gmt)

        def __str__(self):
            return f'Город: {self.city}\n' \
                   f'Страна: {self.country}\n' \
                   f'Время рассвета: {self.sun_rise}\n' \
                   f'Время заката: {self.sun_set}'


class Time:

    @staticmethod
    def from_unix_to_str(unix_time, city_gmt):
        minute = unix_time // 60 % 60
        hours = (unix_time // 60 // 60 + city_gmt) % 24
        return f'{hours}.{minute}'

    def get_time(self, city):
        res = requests.get(f'https://timezone.abstractapi.com/v1/current_time/?api_key={TIME_API}&location={city}')

        data = res.json()
        if res.status_code != 200:
            if res.status_code == 429:
                time.sleep(1)
                return self.get_time(city)
            raise Exception(data['error']['message'])

        if len(data) == 0:
            raise Exception("Not found")

        return self.TimeInfo(
            data['requested_location'],
            data['timezone_abbreviation'],
            data['timezone_name'],
            data['gmt_offset'],
            data['datetime']
        )

    class TimeInfo:
        def __init__(self, city, abb, timezone_name, gmt_offset, current_time):
            self.city = city
            self.abb = abb
            self.timezone_name = timezone_name
            self.gmt_offset = gmt_offset
            self.current_time = current_time

        def __str__(self):
            return f'Город: {self.city}\n' \
                   f'Часовой пояс: {self.abb} - {self.timezone_name}, {self.gmt_offset}\n' \
                   f'Текущее время: {self.current_time}'


class Geo:
    def get_lat_and_lon_by_name(self, city_name):
        res = requests.get(
            f'http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={OPEN_WEATHER_API}'
        )
        if res.status_code != 200:
            raise Exception(f'Ошибка с кодом {res.status_code}')
        data = res.json()[0]
        return self.Coordinate(
            data['name'],
            data['country'],
            data['state'],
            data['lat'],
            data['lon']
        )

    class Coordinate:

        def __init__(self, city_name, country_code, state, lat, lon):
            self.city_name = city_name
            self.country_code = country_code
            self.state = state
            self.lat = lat
            self.lon = lon

        def __str__(self):
            return f'Город: {self.city_name}\n' \
                   f'Страна: {self.country_code}\n' \
                   f'Область/штат: {self.state}\n' \
                   f'Широта: {self.lat}\n' \
                   f'Долгота: {self.lon}\n'
