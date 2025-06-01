// src/api/hooks.js
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiService } from './api';

export const useOffers = () => {
  return useQuery({
    queryKey: ['offers'],
    queryFn: apiService.getOffers,
  });
};

export function useCreateOffer() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (offerData) => apiService.createOffer(offerData),
    onSuccess: () => {
      queryClient.invalidateQueries(['offers']);
    }
  });
}

export const useProposeBarter = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ offerId, proposalData }) => 
      apiService.proposeBarter(offerId, proposalData),
    onSuccess: () => {
      queryClient.invalidateQueries(['offers']);
      queryClient.invalidateQueries(['barters']);
    },
  });
};

