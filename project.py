#Yousuf MUhammud and Danial Khurshid 
import threading
import csv
import os
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException, ElementClickInterceptedException, WebDriverException
from datetime import datetime, timedelta
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import re
from selenium_stealth import stealth
from pyvirtualdisplay import Display
import subprocess
import subprocess
import cv2
import numpy as np
import mss
import pyairports
from dotenv import load_dotenv
from selenium.webdriver.chrome.service import Service



def start_recording(video_path):
    sct = mss.mss()
    monitor = sct.monitors[1]

    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out = cv2.VideoWriter(video_path, fourcc, 8.0, (monitor["width"], monitor["height"]))

    while True:
        img = sct.grab(monitor)
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
        out.write(frame)


def get_random_user_agent():
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0'
    ]
    return random.choice(user_agents)

driver_mutex = threading.Lock()

def oneway(departure, ending, departure_date):
    user_agent = get_random_user_agent()
    print(f"Using User-Agent: {user_agent}")
    
    options = uc.ChromeOptions()
    options.add_argument(f"user-agent={user_agent}")
    
    driver = uc.Chrome(options=options, executable_path=ChromeDriverManager().install())
    driver.maximize_window()
    driver.implicitly_wait(10)
    
    driver.get("https://www.expedia.com/")
    
    try:
        flight_xpath = '//a[@aria-controls="search_form_product_selector_flights"]'
        flight_element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, flight_xpath)))
        flight_element.click()
        time.sleep(1)

        oneway_xpath = '//a[@aria-controls="FlightSearchForm_ONE_WAY"]'
        oneway_element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, oneway_xpath)))
        oneway_element.click()
        time.sleep(1)

        beginning_xpath = '//button[@aria-label="Leaving from"]'
        beginning_element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, beginning_xpath)))
        beginning_element.click()
        time.sleep(1)

        input_field = driver.find_element(By.ID, 'origin_select')
        input_field.send_keys(departure)
        time.sleep(1)

        beginning_xpath1 = driver.find_element(By.XPATH, '//*[@data-stid="origin_select-result-item-button"]')
        beginning_xpath1.click()
        time.sleep(1)

        ending_xpath = '//*[@data-stid="destination_select-menu-trigger"]'
        ending_element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, ending_xpath)))
        ending_element.click()
        time.sleep(1)

        input_field_ending = driver.find_element(By.ID, 'destination_select')
        input_field_ending.send_keys(ending)
        time.sleep(1)

        ending_xpath1 = driver.find_element(By.XPATH, '//*[@data-stid="destination_select-result-item-button"]')
        ending_xpath1.click()
        time.sleep(1)

        date_path = driver.find_element(By.XPATH, '//*[@data-testid="uitk-date-selector-input1-default"]')
        time.sleep(2)
        date_path.click()
        
        departure_date_obj = datetime.strptime(departure_date, "%Y-%m-%d")

        # Format the date to match the aria-label format in the HTML
        formatted_date = departure_date_obj.strftime("%b %d, %Y")
        print(f"Formatted Date: {formatted_date}")

        # Create the XPath expression for the button with the correct aria-label
        trip_date_xpath = f'//button[contains(@class, "uitk-date-picker-day") and contains(@aria-label, "{formatted_date}")]'
        selected_date_xpath = f'//button[contains(@class, "uitk-date-picker-day") and contains(@aria-label, "{formatted_date}") and contains(@class, "selected")]'
        done_xpath = '//*[@data-stid="apply-date-selector"]'
        print(f"XPath: {trip_date_xpath}")

        try:
            # Check if the date is already selected
            selected_date_element = driver.find_element(By.XPATH, selected_date_xpath)
            print("Date is already selected.")
            
            # Click the "Done" button
            done_element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, done_xpath))
            )
            done_element.click()
            print("Done button clicked.")
            
        except NoSuchElementException:
            print("Date is not already selected, navigating the calendar.")
            
            trip_date_exact = None
            while not trip_date_exact:
                try:
                    trip_date_exact = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, trip_date_xpath))
                    )
                    trip_date_exact.click()
                    print("Date selected successfully.")
                    time.sleep(1)

                    # Click the "Done" button
                    done_element = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, done_xpath))
                    )
                    done_element.click()
                    print("Done button clicked.")
                    break

                except TimeoutException:
                    next_button = '//*[@data-stid="uitk-calendar-navigation-controls-next-button"]'
                    driver.find_element(By.XPATH, next_button).click()
                    print("Next button clicked.")
                    time.sleep(1)  # Adding a short delay to allow the calendar to load
        
        search_button_xpath = driver.find_element(By.ID, 'search_button')
        time.sleep(1)
        search_button_xpath.click()
        time.sleep(5)

        nonestop_xpath = '/html/body[@id="flight-search-page"]/div[@id="app-flights-shopping-pwa"]/div[@id="app-layer-manager"]/div[@id="app-layer-base"]/div[@class="uitk-view"]/div[@class="uitk-view-row uitk-view-row-theme-primary uitk-view-row-layout-fullwidth uitk-view-row-adslot-true"][2]/div[@class="uitk-spacing uitk-spacing-margin-blockstart-two"][1]/div[@class="uitk-layout-grid uitk-layout-grid-has-auto-columns uitk-layout-grid-has-columns-by-large uitk-layout-grid-has-columns-by-medium uitk-layout-grid-has-columns uitk-layout-grid-has-space uitk-layout-grid-display-grid"]/div[@class="uitk-layout-grid-item uitk-layout-grid-item-has-column-start"]/fieldset/form[@class="uitk-form"]/div[@class="uitk-spacing uitk-spacing-margin-blockstart-unset"]/div[@class="uitk-spacing uitk-spacing-margin-blockstart-six"][1]/div/fieldset/div[@class="uitk-layout-flex uitk-layout-flex-align-items-center uitk-layout-flex-gap-two"][1]/div[@class="uitk-layout-flex-item uitk-layout-flex-item-flex-grow-1 uitk-spacing uitk-spacing-padding-inlinestart-one"]/div[@class="uitk-layout-flex uitk-layout-flex-flex-wrap-nowrap uitk-checkbox"]/div[@class="uitk-layout-flex-item uitk-layout-flex-item-flex-grow-1 uitk-checkbox-content"]/label[@class="uitk-checkbox-label"]/span[@class="uitk-checkbox-label-content"]'
        onestop_xpath = '/html/body[@id="flight-search-page"]/div[@id="app-flights-shopping-pwa"]/div[@id="app-layer-manager"]/div[@id="app-layer-base"]/div[@class="uitk-view"]/div[@class="uitk-view-row uitk-view-row-theme-primary uitk-view-row-layout-fullwidth uitk-view-row-adslot-true"][2]/div[@class="uitk-spacing uitk-spacing-margin-blockstart-two"][1]/div[@class="uitk-layout-grid uitk-layout-grid-has-auto-columns uitk-layout-grid-has-columns-by-large uitk-layout-grid-has-columns-by-medium uitk-layout-grid-has-columns uitk-layout-grid-has-space uitk-layout-grid-display-grid"]/div[@class="uitk-layout-grid-item uitk-layout-grid-item-has-column-start"]/fieldset/form[@class="uitk-form"]/div[@class="uitk-spacing uitk-spacing-margin-blockstart-unset"]/div[@class="uitk-spacing uitk-spacing-margin-blockstart-six"][1]/div/fieldset/div[@class="uitk-layout-flex uitk-layout-flex-align-items-center uitk-layout-flex-gap-two"][2]/div[@class="uitk-layout-flex-item uitk-layout-flex-item-flex-grow-1 uitk-spacing uitk-spacing-padding-inlinestart-one"]/div[@class="uitk-layout-flex uitk-layout-flex-flex-wrap-nowrap uitk-checkbox"]/div[@class="uitk-layout-flex-item uitk-layout-flex-item-flex-grow-1 uitk-checkbox-content"]/label[@class="uitk-checkbox-label"]/span[@class="uitk-checkbox-label-content"]'
        twostop_xpath = '/html/body[@id="flight-search-page"]/div[@id="app-flights-shopping-pwa"]/div[@id="app-layer-manager"]/div[@id="app-layer-base"]/div[@class="uitk-view"]/div[@class="uitk-view-row uitk-view-row-theme-primary uitk-view-row-layout-fullwidth uitk-view-row-adslot-true"][2]/div[@class="uitk-spacing uitk-spacing-margin-blockstart-two"][1]/div[@class="uitk-layout-grid uitk-layout-grid-has-auto-columns uitk-layout-grid-has-columns-by-large uitk-layout-grid-has-columns-by-medium uitk-layout-grid-has-columns uitk-layout-grid-has-space uitk-layout-grid-display-grid"]/div[@class="uitk-layout-grid-item uitk-layout-grid-item-has-column-start"]/fieldset/form[@class="uitk-form"]/div[@class="uitk-spacing uitk-spacing-margin-blockstart-unset"]/div[@class="uitk-spacing uitk-spacing-margin-blockstart-six"][1]/div/fieldset/div[@class="uitk-layout-flex uitk-layout-flex-align-items-center uitk-layout-flex-gap-two"][3]/div[@class="uitk-layout-flex-item uitk-layout-flex-item-flex-grow-1 uitk-spacing uitk-spacing-padding-inlinestart-one"]/div[@class="uitk-layout-flex uitk-layout-flex-flex-wrap-nowrap uitk-checkbox"]/div[@class="uitk-layout-flex-item uitk-layout-flex-item-flex-grow-1 uitk-checkbox-content"]/label[@class="uitk-checkbox-label"]/span[@class="uitk-checkbox-label-content"]'
        
        if len(driver.find_elements(By.XPATH, nonestop_xpath)) > 0:
            driver.find_element(By.XPATH, nonestop_xpath).click()
            time.sleep(1)

        if len(driver.find_elements(By.XPATH, onestop_xpath)) > 0:
            driver.find_element(By.XPATH, onestop_xpath).click()
            time.sleep(1)

        if len(driver.find_elements(By.XPATH, twostop_xpath)) > 0:
            driver.find_element(By.XPATH, twostop_xpath).click()
            time.sleep(1)

        time.sleep(1)
        sort_dropdown_xpath = driver.find_element(By.XPATH, '//*[@id="sort-filter-dropdown-SORT"]')
        time.sleep(1)
        sort_dropdown_xpath.click()
        time.sleep(1)
        sort_dropdown_xpath.send_keys(Keys.DOWN)
        time.sleep(1)
        sort_dropdown_xpath.send_keys(Keys.ENTER)
        time.sleep(5)

        generalized_available_xpath = "//button[contains(@stid, 'FLIGHTS_DETAILS_AND_FARES-index-') and contains(@data-test-id, 'select-link')]"
        available_flights = driver.find_elements(By.XPATH, generalized_available_xpath)
        
        if len(available_flights) > 0:
            flights = []
            for item in available_flights[:5]:
                # Extract text and split it to capture all necessary details
                flight_details = item.find_element(By.XPATH, ".//span").text.split(", ")

                if len(flight_details) < 3:
                    continue

                # Handle the case for Multiple Airlines
                if 'multipleAirlines flight' in flight_details[0]:
                    flight_name = flight_details[0].split('for')[-1].strip().title()
                else:
                    flight_name = flight_details[0].split('for')[-1].strip().title()

                departing = flight_details[1].strip().replace("at", ":").title() if len(flight_details) > 1 else "N/A"
                arriving = flight_details[2].strip().replace("at", ":").title() if len(flight_details) > 2 else "N/A"

                # Extract additional details
                price = "N/A"
                seats_left = "N/A"
                days_later = "N/A"
                total_travel_time = "N/A"
                stops = "N/A"
                layovers = "N/A"

                for detail in flight_details:
                    if "Priced at $" in detail:
                        price = detail.split("Priced at $")[1].split(" ")[0].replace(",", "").strip()
                    if "One way per traveler" in detail and "left at this price" in detail:
                        seats_left = detail.split("left at this price")[0].split()[-1].strip()
                    if "Arrives" in detail and "days later" in detail:
                        days_later = detail.split("Arrives")[1].split("days later")[0].strip()
                    

