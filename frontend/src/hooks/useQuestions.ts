import { useMutation } from '@tanstack/react-query'
import api from '../lib/api'
import { QuestionRequest, QuestionResponse } from '../types'

export const useAskQuestion = () => {
  return useMutation<QuestionResponse, Error, QuestionRequest>({
    mutationFn: async (questionData: QuestionRequest) => {
      const response = await api.post('/ask', questionData)
      return response.data
    },
  })
}