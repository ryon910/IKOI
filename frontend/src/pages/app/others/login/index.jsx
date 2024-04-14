import { useState } from 'react';
import Link from 'next/link';

export default function LoginForm() {
  const [email, setEmail] = useState('');
  const [id, setId] = useState('');
  const [user, setUser] = useState(null);
  const [message, setMessage] = useState('');
  const [showModal, setShowModal] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    try {
      const res = await fetch('http://127.0.0.1:5000/fetchtest');
      if (!res.ok) throw new Error(res.statusText);

      const data = await res.json();
      const user = data.find((user) =>
        user.email === email && user.id.toString() === id
      );

      if (user) {
        setUser(user.name);
        setMessage('');
        setShowModal(true);
      } else {
        setUser(null);
        setMessage('データが一致しません');
        setShowModal(false);
      }
    } catch (error) {
      console.error('Failed to fetch data:', error);
      setMessage('データの取得に失敗しました');
      setShowModal(false);
    }
  }

  return (
    <div className="flex flex-col items-center justify-center h-screen bg-gray-100">
      <form className="p-10 bg-white rounded-lg shadow-lg" onSubmit={handleSubmit}>
        <div className="mb-6">
          <label htmlFor="email" className="block mb-2 text-sm font-medium text-gray-900">Email:</label>
          <input
            type="email"
            id="email"
            className="input input-bordered w-full max-w-xs"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div className="mb-6">
          <label htmlFor="id" className="block mb-2 text-sm font-medium text-gray-900">Id:</label>
          <input
            type="text"
            id="id"
            className="input input-bordered w-full max-w-xs"
            value={id}
            onChange={(e) => setId(e.target.value)}
            required
          />
        </div>
        <button type="submit" className="btn btn-primary">Login</button>
      </form>

      {showModal && (
        <div className="modal modal-open">
          <div className="modal-box">
            <h3 className="font-bold text-lg">ようこそ、{user}さん</h3>
            <p className="py-4">Weekly Reportへ進んでください。</p>
            <div className="modal-action font-bold text-lg">
              <Link href="/weekly">Your Weekly Page</Link>
              <a href="#" className="btn" onClick={() => setShowModal(false)}>閉じる</a>
            </div>
          </div>
        </div>
      )}

      {message && <p className="mt-2 text-sm text-red-500">{message}</p>}
    </div>
  );
}
