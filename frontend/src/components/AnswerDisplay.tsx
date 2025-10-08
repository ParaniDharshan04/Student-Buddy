import { QuestionResponse } from '../types'
import { cleanMarkdown } from '../utils/formatText'

interface AnswerDisplayProps {
  answer: QuestionResponse
  onNewQuestion: () => void
}

const AnswerDisplay = ({ answer, onNewQuestion }: AnswerDisplayProps) => {
  return (
    <div className="bg-gray-900 p-6 rounded-lg shadow-xl border-2 border-yellow-500">
      <div className="flex justify-between items-start mb-4">
        <h2 className="text-xl font-semibold text-yellow-500">Answer</h2>
        <div className="flex items-center space-x-2">
          <span className="text-sm text-yellow-400">Style: {answer.style}</span>
          <span className="text-sm text-yellow-400">•</span>
          <span className="text-sm text-yellow-400">
            Confidence: {Math.round(answer.confidence_score * 100)}%
          </span>
        </div>
      </div>

      <div className="prose max-w-none">
        <div className="bg-black p-4 rounded-md mb-4 border border-yellow-600">
          <h3 className="text-lg font-medium text-yellow-500 mb-3">Answer</h3>
          <div className="text-yellow-100 whitespace-pre-wrap">
            {cleanMarkdown(answer.answer)}
          </div>
        </div>

        {answer.explanation_steps && answer.explanation_steps.length > 0 && (
          <div className="bg-black p-4 rounded-md mb-4 border border-yellow-600">
            <h3 className="text-lg font-medium text-yellow-500 mb-3">Step-by-Step Explanation</h3>
            <ol className="space-y-2">
              {answer.explanation_steps.map((step, index) => (
                <li key={index} className="text-yellow-100">
                  {cleanMarkdown(step)}
                </li>
              ))}
            </ol>
          </div>
        )}

        {answer.related_topics && answer.related_topics.length > 0 && (
          <div className="mt-4">
            <h4 className="text-sm font-medium text-yellow-400 mb-2">Related Topics:</h4>
            <div className="flex flex-wrap gap-2">
              {answer.related_topics.map((topic, index) => (
                <span key={index} className="px-3 py-1 bg-yellow-500 text-black rounded-full text-sm font-medium">
                  {topic}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>

      <div className="mt-6 pt-4 border-t border-yellow-600">
        <button
          onClick={onNewQuestion}
          className="bg-yellow-500 text-black font-bold py-2 px-4 rounded-md hover:bg-yellow-400 focus:outline-none focus:ring-2 focus:ring-yellow-500"
        >
          Ask Another Question
        </button>
      </div>
    </div>
  )
}

export default AnswerDisplay