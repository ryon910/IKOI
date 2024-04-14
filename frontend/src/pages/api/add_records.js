// pages/api/add_records.js
export default async function handler(req, res) {
    // POSTリクエストを処理
    if (req.method === 'POST') {
      try {
        // Flaskバックエンドへのリクエストを設定
        const flaskResponse = await fetch('http://localhost:5000/add_records', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(req.body),
        });
  
        // Flaskバックエンドからのレスポンスを確認
        if (!flaskResponse.ok) {
          // レスポンスがOKではない場合は、エラーメッセージを抽出して投げる
          const errorData = await flaskResponse.json();
          throw new Error(errorData.message || flaskResponse.statusText);
        }
  
        // レスポンスがOKの場合は、その内容をクライアントに転送
        const data = await flaskResponse.json();
        res.status(200).json(data);
      } catch (error) {
        // エラーハンドリング
        res.status(500).json({ message: error.message });
      }
    } else {
      // POST以外のリクエストに対して405 Method Not Allowedを返す
      res.setHeader('Allow', ['POST']);
      res.status(405).end(`Method ${req.method} Not Allowed`);
    }
  }
  