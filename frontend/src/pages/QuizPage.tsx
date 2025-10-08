import { useState } from 'react'
import { Link } from 'react-router-dom'
import { useGenerateQuiz } from '../hooks/useQuiz'
import { useUploadFile } from '../hooks/useUpload'
import { QuizResponse } from '../types'
import QuizDisplay from '../components/QuizDisplay'

const QuizPage = () => {
  const [topic, setTopic] = useState('')
  const [difficulty, setDifficulty] = useState<'easy' | 'medium' | 'hard'>('medium')
  const [questionCount, setQuestionCount] = useState(5)
  const [useFile, setUseFile] = useState(false)
  const [uploadedContent, setUploadedContent] = useState('')
  const [currentQuiz, setCurrentQuiz] = useState<QuizResponse | null>(null)
  const studentId = localStorage.getItem('studentId') ? parseInt(localStorage.getItem('studentId')!) : undefined

  const generateQuizMutation = useGenerateQuiz()
  const uploadFileMutation = useUploadFile()

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return

    try {
      const result = await uploadFileMutation.mutateAsync(file)
      setUploadedContent(result.content)
      // Don't show the content, just show filename
      setTopic(result.filename)
    } catch (error) {
      console.error('Error uploading file:', error)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    // Use uploaded content or manual topic
    // Limit to 4000 chars to avoid validation errors
    let quizTopic: string
    
    if (useFile && uploadedContent) {
      // Use the uploaded content, truncated to safe length
      quizTopic = uploadedContent.substring(0, 4000)
    } else {
      quizTopic = topic
    }

    if (!quizTopic.trim()) return

    try {
      const result = await generateQuizMutation.mutateAsync({
        topic: quizTopic,
        question_count: questionCount,
        difficulty,
        question_types: ['multiple_choice', 'true_false'],
        student_id: studentId
      })
      setCurrentQuiz(result)
    } catch (error) {
      console.error('Error generating quiz:', error)
    }
  }

  const handleNewQuiz = () => {
    setCurrentQuiz(null)
    setUploadedContent('')
    setTopic('')
  }

  if (currentQuiz) {
    return <QuizDisplay quiz={currentQuiz} onNewQuiz={handleNewQuiz} />
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-yellow-500">Generate Quiz</h1>
        {!studentId && (
          <Link
            to="/profile"
            className="text-sm px-4 py-2 bg-yellow-500 text-black rounded-md hover:bg-yellow-400 font-bold"
          >
            Create Profile to Track Progress
          </Link>
        )}
      </div>
      
      <div className="bg-gray-900 p-6 rounded-lg shadow-xl border-2 border-yellow-500">
        <div className="mb-4">
          <label className="flex items-center space-x-2 cursor-pointer">
            <input
              type="checkbox"
              checked={useFile}
              onChange={(e) => setUseFile(e.target.checked)}
              className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
            />
            <span className="text-sm font-medium text-gray-700">
              Upload study material (PDF, TXT, DOCX)
            </span>
          </label>
        </div>

        {useFile && (
          <div className="mb-4 p-4 bg-blue-50 rounded-md">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Upload File
            </label>
            <input
              type="file"
              accept=".pdf,.txt,.docx,.doc"
              onChange={handleFileUpload}
              className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-blue-600 file:text-white hover:file:bg-blue-700"
            />
            {uploadFileMutation.isPending && (
              <p className="mt-2 text-sm text-blue-600">Uploading and processing file...</p>
            )}
            {uploadedContent && (
              <p className="mt-2 text-sm text-green-600">
                ✓ File processed successfully ({uploadedContent.split(' ').length} words)
              </p>
            )}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          {!useFile && (
            <div>
              <label htmlFor="topic" className="block text-sm font-medium text-gray-700 mb-2">
                Quiz Topic
              </label>
              <input
                type="text"
                id="topic"
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
                placeholder="e.g., World War II, Photosynthesis, Python Programming"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                required={!useFile}
              />
            </div>
          )}

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label htmlFor="difficulty" className="block text-sm font-medium text-gray-700 mb-2">
                Difficulty
              </label>
              <select
                id="difficulty"
                value={difficulty}
                onChange={(e) => setDifficulty(e.target.value as 'easy' | 'medium' | 'hard')}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="easy">Easy</option>
                <option value="medium">Medium</option>
                <option value="hard">Hard</option>
              </select>
            </div>

            <div>
              <label htmlFor="questionCount" className="block text-sm font-medium text-gray-700 mb-2">
                Number of Questions
              </label>
              <select
                id="questionCount"
                value={questionCount}
                onChange={(e) => setQuestionCount(Number(e.target.value))}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                {[5, 6, 7, 8, 9, 10].map(num => (
                  <option key={num} value={num}>{num}</option>
                ))}
              </select>
            </div>
          </div>

          <button
            type="submit"
            disabled={generateQuizMutation.isPending || (!topic.trim() && !uploadedContent)}
            className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {generateQuizMutation.isPending ? 'Generating Quiz...' : 'Generate Quiz'}
          </button>
        </form>

        {generateQuizMutation.error && (
          <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-md">
            <p className="text-red-700 text-sm font-semibold mb-2">
              Error: {generateQuizMutation.error.message}
            </p>
            {generateQuizMutation.error.message.includes('402') || 
             generateQuizMutation.error.message.includes('quota') ? (
              <div className="text-sm text-red-600 mt-2">
                <p className="font-medium">API Quota Limit Reached</p>
                <ul className="list-disc ml-5 mt-1 space-y-1">
                  <li>Try using a smaller document (under 5 pages)</li>
                  <li>Wait 60 seconds and try again</li>
                  <li>Or type the topic manually instead of uploading</li>
                </ul>
              </div>
            ) : null}
          </div>
        )}
      </div>
    </div>
  )
}

export default QuizPage
