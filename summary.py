import argparse
import re
import traceback

from pathlib import Path

from retrying import retry
from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from exceptions import InternalException
from logs import logger


def get_driver(headless):
    """
    Get a webdriver. Use Firefox if headless mode is enabled, otherwise use Chrome.

    Parameters:
    headless (bool): Whether to run the browser in headless mode.

    Returns:
    webdriver: The webdriver.
    """
    if headless:
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")
        options.set_capability("pageLoadStrategy", "eager")
        return webdriver.Firefox(options=options)

    options = webdriver.ChromeOptions()
    options.set_capability("pageLoadStrategy", "eager")
    return webdriver.Chrome(options=options)


def ask_user_for_url():
    """Prompt the user for a URL and return it."""
    url = input("Mete la URL de la peli: ")
    return url


def write_to_file(title, cast_names, director, year, folder):
    """Write the title, cast_names, and director to a file named after the title."""
    print("creando fichero ...")
    Path(f"{folder}").mkdir(parents=True, exist_ok=True)

    with open(f"{folder}/{title}.txt", "w") as file:
        file.write(f"{title}\n.\n{' '.join(cast_names)}\n.\n{director}\n".upper())
    print(f"fichero creado en: {Path(f'{folder}').resolve()}/{title}.txt")


def get_parenthesis_content(string):
    """
    Extract the content inside the first pair of parentheses in a string.

    Parameters:
    string (str): The string to extract from.

    Returns:
    str: The content inside the parentheses.
    """
    start = string.find("(") + 1
    end = string.find(")")
    return string[start:end]


def get_cast_member_info(headless, person):
    """
    Retrieve and return the name and number of movies of a cast member.

    Parameters:
    headless (bool): Whether to run the browser in headless mode.
    person (selenium.webdriver.remote.webelement.WebElement): The WebElement representing
    the cast member.

    Returns:
    dict: A dictionary containing the name and number of movies of the cast member.
    """
    person_tag = person.find_element(By.TAG_NAME, "a")
    href = person_tag.get_attribute("href")
    name = person_tag.text
    gender = re.match(".*/gender=(.)/", href).group(1)

    with get_driver(headless) as driver:
        driver.get(href)
        performer_credits = driver.find_element(
            By.XPATH, "/html/body/div/div[2]/div[2]/div[2]/ul/li[1]/a"
        ).text
        movies_number = int(get_parenthesis_content(performer_credits))
    return {"name": name, "movies_number": movies_number, "gender": gender}


def ordered_cast_members(headless, castbox):
    """
    Order the cast members by their number of movies and return them.

    Parameters:
    headless (bool): Whether to run the browser in headless mode.
    castbox (list): A list of WebElements representing the cast members.

    Returns:
    list: A list of dictionaries containing the names and number of movies of the
    cast members, ordered by number of movies.
    """
    cast_members = []
    for person in castbox:
        data = get_cast_member_info(headless, person)
        if not data["name"].startswith("Unknown"):
            cast_members.append(data)
    return sorted(
        cast_members,
        key=lambda member: (member["gender"] == "f", member["movies_number"]),
        reverse=True,
    )


def get_url(url):
    """
    Prompt the user for a URL if none is provided.

    Parameters:
    url (str): The URL provided.

    Returns:
    str: The URL.
    """
    if url is None:
        url = input("Mete la URL de la peli: ")
    return url


@retry(
    retry_on_exception=lambda e: isinstance(e, (InternalException)),
    stop_max_attempt_number=3,
    wait_fixed=2000,
)
def main(headless, url, folder):
    """
    Main function that prompts for a URL, scrapes data, and writes it to a file.

    Parameters:
    headless (bool): Whether to run the browser in headless mode.
    url (str): The URL to be searched.
    folder (str): The destination folder for the generated file.
    """
    url = get_url(url)
    try:
        with get_driver(headless) as driver:
            print("getting page at url: ", url)
            driver.get(url)
            print("recopilando datos sobre la peli... ", end="")
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "h1"))
            )
            title = driver.find_element(By.TAG_NAME, "h1").text
            print(title)
            year = get_parenthesis_content(title)
            castbox = driver.find_elements(By.CLASS_NAME, "castbox")
            director = driver.find_element(
                By.XPATH, "/html/body/div/div[2]/div[1]/p[4]"
            ).text
            print("recopilando datos sobre el reparto... ")
            cast_members = ordered_cast_members(headless, castbox)
            write_to_file(
                title, [member["name"] for member in cast_members], director, year, folder
            )

    except NoSuchElementException:
        error_message = (
            f"{traceback.format_exc()}\nURL: {url}. An element was not found on the page."
        )
        logger.error(error_message)
        raise InternalException(error_message)
    except TimeoutException:
        error_message = f"{traceback.format_exc()}\nURL: {url}. The operation timed out."
        logger.error(error_message)
        raise InternalException(error_message)
    except WebDriverException as e:
        error_message = (
            f"{traceback.format_exc()}\nURL: {url}. A WebDriver exception occurred: {e}."
        )
        logger.error(error_message)
        raise InternalException(error_message)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Web scraping script.")
    parser.add_argument(
        "--headless", action="store_true", help="Run the script in headless mode."
    )
    parser.add_argument("-u", "--url", type=str, help="URL to be searched.")
    parser.add_argument(
        "-f",
        "--folder",
        type=str,
        default="./sumarios",
        help="Destination folder for the generated file.",
    )
    args = parser.parse_args()
    main(args.headless, args.url, args.folder)
