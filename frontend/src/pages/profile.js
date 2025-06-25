import { useState, useEffect } from 'react';
import api from '../utils/api';
import Navbar from '../components/Navbar';
import OfferCard from '../components/OfferCard';

const RatingStars = ({ rating }) => {
  const stars = Math.round(parseFloat(rating || 0));
  return (
    <div className="flex rtl:justify-end text-yellow-500 text-xl">
      {'★'.repeat(stars || 0)}{'☆'.repeat(5 - stars)}
    </div>
  );
};

export default function ProfilePage() {
  const [profile, setProfile] = useState(null);
  const [form, setForm] = useState({});
  const [offers, setOffers] = useState([]);

  useEffect(() => {
    async function fetchData() {
      try {
        // Step 1: Load user info
        const meRes = await api.get('/accounts/me/');
        const meData = meRes.data;

        setProfile(meData);
        setForm({
          first_name: meData.first_name,
          last_name: meData.last_name,
          email: meData.email,
        });

        // Step 2: Load user's offers
        if (meData.offers) {
          const offerRes = await api.get(meData.offers);
          setOffers(Array.isArray(offerRes.data) ? offerRes.data : offerRes.data.results || []);
        }
      } catch (err) {
        console.error(err);
        alert('❌ خطا در دریافت اطلاعات پروفایل یا آگهی‌ها');
      }
    }

    fetchData();
  }, []);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleUpdate = async (e) => {
    e.preventDefault();
    try {
      const updateRes = await fetchWithAuth('/api/accounts/me/', 'patch', form);
      setProfile(updateRes.data);
      alert('✅ اطلاعات با موفقیت ذخیره شد');
    } catch (err) {
      console.error(err);
      alert('❌ خطا:\n' + JSON.stringify(err?.response?.data || err.message, null, 2));
    }
  };

  const handleDeleteOffer = (id) => {
    setOffers((prev) => prev.filter((o) => o.id !== id));
  };

  if (!profile) return <p className="p-10 font-sahel">در حال بارگذاری...</p>;

  return (
    <>
      <Navbar />

      {/* 🧑 User Profile Section */}
      <div className="max-w-4xl mx-auto p-6 font-sahel">
        <h2 className="text-right text-2xl font-bold text-indigo-700 mb-6">پروفایل من</h2>

        <form onSubmit={handleUpdate} className="grid md:grid-cols-2 gap-4 mb-4">
          <input
            name="first_name"
            value={form.first_name}
            onChange={handleChange}
            className="border p-2 rounded"
            placeholder="نام"
            required
          />
          <input
            name="last_name"
            value={form.last_name}
            onChange={handleChange}
            className="border p-2 rounded"
            placeholder="نام خانوادگی"
            required
          />
          <input
            name="email"
            type="email"
            value={form.email}
            onChange={handleChange}
            className="border p-2 rounded"
            placeholder="ایمیل"
            required
          />
          <input
            value={profile.student_id}
            readOnly
            className="border bg-gray-100 text-gray-500 p-2 rounded"
            placeholder="شماره دانشجویی"
          />
          <input
            value={profile.phone_number}
            readOnly
            className="border bg-gray-100 text-gray-500 p-2 rounded"
            placeholder="شماره تلفن"
          />
        </form>

        <button
          type="submit"
          onClick={handleUpdate}
          className="bg-indigo-600 text-white py-2 px-4 rounded hover:bg-indigo-700"
        >
          ذخیره تغییرات
        </button>

        <div className="mt-8 text-right">
          <h3 className="font-bold text-lg mb-2">امتیاز شما:</h3>
          <RatingStars rating={profile.average_rating} />
          <p className="text-sm text-gray-500">
            {profile.average_rating || "بدون امتیاز"}
          </p>
        </div>
      </div>

      {/* 📦 User Offers Section */}
      <div className="max-w-4xl mx-auto mt-10 p-6 bg-white dark:bg-gray-800 rounded font-sahel">
        <h3 className="text-xl font-bold mb-4 text-right">آگهی‌های من</h3>
        {offers.length === 0 ? (
          <p className="text-right">🎯 هنوز آگهی‌ای ثبت نکرده‌اید.</p>
        ) : (
          <div className="space-y-4">
            {offers.map((offer) => (
              <OfferCard
                key={offer.id}
                offer={offer}
                isOwner={true}
                onDeleted={handleDeleteOffer}
              />
            ))}
          </div>
        )}
      </div>
    </>
  );
}