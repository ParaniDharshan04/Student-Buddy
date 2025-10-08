import { useState } from 'react'
import { useGenerateQuiz } from '../hooks/useQuiz'

interface QuizGeneratorProps {
  onQuizGenerated: (quiz: any) => void
}

const QuizGenerator = ({ onQuizGenerated }: QuizGeneratorProps) => {
  const [topic, setTopic] = useState('')
  const [difficulty, setDifficulty] = useState<'easy' | 'medium' | 'hard'>('medium')
  const [numQuestions, setNumQuestions] = useState(5)
  const [questionTypes, setQuestionTypes] = useState<('multiple_choice' | 'true_false')[]>(['multiple_choice'])

  const generateQuizMutation = useGenerateQuiz()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!topic.trim()) return

    try {
      const result = await generateQuizMutation.mutateAsync({
        topic: topic.trim(),
        difficulty,
        num_questions: numQuestions,
        question_types: questionTypes,
      })
      onQuizGenerated(result)
    } catch (error) {
      console.error('Error generating quiz:', error)
    }
  }

  const handleQuestionTypeChange = (type: 'multiple_choice' | 'true_false', checked: boolean) => {
    if (checked) {
      setQuestionTypes([...questionTypes, type])
    } else {
      setQuestionTypes(questionTypes.filter(t => t !== type))
    }
  }

  return (
    <div className="bg-white p-6 rounded-lg shadow-md border border-gray-200">
      <h2 className="text-xl font-semibold text-gray-900 mb-4">Generate Quiz</h2>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="topic" className="block text-sm font-medium text-gray-700 mb-2">
            Topic
          </label>
          <input
            type="text"
            id="topic"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            placeholder="Enter the topic for your quiz..."
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            required
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label htmlFor="difficulty" className="block text-sm font-medium text-gray-700 mb-2">
              Difficulty
            </label>
            <select
              id="difficulty"
              value={difficulty}
              onChange={(e) => setDifficulty(e.target.value as 'easy' | 'medium' | 'hard')}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            >
              <option value="easy">Easy</option>
              <option value="medium">Medium</option>
              <option value="hard">Hard</option>
            </select>
          </div>

          <div>
            <label htmlFor="numQuestions" className="block text-sm font-medium text-gray-700 mb-2">
              Number of Questions
            </label>
            <select
              id="numQuestions"
              value={numQuestions}
              onChange={(e) => setNumQuestions(parseInt(e.target.value))}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            >
              <option value={3}>3 Questions</option>
              <option value={5}>5 Questions</option>
              <option value={10}>10 Questions</option>
            </select>
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Question Types
          </label>
          <div className="space-y-2">
            <label className="flex items-center">
              <input
                type="checkbox"
                checked={questionTypes.includes('multiple_choice')}
                onChange={(e) => handleQuestionTypeChange('multiple_choice', e.target.checked)}
                className="mr-2"
              />
              Multiple Choice
            </label>
            <label className="flex items-center">
              <input
                type="checkbox"
                checked={questionTypes.includes('true_false')}
                onChange={(e) => handleQuestionTypeChange('true_false', e.target.checked)}
                className="mr-2"
              />
              True/False
            </label>
          </div>
        </div>

        <button
          type="submit"
          disabled={generateQuizMutation.isPending || !topic.trim() || questionTypes.length === 0}
          className="w-full bg-primary-600 text-white py-2 px-4 rounded-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {generateQuizMutation.isPending ? 'Generating Quiz...' : 'Generate Quiz'}
        </button>
      </form>

      {generateQuizMutation.error && (
        <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-md">
          <p className="text-red-700 text-sm">
            Error: {generateQuizMutation.error.message}
          </p>
        </div>
      )}
    </div>
  )
}

export default QuizGenerator