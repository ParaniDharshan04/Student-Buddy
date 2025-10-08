import { useState } from 'react'
import { Link } from 'react-router-dom'
import QuestionForm from '../components/QuestionForm'
import AnswerDisplay from '../components/AnswerDisplay'
import { QuestionResponse } from '../types'

const QuestionPage = () => {
  const [currentAnswer, setCurrentAnswer] = useState<QuestionResponse | null>(null)
  const studentId = localStorage.getItem('studentId') ? parseInt(localStorage.getItem('studentId')!) : undefined

  const handleAnswer = (answer: QuestionResponse) => {
    setCurrentAnswer(answer)
  }

  const handleNewQuestion = () => {
    setCurrentAnswer(null)
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-yellow-500">Ask a Question</h1>
        {!studentId && (
          <Link
            to="/profile"
            className="text-sm px-4 py-2 bg-yellow-500 text-black rounded-md hover:bg-yellow-400 font-bold"
          >
            Create Profile to Track Progress
          </Link>
        )}
      </div>
      
      {!currentAnswer ? (
        <QuestionForm onAnswer={handleAnswer} studentId={studentId} />
      ) : (
        <AnswerDisplay answer={currentAnswer} onNewQuestion={handleNewQuestion} />
      )}
    </div>
  )
}

export default QuestionPage