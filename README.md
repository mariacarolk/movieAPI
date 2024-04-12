<h1 style="text-align: center;"> Golden Raspberry Awards API Service </h1>
This Flask application provides an API endpoint to retrieve intervals between awards won for Golden Raspberry Awards by movie producers. It also includes integration tests to ensure the correctness of the data and the functionality of the API endpoint.

## Prerequisites
Before running the application or the tests, ensure you have the following prerequisites installed:

* Python 3.x
* Flask
* pytest

## Installation
1. Clone this repository to your local machine:


```
git clone https://github.com/mariacarolk/movieAPI
```

2 - Install dependencies:

```
pip install -r requirements.txt
```

3. Save the CSV file:

The CSV file should be saved in the directory **/files** with the name: **movielist.csv**.

## Usage

### Running the Application

To run the Flask application:

```
python app.py
```

The application will start on http://127.0.0.1:5000/ by default.

### Running Integration Tests

To run the integration tests:

```
pytest test_integration.py
```

This will execute the integration tests defined in test_integration.py and provide output regarding the success or failure of each test.

## Structure
* app.py: Contains the Flask application code, including the route definitions.
* test_integration.py: Integration tests for the Flask application, covering the /awards/intervals endpoint and related functionality.
* utils.py: Utility functions for interacting with the database and handling data.

## Database
The application uses an in-memory SQLite database initialized with data from a CSV file (movielist.csv). The database schema includes a movies table to store movie details.

## Endpoints
/awards/intervals (GET)
This endpoint returns JSON data containing information about the movie producer who has the longest interval between two consecutive awards at the Golden Raspberry Awards, and also provides details about the producer with the shortest interval between two consecutive awards. The data includes details about the producers, such as their names and the intervals between the awards they have won.

## Testing
Integration tests are included to verify the correctness of the data returned by the API endpoint, as well as to ensure the integrity of the CSV file used to initialize the database.
