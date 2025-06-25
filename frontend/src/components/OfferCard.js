import Link from 'next/link';
import { useState, useEffect } from 'react'; // Import React hooks
import api from '../utils/api';

// Utility to extract user id from owner URL (This is good)
function extractUserId(ownerUrl) {
  if (!ownerUrl) return null;
  const parts = ownerUrl.split('/').filter(Boolean);
  return parts.pop(); // .pop() gets the last item
}

// Utility to format the date (This is good)
function formatDate(isoString) {
  if (!isoString) return '';
  // Use a modern Intl.DateTimeFormat for better performance and options
  return new Intl.DateTimeFormat('fa-IR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  }).format(new Date(isoString));
}

export default function OfferCard({ offer, isOwner = false, onDeleted }) {
  // --- STATE MANAGEMENT ---
  // Create state to store the owner's name after we fetch it
  const [ownerName, setOwnerName] = useState('');

  // --- DATA FETCHING ---
  // This effect runs when the component mounts or when the offer.owner URL changes
  useEffect(() => {
    // Only run if the owner URL exists
    if (offer.owner) {
      const fetchOwnerName = async () => {
        try {
          // Asynchronously fetch the user's profile from the URL
          const ownerRes = await api.get(offer.owner);
          // Set the full name in our state
          setOwnerName(ownerRes.data.full_name);
        } catch (error) {
          console.error("Failed to fetch offer owner details", error);
          // If fetching fails, we can fall back to a default name
          const ownerId = extractUserId(offer.owner);
          setOwnerName(`کاربر ${ownerId}`);
        }
      };

      fetchOwnerName();
    }
  }, [offer.owner]); // Dependency array ensures this runs only when needed

  const handleDelete = async () => {
    if (!confirm('آیا از حذف این آگهی اطمینان دارید؟')) return;

    try {
      // Corrected the api.delete call, it usually doesn't need a second argument
      await api.delete(`/barter/offers/${offer.id}/`);
      if (onDeleted) onDeleted(offer.id);
      alert('✅ آگهی حذف شد');
    } catch (err) {
      alert('❌ خطا در حذف آگهی');
      console.error(err);
    }
  };

  // Prepare variables for rendering
  const ownerId = extractUserId(offer.owner);
  const createdAtLabel = formatDate(offer.created_at);
  // Use the name from our state, with a fallback while it's loading
  const ownerDisplayName = ownerName || `کاربر ${ownerId}`;

  return (
    <div className="rounded shadow p-4 bg-white dark:bg-gray-800 font-sahel mb-6">
      <div className="flex justify-between items-center mb-2">
        {/* Owner profile link */}
        {ownerId ? (
          <Link href={`/user/${ownerId}`} className="text-blue-600 hover:underline font-bold">
            {ownerDisplayName}
          </Link>
        ) : (
          <span className="font-bold">{ownerDisplayName}</span>
        )}
        <span className="text-xs text-gray-400">{createdAtLabel}</span>
      </div>

      <h3 className="text-lg font-bold mt-1">{offer.title}</h3>
      <p className="text-sm text-gray-600 mt-2">{offer.description}</p>
      {/* <p className="text-xs text-right mt-1 text-gray-400">وضعیت: {offer.status}</p> */}

      <div className="flex justify-end gap-4 mt-4 text-sm">
        <Link href={`/edit-offer/${offer.id}`} className="text-indigo-700 hover:underline">مشاهده</Link>
        {isOwner && (
          <>
          {/* <Link href={`/offer/${offer.id}`} className="text-indigo-600 hover:underline">مشاهده</Link> */}
            {/* <button onClick={handleDelete} className="text-red-600 hover:underline">حذف</button> */}
          </>
        )}
      </div>
    </div>
  );
}