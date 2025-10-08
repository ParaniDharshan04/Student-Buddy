import { useState } from 'react'
import { useAskQuestion } from '../hooks/useQuestions'

interface QuestionFormProps {
  onAnswer: (answer: any) => void
  studentId?: number
}

const QuestionForm = ({ onAnswer, studentId }: QuestionFormProps) => {
  const [question, setQuestion] = useState('')
  const [style, setStyle] = useState<'simple' | 'exam-style' | 'real-world'>('simple')
  
  const askQuestionMutation = useAskQuestion()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!question.trim()) return

    try {
      const result = await askQuestionMutation.mutateAsync({
        question: question.trim(),
        explanation_style: style,
        student_id: studentId,
      })
      onAnswer(result)
    } catch (error) {
      console.error('Error asking question:', error)
    }
  }

  return (
    <div className="bg-gray-900 p-6 rounded-lg shadow-xl border-2 border-yellow-500">
      <h2 className="text-xl font-semibold text-yellow-500 mb-4">Ask a Question</h2>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="question" className="block text-sm font-medium text-yellow-400 mb-2">
            Your Question
          </label>
          <textarea
            id="question"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Enter your question here..."
            className="w-full px-3 py-2 bg-gray-800 border-2 border-yellow-500 text-yellow-100 rounded-md focus:outline-none focus:ring-2 focus:ring-yellow-400 placeholder-gray-500"
            rows={4}
            required
          />
        </div>

        <div>
          <label htmlFor="style" className="block text-sm font-medium text-yellow-400 mb-2">
            Explanation Style
          </label>
          <select
            id="style"
            value={style}
            onChange={(e) => setStyle(e.target.value as 'simple' | 'exam-style' | 'real-world')}
            className="w-full px-3 py-2 bg-gray-800 border-2 border-yellow-500 text-yellow-100 rounded-md focus:outline-none focus:ring-2 focus:ring-yellow-400"
          >
            <option value="simple">Simple - Easy to understand explanations</option>
            <option value="exam-style">Exam Style - Detailed for test preparation</option>
            <option value="real-world">Real World - Practical applications</option>
          </select>
        </div>

        <button
          type="submit"
          disabled={askQuestionMutation.isPending || !question.trim()}
          className="w-full bg-yellow-500 text-black font-bold py-2 px-4 rounded-md hover:bg-yellow-400 focus:outline-none focus:ring-2 focus:ring-yellow-500 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {askQuestionMutation.isPending ? 'Getting Answer...' : 'Ask Question'}
        </button>
      </form>

      {askQuestionMutation.error && (
        <div className="mt-4 p-3 bg-red-900 border-2 border-red-500 rounded-md">
          <p className="text-red-200 text-sm">
            Error: {askQuestionMutation.error.message}
          </p>
        </div>
      )}
    </div>
  )
}

export default QuestionForm