export const translations = {
  fa: {
    login: 'ورود',
    register: 'ثبت‌نام',
    logout: 'خروج',
    createOffer: 'ایجاد آگهی',
    myOffers: 'آگهی‌های من',
    profile: 'پروفایل',
    home: 'خانه',
  },
  en: {
    login: 'Login',
    register: 'Register',
    logout: 'Logout',
    createOffer: 'Create Offer',
    myOffers: 'My Offers',
    profile: 'Profile',
    home: 'Home',
  },
};

export function getLocale() {
  if (typeof window === 'undefined') return 'fa'; // for SSR fallback
  return localStorage.getItem('locale') || 'fa';
}

export function setLocale(lang) {
  if (typeof window !== 'undefined') {
    localStorage.setItem('locale', lang);
  }
}

export function t(key) {
  const lang = getLocale();
  return translations[lang]?.[key] || key;
}