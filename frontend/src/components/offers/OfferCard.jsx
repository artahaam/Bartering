// src/components/CreateOfferForm.jsx
import { useForm } from 'react-hook-form';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { apiService } from '../api/api';

export default function CreateOfferForm() {
  const { register, handleSubmit, reset } = useForm();
  const queryClient = useQueryClient();

  // Create the mutation hook directly if not using a central hooks file
  const { mutate: createOffer, isLoading } = useMutation({
    mutationFn: (offerData) => apiService.createOffer(offerData),
    onSuccess: () => {
      queryClient.invalidateQueries(['offers']); // Refresh offers list
      reset(); // Reset form
    }
  });

  const onSubmit = (data) => {
    createOffer(data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div>
        <label>What you're offering</label>
        <input
          {...register('offering', { required: true })}
          className="w-full p-2 border rounded"
        />
      </div>
      
      <div>
        <label>What you want in return</label>
        <input
          {...register('requesting', { required: true })}
          className="w-full p-2 border rounded"
        />
      </div>
      
      <div>
        <label>Description</label>
        <textarea
          {...register('description')}
          className="w-full p-2 border rounded"
        />
      </div>
      
      <button
        type="submit"
        disabled={isLoading}
        className="bg-blue-500 text-white p-2 rounded hover:bg-blue-600"
      >
        {isLoading ? 'Creating...' : 'Create Offer'}
      </button>
    </form>
  );
}