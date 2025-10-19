#!/usr/bin/env bash
set -euo pipefail

# Ensure output directory exists
mkdir -p output

# Step 1 — Run Python cleaning script
python clean.py

# Remove any old database file
rm -f data.db

# Step 2 — Create SQLite database and table
# TODO: Write a CREATE TABLE statement here. name the table "students" and define columns as follows:
# id (INTEGER), date (TEXT), category (TEXT), amount (TEXT)
sqlite3 data.db "
-- Your code under this line --
CREATE TABLE students (
    id INTEGER PRIMARY KEY,
    date TEXT,
    category TEXT,
    amount TEXT
);
"

# Step 3 — Import CSV into the students table inside data database
sqlite3 -cmd ".mode csv" -cmd ".separator ," data.db ".import --skip 1 output/cleaned.csv students"

# Step 4 — Run SQL query and save result
sqlite3 -header -csv data.db < query.sql > output/category_counts.csv


echo "Pipeline finished. Outputs are in ./output"
