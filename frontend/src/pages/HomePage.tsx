import { Link } from 'react-router-dom'

const HomePage = () => {
  return (
    <div className="max-w-4xl mx-auto">
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold text-yellow-500 mb-4">
          Welcome to Student Learning Buddy
        </h1>
        <p className="text-xl text-yellow-100 mb-8">
          Your AI-powered personal tutor for enhanced learning
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Link
          to="/question"
          className="bg-gray-900 p-6 rounded-lg shadow-xl hover:shadow-2xl transition-all border-2 border-yellow-500 hover:border-yellow-400 hover:scale-105"
        >
          <div className="text-4xl mb-4">❓</div>
          <h3 className="text-lg font-semibold text-yellow-500 mb-2">
            Ask Questions
          </h3>
          <p className="text-yellow-100 text-sm">
            Get detailed explanations for any topic with multiple explanation styles
          </p>
        </Link>

        <Link
          to="/quiz"
          className="bg-gray-900 p-6 rounded-lg shadow-xl hover:shadow-2xl transition-all border-2 border-yellow-500 hover:border-yellow-400 hover:scale-105"
        >
          <div className="text-4xl mb-4">📝</div>
          <h3 className="text-lg font-semibold text-yellow-500 mb-2">
            Take Quizzes
          </h3>
          <p className="text-yellow-100 text-sm">
            Test your knowledge with AI-generated quizzes on any subject
          </p>
        </Link>

        <Link
          to="/notes"
          className="bg-gray-900 p-6 rounded-lg shadow-xl hover:shadow-2xl transition-all border-2 border-yellow-500 hover:border-yellow-400 hover:scale-105"
        >
          <div className="text-4xl mb-4">📄</div>
          <h3 className="text-lg font-semibold text-yellow-500 mb-2">
            Summarize Notes
          </h3>
          <p className="text-yellow-100 text-sm">
            Transform your study materials into concise, structured summaries
          </p>
        </Link>

        <Link
          to="/profile"
          className="bg-gray-900 p-6 rounded-lg shadow-xl hover:shadow-2xl transition-all border-2 border-yellow-500 hover:border-yellow-400 hover:scale-105"
        >
          <div className="text-4xl mb-4">👤</div>
          <h3 className="text-lg font-semibold text-yellow-500 mb-2">
            Profile
          </h3>
          <p className="text-yellow-100 text-sm">
            Manage your learning preferences and track your progress
          </p>
        </Link>
      </div>

      <div className="mt-12 bg-gray-900 p-8 rounded-lg shadow-xl border-2 border-yellow-500">
        <h2 className="text-2xl font-semibold text-yellow-500 mb-4">
          How it works
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="text-center">
            <div className="text-3xl mb-3">🤖</div>
            <h3 className="font-semibold text-yellow-400 mb-2">AI-Powered</h3>
            <p className="text-yellow-100 text-sm">
              Leverages advanced AI to provide personalized learning experiences
            </p>
          </div>
          <div className="text-center">
            <div className="text-3xl mb-3">📚</div>
            <h3 className="font-semibold text-yellow-400 mb-2">Adaptive Learning</h3>
            <p className="text-yellow-100 text-sm">
              Adjusts to your learning style and tracks your progress over time
            </p>
          </div>
          <div className="text-center">
            <div className="text-3xl mb-3">⚡</div>
            <h3 className="font-semibold text-yellow-400 mb-2">Instant Feedback</h3>
            <p className="text-yellow-100 text-sm">
              Get immediate responses and explanations to enhance understanding
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default HomePage