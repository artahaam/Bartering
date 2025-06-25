// src/pages/login.js

import { useRouter } from 'next/router';
import AuthForm from '../components/AuthForm';
import api from '../utils/api'; // Import the new default export
import { saveToken } from '../utils/auth';
import Navbar from '../components/Navbar';

export default function LoginPage() {
  const router = useRouter();

  const handleLogin = async (data) => {
    try {
      // Use the new api instance. Remember, for our login endpoint,
      // the backend expects the key to be 'username', not 'phone_number'.
      const loginData = {
        username: data.username,
        password: data.password,
      };
      console.log("Submitting login data:", loginData); 

      // Now this call will work correctly.
      const res = await api.post('/accounts/login/', loginData);
      
      // Save the token from the response
      saveToken(res.data.token);
      
      // Redirect to the homepage on successful login
      router.push('/'); 
    } catch (err) {
      console.error("Login failed:", err.response?.data || err.message);
      alert('ورود ناموفق بود، شماره تلفن یا گذرواژه اشتباه است.');
    }
  };

  return (
    <>
      <Navbar />
      <AuthForm onSubmit={handleLogin} type="login" />
    </>
  );
}