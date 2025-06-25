import { useState, useEffect } from 'react';
import Navbar from '../components/Navbar';
import OfferCard from '../components/OfferCard';
import api from '../utils/api';

export default function MyOffersPage() {
  const [offers, setOffers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        // 🔐 Get current user
        const me = await api.get('/accounts/me/');

        // ✅ Use URL to their offers (e.g. '/api/accounts/users/11/offers/')
        const offersUrl = me.data.offers;

        const offerRes = await api.get(offersUrl);
        setOffers(Array.isArray(offerRes.data) ? offerRes.data : offerRes.data.results || []);
      } catch (err) {
        console.warn(err);
        alert('خطا در دریافت آگهی‌های شما ❌');
      } finally {
        setLoading(false);
      }
    }

    load();
  }, []);

  if (loading) return <p className="p-10 font-sahel">در حال بارگذاری...</p>;

  return (
    <>
      <Navbar />
      <div className="max-w-4xl mx-auto p-6 font-sahel">
        <h2 className="text-2xl font-bold mb-4 text-right">آگهی‌های من 📦</h2>
        {offers.length === 0 ? (
          <p className="text-right text-gray-600">🎯 هنوز آگهی‌ای ثبت نکرده‌اید.</p>
        ) : (
          <div className="space-y-4">
            {offers.map((offer) => (
              <OfferCard key={offer.id} offer={offer} isOwner={true} />
            ))}
          </div>
        )}
      </div>
    </>
  );
}