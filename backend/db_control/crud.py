# uname() error回避
import platform
print("platform", platform.uname())

# 必要なライブラリのインポート
import sqlalchemy
from sqlalchemy import insert
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import sessionmaker
from datetime import date
import json
from db_control.connect import engine
from db_control.mymodels import Employees, Positions, Records, Actions, Categories

# app.pyで使用する関数を以下に記載
# mymodelはmymodels.pyに記載のどのテーブルに対して操作をするかを指定する変数。

# mymodel,employee_id, from_date, to_dateを指定することで、特定の人、期間のrecordsデータを返す関数。
def get_filtered_records(employee_id, from_date:date, to_date:date):
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        query = session.query(Records, Employees, Actions, Categories, Positions) \
            .join(Employees, Records.employee_id == Employees.employee_id) \
            .join(Actions, Records.action_id == Actions.action_id) \
            .join(Categories, Actions.action_category_id == Categories.action_category_id) \
            .join(Positions, Employees.position_id == Positions.position_id) \
            .filter(Employees.employee_id == employee_id) \
            .filter(Records.record_date >= from_date) \
            .filter(Records.record_date <= to_date)

        result = query.all()
        result_dict_list = [{
            "employee_name": employee.employee_name,
            "record_date": record.record_date.strftime('%Y-%m-%d'),
            "action_name": action.action_name,
            "action_category_name": category.action_category_name,
            "position_name": position.position_name
        } for record, employee, action, category, position in result]

        result_json = json.dumps(result_dict_list, ensure_ascii=False)
        session.close()
        return result_json

    except NoResultFound:
        session.close()
        return json.dumps({"error": "No records found"}), 404
    except MultipleResultsFound:
        session.close()
        return json.dumps({"error": "Multiple records found"}), 400
    except DBAPIError as e:
        session.close()
        return json.dumps({"error": str(e)}), 500

# mymodel,employee_idを指定することで、特定の人に表示すべきactionsデータを返す関数。
def get_filtered_actions(employee_id):
    Session = sessionmaker(bind=engine)
    session = Session()

    # クエリの基点を明確にし、JOIN順を修正
    query = session.query(Actions.action_name, Categories.action_category_name, Positions.position_name) \
                .select_from(Employees) \
                .join(Records, Employees.employee_id == Records.employee_id) \
                .join(Actions, Records.action_id == Actions.action_id) \
                .join(Categories, Actions.action_category_id == Categories.action_category_id) \
                .join(Positions, Employees.position_id == Positions.position_id) \
                .filter(Employees.employee_id == employee_id)

    try:
        result = query.all()
        if not result:
            return json.dumps({"error": "No actions found for the given employee ID"}), 404

        # 結果をオブジェクトから辞書に変換し、リストに追加
        result_dict_list = [{
            "action_name": action_name,
            "category_name": category_name,
            "position_name": position_name
        } for action_name, category_name, position_name in result]

        # リストをJSONに変換
        result_json = json.dumps(result_dict_list, ensure_ascii=False)
        return result_json, 200

    except NoResultFound:
        return json.dumps({"error": "No actions found"}), 404
    except MultipleResultsFound:
        return json.dumps({"error": "Multiple actions found"}), 400
    except DBAPIError as e:
        return json.dumps({"error": f"Database query failed: {e}"}), 500
    finally:
        # セッションを閉じる
        session.close()


# mymodel, valuesを渡すことで、recordsテーブルにデータを追加する関数。
def add_new_record(record_model, values):
    # session構築
    Session = sessionmaker(bind=engine)
    session = Session()

    # モデルのインスタンスを作成
    instance = record_model(**values)
    try:
        # トランザクションを開始
        with session.begin():
            # データの挿入
            session.add(instance)
        return "Record inserted successfully."
    except sqlalchemy.exc.IntegrityError as e:
        print("Integrity Error: 一意制約違反により、挿入に失敗しました。", str(e))
        return "Integrity error occurred."
    except sqlalchemy.exc.SQLAlchemyError as e:
        print("SQLAlchemy Error: データベース操作中にエラーが発生しました。", str(e))
        return "Database error occurred."
    except Exception as e:
        print("General Error: 操作中に予期しないエラーが発生しました。", str(e))
        return "An unexpected error occurred."
    finally:
        # セッションを閉じる
        session.close()