# Update the code to handle various formats of the travel time details
# Update the code to handle various formats of the travel time details
                    if "total travel time" in detail:
                        try:
                            total_travel_time = detail.split("total travel time")[0]
                            if "left at this price." in total_travel_time:
                                total_travel_time = total_travel_time.split("left at this price.")[1].strip()
                            elif "One way per traveler." in total_travel_time:
                                total_travel_time = total_travel_time.split("One way per traveler.")[1].strip()
                            elif "Arrives" in total_travel_time:
                                total_travel_time = total_travel_time.split("Arrives")[1].strip()
                            else:
                                total_travel_time = total_travel_time.strip()
                        except IndexError:
                            total_travel_time = "N/A"


                    if "stop" in detail:
                        stops = detail.split(" ")[0].strip()
                    # Adjust the code for extracting layovers
                    if "Layover for" in detail:
                        layovers = detail.split("Layover for")[1:]  # Split by "Layover for" and skip the first part
                        layovers = [f"Layover for {layover.strip()}" for layover in layovers]  # Reattach "Layover for" and strip whitespace
                        layovers = " • ".join(layovers)  # Join the layovers back together with " • "


                flights.append((flight_name, departing, arriving, f"${price}", seats_left, total_travel_time, stops, layovers))

            print(f"Conditions satisfied for: Departure: {departure}, Arrival: {ending}, Date: {departure_date}")

            # Define the file path
            file_path = os.path.abspath("data.csv")

            # Write the flights data to a CSV file
            with open(file_path, "w", newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Flight", "Departure Time", "Arrival Time", "Price", "Seats Left", "Total Travel Time", "Stops", "Layovers"])
                writer.writerows(flights)

            print(f"Data written to {file_path} successfully.")
            return flights
        else:
            print(f'No flights found for: Departure: {departure}, Arrival: {ending}, Date: {departure_date}')
            return []
    finally:
        time.sleep(10)

#use this function for all addition things
def parse_duration(duration_str):
    hours = 0
    minutes = 0
    if 'hr' in duration_str:
        hours = int(duration_str.split('hr')[0].strip())
        duration_str = duration_str.split('hr')[1].strip()
    if 'min' in duration_str:
        minutes = int(duration_str.split('min')[0].strip())
    return timedelta(hours=hours, minutes=minutes)






def format_travel_time(total_minutes):
    hours = total_minutes // 60
    minutes = total_minutes % 60
    return f"{hours} hr {minutes} min"

total_travel_time1 = 0
total_travel_time2 = 0



# Call the function to test with initial departure input 
def parse_durations(duration_str):
    hours = 0
    minutes = 0
    if 'hour' in duration_str:
        hours_part = duration_str.split('hour')[0].strip()
        hours = int(hours_part.split()[0].strip())
        duration_str = 'hour'.join(duration_str.split('hour')[1:]).strip()
    if 'minutes' in duration_str:
        minutes_part = duration_str.split('minute')[0].strip()
        minutes = int(minutes_part.split()[-1].strip())
    return timedelta(hours=hours, minutes=minutes)


def setup_stealth(driver):
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True)




