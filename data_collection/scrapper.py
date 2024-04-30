import time
import argparse
from rich.console import Console
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from . import model

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--season", default="All Seasons")
parser.add_argument("-c", "--club", default="All Clubs")
parser.add_argument("-n", "--nationality", default="All Nationalities")
parser.add_argument("-p", "--position", default="All Positions")
parser.add_argument("-N", "--number", default=1, type=int)

BASE_URL = "https://www.premierleague.com"
links = {
    "goal": "/stats/top/players/goals",
    "saves": "/stats/top/players/saves",
}
console = Console()
print = console.print


def handle_cookie_banner(browser: webdriver.Firefox, delay: float = 0.6, timeout=30):
    delay /= 2
    m = browser.find_element(By.ID, "onetrust-pc-btn-handler")
    if m.is_displayed():
        WebDriverWait(browser, timeout).until(
            EC.element_to_be_clickable((By.ID, "onetrust-pc-btn-handler"))
        ).click()
        time.sleep(delay)

    n = browser.find_element(
        By.XPATH, "./html/body/div[2]/div[3]/div/div[3]/div[1]/button"
    )
    if n.is_displayed():
        WebDriverWait(browser, timeout).until(
            EC.element_to_be_clickable(
                (By.XPATH, "./html/body/div[2]/div[3]/div/div[3]/div[1]/button")
            )
        ).click()
        time.sleep(delay)


def close_vote_banner(browser: webdriver.Firefox, delay: float = 0.3, timeout=30):
    m = browser.find_element(By.ID, "advertClose")
    if not m.is_displayed():
        return
    WebDriverWait(browser, timeout).until(
        EC.element_to_be_clickable((By.ID, "advertClose"))
    ).click()
    time.sleep(delay)


def select_filter(
    browser: webdriver.Firefox, filter_name: str, filter_value: str, delay: float = 1.0
):
    print("Applying filter...")
    print(f"\tSelecting {filter_name}")
    WebDriverWait(browser, 60).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, f'div[data-dropdown-block="{filter_name}"]')
        )
    ).click()
    time.sleep(0.3)
    print(f"\tChange to {filter_value}")
    WebDriverWait(browser, 60).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, f'li[data-option-name="{filter_value.title()}"]')
        )
    ).click()
    print("Done applying filter.")
    time.sleep(delay)


def collect_data(
    season="All Seasons",
    club="All Clubs",
    nationality="All Nationalities",
    position="All Positions",
    n=10,
):
    options = Options()
    # options.add_argument("--headless")
    browser = webdriver.Firefox(options=options)

    print("Requesting home page...")

    if position == "All Positions":
        for link in links.values():
            browser.get(BASE_URL + link)
    elif position.lower() == "goalkeeper":
        browser.get(BASE_URL + links["saves"])
    else:
        browser.get(BASE_URL + links["goal"])

    handle_cookie_banner(browser)
    close_vote_banner(browser, delay=1)
    time.sleep(3)

    if season != parser.get_default("season"):
        select_filter(browser, "FOOTBALL_COMPSEASON", season)
    if club != parser.get_default("club"):
        select_filter(browser, "FOOTBALL_CLUB", club)
    if nationality != parser.get_default("nationality"):
        select_filter(browser, "Nationality", nationality)
    if position != parser.get_default("position"):
        select_filter(browser, "Position", position)

    time.sleep(2)

    print("Collecting redirect links...")

    table = browser.find_element(By.CLASS_NAME, "table.statsTable")
    names = table.find_elements(By.CLASS_NAME, "playerName")
    players = [
        {
            "name": name.text,
            "url": name.get_attribute("href").replace("/overview", "/stats"),
        }
        for name in names
    ]

    all_data = {}

    while len(all_data) < n:
        i = len(all_data)
        player = players[i]
        print(f"Requesting [green]{player['name']}[/green] stats page...")

        browser.get(player["url"])
        time.sleep(2)
        print("Collecting data...")

        if browser.find_element(By.ID, "advertClose").is_displayed():
            close_vote_banner(browser, delay=1)
        select_filter(browser, "compSeasons", season, 2.5)

        data_table = browser.find_element(
            By.XPATH, "./html/body/main/div[3]/div/div/div[2]/div/div/ul"
        )
        dmodel = model.DataExtractor(data_table)
        data = dmodel.get_stats(model.data_model.get(position.lower(), None))

        print(f"Process Complete for [green]{player['name']}[/green]")
        print(data)

        all_data[player["name"]] = data
        time.sleep(0.5)

    print("All data collected successfully!")
    print(all_data)
    browser.quit()
    return all_data


if __name__ == "__main__":
    args = parser.parse_args()
    collect_data(args.season, args.club, args.nationality, args.position, args.number)
