import { useEffect, useState } from 'react';
import api from '../utils/api';
import OfferCard from '../components/OfferCard';
import Navbar from '../components/Navbar';

export default function HomePage() {
  const [offers, setOffers] = useState([]);
  const [userId, setUserId] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      try {
        // Get current user (optional: to hide own offers or show owned offers differently)
        const meRes = await api.get('/accounts/me/');
        setUserId(meRes.data.id);

        // Get all "open" offers
        const res = await api.get('/barter/offers/?status=open&?ordering=created_at');
        setOffers(Array.isArray(res.data) ? res.data : res.data.results || []);
      } catch (err) {
        console.error(err);
        alert('❌ خطا در بارگیری آگهی‌ها:\n' + JSON.stringify(err.response?.data || err.message));
      } finally {
        setLoading(false);
      }
    };

    load();
  }, []);

  return (
    <>
      <Navbar />
      <div className="max-w-4xl mx-auto px-4 py-6 font-sahel">
        <h1 className="text-2xl font-bold mb-6 text-right text-indigo-800">تمام آگهی‌های فعال</h1>

        {loading ? (
          <p className="text-right">در حال بارگذاری...</p>
        ) : offers.length === 0 ? (
          <p className="text-right text-gray-500">هیچ آگهی فعالی وجود ندارد.</p>
        ) : (
          <div className="space-y-4">
            {offers.map(offer => (
              <OfferCard
                key={offer.id}
                offer={offer}
                isOwner={offer.owner === userId}
              />
            ))}
          </div>
        )}
      </div>
    </>
  );
}