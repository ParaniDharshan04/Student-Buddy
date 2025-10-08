import { useMutation } from '@tanstack/react-query'
import api from '../lib/api'

interface VoiceChatRequest {
  message: string
  conversation_mode: string
  conversation_history: Array<{ role: string; content: string }>
}

interface VoiceChatResponse {
  response: string
  feedback?: {
    mode: string
    encouragement: string
    areas_to_improve: string[]
  }
  suggestions: string[]
}

export const useVoiceChat = () => {
  return useMutation<VoiceChatResponse, Error, VoiceChatRequest>({
    mutationFn: async (data: VoiceChatRequest) => {
      const response = await api.post('/voice-chat', data)
      return response.data
    },
  })
}

export const useVoiceChatHistory = () => {
  return useMutation({
    mutationFn: async () => {
      const response = await api.get('/voice-chat/history')
      return response.data
    },
  })
}
