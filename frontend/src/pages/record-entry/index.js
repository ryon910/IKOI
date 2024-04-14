//データをインプットするファイル

import { useState } from 'react';

export default function RecordEntry() {
  // ユーザーID、登録日、アクションに関する状態を保持する
  const [userId, setUserId] = useState('');
  const [recordDate, setRecordDate] = useState('');
  const [actions, setActions] = useState({
    action1: false,
    action2: false,
    action3: false,
    action4: false,
    action5: false
  });

  // 入力値を状態に設定するハンドラー
  const handleInputChange = (e) => {
    const { name, value, checked, type } = e.target;
    if (type === 'checkbox') {
      // アクションの処理
      setActions({ ...actions, [name]: checked });
    } else {
      // ユーザーIDと登録日の処理
      if (name === 'userId') setUserId(value);
      if (name === 'recordDate') setRecordDate(value);
    }
  };

  // フォーム送信ハンドラー
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // 選択されたアクションのIDを取得
    const selectedActionIds = Object.entries(actions)
      .filter(([key, value]) => value)
      .map(([key]) => parseInt(key.replace('action', ''), 10)); // 'action1' -> 1 に変換

    // データを整形　//FlaskのIKOI.dbのKey名にあうように変更をかけました。

    const dataToSend = {
      employee_id: userId, // Flaskが期待するキー名に変更
      record_date: recordDate, // Flaskが期待するフォーマットを保証
      action_ids: selectedActionIds // 選択されたアクションIDの配列
    };

    // POSTリクエストを送信
    try {
      const response = await fetch('/api/add_records', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(dataToSend)
      });
      if (!response.ok) {
        const errorData = await response.json(); // エラーメッセージを取得
        throw new Error(errorData.message || 'Something went wrong');
      }
      // 成功時の処理
      console.log('Data sent successfully');
    } catch (error) {
      // エラー処理
      console.error('データ入力がうまくいきませんでした', error);
    }
  };

  // ここで入力フォームのUIを返す
  return (
    <form onSubmit={handleSubmit}>
      <label htmlFor="userId">ユーザーID:</label>
      <input
        type="text"
        id="userId"
        name="userId"
        value={userId}
        onChange={handleInputChange}
        required
      />
      <br />
      <label htmlFor="recordDate">登録日:</label>
      <input
        type="date"
        id="recordDate"
        name="recordDate"
        value={recordDate}
        onChange={handleInputChange}
        required
      />
      <br />
      {/* 以下、5つのアクションに対するチェックボックスを作成 */}
      <div>
        {Object.keys(actions).map((action, index) => (
          <label key={action}>
            <input
              type="checkbox"
              name={action}
              checked={actions[action]}
              onChange={handleInputChange}
            />
            質問{index + 1}
          </label>
        ))}
      </div>
      <button type="submit">登録する</button>
    </form>
  );
}
