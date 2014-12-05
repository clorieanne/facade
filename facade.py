"""import on the first class #WeatherProvide """
import urllib
import urllib2

"""import on the second class #Parser"""
from datetime import datetime
import json

"""import on the third class #Cache"""
from datetime import timedelta
import pickle 

#first class
class WeatherProvider(object):
  def __init__(self):
    self.api_url = 'http://api.openweathermap.org/data/2.5/forecast?q={},{}'

  def get_weather_data(self, city, country):
    city = urllib.quote(city)
    url = self.api_url.format(city, country)
    return urllib2.urlopen(url).read()

#second class
class Parser(object):
  def parse_weather_data(self, weather_data):
    parsed = json.loads(weather_data)
    start_date = None
    result = []

    for data in parsed['list']:
      date = datetime.strptime(data['dt_txt'], '%Y-%m-%d %H:%M:%S')
      start_date = start_date or date
      if start_date.day != date.day:
      	return result
      result.append(data['main']['temp'])

#third class 
class Cache(object):
  def __init__(self, filename):
    self.filename = filename

  def save(self, obj):
    with open(self.filename, 'w') as file:
      dct = {
        'obj' : obj,
        'expired': datetime.utcnow() + timedelta(hours=3)
      }
      pickle.dump(dct, file)

  def load(self):
    try:
      with open (self.filename) as file:
        result = pickle.load(file)
        if result['expired'] > datetime.utcnow():
          return result['obj']
    except IOError:
    	pass

#fourth class (Kelvin to Celsius)
class Converter(object):
  def from_kelvin_to_celcius(self, kelvin):
    return kelvin - 273.15

#fifth class (receives iterable weather forecast for a day and calculates the median forecast)
class Weather(object):
  """docstring for Weather"""
  def __init__(self, data):
    result = 0

    for r in data:
      result += r

    self.temperature = result / len(data)
  
# the FACADE class  
class Facade(object):
  def get_forecast(self, city, country):
    cache = Cache('myfile')
    cache_result = cache.load()
    if cache_result:
      return cache_result
    else:
      weather_provider = WeatherProvider()
      weather_data = weather_provider.get_weather_data(city, country)
      parser = Parser()
      parsed_data = parser.parse_weather_data(weather_data)
      weather = Weather(parsed_data)
      converter = Converter()
      temperature_celcius = converter.from_kelvin_to_celcius(weather.temperature)
      cache.save(temperature_celcius)
      return temperature_celcius
    
if __name__ == '__main__':
  facade = Facade()
  print facade.get_forecast('London', 'UK')
		

