import { useState, useEffect } from 'react'
import { useCreateProfile, useGetProfileWithStats, useUpdateProfile } from '../hooks/useProfile'
import { useAuth } from '../contexts/AuthContext'
import { ProfileRequest } from '../types'

const ProfilePage = () => {
  const { user } = useAuth()
  const [showForm, setShowForm] = useState(false)
  const [isEditing, setIsEditing] = useState(false)
  const [formData, setFormData] = useState<ProfileRequest>({
    name: '',
    email: '',
    date_of_birth: '',
    phone_number: '',
    school_name: '',
    grade_level: '',
    major_field: '',
    preferred_subjects: [],
    learning_style: 'visual',
    study_goals: '',
    bio: ''
  })
  const [subjectInput, setSubjectInput] = useState('')

  const createProfileMutation = useCreateProfile()
  const updateProfileMutation = useUpdateProfile()
  const { data: profileData, isLoading, error, refetch } = useGetProfileWithStats()

  useEffect(() => {
    if (profileData && isEditing) {
      setFormData({
        name: profileData.name,
        email: profileData.email || '',
        date_of_birth: profileData.date_of_birth || '',
        phone_number: profileData.phone_number || '',
        school_name: profileData.school_name || '',
        grade_level: profileData.grade_level || '',
        major_field: profileData.major_field || '',
        preferred_subjects: profileData.preferred_subjects || [],
        learning_style: (profileData.learning_style as any) || 'visual',
        study_goals: profileData.study_goals || '',
        bio: profileData.bio || ''
      })
    }
  }, [profileData, isEditing])

  // Show form if profile doesn't exist (404 error)
  useEffect(() => {
    if (error && (error as any).response?.status === 404) {
      setShowForm(true)
    }
  }, [error])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      if (isEditing) {
        await updateProfileMutation.mutateAsync(formData)
        setIsEditing(false)
        setShowForm(false)
        await refetch()
      } else {
        await createProfileMutation.mutateAsync(formData)
        setShowForm(false)
        await refetch()
      }
    } catch (error) {
      console.error('Error saving profile:', error)
    }
  }

  const handleAddSubject = () => {
    if (subjectInput.trim() && !formData.preferred_subjects?.includes(subjectInput.trim())) {
      setFormData({
        ...formData,
        preferred_subjects: [...(formData.preferred_subjects || []), subjectInput.trim()]
      })
      setSubjectInput('')
    }
  }

  const handleRemoveSubject = (subject: string) => {
    setFormData({
      ...formData,
      preferred_subjects: formData.preferred_subjects?.filter(s => s !== subject) || []
    })
  }

  const handleCreateProfile = () => {
    setShowForm(true)
    setIsEditing(false)
    setFormData({
      name: user?.full_name || '',
      email: user?.email || '',
      date_of_birth: '',
      phone_number: '',
      school_name: '',
      grade_level: '',
      major_field: '',
      preferred_subjects: [],
      learning_style: 'visual',
      study_goals: '',
      bio: ''
    })
  }

  const handleEdit = () => {
    setIsEditing(true)
    setShowForm(true)
  }

  const handleCancelEdit = () => {
    setIsEditing(false)
    setShowForm(false)
  }

  if (showForm) {
    return (
      <div className="max-w-2xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-yellow-500">
            {isEditing ? 'Edit Profile' : 'Create Student Profile'}
          </h1>
          {isEditing && (
            <button
              onClick={handleCancelEdit}
              className="text-sm text-gray-400 hover:text-gray-300"
            >
              Cancel
            </button>
          )}
        </div>
        
        <div className="bg-gray-800 p-6 rounded-lg shadow-xl border-2 border-yellow-500">
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Personal Information Section */}
            <div className="space-y-4">
              <h3 className="text-lg font-semibold text-yellow-500 border-b border-yellow-500/30 pb-2">
                Personal Information
              </h3>
              
              <div className="grid md:grid-cols-2 gap-4">
                <div>
                  <label htmlFor="name" className="block text-sm font-medium text-gray-300 mb-2">
                    Full Name *
                  </label>
                  <input
                    type="text"
                    id="name"
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                    className="w-full px-3 py-2 bg-gray-900 border border-gray-700 text-white rounded-md focus:outline-none focus:ring-2 focus:ring-yellow-500"
                    required
                  />
                </div>

                <div>
                  <label htmlFor="email" className="block text-sm font-medium text-gray-300 mb-2">
                    Email
                  </label>
                  <input
                    type="email"
                    id="email"
                    value={formData.email}
                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                    className="w-full px-3 py-2 bg-gray-900 border border-gray-700 text-white rounded-md focus:outline-none focus:ring-2 focus:ring-yellow-500"
                  />
                </div>

                <div>
                  <label htmlFor="date_of_birth" className="block text-sm font-medium text-gray-300 mb-2">
                    Date of Birth
                  </label>
                  <input
                    type="date"
                    id="date_of_birth"
                    value={formData.date_of_birth}
                    onChange={(e) => setFormData({ ...formData, date_of_birth: e.target.value })}
                    className="w-full px-3 py-2 bg-gray-900 border border-gray-700 text-white rounded-md focus:outline-none focus:ring-2 focus:ring-yellow-500"
                  />
                </div>

                <div>
                  <label htmlFor="phone_number" className="block text-sm font-medium text-gray-300 mb-2">
                    Phone Number
                  </label>
                  <input
                    type="tel"
                    id="phone_number"
                    value={formData.phone_number}
                    onChange={(e) => setFormData({ ...formData, phone_number: e.target.value })}
                    placeholder="+1 (555) 123-4567"
                    className="w-full px-3 py-2 bg-gray-900 border border-gray-700 text-white placeholder-gray-500 rounded-md focus:outline-none focus:ring-2 focus:ring-yellow-500"
                  />
                </div>
              </div>
            </div>

            {/* Education Information Section */}
            <div className="space-y-4">
              <h3 className="text-lg font-semibold text-yellow-500 border-b border-yellow-500/30 pb-2">
                Education Information
              </h3>
              
              <div className="grid md:grid-cols-2 gap-4">
                <div>
                  <label htmlFor="school_name" className="block text-sm font-medium text-gray-300 mb-2">
                    School/College Name
                  </label>
                  <input
                    type="text"
                    id="school_name"
                    value={formData.school_name}
                    onChange={(e) => setFormData({ ...formData, school_name: e.target.value })}
                    placeholder="e.g., Harvard University"
                    className="w-full px-3 py-2 bg-gray-900 border border-gray-700 text-white placeholder-gray-500 rounded-md focus:outline-none focus:ring-2 focus:ring-yellow-500"
                  />
                </div>

                <div>
                  <label htmlFor="grade_level" className="block text-sm font-medium text-gray-300 mb-2">
                    Grade Level
                  </label>
                  <select
                    id="grade_level"
                    value={formData.grade_level}
                    onChange={(e) => setFormData({ ...formData, grade_level: e.target.value })}
                    className="w-full px-3 py-2 bg-gray-900 border border-gray-700 text-white rounded-md focus:outline-none focus:ring-2 focus:ring-yellow-500"
                  >
                    <option value="">Select grade level</option>
                    <option value="Elementary School">Elementary School</option>
                    <option value="6th Grade">6th Grade</option>
                    <option value="7th Grade">7th Grade</option>
                    <option value="8th Grade">8th Grade</option>
                    <option value="9th Grade">9th Grade</option>
                    <option value="10th Grade">10th Grade</option>
                    <option value="11th Grade">11th Grade</option>
                    <option value="12th Grade">12th Grade</option>
                    <option value="College Freshman">College Freshman</option>
                    <option value="College Sophomore">College Sophomore</option>
                    <option value="College Junior">College Junior</option>
                    <option value="College Senior">College Senior</option>
                    <option value="Graduate Student">Graduate Student</option>
                    <option value="Other">Other</option>
                  </select>
                </div>

                <div className="md:col-span-2">
                  <label htmlFor="major_field" className="block text-sm font-medium text-gray-300 mb-2">
                    Major/Field of Study
                  </label>
                  <input
                    type="text"
                    id="major_field"
                    value={formData.major_field}
                    onChange={(e) => setFormData({ ...formData, major_field: e.target.value })}
                    placeholder="e.g., Computer Science, Biology"
                    className="w-full px-3 py-2 bg-gray-900 border border-gray-700 text-white placeholder-gray-500 rounded-md focus:outline-none focus:ring-2 focus:ring-yellow-500"
                  />
                </div>
              </div>
            </div>

            {/* Learning Preferences Section */}
            <div className="space-y-4">
              <h3 className="text-lg font-semibold text-yellow-500 border-b border-yellow-500/30 pb-2">
                Learning Preferences
              </h3>

              <div>
                <label htmlFor="learning_style" className="block text-sm font-medium text-gray-300 mb-2">
                  Learning Style
                </label>
                <select
                  id="learning_style"
                  value={formData.learning_style}
                  onChange={(e) => setFormData({ ...formData, learning_style: e.target.value as any })}
                  className="w-full px-3 py-2 bg-gray-900 border border-gray-700 text-white rounded-md focus:outline-none focus:ring-2 focus:ring-yellow-500"
                >
                  <option value="visual">Visual - Learn through images and diagrams</option>
                  <option value="auditory">Auditory - Learn through listening</option>
                  <option value="kinesthetic">Kinesthetic - Learn through hands-on activities</option>
                  <option value="reading_writing">Reading/Writing - Learn through text</option>
                  <option value="mixed">Mixed - Combination of styles</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Preferred Subjects
                </label>
                <div className="flex gap-2 mb-2">
                  <input
                    type="text"
                    value={subjectInput}
                    onChange={(e) => setSubjectInput(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), handleAddSubject())}
                    placeholder="e.g., Mathematics, Physics"
                    className="flex-1 px-3 py-2 bg-gray-900 border border-gray-700 text-white placeholder-gray-500 rounded-md focus:outline-none focus:ring-2 focus:ring-yellow-500"
                  />
                  <button
                    type="button"
                    onClick={handleAddSubject}
                    className="px-4 py-2 bg-yellow-500 text-black font-semibold rounded-md hover:bg-yellow-600"
                  >
                    Add
                  </button>
                </div>
                <div className="flex flex-wrap gap-2">
                  {formData.preferred_subjects?.map((subject) => (
                    <span
                      key={subject}
                      className="px-3 py-1 bg-yellow-500/20 text-yellow-400 border border-yellow-500/30 rounded-full text-sm flex items-center gap-2"
                    >
                      {subject}
                      <button
                        type="button"
                        onClick={() => handleRemoveSubject(subject)}
                        className="text-yellow-400 hover:text-yellow-300 font-bold"
                      >
                        ×
                      </button>
                    </span>
                  ))}
                </div>
              </div>

              <div>
                <label htmlFor="study_goals" className="block text-sm font-medium text-gray-300 mb-2">
                  Study Goals
                </label>
                <textarea
                  id="study_goals"
                  value={formData.study_goals}
                  onChange={(e) => setFormData({ ...formData, study_goals: e.target.value })}
                  placeholder="What are your learning goals? e.g., Prepare for SAT, Master calculus, etc."
                  rows={3}
                  className="w-full px-3 py-2 bg-gray-900 border border-gray-700 text-white placeholder-gray-500 rounded-md focus:outline-none focus:ring-2 focus:ring-yellow-500"
                />
              </div>
            </div>

            {/* Additional Information Section */}
            <div className="space-y-4">
              <h3 className="text-lg font-semibold text-yellow-500 border-b border-yellow-500/30 pb-2">
                About You
              </h3>

              <div>
                <label htmlFor="bio" className="block text-sm font-medium text-gray-300 mb-2">
                  Bio
                </label>
                <textarea
                  id="bio"
                  value={formData.bio}
                  onChange={(e) => setFormData({ ...formData, bio: e.target.value })}
                  placeholder="Tell us a bit about yourself..."
                  rows={4}
                  maxLength={500}
                  className="w-full px-3 py-2 bg-gray-900 border border-gray-700 text-white placeholder-gray-500 rounded-md focus:outline-none focus:ring-2 focus:ring-yellow-500"
                />
                <p className="text-xs text-gray-500 mt-1">{formData.bio?.length || 0}/500 characters</p>
              </div>
            </div>

            <button
              type="submit"
              disabled={createProfileMutation.isPending || updateProfileMutation.isPending}
              className="w-full bg-gradient-to-r from-yellow-500 to-yellow-600 text-black font-semibold py-3 px-4 rounded-md hover:from-yellow-600 hover:to-yellow-700 focus:outline-none focus:ring-2 focus:ring-yellow-500 disabled:opacity-50"
            >
              {createProfileMutation.isPending || updateProfileMutation.isPending
                ? 'Saving...'
                : isEditing
                ? 'Update Profile'
                : 'Create Profile'}
            </button>
          </form>

          {(createProfileMutation.error || updateProfileMutation.error) && (
            <div className="mt-4 p-3 bg-red-500/10 border border-red-500 rounded-md">
              <p className="text-red-400 text-sm">
                Error: {(createProfileMutation.error || updateProfileMutation.error)?.message}
              </p>
            </div>
          )}
        </div>
      </div>
    )
  }

  if (isLoading) {
    return (
      <div className="max-w-4xl mx-auto">
        <div className="text-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600 mx-auto"></div>
          <p className="text-gray-600 mt-4">Loading profile...</p>
        </div>
      </div>
    )
  }

  if (!profileData && !isLoading) {
    return (
      <div className="max-w-4xl mx-auto">
        <div className="text-center py-12">
          <div className="mb-6">
            <div className="w-20 h-20 bg-yellow-500 rounded-full flex items-center justify-center text-black text-3xl font-bold mx-auto mb-4">
              {user?.full_name?.charAt(0).toUpperCase() || '?'}
            </div>
            <h2 className="text-2xl font-bold text-white mb-2">Welcome, {user?.full_name}!</h2>
            <p className="text-gray-400 mb-6">Let's set up your learning profile</p>
          </div>
          <button
            onClick={handleCreateProfile}
            className="bg-gradient-to-r from-yellow-500 to-yellow-600 text-black font-semibold py-3 px-6 rounded-lg hover:from-yellow-600 hover:to-yellow-700 transition-all"
          >
            Create Your Profile
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-yellow-500">Student Profile</h1>
        <button
          onClick={handleEdit}
          className="text-sm px-4 py-2 bg-yellow-500 text-black font-semibold rounded-md hover:bg-yellow-600"
        >
          Edit Profile
        </button>
      </div>

      <div className="grid gap-6">
        {/* Profile Info Card */}
        <div className="bg-gradient-to-r from-yellow-500 to-yellow-600 p-6 rounded-lg shadow-xl border-2 border-yellow-400">
          <div className="flex items-center gap-4 mb-4">
            <div className="w-20 h-20 bg-black rounded-full flex items-center justify-center text-yellow-500 text-3xl font-bold border-2 border-yellow-500">
              {profileData.name.charAt(0).toUpperCase()}
            </div>
            <div>
              <h2 className="text-2xl font-bold text-black">{profileData.name}</h2>
              {profileData.email && <p className="text-gray-800">{profileData.email}</p>}
              {profileData.learning_style && (
                <p className="text-gray-800 text-sm mt-1 capitalize">
                  {profileData.learning_style.replace('_', '/')} Learner
                </p>
              )}
            </div>
          </div>
          
          {profileData.preferred_subjects && profileData.preferred_subjects.length > 0 && (
            <div>
              <p className="text-purple-100 text-sm mb-2">Preferred Subjects:</p>
              <div className="flex flex-wrap gap-2">
                {profileData.preferred_subjects.map((subject) => (
                  <span key={subject} className="px-3 py-1 bg-white bg-opacity-20 rounded-full text-sm">
                    {subject}
                  </span>
                ))}
              </div>
            </div>
          )}
          
          {profileData.last_studied_topic && (
            <div className="mt-4 pt-4 border-t border-purple-400">
              <p className="text-purple-100 text-sm">Last Studied:</p>
              <p className="font-medium">{profileData.last_studied_topic}</p>
            </div>
          )}
        </div>

        {/* Quick Stats Grid */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="bg-blue-50 p-4 rounded-lg border-2 border-blue-200">
            <div className="text-blue-600 text-sm font-medium mb-1">Questions</div>
            <div className="text-3xl font-bold text-blue-700">{profileData.stats.total_questions_asked}</div>
          </div>
          <div className="bg-green-50 p-4 rounded-lg border-2 border-green-200">
            <div className="text-green-600 text-sm font-medium mb-1">Quizzes</div>
            <div className="text-3xl font-bold text-green-700">{profileData.stats.total_quizzes_taken}</div>
          </div>
          <div className="bg-purple-50 p-4 rounded-lg border-2 border-purple-200">
            <div className="text-purple-600 text-sm font-medium mb-1">Notes</div>
            <div className="text-3xl font-bold text-purple-700">{profileData.stats.total_notes_summarized}</div>
          </div>
          <div className="bg-orange-50 p-4 rounded-lg border-2 border-orange-200">
            <div className="text-orange-600 text-sm font-medium mb-1">Streak</div>
            <div className="text-3xl font-bold text-orange-700">{profileData.stats.learning_streak} 🔥</div>
          </div>
        </div>

        {/* Detailed Statistics */}
        <div className="bg-white p-6 rounded-lg shadow-md border border-gray-200">
          <h3 className="text-xl font-semibold text-gray-900 mb-4">Learning Statistics</h3>
          
          <div className="grid md:grid-cols-2 gap-6">
            {/* Quiz Performance */}
            {profileData.stats.average_quiz_score !== null && profileData.stats.average_quiz_score !== undefined && (
              <div className="bg-gradient-to-br from-yellow-50 to-orange-50 p-4 rounded-lg border border-yellow-200">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium text-gray-700">Average Quiz Score</span>
                  <span className="text-xs text-gray-500">{profileData.stats.total_quizzes_taken} quizzes</span>
                </div>
                <div className="flex items-end gap-2">
                  <span className="text-4xl font-bold text-yellow-600">{profileData.stats.average_quiz_score}%</span>
                  <span className="text-sm text-gray-600 mb-1">
                    {profileData.stats.average_quiz_score >= 80 ? '🌟 Excellent!' : 
                     profileData.stats.average_quiz_score >= 60 ? '👍 Good!' : '💪 Keep practicing!'}
                  </span>
                </div>
              </div>
            )}

            {/* Study Time */}
            <div className="bg-gradient-to-br from-indigo-50 to-purple-50 p-4 rounded-lg border border-indigo-200">
              <div className="text-sm font-medium text-gray-700 mb-2">Total Study Time</div>
              <div className="flex items-end gap-2">
                <span className="text-4xl font-bold text-indigo-600">
                  {Math.floor(profileData.stats.total_study_time / 60)}h
                </span>
                <span className="text-2xl font-semibold text-indigo-500 mb-1">
                  {profileData.stats.total_study_time % 60}m
                </span>
              </div>
              <div className="text-xs text-gray-600 mt-2">
                ≈ {Math.round(profileData.stats.total_study_time / 60 * 10) / 10} hours of learning
              </div>
            </div>
          </div>
        </div>

        {/* Most Studied Topics */}
        {profileData.stats.most_studied_topics && profileData.stats.most_studied_topics.length > 0 && (
          <div className="bg-white p-6 rounded-lg shadow-md border border-gray-200">
            <h3 className="text-xl font-semibold text-gray-900 mb-4">Most Studied Topics</h3>
            <div className="flex flex-wrap gap-3">
              {profileData.stats.most_studied_topics.map((topic, index) => (
                <div
                  key={index}
                  className="px-4 py-2 bg-gradient-to-r from-indigo-100 to-purple-100 text-indigo-800 rounded-lg text-sm font-medium border border-indigo-200 flex items-center gap-2"
                >
                  <span className="text-lg">{index === 0 ? '🥇' : index === 1 ? '🥈' : index === 2 ? '🥉' : '📚'}</span>
                  {topic}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Motivational Message */}
        <div className="bg-gradient-to-r from-green-50 to-teal-50 p-6 rounded-lg border-2 border-green-200">
          <div className="flex items-center gap-3">
            <span className="text-4xl">🎯</span>
            <div>
              <h4 className="font-semibold text-gray-900">Keep up the great work!</h4>
              <p className="text-sm text-gray-600 mt-1">
                {profileData.stats.learning_streak > 0 
                  ? `You're on a ${profileData.stats.learning_streak} day streak! Don't break it!`
                  : 'Start your learning journey today!'}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ProfilePage
