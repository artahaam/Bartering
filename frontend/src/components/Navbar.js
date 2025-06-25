import { useEffect, useState } from 'react';
import Link from 'next/link';
import { logout, isLoggedIn } from '../utils/auth';
import { getLocale, setLocale, t } from '../utils/locale';

export default function Navbar() {
  const [lang, setLang] = useState('fa');
  const [theme, setTheme] = useState('light');
  const [mounted, setMounted] = useState(false);
  const [loggedIn, setLoggedIn] = useState(false);

  useEffect(() => {
    // Only run this on the client
    setLang(getLocale());
    setTheme(localStorage.getItem('theme') || 'light');
    setLoggedIn(isLoggedIn());
    setMounted(true);
  }, []);

  const toggleLanguage = () => {
    const newLang = lang === 'fa' ? 'en' : 'fa';
    setLocale(newLang);
    setLang(newLang);
    window.location.reload();
  };

  const toggleTheme = () => {
    const html = document.documentElement;
    const newTheme = theme === 'dark' ? 'light' : 'dark';
    html.classList.toggle('dark', newTheme === 'dark');
    setTheme(newTheme);
    localStorage.setItem('theme', newTheme);
  };

  // Prevent hydration mismatch
  if (!mounted) return null;

  return (
    <nav className="bg-white dark:bg-gray-900 shadow px-4 py-3 text-sm text-gray-800 dark:text-white font-sahel flex justify-between items-center">
      <Link href="/" className="text-xl font-bold text-indigo-600 dark:text-indigo-400">
        🌐 بارتر اسپیس
      </Link>

      <div className="flex gap-4 items-center">
        <Link href="/">{t('home')}</Link>
        <Link href="/create-offer">{t('createOffer')}</Link>
        <Link href="/my-offers">{t('myOffers')}</Link>

        {loggedIn ? (
          <>
            <Link href="/profile">{t('profile')}</Link>
            <button onClick={logout} className="text-red-500">{t('logout')}</button>
          </>
        ) : (
          <>
            <Link href="/login">{t('login')}</Link>
            <Link href="/register">{t('register')}</Link>
          </>
        )}

        <button onClick={toggleLanguage}>
          🌐 {lang === 'fa' ? 'EN' : 'FA'}
        </button>
        <button onClick={toggleTheme}>
          {theme === 'dark' ? '☀️' : '🌙'}
        </button>
      </div>
    </nav>
  );
}