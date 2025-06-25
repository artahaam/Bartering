import { useState } from 'react';
import { useRouter } from 'next/router';
import Navbar from '../components/Navbar';
import api from '../utils/api';
import { saveToken } from '../utils/auth';

export default function RegisterPage() {
  const router = useRouter();
  const [form, setForm] = useState({
    username: '', password: '', email: '', first_name: '', last_name: '', phone_number: '', student_id: ''
  });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await api.post('/accounts/register/', form);
      if (res.data.token) {
        saveToken(res.data.token);
        router.push('/');
      } else {
        router.push('/login');
      }
    } catch (err) {
      alert('خطا در ثبت‌نام. لطفاً اطلاعات را بررسی کنید.');
    }
  };

  return (
    <>
      <Navbar />
      <form onSubmit={handleSubmit} className="bg-white dark:bg-gray-800 shadow-md rounded p-6 w-full max-w-md mx-auto mt-12 space-y-4 font-sahel">
        <h2 className="text-center text-xl text-indigo-600 font-bold">ثبت‌نام</h2>
        
        <input name="username" onChange={handleChange} value={form.username} placeholder="نام کاربری" required className="w-full p-2 border rounded" />
        <input type="password" name="password" onChange={handleChange} value={form.password} placeholder="رمز عبور" required className="w-full p-2 border rounded" />
        <input type="email" name="email" onChange={handleChange} value={form.email} placeholder="ایمیل" className="w-full p-2 border rounded" />
        <input name="first_name" onChange={handleChange} value={form.first_name} placeholder="نام" className="w-full p-2 border rounded" />
        <input name="last_name" onChange={handleChange} value={form.last_name} placeholder="نام خانوادگی" className="w-full p-2 border rounded" />
        <input name="phone_number" onChange={handleChange} value={form.phone_number} placeholder="شماره تماس (09...)" className="w-full p-2 border rounded" />
        <input name="student_id" onChange={handleChange} value={form.student_id} placeholder="شماره دانشجویی (40...)" className="w-full p-2 border rounded" />
        
        <button type="submit" className="w-full py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700">
          ایجاد حساب
        </button>
      </form>
    </>
  );
}