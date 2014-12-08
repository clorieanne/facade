from lettuce import step
from facade.facade import Facade
import os
from nose.tools import assert_equal

@step(u'Given the city "([^"]*)" and the country "([^"]*)"')
def given_the_city_group1_and_the_country_group2(step, city, country):
  facade = Facade()
  weather = facade.get_forecast(city, country)
  #assert True

@step(u'When I run the program')
def when_i_run_the_program(step):
  os.system('python facade.py')

@step(u'Then I was able to get the "([^"]*)"')
def then_i_was_able_to_get_the_group1(step, weather):
  facade = Facade()
  assert_equal(str(weather), str(facade.get_forecast('London', 'UK')))