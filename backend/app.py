# 必要なライブラリのインポート
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from db_control import mymodels, crud
from datetime import datetime

# Flaskアプリのインスタンスを生成。CORSによって、異なるドメインからのappへのリクエストを許可。
app = Flask(__name__)
CORS(app)

# Flaskトップページの表示
@app.route('/')
def index():
    return "WELCOME to IKOI app"

# employee_idとrecord_dateの期間を指定することで、特定の人、期間のrecordsデータを返すAPI
@app.route('/get_records', methods=['POST'])
def get_records():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    values = request.get_json()

    try:
        employee_id = int(values['employee_id'])  # 整数への変換を試みる
        from_date = datetime.strptime(values['from_date'], '%Y-%m-%d')
        to_date = datetime.strptime(values['to_date'], '%Y-%m-%d')
    except KeyError as e:
        return jsonify({'error': f'Missing data for key: {e}'}), 400
    except ValueError as e:
        return jsonify({'error': f'Invalid date format or data type: {e}'}), 400

    result = crud.get_filtered_records(employee_id, from_date, to_date)
    if result:
        return jsonify(result), 200
    else:
        return jsonify({'error': 'No records found'}), 404

# employee_idを指定することで、特定の人に表示すべきactionsデータを返すAPI
@app.route('/get_action_data', methods=['POST'])
def get_action_data():
    if not request.is_json:
        return jsonify({"error": "Request body must be JSON"}), 400

    value = request.get_json()
    employee_id = value.get('employee_id')

    if employee_id is None:
        return jsonify({"error": "Missing employee_id"}), 400

    try:
        employee_id = int(employee_id)  # 整数への変換を確実に行う
    except ValueError:
        return jsonify({"error": "employee_id must be an integer"}), 400

    try:
        result = crud.get_filtered_actions(employee_id)
        if not result:
            return jsonify({"error": "No actions found"}), 404
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# employee_idとrecord_dateとaction_idを渡すことで、recordsテーブルにデータを追加するAPI
@app.route('/add_records', methods=['POST'])
def add_records():
    # frontendからJSON形式で以下の情報を受け取る。
    data = request.get_json()
    employee_id = data['employee_id']
    record_date = datetime.strptime(data["record_date"], "%Y-%m-%d").date()  # 日付のデータはstr型なので、datetime型に変換する
    for action_id in data['action_ids']:  # frontendからは複数のaction_idが送られてくるが、1つずつrecordsテーブルに追加する
        values = {
            'employee_id': employee_id,
            'record_date': record_date,
            'action_id': action_id,
        }
        # 登録関数の呼び出し(crud.pyに記載の関数add_new_recordを、mymodels.pyに記載のRecordsテーブルに対して実行する。必要な引数も渡す。)
        crud.add_new_record(mymodels.Records, values)
    return "All records inserted"


# frontend側のfetchtest用のAPI。jsonplaceholderというサービスを利用。
@app.route("/fetchtest")
def fetchtest():
    response = requests.get('https://jsonplaceholder.typicode.com/users')
    return response.json(), 200


if __name__ == '__main__':
    app.run(debug=True)