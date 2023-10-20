# Summary Script

This script is used to scrape data from a given URL and write the data to a file.

## Installation

1. Clone the repository.
2. Navigate to the project directory.
3. Run the following command to install the necessary dependencies:

```bash
make install
```

## Usage

To run the script, use the following command:

```bash
make run
```

When prompted, enter the URL of the movie.

The script will scrape the data and write it to a file in the `sumarios` directory. The file will be named after the title of the movie and will contain the title, cast names, and director.

## Cleaning Up

To clean up the generated files, use the following command:

```bash
make clean
```
