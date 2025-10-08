import { useMutation } from '@tanstack/react-query'
import api from '../lib/api'
import { QuizRequest, QuizResponse } from '../types'

export const useGenerateQuiz = () => {
  return useMutation<QuizResponse, Error, QuizRequest>({
    mutationFn: async (quizData: QuizRequest) => {
      const response = await api.post('/quiz', quizData)
      return response.data
    },
  })
}

export const useSubmitQuiz = () => {
  return useMutation({
    mutationFn: async (submissionData: {
      quiz_id: string
      answers: Record<string, string>
      time_taken?: number
    }) => {
      const response = await api.post('/quiz/submit', submissionData)
      return response.data
    },
  })
}
