from connect import get_connection

def create_tables():
    conn = get_connection()
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS records;')  # 既存のテーブルを削除
    c.execute('''
        CREATE TABLE records (
            record_id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT
        );
    ''')  # テーブルを再作成
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()