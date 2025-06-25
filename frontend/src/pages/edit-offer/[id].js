import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import Navbar from '../../components/Navbar';
import api from '../../utils/api';

export default function EditOfferPage() {
  const router = useRouter();
  const { id } = router.query;

  const [form, setForm] = useState(null);
  const [me, setMe] = useState(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    if (!id) return;

    (async () => {
      try {
        const offerRes = await api.get(`/barter/offers/${id}/`);
        const meRes = await api.get(`/accounts/me/`);
        const ownerUrl = offerRes.data.owner;
        const ownerId = parseInt(ownerUrl.split('/').filter(Boolean).pop())

        if (ownerId !== meRes.data.id) {
          alert('❌ شما اجازه ویرایش این آگهی را ندارید');
          router.push('/');
          return;
        }

        setMe(meRes.data);
        setForm({
          title: offerRes.data.title,
          description: offerRes.data.description,
          to_give: offerRes.data.to_give,
          to_get: offerRes.data.to_get,
        });
      } catch (err) {
        console.error(err);
        alert('خطا در بارگیری آگهی');
      } finally {
        setLoading(false);
      }
    })();
  }, [id]);

  const handleChange = (e) => {
    const { name, value } = e.target;

    if (name.startsWith('to_give.') || name.startsWith('to_get.')) {
      const [group, field] = name.split('.');
      setForm((prev) => ({
        ...prev,
        [group]: {
          ...prev[group],
          [field]: value,
        },
      }));
    } else {
      setForm((prev) => ({
        ...prev,
        [name]: value,
      }));
    }
  };

  // FIXED: Changed from creating a new offer to updating the existing one.
  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      // Use PATCH to update the offer with the specific ID
      await api.patch(`/barter/offers/${id}/`, form);
      alert('✅ تغییرات با موفقیت ذخیره شد');
      router.push(`/offers/${id}`); // Redirect to the offer page after editing
    } catch (err) {
      console.error(err);
      alert('❌ خطا در ذخیره تغییرات:\n' + JSON.stringify(err.response?.data || err.message));
    } finally {
      setSubmitting(false);
    }
  };

  // NEW: Function to handle deleting the offer.
  const handleDelete = async () => {
    // Confirm before deleting
    if (!window.confirm('آیا از حذف این آگهی مطمئن هستید؟ این عمل غیرقابل بازگشت است.')) {
      return;
    }

    setSubmitting(true);
    try {
      await api.delete(`/barter/offers/${id}/`);
      alert('✅ آگهی با موفقیت حذف شد');
      router.push('/'); // Redirect to home page after deletion
    } catch (err) {
      console.error(err);
      alert('❌ خطا در حذف آگهی:\n' + JSON.stringify(err.response?.data || err.message));
    } finally {
      setSubmitting(false);
    }
  };


  if (loading || !form) return <p className="p-10 font-sahel">در حال بارگذاری...</p>;

  return (
    <>
      <Navbar />
      <main className="max-w-3xl mx-auto mt-8 bg-white dark:bg-gray-900 p-6 rounded shadow font-sahel">
        <h2 className="text-2xl font-bold text-indigo-700 mb-6 text-right">ویرایش آگهی</h2>

        <form onSubmit={handleSubmit} className="grid gap-4">
          <input
            name="title"
            value={form.title}
            onChange={handleChange}
            placeholder="عنوان آگهی"
            required
            className="p-2 border rounded"
          />
          <textarea
            name="description"
            value={form.description}
            onChange={handleChange}
            placeholder="توضیحات"
            required
            className="p-2 border rounded"
          />

          <h3 className="font-bold mt-4">آنچه می‌دهید (to_give)</h3>
          <input
            name="to_give.name"
            value={form.to_give.name}
            onChange={handleChange}
            placeholder="نام"
            className="p-2 border rounded"
          />
          <select
            name="to_give.type"
            value={form.to_give.type}
            onChange={handleChange}
            className="p-2 border rounded"
          >
            <option value="item">کالا</option>
            <option value="service">خدمت</option>
          </select>
          <input
            name="to_give.description"
            value={form.to_give.description}
            onChange={handleChange}
            placeholder="توضیحات"
            className="p-2 border rounded"
          />

          <h3 className="font-bold mt-4">آنچه می‌خواهید (to_get)</h3>
          <input
            name="to_get.name"
            value={form.to_get.name}
            onChange={handleChange}
            placeholder="نام"
            className="p-2 border rounded"
          />
          <select
            name="to_get.type"
            value={form.to_get.type}
            onChange={handleChange}
            className="p-2 border rounded"
          >
            <option value="item">کالا</option>
            <option value="service">خدمت</option>
          </select>
          <input
            name="to_get.description"
            value={form.to_get.description}
            onChange={handleChange}
            placeholder="توضیحات"
            className="p-2 border rounded"
          />

          {/* --- NEW: Button container for Edit and Delete --- */}
          <div className="flex items-center gap-4 mt-4">
            <button
              type="submit"
              disabled={submitting}
              className="flex-1 bg-indigo-600 text-white py-2 rounded hover:bg-indigo-700 disabled:bg-indigo-400"
            >
              {submitting ? 'در حال ذخیره...' : 'ذخیره تغییرات'}
            </button>
            <button
              type="button" // Important: type="button" to prevent form submission
              onClick={handleDelete}
              disabled={submitting}
              className="flex-1 bg-red-600 text-white py-2 rounded hover:bg-red-700 disabled:bg-red-400"
            >
              {submitting ? '...' : 'حذف آگهی'}
            </button>
          </div>
        </form>
      </main>
    </>
  );
}