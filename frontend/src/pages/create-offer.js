import { useState } from 'react';
import { useRouter } from 'next/router';
import Navbar from '../components/Navbar';
import api from '../utils/api';

export default function CreateOfferPage() {
  const router = useRouter();

  const [form, setForm] = useState({
    title: '',
    description: '',
    to_give: {
      name: '',
      description: '',
      type: 'item'
    },
    to_get: {
      name: '',
      description: '',
      type: 'item'
    }
  });

  const [submitting, setSubmitting] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    if (name.includes('to_give.') || name.includes('to_get.')) {
      const [group, field] = name.split('.');
      setForm(prev => ({
        ...prev,
        [group]: { ...prev[group], [field]: value }
      }));
    } else {
      setForm(prev => ({ ...prev, [name]: value }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log('📤 Submitting form with data:', form); // ✅ Debug
    setSubmitting(true);

    try {
      const res = await api.post('/barter/offers/', form);

      alert('✅ آگهی ثبت شد!');
      router.push('/my-offers');
    } catch (err) {
      console.error('❌ Error submitting offer:', err.response?.data || err.message);
      alert('❌ خطا در ثبت آگهی\n' + JSON.stringify(err.response?.data || err.message));
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <>
      <Navbar />
      <main className="max-w-3xl mx-auto p-6 mt-8 bg-white dark:bg-gray-900 shadow-lg rounded font-sahel">
        <h1 className="text-2xl font-bold mb-6 text-indigo-700">ایجاد آگهی جدید</h1>
        <form onSubmit={handleSubmit} className="space-y-4">
          <input
            name="title"
            value={form.title}
            onChange={handleChange}
            placeholder="عنوان آگهی"
            required
            className="w-full p-2 border rounded"
          />
          <textarea
            name="description"
            value={form.description}
            onChange={handleChange}
            placeholder="توضیحات کلی"
            required
            className="w-full p-2 border rounded"
          />

          <div>
            <h3 className="font-bold">آنچه می‌دهید (to_give):</h3>
            <input
              name="to_give.name"
              value={form.to_give.name}
              onChange={handleChange}
              placeholder="نام"
              required
              className="w-full border rounded p-2 my-1"
            />
            <select
              name="to_give.type"
              value={form.to_give.type}
              onChange={handleChange}
              className="w-full border rounded p-2 my-1"
            >
              <option value="item">کالا</option>
              <option value="service">خدمت</option>
            </select>
            <textarea
              name="to_give.description"
              value={form.to_give.description}
              onChange={handleChange}
              placeholder="توضیحات"
              required
              className="w-full border rounded p-2 my-1"
            />
          </div>

          <div>
            <h3 className="font-bold">آنچه می‌خواهید (to_get):</h3>
            <input
              name="to_get.name"
              value={form.to_get.name}
              onChange={handleChange}
              placeholder="نام"
              required
              className="w-full border rounded p-2 my-1"
            />
            <select
              name="to_get.type"
              value={form.to_get.type}
              onChange={handleChange}
              className="w-full border rounded p-2 my-1"
            >
              <option value="item">کالا</option>
              <option value="service">خدمت</option>
            </select>
            <textarea
              name="to_get.description"
              value={form.to_get.description}
              onChange={handleChange}
              placeholder="توضیحات"
              required
              className="w-full border rounded p-2 my-1"
            />
          </div>

          <button
            type="submit"
            className="w-full py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700"
            disabled={submitting}
          >
            {submitting ? 'در حال ارسال...' : 'ثبت آگهی'}
          </button>
        </form>
      </main>
    </>
  );
}