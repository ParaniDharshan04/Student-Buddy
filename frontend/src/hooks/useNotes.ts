import { useMutation } from '@tanstack/react-query'
import api from '../lib/api'
import { NotesRequest, NotesResponse } from '../types'

export const useSummarizeNotes = () => {
  return useMutation<NotesResponse, Error, NotesRequest>({
    mutationFn: async (notesData: NotesRequest) => {
      const response = await api.post('/notes', notesData)
      return response.data
    },
  })
}
