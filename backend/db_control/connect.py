from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
import os

# ファイルパスの指定
main_path = os.path.dirname(os.path.abspath(__file__))
database_path = os.path.join(main_path, 'IKOI.db')

# エンジンの作成
engine = create_engine(
    f"sqlite:///{database_path}",
    echo=True
)

# SQLiteで外部キーを有効にするためのリスナー関数
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
