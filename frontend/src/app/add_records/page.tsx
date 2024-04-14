"use client";
import { useState } from 'react';

export default function Record() {
    const [responseMessage, setResponseMessage] = useState("");
    const [selectedActions, setSelectedActions] = useState<number[]>([]);

    const toggleAction = (id: number) => {
        setSelectedActions(prev =>
        prev.includes(id) ? prev.filter(item => item !== id) : [...prev, id]
        );
    };

    const postData = async () => {
        const japanTime = new Date().toLocaleString("ja-JP", { timeZone: "Asia/Tokyo" });
        const japanDate = new Date(japanTime);
        const formattedDate = japanDate.toISOString().split('T')[0];

        try {
        const response = await fetch('http://127.0.0.1:5000/add_records', {
            method: 'POST',
            headers: {
            'Content-Type': 'application/json',
            },
            body: JSON.stringify({
            employee_id: 5,
            record_date: formattedDate,
            action_ids: selectedActions.sort((a, b) => a - b)
            })
        });

        const responseBody = await response.text();  // テキストとしてレスポンスを受け取る

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}; Body: ${responseBody}`);
        }

        // レスポンスが 'All records inserted' というテキストを含む場合、成功と見なす
        if (responseBody === "All records inserted") {
            setResponseMessage("Record added successfully!");
        } else {
            throw new Error(`Unexpected response body: ${responseBody}`);
        }
        } catch (error) {
        setResponseMessage(`Failed to add record. ${error}`);
        console.error('Error:', error);
        }
    };

    return (
        <div>
        <h1>Add Record</h1>
        <div>
            {Array.from({ length: 10 }, (_, i) => i + 1).map(id => (
            <button key={id} onClick={() => toggleAction(id)}
                style={{ margin: "4px", backgroundColor: selectedActions.includes(id) ? "lightblue" : "initial" }}>
                {id}
            </button>
            ))}
        </div>
        <button onClick={postData}>Send Data</button>
        <p>Response: {responseMessage}</p>
        </div>
    );
}
