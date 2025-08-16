import sqlite3

conn = sqlite3.connect('weather.db')
cursor = conn.cursor()

# Drop the table if it exists (warning: deletes all existing data)
cursor.execute('DROP TABLE IF EXISTS weather_records;')

# Create the new table with updated schema
cursor.execute('''
CREATE TABLE weather_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    location VARCHAR(100) NOT NULL,
    date_range VARCHAR(50) NOT NULL,
    weather_data TEXT NOT NULL,
    created_at DATETIME DEFAULT (datetime('now')),
    updated_at DATETIME
);
''')

conn.commit()
conn.close()

print('weather_records table has been recreated with the updated schema.')
