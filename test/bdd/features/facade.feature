Feature: As a customer, I want to check the weather of a
		 certain city and country.

		Scenario: Getting the weather
		Given the city "London" and the country "UK"
		When I run the program
		Then I was able to get the "5.358"