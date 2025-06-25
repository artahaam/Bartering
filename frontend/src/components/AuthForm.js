import { useState } from 'react';

export default function AuthForm({ onSubmit, type = 'login' }) {
  const [form, setForm] = useState({ username: '', password: '' });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(form);
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white dark:bg-gray-800 shadow-md rounded p-6 w-full max-w-sm mx-auto mt-12 space-y-4 font-sahel">
      <h2 className="text-center text-xl font-bold text-indigo-600">
        {type === 'login' ? 'ورود' : 'ثبت‌نام'}
      </h2>
      <input
        name="username"
        value={form.username}
        onChange={handleChange}
        placeholder="نام کاربری"
        className="w-full p-2 border rounded"
        required
      />
      <input
        type="password"
        name="password"
        value={form.password}
        onChange={handleChange}
        placeholder="رمز عبور"
        className="w-full p-2 border rounded"
        required
      />
      <button type="submit" className="w-full py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700">
        {type === 'login' ? 'ورود به حساب' : 'ایجاد حساب'}
      </button>
    </form>
  );
}