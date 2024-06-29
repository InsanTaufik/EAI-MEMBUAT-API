from flask import Flask, request, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

# MYSQL Config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'sekolah'
mysql = MySQL(app)

@app.route('/')
def root():
    return "tugas membuat API"

@app.route('/orang')
def orang():
    return jsonify({'name': 'insan',
                    'address': 'bandung'})

@app.route('/guru', methods=['GET', 'POST'])
def guru():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM GURU")

        column_names = [i[0] for i in cursor.description]

        data = []
        for row in cursor.fetchall():
            data.append(dict(zip(column_names, row)))

        cursor.close()
        return jsonify(data)

    elif request.method == 'POST':
        nama = request.json['nama']
        mapel = request.json['mata_pelajaran']
        # Open Connection and Insert to DB
        cursor = mysql.connection.cursor()
        sql = "INSERT INTO GURU (nama, mata_pelajaran) VALUES (%s, %s)"
        val = (nama, mapel)
        cursor.execute(sql, val)
        # Commit to DB
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'data added successfully!'})

@app.route('/detailguru/<int:id>')
def detailguru(id):
    cursor = mysql.connection.cursor()
    sql = "SELECT * FROM GURU WHERE guru_id = %s"
    val = (id,)
    cursor.execute(sql, val)
    column_names = [i[0] for i in cursor.description]
    data = []
    for row in cursor.fetchall():
        data.append(dict(zip(column_names, row)))
    cursor.close()
    return jsonify(data)

@app.route('/deleteguru/<int:id>', methods=['DELETE'])
def deleteguru(id):
    cursor = mysql.connection.cursor()
    sql = "DELETE FROM GURU WHERE guru_id = %s"
    val = (id,)
    cursor.execute(sql, val)
    mysql.connection.commit()
    cursor.close()
    return jsonify({'message': 'data deleted successfully!'})

@app.route('/editguru/<int:id>', methods=['PUT'])
def editguru(id):
    data = request.get_json()
    cursor = mysql.connection.cursor()
    sql = "UPDATE GURU SET nama=%s, mata_pelajaran=%s WHERE guru_id = %s"
    val = (data['nama'], data['mata_pelajaran'], id)
    cursor.execute(sql, val)
    mysql.connection.commit()
    cursor.close()
    return jsonify({'message': 'data updated successfully!'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=50, debug=True)
