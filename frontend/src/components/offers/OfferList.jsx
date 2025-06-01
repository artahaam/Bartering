// src/components/offers/OfferList.jsx
import { useOffers } from '../../api/hooks';
import OfferCard from './OfferCard'; // Add this import

export default function OfferList() { // Add 'export default'
  const { data: offers } = useOffers();

  return (
    <div>
      {offers?.map((offer) => (
        <OfferCard key={offer.id} offer={offer} /> // Fix undefined OfferCard
      ))}
    </div>
  );
}