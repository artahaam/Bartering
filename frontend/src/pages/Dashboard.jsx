// src/pages/Dashboard.jsx
import React from 'react';
// import OfferList from '../components/OfferList';
import { OfferList, OfferCard } from '../components/offers';

export default function Dashboard() {
  return (
    <div>
      <h1>Student Bartering Dashboard</h1>
      <OfferList />
    </div>
  );
}