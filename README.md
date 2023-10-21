# IAFD Web Scraping Script

This script is designed to scrape movie data from the Internet Adult Film Database (IAFD) from a given URL and write the data to a file. The data includes the movie title, cast names, and director.

## Installation

1. Clone the repository.
2. Navigate to the project directory.
3. Run the following command to install the necessary dependencies:

```bash
make install
```

## Usage

There are two ways to run the script:

### Terminal

To run the script via terminal, use the following command:

```bash
make run
```

When prompted, enter the URL of the movie. The script will scrape the data and write it to a file in the `sumarios` directory. The file will be named after the title of the movie.

### GUI

To run the script via GUI, use the following command:

```bash
make run-gui
```

In the GUI, enter the URL of the movie in the URL field, specify the destination folder, and click the "Run Script" button. The script will scrape the data and write it to a file in the specified directory. The file will be named after the title of the movie.

The GUI also provides an option to run the script in headless mode (without opening the browser window), and a button to clear the URL input.

## Cleaning Up

To clean up the generated files, use the following command:

```bash
make clean
```

This will delete all the `.pyc` files, `__pycache__` directories, `sumarios` directory, and the virtual environment.
