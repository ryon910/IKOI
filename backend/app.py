# 必要なライブラリのインポート
from flask import Flask, request
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
    #frontendからJSON形式で以下の情報を受け取る。
    values = request.get_json()
    employee_id = values.get('employee_id')
    from_date = values.get('from_date')
    to_date = values.get('to_date')

    # 文字列からdatetimeオブジェクトに変換
    from_date = datetime.strptime(from_date, '%Y-%m-%d')
    to_date = datetime.strptime(to_date, '%Y-%m-%d')

    # 取得関数を呼び出し(crud.pyに記載の関数get_filtered_recordsを、mymodels.pyに記載のRecordsテーブルに対して実行する。必要な引数も渡す。)
    result = crud.get_filtered_records(mymodels.Records, employee_id, from_date, to_date)
    return result, 200

# employee_idを指定することで、特定の人に表示すべきactionsデータを返すAPI
@app.route('/get_action_data', methods=['POST'])
def get_action_data():
    #frontendからJSON形式で以下の情報を受け取る。
    value = request.get_json()
    employee_id = value.get('employee_id')

    # 取得関数を呼び出し(crud.pyに記載の関数get_filtered_actionsを、mymodels.pyに記載のEmployeesテーブルに対して実行する。必要な引数も渡す。)
    result = crud.get_filtered_actions(mymodels.Employees, employee_id)
    return result, 200

# employee_idとrecord_dateとaction_idを渡すことで、recordsテーブルにデータを追加するAPI
@app.route('/add_records', methods=['POST'])
def add_records():
    #frontendからJSON形式で以下の情報を受け取る。
    data = request.get_json()
    employee_id = data['employee_id']
    record_date = datetime.strptime(data["record_date"], "%Y-%m-%d").date() #日付のデータはstr型なので、datetime型に変換する
    for action_id in data['action_ids']: #frontendからは複数のaction_idが送られてくるが、1つずつrecordsテーブルに追加する
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