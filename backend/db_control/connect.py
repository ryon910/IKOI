# Pythonの標準ライブラリで、実行中のプラットフォーム（オペレーティングシステムやハードウェアなど）に関する詳細情報を提供します。
# platform.uname(): システムの詳細情報を含む名前付きタプルを返します。これには、システム名、ノード名（フルネーム）、リリース、バージョン、マシンタイプ、およびプロセッサ情報が含まれます。

# uname() error回避
import platform
print(platform.uname())


# SQLAlchemyのコアコンポーネントで、データベースとのコネクションを確立するためのエンジンを作成
from sqlalchemy import create_engine
import sqlalchemy
import os

# ファイルパスの指定
main_path = os.path.dirname(os.path.abspath(__file__))
path = os.chdir(main_path)
print(path)
engine = create_engine("sqlite:///IKOI.db", echo=True)