def roundTrip(driver, departure, ending, departure_date, returning_date):
    print("Loading environment variables for Expedia...")
    load_dotenv('C:\\PythonStuff\\.env')
    
    chrome_path = os.getenv('CHROME_PATH')
    chromedriver_path = os.getenv('CHROMEDRIVER_PATH')
    print(f"Chrome path: {chrome_path}")
    print(f"ChromeDriver path: {chromedriver_path}")

    if not chrome_path or not chromedriver_path:
        print("Error: CHROME_PATH or CHROMEDRIVER_PATH not set.")
        return

    user_agent = get_random_user_agent()
    print(f"Using User-Agent: {user_agent}")

    options = Options()
    options.binary_location = chrome_path
    options.add_argument("--headless")
    options.add_argument("--window-size=1656,1080")
    options.add_argument("--start-maximized")
    print("Chrome options set.")

    for attempt in range(3):
        try:
            print("Initializing WebDriver for Expedia...")
            driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)
            break
        except WebDriverException as e:
            print(f"Error initializing WebDriver for Expedia: {e}")
            if attempt < 2:
                print("Retrying...")
                time.sleep(10)
            else:
                print("Failed to initialize WebDriver for Expedia after retries.")
                return
    
    # Apply stealth mode
    setup_stealth(driver)
    driver.implicitly_wait(5)
    
    driver.get("https://www.expedia.com/")
    print("im working")
    flight_xpath = '//a[@aria-controls="search_form_product_selector_flights"]'
    time.sleep(1)
    flight_element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, flight_xpath)))
    flight_element.click()
    time.sleep(1)
    beginning_xpath = '//button[@aria-label="Leaving from"]'
    beginning_element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, beginning_xpath)))
    beginning_element.click()
    time.sleep(1)
    input_field = driver.find_element(By.ID, 'origin_select')
    input_field.send_keys(departure)
    time.sleep(1)
    beginning_xpath1 = driver.find_element(By.XPATH, '//*[@data-stid="origin_select-result-item-button"]')
    beginning_xpath1.click()
    time.sleep(1)
    ending_xpath = '//*[@data-stid="destination_select-menu-trigger"]'
    ending_element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, ending_xpath)))
    ending_element.click()
    time.sleep(1)

    input_field_ending = driver.find_element(By.ID, 'destination_select')
    input_field_ending.send_keys(ending)
    time.sleep(1)

    ending_xpath1 = driver.find_element(By.XPATH, '//*[@data-stid="destination_select-result-item-button"]')
    ending_xpath1.click()
    time.sleep(1)


    date = driver.find_element(By.XPATH, '//*[@id="FlightSearchForm_ROUND_TRIP"]/div/div[2]/div/div/div/div/button')
    date.click()
    time.sleep(1)


    departure_date_obj = datetime.strptime(departure_date, "%A, %B %d, %Y")
    returning_date_obj = datetime.strptime(returning_date, "%A, %B %d, %Y")

    beginning_formatted_date = departure_date_obj.strftime("%A, %B %d, %Y")
    formatted_date_returning = returning_date_obj.strftime("%A, %B %d, %Y")

    # Remove leading zero from day
    beginning_formatted_date_alt = departure_date_obj.strftime("%A, %B %d, %Y").replace(" 0", " ")
    formatted_date_returning_alt = returning_date_obj.strftime("%A, %B %d, %Y").replace(" 0", " ")

    print(f"Leaving date: {beginning_formatted_date}")
    print(f"Coming back date: {formatted_date_returning}")

    beginning_date_xpath = f'//div[@aria-label="{beginning_formatted_date}"]/parent::div[@class="uitk-day-button uitk-day-selectable uitk-day-clickable"]'
    beginning_date_xpath_alt = f'//div[@aria-label="{beginning_formatted_date_alt}"]/parent::div[@class="uitk-day-button uitk-day-selectable uitk-day-clickable"]'
    selected_date_xpath = f'//div[@aria-label="{beginning_formatted_date}, Selected date"]/parent::div[@class="uitk-day-button uitk-day-selectable uitk-day-clickable"]'
    selected_date_xpath_alt = f'//div[@aria-label="{beginning_formatted_date_alt}, Selected date"]/parent::div[@class="uitk-day-button uitk-day-selectable uitk-day-clickable"]'
    done_xpath = '//*[@data-stid="apply-date-selector"]'
    print(f"XPath: {beginning_date_xpath}")

    # Select departure date
    try:
        try:
            selected_date_element = driver.find_element(By.XPATH, selected_date_xpath)
        except NoSuchElementException:
            selected_date_element = driver.find_element(By.XPATH, selected_date_xpath_alt)
        print("Date is already selected.")
    except NoSuchElementException:
        print("Date is not already selected, navigating the calendar.")
        trip_date_exact = None
        back_button = '//*[@data-stid="uitk-calendar-navigation-controls-previous-button"]'
        driver.find_element(By.XPATH, back_button).click()
        while not trip_date_exact:
            try:
                try:
                    trip_date_exact = WebDriverWait(driver, 1).until(
                        EC.element_to_be_clickable((By.XPATH, beginning_date_xpath))
                    )
                except TimeoutException:
                    trip_date_exact = WebDriverWait(driver, 1).until(
                        EC.element_to_be_clickable((By.XPATH, beginning_date_xpath_alt))
                    )
                trip_date_exact.click()
                print("Date selected successfully.")
                time.sleep(1)
            except TimeoutException:
                next_button = '//*[@data-stid="uitk-calendar-navigation-controls-next-button"]'
                driver.find_element(By.XPATH, next_button).click()
                print("Next button clicked.")
                time.sleep(1)  # Adding a short delay to allow the calendar to load

    ending_date_xpath = f'//div[@aria-label="{formatted_date_returning}"]/parent::div[@class="uitk-day-button uitk-day-selectable uitk-day-clickable"]'
    ending_date_xpath_alt = f'//div[@aria-label="{formatted_date_returning_alt}"]/parent::div[@class="uitk-day-button uitk-day-selectable uitk-day-clickable"]'
    ending_selected_date_xpath = f'//div[@aria-label="{formatted_date_returning}, Selected date"]/parent::div[@class="uitk-day-button uitk-day-selectable uitk-day-clickable"]'
    ending_selected_date_xpath_alt = f'//div[@aria-label="{formatted_date_returning_alt}, Selected date"]/parent::div[@class="uitk-day-button uitk-day-selectable uitk-day-clickable"]'
    done_xpath = '//*[@data-stid="apply-date-selector"]'
    print(f"XPath: {ending_date_xpath}")

    # Select return date
    try:
        try:
            ending_selected_date_element = driver.find_element(By.XPATH, ending_selected_date_xpath)
        except NoSuchElementException:
            ending_selected_date_element = driver.find_element(By.XPATH, ending_selected_date_xpath_alt)
        print("Date is already selected.")
    except NoSuchElementException:
        print("Date is not already selected, navigating the calendar.")
        ending_trip_date_exact = None
        max_retries = 12  # Set a maximum number of retries
        retries = 0
        while not ending_trip_date_exact and retries < max_retries:
            try:
                try:
                    ending_trip_date_exact = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, ending_date_xpath))
                    )
                except TimeoutException:
                    ending_trip_date_exact = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, ending_date_xpath_alt))
                    )
                ending_trip_date_exact.click()
                print("Date selected successfully.")
                time.sleep(1)
                done = driver.find_element(By.XPATH, done_xpath).click()
                time.sleep(1)
                search_button = driver.find_element(By.ID, 'search_button')
                search_button.click()
                print("Search button clicked.")
                time.sleep(1)
            except TimeoutException:
                next_button = '//*[@data-stid="uitk-calendar-navigation-controls-next-button"]'
                driver.find_element(By.XPATH, next_button).click()
                print("Next button clicked.")
                time.sleep(1)  # Adding a short delay to allow the calendar to load
                retries += 1
            except ElementClickInterceptedException as e:
                print(f"ElementClickInterceptedException: {e}")
                retries += 1
            except NoSuchElementException as e:
                print(f"NoSuchElementException: {e}")
                retries += 1
            except Exception as e:
                print(f"Unexpected exception: {e}")
                retries += 1
        if retries >= max_retries:
            print("Max retries reached. Date not found.")

    nonestop_xpath = '/html/body[@id="flight-search-page"]/div[@id="app-flights-shopping-pwa"]/div[@id="app-layer-manager"]/div[@id="app-layer-base"]/div[@class="uitk-view"]/div[@class="uitk-view-row uitk-view-row-theme-primary uitk-view-row-layout-fullwidth uitk-view-row-adslot-true"][2]/div[@class="uitk-spacing uitk-spacing-margin-blockstart-two"][1]/div[@class="uitk-layout-grid uitk-layout-grid-has-auto-columns uitk-layout-grid-has-columns-by-large uitk-layout-grid-has-columns-by-medium uitk-layout-grid-has-columns uitk-layout-grid-has-space uitk-layout-grid-display-grid"]/div[@class="uitk-layout-grid-item uitk-layout-grid-item-has-column-start"]/fieldset/form[@class="uitk-form"]/div[@class="uitk-spacing uitk-spacing-margin-blockstart-unset"]/div[@class="uitk-spacing uitk-spacing-margin-blockstart-six"][1]/div/fieldset/div[@class="uitk-layout-flex uitk-layout-flex-align-items-center uitk-layout-flex-gap-two"][1]/div[@class="uitk-layout-flex-item uitk-layout-flex-item-flex-grow-1 uitk-spacing uitk-spacing-padding-inlinestart-one"]/div[@class="uitk-layout-flex uitk-layout-flex-flex-wrap-nowrap uitk-checkbox"]/div[@class="uitk-layout-flex-item uitk-layout-flex-item-flex-grow-1 uitk-checkbox-content"]/label[@class="uitk-checkbox-label"]/span[@class="uitk-checkbox-label-content"]'
    onestop_xpath = '/html/body[@id="flight-search-page"]/div[@id="app-flights-shopping-pwa"]/div[@id="app-layer-manager"]/div[@id="app-layer-base"]/div[@class="uitk-view"]/div[@class="uitk-view-row uitk-view-row-theme-primary uitk-view-row-layout-fullwidth uitk-view-row-adslot-true"][2]/div[@class="uitk-spacing uitk-spacing-margin-blockstart-two"][1]/div[@class="uitk-layout-grid uitk-layout-grid-has-auto-columns uitk-layout-grid-has-columns-by-large uitk-layout-grid-has-columns-by-medium uitk-layout-grid-has-columns uitk-layout-grid-has-space uitk-layout-grid-display-grid"]/div[@class="uitk-layout-grid-item uitk-layout-grid-item-has-column-start"]/fieldset/form[@class="uitk-form"]/div[@class="uitk-spacing uitk-spacing-margin-blockstart-unset"]/div[@class="uitk-spacing uitk-spacing-margin-blockstart-six"][1]/div/fieldset/div[@class="uitk-layout-flex uitk-layout-flex-align-items-center uitk-layout-flex-gap-two"][2]/div[@class="uitk-layout-flex-item uitk-layout-flex-item-flex-grow-1 uitk-spacing uitk-spacing-padding-inlinestart-one"]/div[@class="uitk-layout-flex uitk-layout-flex-flex-wrap-nowrap uitk-checkbox"]/div[@class="uitk-layout-flex-item uitk-layout-flex-item-flex-grow-1 uitk-checkbox-content"]/label[@class="uitk-checkbox-label"]/span[@class="uitk-checkbox-label-content"]'
    twostop_xpath = '/html/body[@id="flight-search-page"]/div[@id="app-flights-shopping-pwa"]/div[@id="app-layer-manager"]/div[@id="app-layer-base"]/div[@class="uitk-view"]/div[@class="uitk-view-row uitk-view-row-theme-primary uitk-view-row-layout-fullwidth uitk-view-row-adslot-true"][2]/div[@class="uitk-spacing uitk-spacing-margin-blockstart-two"][1]/div[@class="uitk-layout-grid uitk-layout-grid-has-auto-columns uitk-layout-grid-has-columns-by-large uitk-layout-grid-has-columns-by-medium uitk-layout-grid-has-columns uitk-layout-grid-has-space uitk-layout-grid-display-grid"]/div[@class="uitk-layout-grid-item uitk-layout-grid-item-has-column-start"]/fieldset/form[@class="uitk-form"]/div[@class="uitk-spacing uitk-spacing-margin-blockstart-unset"]/div[@class="uitk-spacing uitk-spacing-margin-blockstart-six"][1]/div/fieldset/div[@class="uitk-layout-flex uitk-layout-flex-align-items-center uitk-layout-flex-gap-two"][3]/div[@class="uitk-layout-flex-item uitk-layout-flex-item-flex-grow-1 uitk-spacing uitk-spacing-padding-inlinestart-one"]/div[@class="uitk-layout-flex uitk-layout-flex-flex-wrap-nowrap uitk-checkbox"]/div[@class="uitk-layout-flex-item uitk-layout-flex-item-flex-grow-1 uitk-checkbox-content"]/label[@class="uitk-checkbox-label"]/span[@class="uitk-checkbox-label-content"]'
    time.sleep(3)
    if len(driver.find_elements(By.XPATH, nonestop_xpath)) > 0:
        driver.find_element(By.XPATH, nonestop_xpath).click()
        time.sleep(1)

    if len(driver.find_elements(By.XPATH, onestop_xpath)) > 0:
        driver.find_element(By.XPATH, onestop_xpath).click()
        time.sleep(1)

    if len(driver.find_elements(By.XPATH, twostop_xpath)) > 0:
        driver.find_element(By.XPATH, twostop_xpath).click()
        time.sleep(1)
    
    time.sleep(1)
    sort_dropdown_xpath = driver.find_element(By.XPATH, '//*[@id="sort-filter-dropdown-SORT"]')
    time.sleep(1)
    sort_dropdown_xpath.click()
    time.sleep(1)
    sort_dropdown_xpath.send_keys(Keys.DOWN)
    time.sleep(1)
    sort_dropdown_xpath.send_keys(Keys.ENTER)
    time.sleep(1)

    generalized_available_xpath = "//button[contains(@stid, 'FLIGHTS_DETAILS_AND_FARES-index-') and contains(@data-test-id, 'select-link')]"
    mainclick = driver.find_elements(By.XPATH, generalized_available_xpath)
    button_xpath = '//button[contains(@class, "uitk-link uitk-expando-link") and span[contains(text(), "Show details")]]'
    flights = []
    columns = [
            'Flight', 'Departure Time of Flight Going to Destination', 'Arrival Time of Flight Going to Destination',
            'Departure Time of Flight Returning', 'Arrival Time of Flight Returning', 'Price', 'Seats Left',
            'Total Travel Time', 'Stops', 'Layovers']
    
    original_window = driver.current_window_handle



    field_1 = '//button[contains(@aria-label, "Flying from") and contains(@class, "uitk-fake-input uitk-form-field-trigger")]'
    field_2 = '//button[contains(@aria-label, "Flying to") and contains(@class, "uitk-fake-input uitk-form-field-trigger")]'
    try:
        # Wait for the button to be clickable and then find the element
        field_1_element = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, field_1)))
        
        # Get the aria-label attribute value
        flying_from = field_1_element.get_attribute("aria-label")
        
        # Extract the part of the string before the second comma
        flying_from = ','.join(flying_from.split(",")[:2])
        
        print(f"Scraped Data: {flying_from}")

    except Exception as e:
        print(f"An error occurred: {e}")


    try:
        # Wait for the button to be clickable and then find the element
        field_2_element = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, field_2)))
        
        # Get the aria-label attribute value
        flying_to = field_2_element.get_attribute("aria-label")
        
        # Extract the part of the string before the second comma
        flying_to = ','.join(flying_to.split(",")[:2])
        
        print(f"Scraped Data: {flying_to}")

    except Exception as e:
        print(f"An error occurred: {e}")



    try:
        for index in range(min(5, len(mainclick))):
            try:
                stopss = "N/A"
                total_travel_time = "N/A"
                total_travel_times = "N/A"
                # Re-fetch the main click elements to avoid stale element reference
                mainclick = driver.find_elements(By.XPATH, generalized_available_xpath)
            except Exception as e:
                print(f'there is an issue with init: {e}')
        
            try:
                try:
                    try:
                        mainclick = driver.find_elements(By.XPATH, generalized_available_xpath)
                        try:
                                mainclick = driver.find_elements(By.XPATH, generalized_available_xpath)
                                flight_detail_departure = mainclick[index].find_element(By.XPATH, ".//span").text.split(", ")
                                print(f"Flight details: {flight_detail_departure}")
                        except Exception as e:
                                print(f"there is an issue with the beg: {e}")

                    except Exception as e:
                        print(f'there is an issue with init: {e}')
                    price = "N/A"
                    flight_name = []
                    departure_info = "N/A"
                    arrival_info = "N/A"
                    return_departure_info = "N/A"
                    return_arrival_info = "N/A"
                    layovers = []  # Initialize layovers as a list
                    webpage_link = "N/A"
                    total_travel_time = "N/A"
                    stops = "N/A"
                except Exception as e:
                    print(f'there is an issue with the code: {e}')
                
                for detail in flight_detail_departure:
                    try:
                        print(f"Processing detail: {detail}")
                        
                        if "Arrives" in detail and "days later" in detail:
                            days_later = detail.split("Arrives")[1].split("days later")[0].strip()
                        
                        if "Priced at" in detail or "total travel time" in detail:
                            try:
                                travel_info = detail.split("per traveler.")[1]
                                total_travel_time = travel_info.split("total travel time")[0].strip()
                                print(f"Travel info: {travel_info}")
                                print(f"Extracted Total Travel Time: {total_travel_time}")
                                if "Arrives" in total_travel_time:
                                    total_travel_time = total_travel_time.split("Arrives")[1].split("later.")[1].strip()
                            except (IndexError, AttributeError) as e:
                                total_travel_time = "N/A"
                                print(f"There is an issue with total travel time: {e}")

                        if re.search(r"\d+ left at this price", detail):
                            try:
                                travel_info = re.split(r"\d+ left at this price\.", detail)[1]
                                total_travel_time = travel_info.split("total travel time")[0].strip()
                                print(f"Travel info: {travel_info}")
                                print(f"Extracted Total Travel Time: {total_travel_time}")
                                if "Arrives" in total_travel_time:
                                    total_travel_time = total_travel_time.split("Arrives")[1].split("later.")[1].strip()
                            except (IndexError, AttributeError) as e:
                                total_travel_time = "N/A"
                                print(f"There is an issue with total travel time: {e}")

                        if "stop" in detail:
                            stopss = detail.split(" ")[0].strip()
                            print(f'expedia first stop: {stopss}')
                        
                    except Exception as e:
                        print(f"There is an issue with processing detail: {e}")

                    print(f"TotalLLLLLLLLL Travel Time: {total_travel_time}")




                    try:
                         
                        # Adjust the code for extracting layovers
                        if "Layover for" in detail:
                            layoverss = detail.split("Layover for")[1:]  # Split by "Layover for" and skip the first part
                            layoverss = [f"Layover for {layoverss.strip()}" for layoverss in layoverss]  # Reattach "Layover for" and strip whitespace
                            layoverss = " • ".join(layoverss)  # Join the layovers back together with " • "
                            print(f"Layovers: {layoverss}")
                        else:
                            layoverss = "N/A"


                    except Exception as e:
                         print(f'there is an issue with layovers: {e}')
                        



                    try:
                        if 'show fare information for' in detail:
                            flight_name1 = detail.split('show fare information for')[-1].split('flight')[0].strip()
                        if flight_name1:
                                print(f"Flight Name: {flight_name1}")
                        else:
                            print("Failed to scrape the flight name")


                    except Exception as e:
                        print(f'there is an issue with show fare information for: {e}')



                    try:
                    # Extract arrival time
                        if "arriving at" in detail:
                            arrival_info = detail.split("arriving at ")[1].strip()
                            print(f"Arrival Time: {arrival_info}")
                    except Exception as e:
                         print(f'there is an issue with arriving at {e}')


                    try:
                        # Extract departure time
                        if "departing at" in detail:
                            departure_info = detail.split("departing at ")[1].strip()
                            print(f"Departure Time: {departure_info}")


                    except Exception as e:
                        print(f'there is an issue with departing at{e}')
                            

                print(f"expedia first stop: {stopss}")
                flight_name.append(flight_name1)
                print(flight_name)

                try:
                    mainclick = driver.find_elements(By.XPATH, generalized_available_xpath)
                    mainclick[index].click()
                    time.sleep(5)
                except Exception as e:
                    print(f"Failed to click main button: {e}")
                    driver.refresh()
                    time.sleep(10)
                    mainclick = driver.find_elements(By.XPATH, generalized_available_xpath)
                    mainclick[index].click()

                # Click the select button
                retries = 3
                for attempt in range(retries):
                    try:
                        select_xpath = '//button[contains(@data-stid, "select-button") and contains(@data-test-id, "select-button")]'
                        select = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, select_xpath))
                        )
                        select.click()
                        print("Successfully clicked the select button")
                        time.sleep(10)
                        break  # Exit the loop if click was successful
                    except StaleElementReferenceException:
                        print(f"Stale element reference encountered. Re-fetching the elements and retrying... Attempt {attempt + 1}")
                        time.sleep(1)  # Adding a short delay before retrying
                    except TimeoutException:
                        print(f"Attempt {attempt + 1} failed: Element not found within the given time")
                        time.sleep(1)  # Adding a short delay before retrying
                    except NoSuchElementException:
                        print(f"Attempt {attempt + 1} failed: Element does not exist")
                        time.sleep(1)  # Adding a short delay before retrying
                    except Exception as e:
                        print(f"Failed to click select button: {e}")
                        break  # Exit the loop on other exceptions
                else:
                    print("Max retries reached. Failed to click select button.")

                try:
                    flight_detail_arrival = mainclick[0].find_element(By.XPATH, ".//span").text.split(", ")
                    print(f"Arrival details: {flight_detail_arrival}")

                    # Your existing code for scraping departure time, total travel time, seats left, layovers, etc.
                    # Ensure to add the appropriate scraping logic here

                except StaleElementReferenceException:
                    print("Stale element reference encountered. Re-fetching the elements and retrying...")
                    
                    # Re-fetch the main click elements to avoid stale element reference
                    mainclick = driver.find_elements(By.XPATH, generalized_available_xpath)
                    
                    # Extract arrival details again
                    flight_detail_arrival = mainclick[0].find_element(By.XPATH, ".//span").text.split(", ")
                    print(f"Arrival details: {flight_detail_arrival}")


                    

                    for details in flight_detail_arrival:
                        try:
                            print(f"Processing details: {details}")
                            
                            if "Arrives" in details and "days later" in details:
                                days_later = details.split("Arrives")[1].split("days later")[0].strip()
                            
                            if "Priced at" in details or "total travel time" in details:
                                try:
                                    travel_infos = details.split("per traveler.")[1]
                                    total_travel_times = travel_infos.split("total travel time")[0].strip()
                                    print(f"Travel infos: {travel_infos}")
                                    print(f"Extracted Total Travel Times: {total_travel_times}")
                                    if "Arrives" in total_travel_times:
                                        total_travel_times = total_travel_times.split("Arrives")[1].split("later.")[1].strip()
                                    total_travel_times = re.sub(r'(\d+ day[s]? later\.)', '', total_travel_times).strip()
                                    print(f"Cleaned Total Travel Times: {total_travel_times}")
                                    break  # Stop looping if total_travel_times is found
                                except (IndexError, AttributeError) as e:
                                    total_travel_times = "N/A"
                                    print(f"There is an issue with total travel times: {e}")

                            if re.search(r"\d+ left at this price", details):
                                try:
                                    travel_infos = re.split(r"\d+ left at this price\.", details)[1]
                                    total_travel_times = travel_infos.split("total travel time")[0].strip()
                                    print(f"Travel infos: {travel_infos}")
                                    print(f"Extracted Total Travel Times: {total_travel_times}")
                                    if "Arrives" in total_travel_times:
                                        total_travel_times = total_travel_times.split("Arrives")[1].split("later.")[1].strip()
                                    total_travel_times = re.sub(r'\d+ day[s]? later\.', '', total_travel_times).strip()
                                    print(f"Cleaned Total Travel Times: {total_travel_times}")
                                    break  # Stop looping if total_travel_times is found
                                except (IndexError, AttributeError) as e:
                                    total_travel_times = "N/A"
                                    print(f"There is an issue with total travel times: {e}")

                        except Exception as e:
                            print(f"There is an issue with processing details: {e}")

                        print(f"Total;;;;;;;;;;;; Travel Times: {total_travel_times}")


                for detailss in flight_detail_arrival:
                    if "stop" in detailss:
                        stopsss = detailss.split(" ")[0].strip()
                        print(f"expedia secound stop : {stopsss}")


                    if 'show fare information for' in detailss:
                        flight_name2 = detailss.split('show fare information for')[-1].split('flight')[0].strip()

                    if flight_name2:
                            print(f"Flight Name: {flight_name2}")
                    else:
                        print("Failed to scrape the flight name")

                    # Adjust the code for extracting layovers
                    if "Layover for" in detailss:
                        layoversss = detailss.split("Layover for")[1:]  # Split by "Layover for" and skip the first part
                        layoversss = [f"Layover for {layoverss.strip()}" for layoverss in layoversss]  # Reattach "Layover for" and strip whitespace
                        layoversss = " • ".join(layoversss)  # Join the layovers back together with " • "
                        print(f"Layovers: {layoversss}")
                    else:
                        layoversss = "N/A"



                # Extract arrival time
                    if "arriving at" in detailss:
                        match = re.search(r"arriving at ([^,]+)", detailss)
                        if match:
                            return_arrival_info = match.group(1).split("for")[0].strip()
                            print(f"Arrival Time: {return_arrival_info}")

                    # Extract departure time
                    if "departing at" in detailss:
                        match = re.search(r"departing at ([^,]+)", detailss)
                        if match:
                            return_departure_info = match.group(1).split("for")[0].strip()
                            print(f"Departure Time: {return_departure_info}")
            except Exception as e:
                print(f"there is an issue with scraping: {e}")


            if total_travel_time != "N/A" and total_travel_times != "N/A":
                            try:
                                td1 = parse_durations(total_travel_time)
                                td2 = parse_durations(total_travel_times)
                                total_duration = td1 + td2
                                total_days = total_duration.days
                                total_hours, remainder = divmod(total_duration.seconds, 3600)
                                total_minutes = remainder // 60
                                if total_days > 0:
                                    total_travel_time = f"{total_days} days {total_hours} hr {total_minutes} min"
                                else:
                                    total_travel_time = f"{total_hours} hr {total_minutes} min"
                                print(f"Total Travel Time: {total_travel_time}")
                            except Exception as e:
                                total_travel_time = "N/A"
                                print(f"Failed to add the times up: {e}")
            else:
                            total_travel_time = "N/A"
                            print("Failed to add the times up due to missing travel times")


























            try:
                if ("Nonstop" in stopss and "Nonstop" in stopsss) or ("Nonstop" in stopsss and "Nonstop" in stopss):
                            stops = "Nonstop"
                elif ("one" in stopss.lower() and "one" in stopsss.lower()) or ("one" in stopsss.lower() and "one" in stopss.lower()):
                            stops = "Two Stops"
                elif ("two" in stopss.lower() and "two" in stopsss.lower()) or ("two" in stopsss.lower() and "two" in stopss.lower()):
                            stops = "Four Stops"
                elif ("three" in stopss.lower() and "three" in stopsss.lower()) or ("three" in stopsss.lower() and "three" in stopss.lower()):
                            stops = "Six Stops"
                elif ("four" in stopss.lower() and "four" in stopsss.lower()) or ("four" in stopsss.lower() and "four" in stopss.lower()):
                            stops = "Eight Stops"
                elif ("five" in stopss.lower() and "five" in stopsss.lower()) or ("five" in stopsss.lower() and "five" in stopss.lower()):
                            stops = "Ten Stops"
                elif ("Nonstop" in stopss and "one" in stopsss.lower()) or ("one" in stopss.lower() and "Nonstop" in stopsss):
                            stops = "One Stop"
                elif ("Nonstop" in stopss and "two" in stopsss.lower()) or ("two" in stopss.lower() and "Nonstop" in stopsss):
                            stops = "Two Stops"
                elif ("Nonstop" in stopss and "three" in stopsss.lower()) or ("three" in stopss.lower() and "Nonstop" in stopsss):
                            stops = "Three Stops"
                elif ("Nonstop" in stopss and "four" in stopsss.lower()) or ("four" in stopss.lower() and "Nonstop" in stopsss):
                            stops = "Four Stops"
                elif ("Nonstop" in stopss and "five" in stopsss.lower()) or ("five" in stopss.lower() and "Nonstop" in stopsss):
                            stops = "Five Stops"
                elif ("one" in stopss.lower() and "two" in stopsss.lower()) or ("two" in stopss.lower() and "one" in stopsss.lower()):
                            stops = "Three Stops"
                elif ("one" in stopss.lower() and "three" in stopsss.lower()) or ("three" in stopss.lower() and "one" in stopsss.lower()):
                            stops = "Four Stops"
                elif ("one" in stopss.lower() and "four" in stopsss.lower()) or ("four" in stopss.lower() and "one" in stopsss.lower()):
                            stops = "Five Stops"
                elif ("one" in stopss.lower() and "five" in stopsss.lower()) or ("five" in stopss.lower() and "one" in stopsss.lower()):
                            stops = "Six Stops"
                elif ("two" in stopss.lower() and "three" in stopsss.lower()) or ("three" in stopss.lower() and "two" in stopsss.lower()):
                            stops = "Five Stops"
                elif ("two" in stopss.lower() and "four" in stopsss.lower()) or ("four" in stopss.lower() and "two" in stopsss.lower()):
                            stops = "Six Stops"
                elif ("two" in stopss.lower() and "five" in stopsss.lower()) or ("five" in stopss.lower() and "two" in stopsss.lower()):
                            stops = "Seven Stops"
                elif ("three" in stopss.lower() and "four" in stopsss.lower()) or ("four" in stopss.lower() and "three" in stopsss.lower()):
                            stops = "Seven Stops"
                elif ("three" in stopss.lower() and "five" in stopsss.lower()) or ("five" in stopss.lower() and "three" in stopsss.lower()):
                            stops = "Eight Stops"
                elif ("four" in stopss.lower() and "five" in stopsss.lower()) or ("five" in stopss.lower() and "four" in stopsss.lower()):
                            stops = "Nine Stops"
                else:
                            stops = "More than 5 stops"
            except Exception as e:
                 print(f"issue with combining stops: {e}")











            #test 1





            layovers.append((layoverss, layoversss))
            print(layovers)

            # Flatten the list of tuples into a single list of strings
            flat_layovers = [item for sublist in layovers for item in sublist]

            layovers_combined = ' • '.join(flat_layovers)
            print(f"this is the total layover: {layovers_combined}")
            layovers = layovers_combined

            if len(driver.find_elements(By.XPATH, nonestop_xpath)) > 0:
                driver.find_element(By.XPATH, nonestop_xpath).click()
                time.sleep(3)

            if len(driver.find_elements(By.XPATH, onestop_xpath)) > 0:
                driver.find_element(By.XPATH, onestop_xpath).click()
                time.sleep(2)

            if len(driver.find_elements(By.XPATH, twostop_xpath)) > 0:
                driver.find_element(By.XPATH, twostop_xpath).click()
                time.sleep(1)




            



            #test 2

            try:
                mainclick = driver.find_elements(By.XPATH, generalized_available_xpath)
                mainclick[0].click()
                time.sleep(3)





            
            except Exception as e:
                print("not working")





            original_window = driver.current_window_handle

            try:
                select_xpath = '//button[contains(@data-stid, "select-button") and contains(@data-test-id, "select-button")]'
                select = driver.find_element(By.XPATH, select_xpath).click()
                print("Successfully clicked the select button")
            except Exception as e:
                print(f'there is an issue with select {e}')




            try:
                exit_xpath = '//*[@id="forced-choice-modal-dismiss-btn"]'
                exit = driver.find_element(By.XPATH, exit_xpath).click()
                time.sleep(1)
            except Exception as e:
                print(f"Failed to click on exit button: {e}")


            try:
                retries = 3  # Number of retry attempts
                for attempt in range(retries):
                    try:
                        time.sleep(10)
                        WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))

                        # New page
                        for handle in driver.window_handles:
                            if handle != original_window:
                                driver.switch_to.window(handle)
                                
                                # Apply stealth settings to the new window
                                stealth(driver,
                                        languages=["en-US", "en"],
                                        vendor="Google Inc.",
                                        platform="Win32",
                                        webgl_vendor="Intel Inc.",
                                        renderer="Intel Iris OpenGL Engine",
                                        fix_hairline=True)
                                
                                # Refresh the page
                                driver.refresh()
                                time.sleep(5)
                                
                                # Take screenshot after applying stealth settings and refreshing
                                print("Successfully applied stealth and refreshed the new window")
                                break
                        else:
                            raise Exception("New window not found")

                        break  # Exit the loop if successful

                    except Exception as e:
                        print(f"Attempt {attempt + 1} failed: {e}")
                        screenshot_path = os.path.abspath(f"screenshot_stealth_attempt_{attempt + 1}.png")
                        driver.save_screenshot(screenshot_path)
                        print(f"Screenshot saved at: {screenshot_path}")
                        if attempt < retries - 1:
                            time.sleep(5)  # Wait before retrying
                        else:
                            print("Max retries reached. There is an issue with stealth only")

                # Make sure to handle any exceptions that might occur outside the retry loop
                try:
                    # Rest of the code that might fail
                    pass
                except Exception as e:
                    print(f"Failed to click select button or handle new window: {e}")
                    screenshot_path = os.path.abspath("screenshot_final_error.png")
                    driver.save_screenshot(screenshot_path)
                    print(f"Screenshot saved at: {screenshot_path}")


            except Exception as e:
                print(f'there is an issue with stealth {e}')




            # Capture the URL of the new tab


            new_tab_url = driver.current_url
            print(f"New Tab URL: {new_tab_url}")

            webpage_link = new_tab_url
            time.sleep(5)



            print(f'flight name 1: {flight_name1}')
            print(f'fllight name 2: {flight_name2}')
            if flight_name2 != flight_name1:
                flight_name.append(flight_name2)
            flight_combined = ' , '.join(flight_name)
            print(f"this is the total flight names: {flight_combined}")
            flight_name = flight_combined


            print(f"expedia total stops: {stops}")















            try:
                price_xpath = '//td[@class="uitk-table-cell uitk-table-cell-padding-zero uitk-table-cell-align-trailing uitk-table-cell-align-top"]/div/h3[@class="uitk-heading uitk-heading-5"]'
                price_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, price_xpath)))   
                # Additional wait to ensure the element is visible
                WebDriverWait(driver, 10).until(EC.visibility_of(price_element))
                
                price = price_element.text.strip()
                print(f"Price: {price}")
            except TimeoutException:
                print("Failed to scrape the price: Element not found within the given time")
            except NoSuchElementException:
                print("Failed to scrape the price: Element does not exist")
            except Exception as e:
                print(f"Failed to scrape the price: {e}")

            # Switch back to the original window
            driver.close()  # Close the new tab
            driver.switch_to.window(original_window)  # Switch back to the original window
            time.sleep(5)
            
            # Re-fetch elements after switching back to the original window
            mainclick = driver.find_elements(By.XPATH, generalized_available_xpath)






            try:
                if "from" in departure_info:
                    time_part = departure_info.split("from")[0].strip()
                    departure_info = f"{time_part} from {flying_from.split('from ')[-1]}"
                     
            except Exception as e:
                print(f"An error occurred: {e}")

            try:
                if "in" in arrival_info:
                    time_parts = arrival_info.split("in")[0].strip()
                    arrival_info = f"{time_parts} arriving in {flying_to.split('to ')[-1]}"
                     
            except Exception as e:
                print(f"An error occurred: {e}")


            try:
                if "from" in return_departure_info:
                    time_partsss = return_departure_info.split("from")[0].strip()
                    return_departure_info = f"{time_partsss} from {flying_to.split('to ')[-1]}"
            except Exception as e:
                print(f"An error occurred: {e}")



            try:
                if "in" in return_arrival_info:
                    time_partssss = return_arrival_info.split("in")[0].strip()
                    location_name = flying_from.split("Flying from")[-1].strip()
                    return_arrival_info = f"{time_partssss} arriving in {location_name}"
            except Exception as e:
                print(f"An error occurred: {e}")


            flights.append([
                                flight_name,
                                departure_info,
                                arrival_info,
                                return_departure_info,
                                return_arrival_info,
                                price,
                                total_travel_time,
                                stops,
                                layovers, webpage_link])










            retries = 3  # Define the number of retries
            for attempt in range(retries):
                try:
                    time.sleep(5)
                    driver.refresh()

                    # Define the XPath for the change button
                    change_button_xpath = '//*[@id="app-layer-base"]/div[2]/div[3]/div/div/div/main/section/div/div[1]/ul/li[1]/div/a'
                    
                    # Wait for the change button to be clickable
                    change_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, change_button_xpath))
                    )
                    
                    # Click the change button
                    change_button.click()
                    print("Successfully clicked the change flight button")
                    break  # Exit the loop if the click was successful
                
                except (TimeoutException, NoSuchElementException, ElementClickInterceptedException) as e:
                    print(f"Attempt {attempt + 1} failed: {e}")
                    screenshot_path = os.path.abspath(f"screenshot_attempt_{attempt + 1}.png")
                    driver.save_screenshot(screenshot_path)
                    print(f"Screenshot saved at: {screenshot_path}")
                    
                    # Try alternative method if click fails
                    try:
                        search_xpath = '//button[contains(@class, "uitk-button") and contains(@class, "uitk-button-primary") and contains(@data-test-id, "search-form-button")]'
                        search_button = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, search_xpath))
                        )
                        search_button.click()
                        print("Successfully clicked the search button as an alternative action")
                        break  # Exit the loop if the alternative click was successful
                    
                    except Exception as e:
                        print(f"Alternative method failed on attempt {attempt + 1}: {e}")
                        screenshot_path = os.path.abspath(f"screenshot_alternative_attempt_{attempt + 1}.png")
                        driver.save_screenshot(screenshot_path)
                        print(f"Screenshot saved at: {screenshot_path}")
                
                except WebDriverException as e:
                    print(f"WebDriver exception occurred: {e}")
                    screenshot_path = os.path.abspath(f"screenshot_attempt_{attempt + 1}.png")
                    driver.save_screenshot(screenshot_path)
                    print(f"Screenshot saved at: {screenshot_path}")
                    
                    # Try alternative method if WebDriverException occurs
                    try:
                        search_xpath = '//button[contains(@class, "uitk-button") and contains(@class, "uitk-button-primary") and contains(@data-test-id, "search-form-button")]'
                        search_button = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, search_xpath))
                        )
                        search_button.click()
                        print("Successfully clicked the search button as an alternative action")
                        break  # Exit the loop if the alternative click was successful
                    
                    except Exception as e:
                        print(f"Alternative method failed on attempt {attempt + 1}: {e}")
                        screenshot_path = os.path.abspath(f"screenshot_alternative_attempt_{attempt + 1}.png")
                        driver.save_screenshot(screenshot_path)
                        print(f"Screenshot saved at: {screenshot_path}")

            print("Completed all retry attempts")




            try:
                                file_path = os.path.abspath("data3.csv")

                                with open(file_path, "w", newline='', encoding='utf-8') as file:
                                    writer = csv.writer(file)
                                    writer.writerows(flights)

                                print(f"Data written to {file_path} successfully.")
            except:
                                print("failed to write data")
    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        driver.quit()
        print("closing expedia")
   




