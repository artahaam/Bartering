import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import Navbar from '../../components/Navbar';
import api from '../../utils/api';

export default function OfferDetailPage() {
  const router = useRouter();
  const { id } = router.query;

  const [offer, setOffer] = useState(null);
  const [isOwner, setIsOwner] = useState(false);
  const [proposing, setProposing] = useState(false);
  const [proposal, setProposal] = useState({
    proposed_tradeable: {
      name: '',
      description: '',
      type: 'item',
    },
  });

  useEffect(() => {
    if (!id) return;
    (async () => {
      try {
        const offerRes = await api.get(`/barter/offers/${id}/`);
        const userRes = await api.get(`/accounts/me/`);
        const ownerUrl = offerRes.data.owner;
        const ownerId = parseInt(ownerUrl.split('/').filter(Boolean).pop());

        setOffer(offerRes.data);
        if (ownerId === userRes.data.id) setIsOwner(true);
      } catch (err) {
        alert('❌ خطا در دریافت آگهی');
        console.error(err);
      }
    })();
  }, [id]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setProposal((prev) => ({
      proposed_tradeable: {
        ...prev.proposed_tradeable,
        [name]: value,
      },
    }));
  };

  const handlePropose = async (e) => {
    e.preventDefault();
    setProposing(true);

    try {
      const payload = {
        proposed_tradeable: {
          ...proposal.proposed_tradeable,
        },
      };

      await api.post(`/barter/offers/${id}/propose/`, payload);

      alert('✅ پیشنهاد شما ثبت شد');
      router.push('/profile'); // future route
    } catch (err) {
      console.error('❌ Proposal failed:', err.response?.data || err.message);
      alert('❌ ارسال پیشنهاد با شکست مواجه شد:\n' + JSON.stringify(err.response?.data || '', null, 2));
    } finally {
      setProposing(false);
    }
  };

  if (!offer) return <p className="p-10 font-sahel">در حال بارگذاری...</p>;

  return (
    <>
      <Navbar />
      <div className="max-w-3xl mx-auto mt-8 p-6 font-sahel bg-white dark:bg-gray-900 shadow rounded">

        <h1 className="text-2xl font-bold text-indigo-700 mb-4">{offer.title}</h1>
        <p className="mb-4">{offer.description}</p>

        <div className="grid md:grid-cols-2 gap-6 mb-6">
          <div>
            <h3 className="font-bold mb-2">آنچه ارائه می‌دهد</h3>
            <p>📦 {offer.to_give.name}</p>
            <p>📝 {offer.to_give.description}</p>
            <p>🧾 {offer.to_give.type === 'item' ? 'کالا' : 'خدمت'}</p>
          </div>
          <div>
            <h3 className="font-bold mb-2">آنچه می‌خواهد</h3>
            <p>📦 {offer.to_get.name}</p>
            <p>📝 {offer.to_get.description}</p>
            <p>🧾 {offer.to_get.type === 'item' ? 'کالا' : 'خدمت'}</p>
          </div>
        </div>
        
        {!isOwner && (
          <form onSubmit={handlePropose} className="border-t pt-6 mt-6">
            <h3 className="text-lg font-bold mb-4">🧾 ارسال پیشنهاد</h3>

            <input
              name="name"
              placeholder="نام پیشنهادی"
              value={proposal.proposed_tradeable.name}
              onChange={handleChange}
              required
              className="w-full border rounded p-2 mb-3"
            />
            <textarea
              name="description"
              placeholder="توضیحات"
              value={proposal.proposed_tradeable.description}
              onChange={handleChange}
              required
              className="w-full border rounded p-2 mb-3"
            />
            <select
              name="type"
              value={proposal.proposed_tradeable.type}
              onChange={handleChange}
              className="w-full border rounded p-2 mb-4"
            >
              <option value="item">کالا</option>
              <option value="service">خدمت</option>
            </select>
            <button
              type="submit"
              className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700"
              disabled={proposing}
            >
              {proposing ? 'در حال ارسال...' : 'ارسال پیشنهاد'}
            </button>
          </form>
        )}

        {/* --- NEW: Added button to edit the offer for the owner --- */}
        {isOwner && (
          <div className="border-t pt-6 mt-6 text-right">
            <p className="text-sm text-gray-500 dark:text-gray-400 mb-4">این آگهی متعلق به شما است.</p>
            <button
              onClick={() => router.push(`/edit-offer/${id}/`)}
              className="bg-indigo-600 text-white px-6 py-2 rounded hover:bg-indigo-700"
            >
              ویرایش آگهی
            </button>
          </div>
        )}
      </div>
    </>
  );
}