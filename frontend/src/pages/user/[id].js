import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import api from '../../utils/api';
import Navbar from '../../components/Navbar';
import OfferCard from '../../components/OfferCard';

const RatingStars = ({ rating }) => {
  const stars = Math.round(parseFloat(rating || 0));
  return (
    <div className="flex rtl:justify-end text-yellow-500 text-xl">
      {'★'.repeat(stars || 0)}{'☆'.repeat(5 - stars)}
    </div>
  );
};

export default function PublicProfilePage() {
  const router = useRouter();
  const { id } = router.query;

  const [user, setUser] = useState(null);
  const [offers, setOffers] = useState([]);

  useEffect(() => {
    if (!id) return;

    const checkOwnerAndFetchData = async () => {
      // --- NEW LOGIC: Check if the viewer is the owner ---
      try {
        const meRes = await api.get('/accounts/me/');
        // Compare the logged-in user's ID with the ID from the URL
        if (meRes.data.id.toString() === id) {
          // If they match, redirect to the private profile and stop.
          router.push('/profile');
          return; 
        }
      } catch (error) {
        // This error is expected if the user is not logged in.
        // We can ignore it and proceed to show the public profile.
        console.log("Visitor is not logged in, showing public profile.");
      }
      // --- END OF NEW LOGIC ---


      // --- Existing Logic: Fetch the public profile data ---
      // This part only runs if the user was not redirected.
      try {
        const userRes = await api.get(`accounts/users/${id}/`);
        const userData = userRes.data;

        setUser(userData);

        if (userData.offers) {
          const offersPath = new URL(userData.offers).pathname.replace('/api', '');
          const offerRes = await api.get(offersPath);
          setOffers(offerRes.data || []); 
        }
      } catch (err) {
        alert('⚠️ خطا در دریافت اطلاعات کاربر');
        console.error(err);
      }
    };

    checkOwnerAndFetchData();
  }, [id, router]); // <-- Add 'router' to the dependency array

  if (!user) return <p className="p-10 font-sahel">در حال بارگیری...</p>;

  return (
    <>
      <Navbar />
      <div className="max-w-4xl mx-auto p-6 font-sahel">
        <h2 className="text-right text-2xl font-bold text-indigo-700 mb-4">
          {user.first_name || ''} {user.last_name || ''}
        </h2>
        <p className="text-sm text-right text-gray-600">
          شماره تماس: {user.phone_number}
        </p>
        <RatingStars rating={user.average_rating} />
      </div>

      <div className="max-w-4xl mx-auto mt-6 p-6 bg-white dark:bg-gray-800 rounded">
        <h3 className="text-right text-xl font-bold mb-4">آگهی‌های این کاربر</h3>
        {offers.length === 0 ? <p>در حال حاظر این کاربر آگهی فعالی ندارد</p> : (
          <div className="space-y-4">
            {offers.map((offer) => (
              <OfferCard key={offer.id} offer={offer} isOwner={false} />
            ))}
          </div>
        )}
      </div>
    </>
  );
}