def get_full_airport_name(location):
    for airport in pyairports.airports:
        if airport.iata.lower() == location.lower():
            return airport.name
    return location

def search_google_flights(driver, departure, destination, departure_date, return_time):
    print("Loading environment variables for Google Flights...")
    load_dotenv('C:\\PythonStuff\\.env')
    
    chrome_path = os.getenv('CHROME_PATH')
    chromedriver_path = os.getenv('CHROMEDRIVER_PATH')
    print(f"Chrome path: {chrome_path}")
    print(f"ChromeDriver path: {chromedriver_path}")

    if not chrome_path or not chromedriver_path:
        print("Error: CHROME_PATH or CHROMEDRIVER_PATH not set.")
        return

    user_agent = get_random_user_agent()
    print(f"Using User-Agent: {user_agent}")

    options = Options()
    options.binary_location = chrome_path
    options.add_argument("--headless")
    options.add_argument("--window-size=1656,1080")
    options.add_argument("--start-maximized")
    print("Chrome options set.")

    for attempt in range(3):
        try:
            print("Initializing WebDriver for Google Flights...")
            driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)
            break
        except WebDriverException as e:
            print(f"Error initializing WebDriver for Google Flights: {e}")
            if attempt < 2:
                print("Retrying...")
                time.sleep(2)
            else:
                print("Failed to initialize WebDriver for Google Flights after retries.")
                return

    # Get a random user agent
        # Get a random user agent

    # Initialize the driver
    driver.maximize_window()
    driver.implicitly_wait(5)
    

    
    try:
        driver.get("https://www.google.com/travel/flights?gl=US&hl=en-US")
        driver.maximize_window()
        driver.implicitly_wait(5)


    
        departure_xpath = '//*[@aria-label="Where from?"]'
        departure_element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, departure_xpath)))
        departure_element.clear()
        departure = departure.title()
        departure_element.send_keys(departure)
        time.sleep(2)
        print("Clicked departure")

        # Click the specific option
        option_xpath = f"//li//*[contains(text(), '{departure}')]"
        option_element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, option_xpath)))
        option_element.click()
        print("clicked option")

        # Find and enter the destination location
        destination_xpath = '//*[@aria-label="Where to? "]'
        destination_element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, destination_xpath)))
        destination_element.clear()
        destination = destination.title()
        destination_element.send_keys(destination)
        time.sleep(2)
        print("Clikced desination")

        # Click the specific option
        option_xpath = f"//li//*[contains(text(), '{destination}')]"
        option_element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, option_xpath)))
        option_element.click()
        print("Clikced option element two")





        # Click on the departure date field
        date_placeholder = "Departure"
        date_xpath = f'//*[@placeholder="{date_placeholder}"]'
        date_element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, date_xpath)))
        date_element.click()
        
        time.sleep(2)
        date_xpath = '//*[@id="ow79"]/div[2]/div/div[2]/div[1]/div[1]/div[1]/div/input'
        date_element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, date_xpath)))
        date_element.click()
        time.sleep(2)
        date_element.send_keys(departure_date)
        date_element.send_keys(Keys.ENTER)
        date_element.send_keys(Keys.ENTER)
        time.sleep(2)
        print("Clikced date element")

        button_xpath = '//*[@id="ow79"]/div[2]/div/div[3]/div[3]'
        button_element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, button_xpath)))
        button_element.click()

        # Handle return time
        time_placeholder = "Return"
        time_xpath = (f"//input[@type='text' and @jsname='yrriRe' and @class='TP4Lpb eoY5cb j0Ppje' and @placeholder='{time_placeholder}' "
                      "and @aria-label='Return']")
        time_element = WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.XPATH, time_xpath)))
        time.sleep(2)
        time_element.send_keys(return_time)
        time_element.send_keys(Keys.ENTER)
        time.sleep(2)

        explore_button_xpath = '//*[@id="yDmH0d"]/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[2]/div/button'
        explore_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, explore_button_xpath)))
        explore_button.click()
        time.sleep(3)
        print("clikced the explore button")

        try:
             driver.refresh
             time.sleep(5)
             print("refreshed the page")

        except Exception as e:
             print(f'there is an errror: {e}')

        try:
            plore_xpath = "//div[@role='button' and @tabindex='0' and contains(@class, 'I0Kcef') and @aria-label='Close']"
            plore_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, plore_xpath)))
            plore_button.click()
            time.sleep(1)
        except TimeoutException:
            print("Plore button not found, continuing with the next steps.")


        try:
            cheapest_xpath = '//button[@aria-label="Top flights, Change sort order." and contains(@class, "VfPpkd-LgbsSe")]'
            cheapest_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, cheapest_xpath)))
            cheapest_button.click()
            try:
                price1_xpath = '//li[@data-value="2" and .//span[text()="Price"]]'
                price1_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, price1_xpath)))
                price1_button.click()
                time.sleep(5)
            except Exception as e:
                print(f'there is an error with price in the cheapest: {e}')
        except Exception as e:
            print(f'there is an error with cheapest: {e}')
        try:
            sortby_xpath = '//*[@id="yDmH0d"]/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[2]/div[3]/div/div/div/div[1]/div'
            sortby_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, sortby_xpath)))
            sortby_button.click()
            time.sleep(2)
        except Exception as e:
            print("there is an issue with sortby_xpath")
        try:
            price_xpath= '//*[@id="yDmH0d"]/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[2]/div[3]/div/div/div/div[2]/div/ul/li[2]'
            price_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, price_xpath)))
            price_button.click()
            time.sleep(2)
        except Exception as e:
            print(f"there is an issue with price_xpath {e}")

        mainclick_xpath = '//ul/li[@class="pIav2d"]'
        secound_click_xpath = '//*[@id="yDmH0d"]/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[2]/div[3]/ul/li'
        secound_click = driver.find_elements(By.XPATH, secound_click_xpath)
        button1_xpath = '//*[@id="yDmH0d"]/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div/div[2]/div[2]/div[3]/div/div[2]/div[1]/div/div/div/div[1]/div[2]/div/div[2]/div/div/button'
        button2_xpath = '//*[@id="yDmH0d"]/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div/div[2]/div[2]/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[2]/div/div[2]/div/div/button'

        columns = [
            'Flight', 'Departure Time of Flight Going to Destination', 'Arrival Time of Flight Going to Destination',
            'Departure Time of Flight Returning', 'Arrival Time of Flight Returning', 'Price', 'Seats Left',
            'Total Travel Time', 'Stops', 'Layovers'
        ]

        flights = []
        travel_times = []
            

        mainclick = driver.find_elements(By.XPATH, mainclick_xpath)
        secound_click_xpath = '//*[@id="yDmH0d"]/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[2]/div[3]/ul/li'
        secound_click = driver.find_elements(By.XPATH, secound_click_xpath)
        button1_xpath = '//*[@id="yDmH0d"]/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div/div[2]/div[2]/div[3]/div/div[2]/div[1]/div/div/div/div[1]/div[2]/div/div[2]/div/div/button'
        button2_xpath = '//*[@id="yDmH0d"]/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div/div[2]/div[2]/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[2]/div/div[2]/div/div/button'


        flights = []
        travel_times = []

        for index in range(min(5, len(mainclick))):

            try:
                plore_xpath = "//div[@role='button' and @tabindex='0' and contains(@class, 'I0Kcef') and @aria-label='Close']"
                plore_button = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, plore_xpath)))
                plore_button.click()
                time.sleep(1)
            except TimeoutException:
                print("Plore button not found, continuing with the next steps.")

            try:
                mainclick = driver.find_elements(By.XPATH, mainclick_xpath)
                time.sleep(3)
                mainclick[index].click()
                time.sleep(3)
            except Exception as e:
                print(f"Failed to click on main click element: {e}")
                

            # Click the secondary option to view more details
            secound_click = driver.find_elements(By.XPATH, secound_click_xpath)
            if len(secound_click) > 0:
                time.sleep(3)
                secound_click[0].click()
                time.sleep(6)

                # Click on the buttons to get flight details
                try:
                    button1 = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, button1_xpath)))
                    button1.click()
                    time.sleep(4)

                    # Re-locate button2 to avoid stale element reference error
                    button2 = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, button2_xpath)))
                    button2.click()
                    time.sleep(4)
                except Exception as e:
                    print(f"Failed to click on flight details buttons: {e}")

                # Travel time
                try:
                    travel_time_xpath1 = '//div[@class="gvkrdb AdWm1c tPgKwe ogfYpf"]'
                    travel_time_elements1 = driver.find_elements(By.XPATH, travel_time_xpath1)
                    if travel_time_elements1:
                        if len(travel_time_elements1) > 0:
                            travel_time1 = travel_time_elements1[0].text.replace('Total duration ', '').strip()
                            if not travel_time1:  # If the text content is empty, try to get the aria-label
                                travel_time1 = travel_time_elements1[0].get_attribute('aria-label').replace('Total duration ', '').strip()
                        else:
                            travel_time1 = "N/A"
                    else:
                        travel_time1 = "N/A"
                    print(f"Travel Time 1: {travel_time1}")
                except Exception as e:
                    travel_time1 = "N/A"
                    print(f"Failed to extract travel time 1: {e}")

                try:
                    # Ensure the travel time elements are re-located to avoid stale element reference
                    travel_time_elements2 = driver.find_elements(By.XPATH, travel_time_xpath1)
                    if travel_time_elements2:
                        if len(travel_time_elements2) > 1:
                            travel_time2 = travel_time_elements2[1].text.replace('Total duration ', '').strip()
                            if not travel_time2:  # If the text content is empty, try to get the aria-label
                                travel_time2 = travel_time_elements2[1].get_attribute('aria-label').replace('Total duration ', '').strip()
                        else:
                            travel_time2 = "N/A"
                    else:
                        travel_time2 = "N/A"
                    print(f"Travel Time 2: {travel_time2}")
                except Exception as e:
                    travel_time2 = "N/A"
                    print(f"Failed to extract travel time 2: {e}")

                travel_times.append((travel_time1, travel_time2))  # Total travel times
                print(travel_times)

                # Adds the two numbers together
                if travel_time1 != "N/A" and travel_time2 != "N/A":
                    td1 = parse_duration(travel_time1)
                    td2 = parse_duration(travel_time2)
                    total_duration = td1 + td2
                    total_days = total_duration.days
                    total_hours, remainder = divmod(total_duration.seconds, 3600)
                    total_minutes = remainder // 60
                    if total_days > 0:
                        total_travel_time = f"{total_days} days {total_hours} hr {total_minutes} min"
                    else:
                        total_travel_time = f"{total_hours} hr {total_minutes} min"
                    print(f"Total Travel Time: {total_travel_time}")
                else:
                    total_travel_time = "N/A"

                travel_times.append((travel_time1, travel_time2, total_travel_time))  # Total travel times

                # Stops
                try:
                    stops_xpath = '//span[@class="ogfYpf" and contains(@aria-label, "stop flight.")]'
                    stop_elements1 = driver.find_elements(By.XPATH, stops_xpath)
                    if stop_elements1:
                        stop_text1 = stop_elements1[0].get_attribute('aria-label')
                        if "Nonstop" in stop_text1:
                            stops_1 = 0
                        else:
                            stops_1 = int(stop_text1.split()[0])  # Extract the first digit and convert to integer
                    else:
                        stops_1 = 0  # Default to 0 if no stops found
                    print(f"First stop: {stops_1}")
                except Exception as e:
                    stops_1 = 0  # Default to 0 if an error occurs
                    print(f"Failed to extract stops: {e}")

                try:
                    # Re-locate the elements to avoid stale element reference
                    stop_elements2 = driver.find_elements(By.XPATH, stops_xpath)
                    if len(stop_elements2) > 1:
                        stop_text2 = stop_elements2[1].get_attribute('aria-label')
                        if "Nonstop" in stop_text2:
                            stops_2 = 0
                        else:
                            stops_2 = int(stop_text2.split()[0])  # Extract the first digit for the second element and convert to integer
                    else:
                        stops_2 = 0  # Default to 0 if no stops found
                    print(f"Second stop: {stops_2}")
                except Exception as e:
                    stops_2 = 0  # Default to 0 if an error occurs
                    print(f"Failed to extract stops: {e}")

                total_stops = stops_1 + stops_2  # Calculate the total stops
                print(f"Total stops: {total_stops}")

                # Format the final output
                if total_stops == 0:
                    stops = "Nonstop"
                elif total_stops == 1:
                    stops = "One Stop"

                elif total_stops == 2:
                    stops = "Two Stops"
                
                elif total_stops == 3:
                    stops = "Three Stops"
                else:
                    stops = f"{total_stops} stops"

                print(f"Formatted stops: {stops}")

                # Initialize variables for flight details
                flight_details_departing = []
                flight_details_returning = []
                departure_info = "N/A"
                arrival_info = "N/A"
                return_departure_info = "N/A"
                return_arrival_info = "N/A"

                # Scrape flight details
                try:
                    flight_details_elements = driver.find_elements(By.XPATH, '//span[@class="mv1WYe"]')
                    if flight_details_elements:
                        flight_details_departing = flight_details_elements[0].get_attribute('aria-label').split('. ')
                        flight_details_returning = flight_details_elements[1].get_attribute('aria-label').split('. ')

                        print(f"Departing Details: {flight_details_departing}")  # Debugging line
                        print(f"Returning Details: {flight_details_returning}")  # Debugging line

                        # Extract departing details and handle city names with periods
                        departing_reconstructed = []
                        i = 0
                        while i < len(flight_details_departing):
                            if "Leaves" in flight_details_departing[i]:
                                city_name = flight_details_departing[i]
                                i += 1
                                while i < len(flight_details_departing) and flight_details_departing[i][0].isupper():
                                    city_name += '. ' + flight_details_departing[i]
                                    i += 1
                                departing_reconstructed.append(city_name)
                            else:
                                departing_reconstructed.append(flight_details_departing[i])
                                i += 1

                        flight_details_departing = departing_reconstructed

                        # Extract returning details and handle city names with periods
                        returning_reconstructed = []
                        i = 0
                        while i < len(flight_details_returning):
                            if "Leaves" in flight_details_returning[i]:
                                city_name = flight_details_returning[i]
                                i += 1
                                while i < len(flight_details_returning) and flight_details_returning[i][0].isupper():
                                    city_name += '. ' + flight_details_returning[i]
                                    i += 1
                                returning_reconstructed.append(city_name)
                            else:
                                returning_reconstructed.append(flight_details_returning[i])
                                i += 1

                        flight_details_returning = returning_reconstructed

                        print(f"Departing Details: {departing_reconstructed}")  # Debugging line
                        print(f"Returning Details: {returning_reconstructed}")  # Debugging line

                        if len(departing_reconstructed) > 1:
                            for detail in departing_reconstructed:
                                if "Leaves" in detail:
                                    parts = detail.split(' ')
                                    departure_info_parts = []
                                    for part in parts:
                                        departure_info_parts.append(part)
                                        if "PM" in part or "AM" in part:
                                            break
                                    departure_info = ' '.join(departure_info_parts)
                                    break
                            if len(departing_reconstructed) > 1:
                                arrival_parts = departing_reconstructed[1].split('arrives at ')
                                if len(arrival_parts) > 1:
                                    arrival_info = 'arrives at ' + arrival_parts[1].strip()

                        if len(returning_reconstructed) > 1:
                            for detail in returning_reconstructed:
                                if "Leaves" in detail:
                                    parts = detail.split(' ')
                                    return_departure_info_parts = []
                                    for part in parts:
                                        return_departure_info_parts.append(part)
                                        if "PM" in part or "AM" in part:
                                            break
                                    return_departure_info = ' '.join(return_departure_info_parts)
                                    break
                            if len(returning_reconstructed) > 1:
                                return_arrival_parts = returning_reconstructed[1].split('arrives at ')
                                if len(return_arrival_parts) > 1:
                                    return_arrival_info = 'arrives at ' + return_arrival_parts[1].strip()

                except Exception as e:
                    print(f"Failed to extract data for a flight: {e}")

                if flight_details_departing:
                    # Initialize default values
                    price = "N/A"
                    flight_name = "N/A"
                    duration = "N/A"
                    layovers = "N/A"
                    seats_left = "N/A"
                    webpage_link = "N/A"

                    # Extract webpage link
                    webpage_link = driver.current_url
                    print(f"Webpage Link: {webpage_link}")

                    # Extract price
                    try:
                        price_flight_xpath = '//*[@id="yDmH0d"]/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div/div[2]/div[2]/div[2]/div/div/div[2]/div/div[1]/span'
                        price_flight = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, price_flight_xpath)))
                        price = price_flight.text.strip()
                        print(f"Price: {price}")
                    except Exception as e:
                        price = "N/A"
                        print(f"Failed to find price: {e}")

                    # Extract flight name
                    try:
                        flight_name1_xpath = '//span[@class="Xsgmwe"]'
                        flight_name_elements = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, flight_name1_xpath)))

                        flight_names = []
                        for element in flight_name_elements:
                            text = element.text.strip()
                            if text.lower() not in ['economy', 'airbus a319', 'boeing 737', 'airbus a320neo', 'boeing 737max 9 passenger', 'airbus a320', 'airbus a220-300 passenger','embraer 175','airbus a321 (sharklets)', 'a220-100 passenger', 'airbus a321', 'boeing 757', 'airbus a220-100 passenger', '737max 8 passenger', 'boeing 737max 8 passenger']:  # Add other non-relevant text here if needed
                                flight_names.append(text)

                        flight_name1 = flight_names[0] if len(flight_names) > 0 else "N/A"
                        flight_name2 = flight_names[1] if len(flight_names) > 1 else "N/A"

                        if flight_name1 == flight_name2:
                            total_flight_name = flight_name1
                        elif flight_name1 == "N/A" and flight_name2 == "N/A":
                            total_flight_name = "N/A"
                        else:
                            total_flight_name = f"{flight_name1}, {flight_name2}"

                        print(f"Flight Name 1: {flight_name1}")
                        print(f"Flight Name 2: {flight_name2}")
                        print(f"Total Flight Names: {total_flight_name}")
                    except Exception as e:
                        total_flight_name = "N/A"
                        print(f"Failed to extract flight names: {e}")

                    # Assign the total flight name to the flight_name variable
                    flight_name = total_flight_name

                    # Extract layovers
                    try:
                                flight_layover1_xpath = '//div[@class="tvtJdb eoY5cb y52p7d"]'
                                flight_layover_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, flight_layover1_xpath)))
                                flight_layover1 = flight_layover_element.text.strip()

                                # Use regex to insert a space between "layover" and the city name
                                flight_layover1 = re.sub(r'(layover)(\w)', r'\1 \2', flight_layover1)

                                print(f"Flight layover: {flight_layover1}")
                    except Exception as e:
                                flight_layover1 = "N/A"
                                print(f"Failed to extract flight layover: {e}")

                            # Re-locate the element to avoid stale element reference
                    try:
                                flight_layover_elements = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, flight_layover1_xpath)))
                                if flight_layover_elements and len(flight_layover_elements) > 1:
                                    flight_layover2 = flight_layover_elements[1].text.strip()
                                    
                                    # Use regex to insert a space between "layover" and the city name
                                    flight_layover2 = re.sub(r'(layover)(\w)', r'\1 \2', flight_layover2)

                                    print(f"Flight layover 2: {flight_layover2}")
                                else:
                                    flight_layover2 = " "
                                    print(f"Failed to extract flight layover 2: No elements found or only one element found")
                    except Exception as e:
                                flight_layover2 = "N/A"
                                print(f"Failed to extract flight layover 2: {e}")

                    combined_layover = f"{flight_layover1} {flight_layover2}".strip()
                    print(f"Combined Flight Layover: {combined_layover}")
                    layovers = combined_layover

                    # Append flight details to flights list
                    flights.append([
                        flight_name,
                        departure_info,
                        arrival_info,
                        return_departure_info,
                        return_arrival_info,
                        price,
                        total_travel_time,
                        stops,
                        layovers,
                        webpage_link
                    ])

                    print(flight_details_departing)
                    print(flight_details_returning)

                # Write data to CSV
                try:
                    file_path = os.path.abspath("data2.csv")
                    with open(file_path, "w", newline='', encoding='utf-8') as file:
                        writer = csv.writer(file)
                        writer.writerows(flights)
                    print(f"Data written to {file_path} successfully.")
                except Exception as e:
                    print(f"Failed to write data: {e}")

                # Navigate back
                try:
                    back_xpath = '//*[@id="gb"]/div[2]/div[1]/div[2]'
                    back_button = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, back_xpath)))
                    back_button.click()
                    time.sleep(2)
                except Exception as e:
                    print(f"Failed to navigate back: {e}")

                # Click on change button
                try:
                    li_xpath = '//*[@id="yDmH0d"]/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[2]/div[2]/div/ol/li[1]/span/span/span/div'
                    li_element = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, li_xpath)))

                    actions = ActionChains(driver)
                    actions.move_to_element(li_element).click().perform()
                    change_xpath = '//*[@id="yDmH0d"]/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[2]/div[2]/div/ol/li[1]/span/span/span/div/div'
                    change_button = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, change_xpath)))
                    change_button.click()
                except Exception as e:
                    print(f"Failed to click on change buttons: {e}")

    finally:
        driver.quit()
        print("closing the browser")           


