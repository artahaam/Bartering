// src/components/LoginForm.jsx
import { useForm } from 'react-hook-form';
import { useAuth } from '../../context/AuthContext';

function LoginForm() {
  const { register, handleSubmit } = useForm();
  const { login } = useAuth();

  const onSubmit = async (data) => {
    try {
      await login(data);
      // Redirect or show success message
    } catch (error) {
      console.error('Login failed', error);
      // Show error message
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register('username')} placeholder="Username" />
      <input {...register('password')} type="password" placeholder="Password" />
      <button type="submit">Login</button>
    </form>
  );
}