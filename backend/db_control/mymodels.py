# データモデルの定義をするファイル

# 必要なライブラリのインポート
from sqlalchemy import ForeignKey, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import date

# DeclarativeBaseはSQLAlchemyの宣言的マッピングシステムの一部。データベーステーブルとPythonクラスを関連付けるための基底クラスです。
class Base(DeclarativeBase):
    pass

# 以下、全てのテーブルはBase()を継承。
# テーブル名、カラム名、データの型、主キー、外部キーなどをテーブルごとに定義していく。

#employees_master tableの定義
class Employees(Base):
    __tablename__ = 'employees_master'
    employee_id:Mapped[int] = mapped_column(primary_key=True)
    employee_pw:Mapped[str] = mapped_column()
    employee_name:Mapped[str] = mapped_column()
    email:Mapped[str] = mapped_column()
    position_id:Mapped[int] = mapped_column(ForeignKey("positions_master.position_id"))

#positions_master tableの定義
class Positions(Base):
    __tablename__ = 'positions_master'
    position_id:Mapped[int] = mapped_column(primary_key=True)
    position_name:Mapped[str] = mapped_column()

#records tableの定義
class Records(Base):
    __tablename__ = 'records'
    record_id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    employee_id:Mapped[int] = mapped_column(ForeignKey("employees_master.employee_id"))
    record_date:Mapped[date] = mapped_column(Date)
    action_id:Mapped[int] = mapped_column(ForeignKey("actions_master.action_id"))

#actions_master tableの定義
class Actions(Base):
    __tablename__ = 'actions_master'
    action_id:Mapped[int] = mapped_column(primary_key=True)
    action_name:Mapped[str] = mapped_column()
    action_category_id:Mapped[int] = mapped_column(ForeignKey("action_categories_master.action_category_id"))

#action_categories_master tableの定義
class Categories(Base):
    __tablename__ = 'action_categories_master'
    action_category_id:Mapped[int] = mapped_column(primary_key=True)
    action_category_name:Mapped[str] = mapped_column()
    position_id : Mapped[int] = mapped_column(ForeignKey("positions_master.position_id"))