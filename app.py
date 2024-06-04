from flask import Flask, jsonify, abort
import csv
import os
import utils
import re

app = Flask(__name__)

def parse_producers(producer_string):
    producers = []
    for producer in re.split(r'\band\b|,', producer_string):
        producers.append(producer.strip())
    return producers

def initialize_database():
    global conn
    conn = utils.get_db()
    utils.create_table(conn)

    file_path_csv = os.path.join(os.path.dirname(__file__), 'files', 'movielist.csv')

    # Check if the CSV file exists
    if not os.path.exists(file_path_csv):
        abort(404, "File not available.")

    # Read data from the CSV file and insert into the database
    with open(file_path_csv, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            producers = parse_producers(row['producers'])
            for producer in producers:
                if producer:
                    row['producers'] = producer
                    utils.insert_movie(row, conn)
    print('Banco de dados inicializado com sucesso!')
    return conn

conn = initialize_database()

def calculate_intervals():
    global conn
    intervals = {"min": [], "max": []}
    min_interval = 0
    max_interval = 0

    # Retrieve distinct producers who have won at least once (reduce processing data)
    producers = utils.get_winner_producers(conn)
    producer_count = 0

    for producer in producers:
        producer_count +=1
        producer_name = producer[0]

        # Retrieve the years when the producer won
        years = utils.get_producer_data(producer_name, conn)

        years.sort() # Sort years in ascending order

        # Calculate intervals between consecutive wins
        for i in range(len(years) - 1):
            interval = years[i + 1][0] - years[i][0]

            if producer_count == 1:
                min_interval = interval
                max_interval = interval

            if interval <= min_interval:
                intervals['min'].append({
                    "producer": producer_name,
                    "interval": interval,
                    "previousWin": years[i][0],
                    "followingWin": years[i + 1][0]
                })
                min_interval = interval

            if interval >= max_interval:
                intervals['max'].append({
                    "producer": producer_name,
                    "interval": interval,
                    "previousWin": years[i][0],
                    "followingWin": years[i + 1][0]
                })
                max_interval = interval

    # Filter the intervals and keep only those that are equal to the maximum and minimum intervals
    intervals['min'] = [record for record in intervals['min'] if record['interval'] == min_interval]
    intervals['max'] = [record for record in intervals['max'] if record['interval'] == max_interval]
    return intervals


@app.route('/awards/intervals', methods=['GET'])
def get_awards_intervals():
    intervals = calculate_intervals()
    return jsonify(intervals)

if __name__ == '__main__':
    app.run(debug=True)
