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
def get_filtered_records(mymodel, employee_id, from_date:date, to_date:date):
    # session構築
    Session = sessionmaker(bind=engine)
    session = Session()
    # 必要なテーブルを結合して、フィルターをかけて、必要なデータのみ抽出する。
    query = session.query(mymodel) \
            .join(Records, Records.employee_id == Employees.employee_id) \
            .join(Actions, Records.action_id == Actions.action_id) \
            .join(Categories, Actions.action_category_id == Categories.action_category_id) \
            .join(Positions, Employees.position_id == Positions.position_id) \
            .filter(Employees.employee_id == employee_id)\
            .filter(Records.record_date >= from_date)\
            .filter(Records.record_date <= to_date)

    try:
        # トランザクションを開始
        with session.begin():
            result = query.all()
        # 結果をオブジェクトから辞書に変換し、リストに追加
        result_dict_list = []
        for records_info in result:
            result_dict_list.append({
                "employee_name": records_info.employee_name,
                "record_date": records_info.record_date,
                "action_id": records_info.action_id,
                "action_name": records_info.action_name,
                "action_category_name": records_info.action_category_name,
            })
        # リストをJSONに変換
        result_json = json.dumps(result_dict_list, ensure_ascii=False)
    except NoResultFound:
        print("フィルターに一致するデータが存在しません。")
    except MultipleResultsFound:
        print("フィルターに一致するデータが複数存在します。")
    except DBAPIError as e:
        print("データベースのクエリ実行に失敗しました。エラー: ", e)

    # セッションを閉じる
    session.close()
    return result_json

# mymodel,employee_idを指定することで、特定の人に表示すべきactionsデータを返す関数。
def get_filtered_actions(mymodel, employee_id):
    # session構築
    Session = sessionmaker(bind=engine)
    session = Session()
    query = session.query(mymodel) \
            .join(Employees, Employees.position_id == Positions.position_id)\
            .join(Positions, Positions.position_id == Categories.position_id)\
            .join(Categories, Categories.action_category_id == Actions.action_category_id)\
            .filter(Employees.employee_id == employee_id)
    try:
        # トランザクションを開始
        with session.begin():
            result = query.all()
        # 結果をオブジェクトから辞書に変換し、リストに追加
        result_dict_list = []
        for actions_info in result:
            result_dict_list.append({
                "action_name": actions_info.action_name,
                "action_category_name": actions_info.action_category_name,
            })
        # リストをJSONに変換
        result_json = json.dumps(result_dict_list, ensure_ascii=False)
    except NoResultFound:
        print("フィルターに一致するデータが存在しません。")
    except MultipleResultsFound:
        print("フィルターに一致するデータが複数存在します。")
    except DBAPIError as e:
        print("データベースのクエリ実行に失敗しました。エラー: ", e)

    # セッションを閉じる
    session.close()
    return result_json


# mymodel, valuesを渡すことで、recordsテーブルにデータを追加する関数。
def add_new_record(mymodel, values):
    # session構築
    Session = sessionmaker(bind=engine)
    session = Session()

    # モデルのインスタンスを作成
    instance = mymodel(**values)
    try:
        # トランザクションを開始
        with session.begin():
            # データの挿入
            session.add(instance)
    except sqlalchemy.exc.IntegrityError:
        print("一意制約違反により、挿入に失敗しました")
        session.rollback()

    # セッションを閉じる
    session.close()
    return "inserted"
