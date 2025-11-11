import pymysql
from flask import Blueprint, jsonify, request

from db_connector import get_db_connection

borrow_blueprint = Blueprint('borrows', __name__, url_prefix='/borrows')


# === 1️⃣ 查询所有借阅记录 ===
@borrow_blueprint.route('/', methods=['GET'])
def get_all_records():
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM borrow_record")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)


# === 2️⃣ 查询单条记录 ===
@borrow_blueprint.route('/<int:record_id>', methods=['GET'])
def get_record(record_id):
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM borrow_record WHERE id=%s", (record_id,))
    record = cursor.fetchone()
    cursor.close()
    conn.close()
    if record:
        return jsonify(record)
    return jsonify({'error': 'Record not found'}), 404


# === 3️⃣ 新增记录 ===
@borrow_blueprint.route('/', methods=['POST'])
def create_record():
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = """INSERT INTO borrow_record (person_id, material_id, borrow_date, expected_return, 
             return_date, status, quantity, remark)
             VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
    values = (
        data.get('person_id'),
        data.get('material_id'),
        data.get('borrow_date'),
        data.get('expected_return'),
        data.get('return_date'),
        data.get('status', 'borrowing'),
        data.get('quantity', 1),
        data.get('remark')
    )
    cursor.execute(sql, values)
    conn.commit()
    new_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return jsonify({'message': 'Record created', 'id': new_id}), 201


# === 4️⃣ 更新记录 ===
@borrow_blueprint.route('/<int:record_id>', methods=['PUT'])
def update_record(record_id):
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = """UPDATE borrow_record
             SET person_id=%s, material_id=%s, borrow_date=%s, expected_return=%s,
                 return_date=%s, status=%s, quantity=%s, remark=%s
             WHERE id=%s"""
    values = (
        data.get('person_id'),
        data.get('material_id'),
        data.get('borrow_date'),
        data.get('expected_return'),
        data.get('return_date'),
        data.get('status'),
        data.get('quantity'),
        data.get('remark'),
        record_id
    )
    cursor.execute(sql, values)
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Record updated'})


# === 5️⃣ 删除记录 ===
@borrow_blueprint.route('/<int:record_id>', methods=['DELETE'])
def delete_record(record_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM borrow_record WHERE id=%s", (record_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Record deleted'})

@borrow_blueprint.route('/query', methods=['GET'])
def get_record_by_person_or_material():
    person_id = request.args.get('person_id')
    material_id = request.args.get('material_id')

    # 没有任何参数
    if not person_id and not material_id:
        return jsonify({'error': 'Please provide person_id or material_id'}), 400

    sql = "SELECT * FROM borrow_record WHERE 1=1"
    params = []

    if person_id:
        sql += " AND person_id=%s"
        params.append(person_id)
    if material_id:
        sql += " AND material_id=%s"
        params.append(material_id)

    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql, params)
    records = cursor.fetchall()
    cursor.close()
    conn.close()

    if records:
        return jsonify(records)
    return jsonify({'error': 'No records found'}), 404