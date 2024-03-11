from flask import Flask, jsonify
from flask_mysqldb import MySQL
import math

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask'

mysql = MySQL(app)

@app.route('/rooms/<string:room_id>', methods=['GET'])
def room_info(room_id):
    try:
        cursor = mysql.connection.cursor()

        sql = (
            "SELECT light.name, light.color, light.flashing_cycle_time "
            "FROM light "
            "JOIN room_light  "
            "   ON light.light_id = room_light.light_id  "
            "JOIN room  "
            "   ON room_light.room_id = room.room_id "
            "WHERE room.room_id = %s "
            "ORDER BY "
            "  CASE light.color "
            "     WHEN 'red' THEN 1 "
            "     WHEN 'orange' THEN 2 "
            "     WHEN 'yellow' THEN 3 "
            "     WHEN 'green' THEN 4 "
            "     WHEN 'blue' THEN 5 "
            "     WHEN 'indigo' THEN 6 "
            "     WHEN 'violet' THEN 7 "
            "     ELSE 8 "
            "END; "
        )

        params = [
            room_id
        ]

        cursor.execute(sql, params)

        result = cursor.fetchall()
        cursor.close()

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)})


def get_distance(flashing_cycle_times):
    if len(flashing_cycle_times) == 0:
        return 0
    return math.lcm(*flashing_cycle_times) - 1


@app.route('/check_lights/<string:room_id>', methods=['GET'])
def check_lights(room_id):
    try:

        lights = room_info(room_id)

        flashing_cycle_times = list(map(lambda lights: lights["flashing_cycle_time"]))

        resurt = get_distance(flashing_cycle_times)
        return resurt

    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == '__main__':
    app.run()
