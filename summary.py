import sys

from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By


def get_driver(headless):
    # Chrome is giving us some issues when trying to run headless, so we use Firefox
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


def write_to_file(title, cast_names, director, year):
    """Write the title, cast_names, and director to a file named after the title."""
    print("creando fichero ...")
    Path(f"./sumarios/{year}").mkdir(parents=True, exist_ok=True)

    with open(f"./sumarios/{year}/{title}.txt", "w") as file:
        file.write(f"{title}\n-\n{' '.join(cast_names)}\n-\n{director} - {year}\n")
    print(f"fichero creado en: {Path(f'./sumarios/{year}').resolve()}/{title}.txt")


def get_parenthesis_content(string):
    """Extract the year from a string that contains it in parentheses."""
    start = string.find("(") + 1
    end = string.find(")")
    return string[start:end]


def get_cast_member_info(headless, person):
    """Retrieve and return the name and number of movies of a cast member."""
    person_tag = person.find_element(By.TAG_NAME, "a")
    href = person_tag.get_attribute("href")
    name = person_tag.text
    with get_driver(headless) as driver:
        driver.get(href)
        performer_credits = driver.find_element(
            By.XPATH, "/html/body/div/div[2]/div[2]/div[2]/ul/li[1]/a"
        ).text
        movies_number = int(get_parenthesis_content(performer_credits))
    print(f"{name} ({movies_number})")
    return {"name": name, "movies_number": movies_number}


def ordered_cast_members(headless, castbox):
    """Order the cast members by their number of movies and return them."""
    cast_members = [get_cast_member_info(headless, person) for person in castbox]
    return sorted(cast_members, key=lambda member: member["movies_number"], reverse=True)


def main(headless):
    """Main function that prompts for a URL, scrapes data, and writes it to a file."""
    url = input("Mete la URL de la peli: ")
    with get_driver(headless) as driver:
        driver.get(url)
        print("recopilando datos sobre la peli ...", end="")
        title = driver.find_element(By.TAG_NAME, "h1").text
        print(title)
        year = get_parenthesis_content(title)
        castbox = driver.find_elements(By.CLASS_NAME, "castbox")
        director = driver.find_element(By.XPATH, "/html/body/div/div[2]/div[1]/p[4]").text
        print("recopilando datos sobre el reparto ...")
        cast_members = ordered_cast_members(headless, castbox)
        write_to_file(title, [member["name"] for member in cast_members], director, year)


if __name__ == "__main__":
    headless = "--headless" in sys.argv
    main(headless)
