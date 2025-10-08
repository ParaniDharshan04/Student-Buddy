import { useState, useEffect } from 'react'
import { QuizResponse, QuizQuestion } from '../types'
import { useSubmitQuiz } from '../hooks/useQuiz'
import { cleanMarkdown } from '../utils/formatText'

interface QuizDisplayProps {
  quiz: QuizResponse
  onNewQuiz: () => void
}

const QuizDisplay = ({ quiz, onNewQuiz }: QuizDisplayProps) => {
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0)
  const [answers, setAnswers] = useState<Record<string, string>>({})
  const [showResults, setShowResults] = useState(false)
  const [startTime] = useState(Date.now())
  const [submitted, setSubmitted] = useState(false)
  
  const submitQuizMutation = useSubmitQuiz()
  const studentId = localStorage.getItem('studentId') ? parseInt(localStorage.getItem('studentId')!) : undefined

  const currentQuestion = quiz.questions[currentQuestionIndex]
  const isLastQuestion = currentQuestionIndex === quiz.questions.length - 1

  const handleAnswer = (answer: string) => {
    setAnswers({ ...answers, [currentQuestion.id]: answer })
  }

  const handleNext = async () => {
    if (isLastQuestion) {
      setShowResults(true)
      
      // Submit quiz to backend if student is logged in
      if (studentId && !submitted) {
        const timeTaken = Math.floor((Date.now() - startTime) / 1000) // seconds
        try {
          await submitQuizMutation.mutateAsync({
            quiz_id: quiz.quiz_id,
            student_id: studentId,
            answers: answers,
            time_taken: timeTaken
          })
          setSubmitted(true)
        } catch (error) {
          console.error('Error submitting quiz:', error)
        }
      }
    } else {
      setCurrentQuestionIndex(currentQuestionIndex + 1)
    }
  }

  const handlePrevious = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(currentQuestionIndex - 1)
    }
  }

  const calculateScore = () => {
    let correct = 0
    quiz.questions.forEach((q) => {
      const userAnswer = (answers[q.id] || '').toUpperCase().trim()
      const correctAnswer = cleanMarkdown(q.correct_answer).toUpperCase().trim()
      
      if (userAnswer === correctAnswer) {
        correct++
      }
    })
    return {
      correct,
      total: quiz.questions.length,
      percentage: Math.round((correct / quiz.questions.length) * 100)
    }
  }

  if (showResults) {
    const score = calculateScore()
    return (
      <div className="max-w-4xl mx-auto">
        <div className="bg-gray-900 p-6 rounded-lg shadow-xl border-2 border-yellow-500">
          <h2 className="text-2xl font-bold text-yellow-500 mb-4">Quiz Results</h2>
          
          <div className="bg-black p-6 rounded-lg mb-6 border-2 border-yellow-500">
            <div className="text-center">
              <p className="text-5xl font-bold text-yellow-500 mb-2">{score.percentage}%</p>
              <p className="text-lg text-yellow-100">
                {score.correct} out of {score.total} correct
              </p>
            </div>
          </div>

          <div className="space-y-4">
            {quiz.questions.map((question, index) => {
              const userAnswerLetter = answers[question.id]
              const correctAnswerLetter = cleanMarkdown(question.correct_answer).toUpperCase().trim()
              const isCorrect = userAnswerLetter === correctAnswerLetter
              
              // Get the full text for the answers
              const getUserAnswerText = () => {
                if (!userAnswerLetter) return 'Not answered'
                if (question.options && question.type === 'multiple_choice') {
                  const optionIndex = userAnswerLetter.charCodeAt(0) - 65 // A=0, B=1, etc.
                  return question.options[optionIndex] ? `${userAnswerLetter}. ${cleanMarkdown(question.options[optionIndex])}` : userAnswerLetter
                }
                return userAnswerLetter
              }
              
              const getCorrectAnswerText = () => {
                if (question.options && question.type === 'multiple_choice') {
                  const optionIndex = correctAnswerLetter.charCodeAt(0) - 65
                  return question.options[optionIndex] ? `${correctAnswerLetter}. ${cleanMarkdown(question.options[optionIndex])}` : correctAnswerLetter
                }
                return correctAnswerLetter
              }
              
              return (
                <div key={question.id} className={`p-4 rounded-lg border-2 ${isCorrect ? 'border-green-500 bg-gray-800' : 'border-red-500 bg-gray-800'}`}>
                  <div className="flex items-start justify-between mb-2">
                    <h3 className="font-semibold text-yellow-400">Question {index + 1}</h3>
                    <span className={`px-2 py-1 rounded text-sm font-medium ${isCorrect ? 'bg-green-500 text-black' : 'bg-red-500 text-white'}`}>
                      {isCorrect ? '✓ Correct' : '✗ Incorrect'}
                    </span>
                  </div>
                  <p className="text-yellow-100 mb-2">{cleanMarkdown(question.question)}</p>
                  <div className="text-sm space-y-1 text-yellow-100">
                    <p><span className="font-medium text-yellow-400">Your answer:</span> {getUserAnswerText()}</p>
                    <p><span className="font-medium text-yellow-400">Correct answer:</span> {getCorrectAnswerText()}</p>
                    <p className="text-gray-300 mt-2"><span className="font-medium text-yellow-400">Explanation:</span> {cleanMarkdown(question.explanation)}</p>
                  </div>
                </div>
              )
            })}
          </div>

          <div className="mt-6 pt-4 border-t border-yellow-600">
            <button
              onClick={onNewQuiz}
              className="bg-yellow-500 text-black font-bold py-2 px-4 rounded-md hover:bg-yellow-400 focus:outline-none focus:ring-2 focus:ring-yellow-500"
            >
              Generate New Quiz
            </button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-gray-900 p-6 rounded-lg shadow-xl border-2 border-yellow-500">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-xl font-semibold text-yellow-500">
            Question {currentQuestionIndex + 1} of {quiz.questions.length}
          </h2>
        </div>

        <div className="mb-6">
          <div className="w-full bg-gray-200 rounded-full h-2 mb-4">
            <div
              className="bg-blue-600 h-2 rounded-full transition-all"
              style={{ width: `${((currentQuestionIndex + 1) / quiz.questions.length) * 100}%` }}
            />
          </div>
        </div>

        <div className="mb-6">
          <h3 className="text-lg font-medium text-yellow-400 mb-4">{cleanMarkdown(currentQuestion.question)}</h3>

          {currentQuestion.type === 'multiple_choice' && currentQuestion.options && (
            <div className="space-y-3">
              {currentQuestion.options.map((option, index) => {
                const cleanOption = cleanMarkdown(option)
                const optionLetter = String.fromCharCode(65 + index) // A, B, C, D
                const isSelected = answers[currentQuestion.id] === optionLetter
                return (
                  <button
                    key={index}
                    type="button"
                    onClick={() => handleAnswer(optionLetter)}
                    className={`w-full text-left p-4 border-2 rounded-lg transition-all ${
                      isSelected
                        ? 'border-yellow-500 bg-gray-800 shadow-lg'
                        : 'border-gray-600 hover:border-yellow-400 hover:bg-gray-800'
                    }`}
                  >
                    <div className="flex items-center">
                      <div className={`w-5 h-5 rounded-full border-2 mr-3 flex items-center justify-center ${
                        isSelected ? 'border-yellow-500 bg-yellow-500' : 'border-gray-500'
                      }`}>
                        {isSelected && (
                          <svg className="w-3 h-3 text-black" fill="currentColor" viewBox="0 0 20 20">
                            <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                          </svg>
                        )}
                      </div>
                      <span className={`text-yellow-100 ${isSelected ? 'font-medium' : ''}`}>
                        <span className="font-bold mr-2">{optionLetter}.</span>{cleanOption}
                      </span>
                    </div>
                  </button>
                )
              })}
            </div>
          )}

          {currentQuestion.type === 'true_false' && (
            <div className="space-y-3">
              {['True', 'False'].map((option) => {
                const optionUpper = option.toUpperCase()
                const isSelected = answers[currentQuestion.id] === optionUpper
                return (
                  <button
                    key={option}
                    type="button"
                    onClick={() => handleAnswer(optionUpper)}
                    className={`w-full text-left p-4 border-2 rounded-lg transition-all ${
                      isSelected
                        ? 'border-yellow-500 bg-gray-800 shadow-lg'
                        : 'border-gray-600 hover:border-yellow-400 hover:bg-gray-800'
                    }`}
                  >
                    <div className="flex items-center">
                      <div className={`w-5 h-5 rounded-full border-2 mr-3 flex items-center justify-center ${
                        isSelected ? 'border-yellow-500 bg-yellow-500' : 'border-gray-500'
                      }`}>
                        {isSelected && (
                          <svg className="w-3 h-3 text-black" fill="currentColor" viewBox="0 0 20 20">
                            <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                          </svg>
                        )}
                      </div>
                      <span className={`text-yellow-100 ${isSelected ? 'font-medium' : ''}`}>{option}</span>
                    </div>
                  </button>
                )
              })}
            </div>
          )}

          {currentQuestion.type === 'short_answer' && (
            <input
              type="text"
              value={answers[currentQuestion.id] || ''}
              onChange={(e) => handleAnswer(e.target.value)}
              placeholder="Type your answer here..."
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          )}
        </div>

        <div className="flex justify-between pt-4 border-t border-yellow-600">
          <button
            onClick={handlePrevious}
            disabled={currentQuestionIndex === 0}
            className="px-4 py-2 text-yellow-400 bg-gray-800 border-2 border-yellow-500 rounded-md hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed font-medium"
          >
            Previous
          </button>
          <button
            onClick={handleNext}
            disabled={!answers[currentQuestion.id]}
            className="px-4 py-2 bg-yellow-500 text-black font-bold rounded-md hover:bg-yellow-400 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLastQuestion ? 'Finish Quiz' : 'Next'}
          </button>
        </div>
      </div>
    </div>
  )
}

export default QuizDisplay
