#山脇書き換え構文
#外部キーのカラムデータタイプをTEXTに変更
#record_dateのデータタイプをDateからTEXTに変更するべき　by GPT（SQLiteはDate型をネイティブにサポートしていないため）。関数を入れたため動くと思うが。
from sqlalchemy import Column, String, ForeignKey, Integer, Date, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import date
from sqlalchemy.orm import Mapped, mapped_column

Base = declarative_base()

class Employees(Base):
    __tablename__ = 'employees_master'
    employee_id = Column(String, primary_key=True)
    employee_pw = Column(String)
    employee_name = Column(String)
    email = Column(String)
    position_id = Column(String, ForeignKey('positions_master.position_id'))

class Positions(Base):
    __tablename__ = 'positions_master'
    position_id = Column(String, primary_key=True)
    position_name = Column(String)

class Categories(Base):
    __tablename__ = 'action_categories_master'
    action_category_id = Column(String, primary_key=True)
    action_category_name = Column(String)
    position_id = Column(String, ForeignKey('positions_master.position_id'))

class Actions(Base):
    __tablename__ = 'actions_master'
    action_id = Column(String, primary_key=True)
    action_name = Column(String)
    action_category_id = Column(String, ForeignKey('action_categories_master.action_category_id'))
    feedback = Column(String)  #山脇追加　中野さんに要確認

class Records(Base):
    __tablename__ = 'records'
    record_id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(String, ForeignKey('employees_master.employee_id'))
    # record_date = Column(String)　dateが有効ならそのまま使いたい、ここでエラーが出たらstringに変更する by 山脇
    record_date:Mapped[date] = mapped_column(Date)
    action_id = Column(String, ForeignKey('actions_master.action_id'))




# # 中野さん作成データ　データモデルの定義をするファイル

# # 必要なライブラリのインポート
# from sqlalchemy import ForeignKey, Date
# from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
# from datetime import date

# # DeclarativeBaseはSQLAlchemyの宣言的マッピングシステムの一部。データベーステーブルとPythonクラスを関連付けるための基底クラスです。
# class Base(DeclarativeBase):
#     pass

# # 以下、全てのテーブルはBase()を継承。
# # テーブル名、カラム名、データの型、主キー、外部キーなどをテーブルごとに定義していく。

# #employees_master tableの定義
# class Employees(Base):
#     __tablename__ = 'employees_master'
#     employee_id:Mapped[str] = mapped_column(primary_key=True)
#     employee_pw:Mapped[str] = mapped_column()
#     employee_name:Mapped[str] = mapped_column()
#     email:Mapped[str] = mapped_column()
#     position_id:Mapped[int] = mapped_column(ForeignKey("positions_master.position_id"))

# #positions_master tableの定義
# class Positions(Base):
#     __tablename__ = 'positions_master'
#     position_id:Mapped[str] = mapped_column(primary_key=True)
#     position_name:Mapped[str] = mapped_column()

# #records tableの定義
# class Records(Base):
#     __tablename__ = 'records'
#     record_id:Mapped[str] = mapped_column(primary_key=True, autoincrement=True)
#     employee_id:Mapped[int] = mapped_column(ForeignKey("employees_master.employee_id"))
#     record_date:Mapped[date] = mapped_column(Date)
#     action_id:Mapped[int] = mapped_column(ForeignKey("actions_master.action_id"))

# #actions_master tableの定義
# class Actions(Base):
#     __tablename__ = 'actions_master'
#     action_id:Mapped[str] = mapped_column(primary_key=True)
#     action_name:Mapped[str] = mapped_column()
#     action_category_id:Mapped[int] = mapped_column(ForeignKey("action_categories_master.action_category_id"))

# #action_categories_master tableの定義
# class Categories(Base):
#     __tablename__ = 'action_categories_master'
#     action_category_id:Mapped[str] = mapped_column(primary_key=True)
#     action_category_name:Mapped[str] = mapped_column()
#     position_id : Mapped[int] = mapped_column(ForeignKey("positions_master.position_id"))