def process_user_input(departure, destination, departure_date, return_date, service="expedia"):
    """
    Process user input for departure and destination cities, and travel dates, then call the appropriate service.
    
    Parameters:
    - departure (str): The departure city.
    - destination (str): The destination city.
    - departure_date (str): The departure date in the format "Jul 22, 2024".
    - return_date (str): The return date in the format "Aug 29, 2024".
    - service (str): The service to use, either "expedia" or "google". Default is "expedia".
    
    Returns:
    - Result from the called service function.
    """
    import threading
    import undetected_chromedriver as uc
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.common.exceptions import WebDriverException
    from datetime import datetime

    # Function to format date
    def format_date(date_str):
        try:
            # Try parsing the date in the format "YYYY-MM-DD"
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            formatted_date = date_obj.strftime("%A, %B %d, %Y")
            return formatted_date
        except ValueError:
            try:
                # If the first format fails, try parsing the date in the format "%b %d, %Y"
                date_obj = datetime.strptime(date_str, "%b %d, %Y")
                formatted_date = date_obj.strftime("%A, %B %d, %Y")
                return formatted_date
            except ValueError as e:
                raise ValueError(f"Invalid date format: {e}")

    # Validate city inputs
    if not all(part.isalpha() for part in departure.split()):
        raise ValueError("Departure city must be alphabetic characters only.")
    if not all(part.isalpha() for part in destination.split()):
        raise ValueError("Destination city must be alphabetic characters only.")

    # Format dates
    formatted_departure_date = format_date(departure_date)
    formatted_return_date = format_date(return_date)

    # Processed input dictionary
    processed_input = {
        "departure": departure,
        "destination": destination,
        "departure_date": formatted_departure_date,
        "return_date": formatted_return_date
    }

    # WebDriver setup within a mutex lock


    driver = None
    try:
        if service == "expedia":
            return roundTrip(driver, processed_input['departure'], processed_input['destination'], processed_input['departure_date'], processed_input['return_date'])
        elif service == "google":
            return search_google_flights(driver, processed_input['departure'], processed_input['destination'], processed_input['departure_date'], processed_input['return_date'])
        else:
            raise ValueError("Invalid service specified. Use 'expedia' or 'google'.")
    except WebDriverException as e:
        print(f"WebDriverException encountered: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if driver:
            driver.quit()

def run_both_services(departure, destination, departure_date, return_date):
    def thread_target(service, results, index):
        result = process_user_input(departure, destination, departure_date, return_date, service)
        results[index] = result

    results = [None, None]
    threads = []

    t1 = threading.Thread(target=thread_target, args=("expedia", results, 0))
    t2 = threading.Thread(target=thread_target, args=("google", results, 1))

    threads.append(t1)
    threads.append(t2)

    t1.start()
    t2.start()

    for t in threads:
        t.join()

    return results

# Example usage
#departure = "Spokane"
#destination = "houston"
#departure_date = "Jul 27, 2024"
#return_time = "Aug 29, 2024"

#results = run_both_services(departure, destination, departure_date, return_time)
#print("Results from Expedia:", results[0])
#print("Results from Google Flights:", results[1])
