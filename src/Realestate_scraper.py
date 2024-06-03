from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import pandas as pd
import csv

class RealEstateScraper:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = webdriver.Chrome()
    
    def login(self):
        try:
            # Navigate to the MagicBricks login page
            self.driver.get("https://accounts.magicbricks.com/userauth/login")

            # Wait for the mobile number input to be visible and enter the mobile number
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "emailOrMobile"))
            ).send_keys(self.username)

            self.driver.find_element(By.ID, "btnStep1").click()

            # Wait for the password field to be visible and enter the password
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "passwordInput"))
            ).send_keys(self.password)

            self.driver.find_element(By.ID, "btnLogin").click()

            # Wait until login is successful
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "user-profile"))
            )

            print("Login successful.")
        except Exception as e:
            print(f"Login failed: {e}")
            self.driver.quit()

 # Data Extraction task from particular cities here we are using BeautifulSoup & request library

    def scrape_properties(self, cities):
        try:
           for city in cities:
            # Navigate to the search page
              self.driver.get("https://www.magicbricks.com/")

            # Find the search box, enter the location, and press Enter or click the search button
              search_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "keyword"))
              )
              search_input.clear()
              search_input.send_keys(city)

              search_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "mb-search__btn"))
              )
              search_button.click()

            # Wait for the search results to load
              time.sleep(5)

            # Get the page source
              page_source = self.driver.page_source

            # Parse the page source with BeautifulSoup
              soup = BeautifulSoup(page_source, 'html.parser')

            # Initialize lists to store data
              titles, prices, landmarks, price_per_sqfts, furnishings, area_sqft = [], [], [], [], [], []

            # Extract data using BeautifulSoup
              title_elements = soup.find_all(class_='mb-srp__card--title')
              for element in title_elements:
                titles.append(element.get_text(strip=True))
            
              area_elements = soup.find_all(class_='mb-srp__card__summary--value')
              for element in area_elements:
                area_sqft.append(element.get_text(strip=True))

              price_elements = soup.find_all(class_='mb-srp__card__price--amount')
              for element in price_elements:
                prices.append(element.get_text(strip=True))

              landmark_elements = soup.find_all(class_='mb-srp__card__developer--name--highlight')
              for element in landmark_elements:
                landmarks.append(element.get_text(strip=True))

              price_sqft_elements = soup.find_all(class_='mb-srp__card__price--size')
              for element in price_sqft_elements:
                price_per_sqfts.append(element.get_text(strip=True))

              furnish_elements = soup.find_all(class_='mb-srp__card__summary--value')
              for element in furnish_elements:
                furnishings.append(element.get_text(strip=True))

            # Ensure all lists are of the same length
              max_length = max(len(titles), len(area_sqft), len(prices), len(landmarks), len(price_per_sqfts), len(furnishings))

              titles += ['Nan'] * (max_length - len(titles))
              area_sqft += ['Nan'] * (max_length - len(area_sqft))
              prices += ['Nan'] * (max_length - len(prices))
              landmarks += ['Nan'] * (max_length - len(landmarks))
              price_per_sqfts += ['Nan'] * (max_length - len(price_per_sqfts))
              furnishings += ['Nan'] * (max_length - len(furnishings))

            # Create a DataFrame from the extracted data
              data = {
                'Title': titles,
                'Area_sqft': area_sqft,
                'Price': prices,
                'Landmark': landmarks,
                'Price per Sqft': price_per_sqfts,
                'Furnishing': furnishings
              }
              df = pd.DataFrame(data)

            # Save data to CSV
              df.to_csv("property_data.csv", index=False)
              print("Data extraction successful and saved to 'property_data.csv'.")

        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            self.driver.quit()

if __name__ == "__main__":
    username = int(input('Enter your Number :'))
    password = input('Enter your password :')
    cities = ["Ahmedabad", "Bengaluru", "Chennai", "Delhi", "Gurgaon", "Kolkata", "Mumbai", "Pune"]
    scraper = RealEstateScraper(username, password)
    scraper.login()
    scraper.scrape_properties(cities)