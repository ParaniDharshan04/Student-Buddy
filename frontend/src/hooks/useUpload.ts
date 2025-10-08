import { useMutation } from '@tanstack/react-query'
import axios from 'axios'

interface UploadResponse {
  filename: string
  content: string
  length: number
  word_count: number
}

export const useUploadFile = () => {
  return useMutation<UploadResponse, Error, File>({
    mutationFn: async (file: File) => {
      const formData = new FormData()
      formData.append('file', file)
      
      const response = await axios.post('/api/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
      return response.data
    },
  })
}
