// Question types
export interface QuestionRequest {
  question: string
  explanation_style: 'simple' | 'exam-style' | 'real-world'
  student_id?: number
}

export interface QuestionResponse {
  answer: string
  explanation_steps: string[]
  style: string
  confidence_score: number
  related_topics: string[]
  session_id?: number
}

// Quiz types
export interface QuizRequest {
  topic: string
  difficulty: 'easy' | 'medium' | 'hard'
  question_count: number
  question_types: ('multiple_choice' | 'true_false' | 'short_answer')[]
  student_id?: number
}

export interface QuizQuestion {
  id: string
  question: string
  type: 'multiple_choice' | 'true_false' | 'short_answer'
  options?: string[]
  correct_answer: string
  explanation: string
  points: number
}

export interface QuizResponse {
  quiz_id: string
  topic: string
  difficulty: string
  questions: QuizQuestion[]
  question_count: number
  estimated_time: number
  total_points: number
}

// Notes types
export interface NotesRequest {
  content: string
  format: 'bullet_points' | 'paragraph' | 'outline' | 'key_concepts'
  max_length?: number
  topic?: string
  student_id?: number
}

export interface NotesResponse {
  summary: string
  format: string
  original_length: number
  summary_length: number
  compression_ratio: number
  key_terms: string[]
  main_topics: string[]
  reading_time: number
  session_id?: number
}

// Profile types
export interface ProfileRequest {
  name: string
  email?: string
  // Personal Information
  date_of_birth?: string
  phone_number?: string
  // Education Information
  school_name?: string
  grade_level?: string
  major_field?: string
  // Learning Preferences
  preferred_subjects?: string[]
  learning_style?: 'visual' | 'auditory' | 'kinesthetic' | 'reading_writing' | 'mixed'
  study_goals?: string
  // Additional Info
  bio?: string
}

export interface ProfileResponse {
  id: number
  name: string
  email?: string
  // Personal Information
  date_of_birth?: string
  phone_number?: string
  // Education Information
  school_name?: string
  grade_level?: string
  major_field?: string
  // Learning Preferences
  preferred_subjects: string[]
  learning_style?: string
  study_goals?: string
  last_studied_topic?: string
  // Additional Info
  bio?: string
  // Timestamps
  created_at: string
  updated_at: string
}

export interface ProfileStats {
  total_questions_asked: number
  total_quizzes_taken: number
  total_notes_summarized: number
  average_quiz_score?: number
  most_studied_topics: string[]
  learning_streak: number
  total_study_time: number
}

export interface ProfileWithStats extends ProfileResponse {
  stats: ProfileStats
}

// API Error types
export interface APIError {
  detail: string | { msg: string; type: string }[]
}