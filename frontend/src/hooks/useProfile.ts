import { useMutation, useQuery } from '@tanstack/react-query'
import api from '../lib/api'
import { ProfileRequest, ProfileResponse, ProfileWithStats } from '../types'

export const useCreateProfile = () => {
  return useMutation<ProfileResponse, Error, ProfileRequest>({
    mutationFn: async (profileData: ProfileRequest) => {
      const response = await api.post('/profile', profileData)
      return response.data
    },
  })
}

export const useGetProfile = () => {
  return useQuery<ProfileResponse, Error>({
    queryKey: ['profile'],
    queryFn: async () => {
      const response = await api.get('/profile')
      return response.data
    },
  })
}

export const useGetProfileWithStats = () => {
  return useQuery<ProfileWithStats, Error>({
    queryKey: ['profile-stats'],
    queryFn: async () => {
      const response = await api.get('/profile/stats')
      return response.data
    },
  })
}

export const useUpdateProfile = () => {
  return useMutation<ProfileResponse, Error, Partial<ProfileRequest>>({
    mutationFn: async (data) => {
      const response = await api.put('/profile', data)
      return response.data
    },
  })
}
