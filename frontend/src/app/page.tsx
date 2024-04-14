"use client";
import { useState, useEffect } from 'react';

export default function Record() {
  const [data, setData] = useState(null);
  const [additionalData, setAdditionalData] = useState(null); // 別のAPIからのデータ用のstate

  const fetchData = async () => {
    const response = await fetch('http://127.0.0.1:5000/get_records', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        employee_id: 5,
        from_date: "2024-04-01",
        to_date: "2024-04-05"
      })
    });

    if (!response.ok) {
      throw new Error('Failed to fetch data');
    }

    const json = await response.json();
    setData(json);
  };

  const fetchAdditionalData = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/get_action_data', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          employee_id: 5
        })
      });

      if (!response.ok) {
        throw new Error('Failed to fetch additional data');
      }

      const json = await response.json();
      setAdditionalData(json);
    } catch (error) {
      console.error('Fetch error:', error);
      setAdditionalData(null); // エラーが発生した場合、additionalDataをnullに設定
    }
  };

  useEffect(() => {
    fetchData();
    fetchAdditionalData();
  }, []);

  return (
    <div>
      <h1>Original Data</h1>
      <pre>{data ? JSON.stringify(data, null, 2) : "No data fetched"}</pre>
      <h1>Additional Data</h1>
      <pre>{additionalData ? JSON.stringify(additionalData, null, 2) : "No additional data fetched"}</pre>
    </div>
  );
}
