import sqlite3

# Kết nối đến cơ sở dữ liệu hoặc tạo nếu chưa tồn tại
conn = sqlite3.connect('local_database.db')
conn = sqlite3.connect('/path/to/your/database/local_database.db')


# Tạo một đối tượng cursor để thực hiện các truy vấn SQL
cursor = conn.cursor()

# Tạo bảng User
cursor.execute('''
    CREATE TABLE IF NOT EXISTS User (
        user_id INTEGER PRIMARY KEY,
        user_name VARCHAR(50),
        password VARCHAR(50),
        email VARCHAR(50),
        created_at TIMESTAMP
    )
''')

# Tạo bảng Home
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Home (
        home_id INTEGER PRIMARY KEY,
        user_id INTEGER,
        name VARCHAR(50),
        FOREIGN KEY (user_id) REFERENCES User(user_id)
    )
''')

# Tạo bảng Room
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Room (
        room_id INTEGER PRIMARY KEY,
        home_id INTEGER,
        name VARCHAR(50),
        created_at TIMESTAMP,
        FOREIGN KEY (home_id) REFERENCES Home(home_id)
    )
''')

# Tạo bảng Light
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Light (
        light_id INTEGER PRIMARY KEY,
        room_id INTEGER,
        name INTEGER,
        color VARCHAR(50),
        flashing_cycle_time FLOAT,
        FOREIGN KEY (room_id) REFERENCES Room(room_id)
    )
''')

# Commit các thay đổi và đóng kết nối
conn.commit()
conn.close()
