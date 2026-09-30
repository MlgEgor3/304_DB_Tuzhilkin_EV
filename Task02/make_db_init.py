import csv
import os
import re

def escape_sql(s):
    if s is None:
        return 'NULL'
    return "'" + str(s).replace("'", "''") + "'"

def parse_movie_title(title_str):
    match = re.search(r'\((\d{4})\)\s*$', title_str)
    if match:
        year = int(match.group(1))
        title = title_str[:match.start()].strip()
        return title, year
    return title_str, None

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_dir = os.path.join(script_dir, '..', 'dataset')
    output_file = os.path.join(script_dir, 'db_init.sql')

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("DROP TABLE IF EXISTS movies;\n")
        f.write("DROP TABLE IF EXISTS ratings;\n")
        f.write("DROP TABLE IF EXISTS tags;\n")
        f.write("DROP TABLE IF EXISTS users;\n\n")

        f.write("""CREATE TABLE movies (
    id INTEGER PRIMARY KEY,
    title TEXT,
    year INTEGER,
    genres TEXT
);

CREATE TABLE ratings (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    movie_id INTEGER,
    rating REAL,
    timestamp INTEGER
);

CREATE TABLE tags (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    movie_id INTEGER,
    tag TEXT,
    timestamp INTEGER
);

CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT,
    gender TEXT,
    register_date TEXT,
    occupation TEXT
);\n\n""")

        with open(os.path.join(dataset_dir, 'movies.csv'), 'r', encoding='utf-8') as mf:
            reader = csv.reader(mf)
            next(reader)
            for row in reader:
                mid, title_raw, genres = row
                title, year = parse_movie_title(title_raw)
                year_val = str(year) if year else 'NULL'
                f.write(f"INSERT INTO movies VALUES ({mid}, {escape_sql(title)}, {year_val}, {escape_sql(genres)});\n")

        with open(os.path.join(dataset_dir, 'ratings.csv'), 'r', encoding='utf-8') as rf:
            reader = csv.reader(rf)
            next(reader)
            rid = 1
            for row in reader:
                uid, mid, rating, ts = row
                f.write(f"INSERT INTO ratings VALUES ({rid}, {uid}, {mid}, {rating}, {ts});\n")
                rid += 1

        with open(os.path.join(dataset_dir, 'tags.csv'), 'r', encoding='utf-8') as tf:
            reader = csv.reader(tf)
            next(reader)
            tid = 1
            for row in reader:
                uid, mid, tag, ts = row
                f.write(f"INSERT INTO tags VALUES ({tid}, {uid}, {mid}, {escape_sql(tag)}, {ts});\n")
                tid += 1

        with open(os.path.join(dataset_dir, 'users.txt'), 'r', encoding='utf-8') as uf:
            for line in uf:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    uid, name, email, gender, reg_date, occ = parts
                    f.write(f"INSERT INTO users VALUES ({uid}, {escape_sql(name)}, {escape_sql(email)}, {escape_sql(gender)}, {escape_sql(reg_date)}, {escape_sql(occ)});\n")

    print(f"SQL-скрипт успешно сгенерирован: {output_file}")

if __name__ == '__main__':
    main()