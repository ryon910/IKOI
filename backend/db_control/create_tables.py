# Pythonの標準ライブラリplatformをインポートしています。このモジュールは、実行中のシステムに関する詳細情報を提供する関数群を含む
# システムの詳細情報（システム名、ノード名、リリース、バージョン、マシン、プロセッサに関する情報）を返す関数
import platform
print(platform.uname())

# mymodels.pyからBaseクラスをインポート
# Baseを継承して定義されたすべてのテーブルクラスに基づいて、データベースにテーブルを作成
# このプロセスは、特に新しいアプリケーションを初めてセットアップする際や、モデルが更新されてデータベーススキーマを再構築する必要がある際に使用される
from mymodels import Base
from connect import engine

print("Creating tables >>> ")
Base.metadata.create_all(bind=engine)