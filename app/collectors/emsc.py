import csv
import time
from datetime import datetime, timedelta
from app.utils.save_file_to_csv import save_csv
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

#Config
#
URL = "https://www.emsc.eu/Earthquake_information/"
OUTPUT_FILE = Path(__file__).resolve().parents[2] /"data"/ "emsc-earthquakes.csv"
WAIT_SECOND = 20

LAT_MIN = 24
LAT_MAX = 46
LON_MIN = 123
LON_MAX = 146

CSV_COLUMNS = [
    "DateTime",
    "Latitude",
    "Longitude",
    "Depth(km)",
    "Magnitude",
    "Region",
]

def get_last_30_days():
    today = datetime.today().date()
    end_date = today - timedelta(days=1)
    start_date = today - timedelta(days=30)
    
    return start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")


def create_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    
    return webdriver.Chrome(options=options)
    
def accept_cookies(driver):
    try:
       cookie_button =  WebDriverWait(driver, 5).until(
           EC.element_to_be_clickable((By.CLASS_NAME, "cookieButton"))
       )
       cookie_button.click()
       
    except TimeoutException:
        print("banner does not show or not clicked")

def fill_input(driver, by, selector, value):
    #Put a Value into one search form
    input_element = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((by, selector))
    )

    if input_element.get_attribute("type") == "date":
        driver.execute_script(
            """
            const input = arguments[0];
            input.value = arguments[1];
            input.dispatchEvent(new Event("input", { bubbles: true }));
            input.dispatchEvent(new Event("change", { bubbles: true }));
            """,
            input_element,
            str(value),
        )
        return

    input_element.clear()
    input_element.send_keys(value)

def fill_search_form(driver, start_date, end_date):
    fill_input(driver,By.NAME, "datemin", start_date)
    fill_input(driver,By.NAME, "datemax", end_date)
    fill_input(driver,By.ID, "latmin", LAT_MIN)
    fill_input(driver,By.ID, "latmax", LAT_MAX)
    fill_input(driver,By.ID, "lonmin", LON_MIN)
    fill_input(driver,By.ID, "lonmax", LON_MAX)

def submit_search(driver):
    search_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'input[type="submit"]')
        )
    )
    search_button.click()

def get_cell_text(row, css_selector):
        #return a text from a table cell
        cells = row.find_elements(By.CSS_SELECTOR, css_selector)
        
        if not cells:
            return ""
        
        return cells[0].text.replace("\n", " ").strip()

    
def read_earthquakes(driver, wait):
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "td.tbdat")))
    
    earthquakes = []
    rows = driver.find_elements(By.XPATH, "//table//tr")
    
    for row in rows:
        try:
            date_time = get_cell_text(row, "td.tbdat")
            latitude = get_cell_text(row, "td.tblat")
            longitude = get_cell_text(row, "td.tblon")
            depth = get_cell_text(row, "td.tbdep")
            magnitude = get_cell_text(row, "td.tbmag")
            region = get_cell_text(row, "td.tbreg")

            if not all([date_time, latitude, longitude, depth, magnitude, region]):
                continue

            earthquakes.append(
                {
                    "DateTime": date_time,
                    "Latitude": latitude,
                    "Longitude": longitude,
                    "Depth(km)": depth,
                    "Magnitude": magnitude,
                    "Region": region
                }
            )
        except StaleElementReferenceException:
            continue
        
    return earthquakes


def read_all_earthquake_pages(driver, wait):
    all_earthquakes = []
    seen_earthquakes = set()
    seen_pages = set()
    page_number = 1

    def get_visible_dates():
        return tuple(
            driver.execute_script(
                """
                return Array.from(document.querySelectorAll("td.tbdat"))
                    .map(cell => cell.textContent.trim());
                """
            )
        )

    def click_next_page():
        return driver.execute_script(
            """
            const nextButton = document.querySelector(
                "body > div.content > div:nth-child(4) > div.spes.spes1.pag"
            );

            if (
                !nextButton ||
                nextButton.textContent.trim() !== "›" ||
                nextButton.offsetParent === null ||
                nextButton.classList.contains("disabled") ||
                nextButton.getAttribute("aria-disabled") === "true"
            ) {
                return false;
            }

            nextButton.scrollIntoView({ block: "center" });
            nextButton.click();
            return true;
            """
        )

    while True:
        page_earthquakes = read_earthquakes(driver, wait)
        page_signature = tuple(
            earthquake["DateTime"] for earthquake in page_earthquakes
        )

        if not page_signature or page_signature in seen_pages:
            break

        seen_pages.add(page_signature)

        for earthquake in page_earthquakes:
            earthquake_key = tuple(
                earthquake[column] for column in CSV_COLUMNS
            )
            if earthquake_key not in seen_earthquakes:
                seen_earthquakes.add(earthquake_key)
                all_earthquakes.append(earthquake)

        print(
            f"scraped page {page_number}: "
            f"{len(page_earthquakes)} rows "
            f"({len(all_earthquakes)} unique total)"
        )

        previous_dates = get_visible_dates()

        if not click_next_page():
            break

        try:
            wait.until(lambda _driver: get_visible_dates() != previous_dates)
        except (TimeoutException, StaleElementReferenceException):
            print("next page did not load; pagination stopped")
            break

        page_number += 1

    return all_earthquakes

def main():
    driver = create_driver()
    wait = WebDriverWait(driver, WAIT_SECOND)
    try:
        print("opening site")
        driver.get(URL)
        time.sleep(2)
        accept_cookies(driver)
        time.sleep(2)
        start_date, end_date = get_last_30_days()
        time.sleep(2)
        print(f"searching from {start_date} to {end_date}...")
        time.sleep(2)
        fill_search_form(driver, start_date, end_date)
        submit_search(driver)
        time.sleep(5)
        
        earthquakes = read_all_earthquake_pages(driver, wait)
        save_csv(OUTPUT_FILE,earthquakes)
        
        print(f"saved {len(earthquakes)} earthquakes to:")
        print(OUTPUT_FILE)
        
    except TimeoutException as error:
        print(f"Timed out while waiting for the EMSC page: {error}")
    except Exception as error:
        print(f"Failed to collect or save earthquakes: {type(error).__name__}: {error}")
        
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
        
