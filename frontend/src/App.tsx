import { Routes, Route, Navigate } from 'react-router-dom'
import Layout from './components/Layout'
import HomePage from './pages/HomePage'
import QuestionPage from './pages/QuestionPage'
import QuizPage from './pages/QuizPage'
import NotesPage from './pages/NotesPage'
import ProfilePage from './pages/ProfilePage'
import VoiceAssistantPage from './pages/VoiceAssistantPage'
import LoginPage from './pages/LoginPage'
import SignupPage from './pages/SignupPage'
import ProtectedRoute from './components/ProtectedRoute'
import { useAuth } from './contexts/AuthContext'

function App() {
  const { isAuthenticated } = useAuth()

  return (
    <Routes>
      {/* Public routes */}
      <Route path="/login" element={isAuthenticated ? <Navigate to="/" replace /> : <LoginPage />} />
      <Route path="/signup" element={isAuthenticated ? <Navigate to="/" replace /> : <SignupPage />} />
      
      {/* Protected routes */}
      <Route path="/" element={
        <ProtectedRoute>
          <Layout>
            <HomePage />
          </Layout>
        </ProtectedRoute>
      } />
      <Route path="/question" element={
        <ProtectedRoute>
          <Layout>
            <QuestionPage />
          </Layout>
        </ProtectedRoute>
      } />
      <Route path="/quiz" element={
        <ProtectedRoute>
          <Layout>
            <QuizPage />
          </Layout>
        </ProtectedRoute>
      } />
      <Route path="/notes" element={
        <ProtectedRoute>
          <Layout>
            <NotesPage />
          </Layout>
        </ProtectedRoute>
      } />
      <Route path="/profile" element={
        <ProtectedRoute>
          <Layout>
            <ProfilePage />
          </Layout>
        </ProtectedRoute>
      } />
      <Route path="/voice-assistant" element={
        <ProtectedRoute>
          <Layout>
            <VoiceAssistantPage />
          </Layout>
        </ProtectedRoute>
      } />
    </Routes>
  )
}

export default App