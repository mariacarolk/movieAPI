import pytest
from app import app
import csv
import os

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_get_awards_intervals(client):
    response = client.get('/awards/intervals')
    assert response.status_code == 200
    data = response.json

    # Verify the structure and content of the JSON response
    assert 'min' in data
    assert 'max' in data
    assert isinstance(data['min'], list)
    assert isinstance(data['max'], list)
    # Add more assertions to validate the data format and values as needed

def test_header_count():
    # Ensure that the CSV file has the correct number of headers
    file_path_csv = os.path.join(os.path.dirname(__file__), 'files', 'movielist.csv')
    with open(file_path_csv, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        headers = next(reader)  # Get the headers
        assert len(headers) == 5

def test_header_names():
    # Ensure that the CSV file has the correct header names
    expected_headers = ['year','title','studios','producers','winner']
    file_path_csv = os.path.join(os.path.dirname(__file__), 'files', 'movielist.csv')
    with open(file_path_csv, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        headers = next(reader)  # Get the headers
        assert headers == expected_headers

if __name__ == "__main__":
    pytest.main([__file__])
