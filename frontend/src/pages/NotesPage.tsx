import { useState } from 'react'
import { Link } from 'react-router-dom'
import { useSummarizeNotes } from '../hooks/useNotes'
import { useUploadFile } from '../hooks/useUpload'
import { NotesResponse } from '../types'
import { cleanMarkdown } from '../utils/formatText'

const NotesPage = () => {
  const [content, setContent] = useState('')
  const [format, setFormat] = useState<'bullet_points' | 'paragraph' | 'outline' | 'key_concepts'>('bullet_points')
  const [useFile, setUseFile] = useState(false)
  const [summary, setSummary] = useState<NotesResponse | null>(null)
  const studentId = localStorage.getItem('studentId') ? parseInt(localStorage.getItem('studentId')!) : undefined

  const summarizeMutation = useSummarizeNotes()
  const uploadFileMutation = useUploadFile()

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return

    try {
      const result = await uploadFileMutation.mutateAsync(file)
      setContent(result.content)
    } catch (error) {
      console.error('Error uploading file:', error)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!content.trim()) return

    try {
      // Limit content to 8000 chars to prevent timeouts
      const limitedContent = content.trim().substring(0, 8000)
      
      const result = await summarizeMutation.mutateAsync({
        content: limitedContent,
        format,
        student_id: studentId,
      })
      setSummary(result)
    } catch (error) {
      console.error('Error summarizing notes:', error)
    }
  }

  const handleNewSummary = () => {
    setSummary(null)
    setContent('')
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-yellow-500">Summarize Notes</h1>
        {!studentId && (
          <Link
            to="/profile"
            className="text-sm px-4 py-2 bg-yellow-500 text-black rounded-md hover:bg-yellow-400 font-bold"
          >
            Create Profile to Track Progress
          </Link>
        )}
      </div>
      
      {!summary ? (
        <div className="bg-gray-900 p-6 rounded-lg shadow-xl border-2 border-yellow-500">
          <div className="mb-4">
            <label className="flex items-center space-x-2 cursor-pointer">
              <input
                type="checkbox"
                checked={useFile}
                onChange={(e) => setUseFile(e.target.checked)}
                className="rounded border-gray-300 text-green-600 focus:ring-green-500"
              />
              <span className="text-sm font-medium text-gray-700">
                Upload document (PDF, TXT, DOCX)
              </span>
            </label>
          </div>

          {useFile && (
            <div className="mb-4 p-4 bg-green-50 rounded-md">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Upload File
              </label>
              <input
                type="file"
                accept=".pdf,.txt,.docx,.doc"
                onChange={handleFileUpload}
                className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-green-600 file:text-white hover:file:bg-green-700"
              />
              {uploadFileMutation.isPending && (
                <p className="mt-2 text-sm text-green-600">Uploading and processing file...</p>
              )}
              {content && (
                <p className="mt-2 text-sm text-green-600">
                  ✓ File processed successfully ({content.split(' ').length} words)
                </p>
              )}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            {!useFile && (
              <div>
                <label htmlFor="content" className="block text-sm font-medium text-gray-700 mb-2">
                  Content to Summarize
                </label>
                <textarea
                  id="content"
                  value={content}
                  onChange={(e) => setContent(e.target.value)}
                  placeholder="Paste your notes, lecture content, or study material here..."
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
                  rows={12}
                  required
                />
                <p className="mt-1 text-sm text-gray-500">
                  {content.length} characters, {content.split(' ').filter(w => w).length} words
                  {content.length > 8000 && (
                    <span className="text-orange-600 font-medium ml-2">
                      (Will be truncated to 8000 chars to prevent timeout)
                    </span>
                  )}
                </p>
              </div>
            )}

            <div>
              <label htmlFor="format" className="block text-sm font-medium text-gray-700 mb-2">
                Summary Format
              </label>
              <select
                id="format"
                value={format}
                onChange={(e) => setFormat(e.target.value as any)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
              >
                <option value="bullet_points">Bullet Points - Organized key information</option>
                <option value="paragraph">Paragraph - Coherent narrative summary</option>
                <option value="outline">Outline - Hierarchical structure</option>
                <option value="key_concepts">Key Concepts - Important concepts with explanations</option>
              </select>
            </div>

            <button
              type="submit"
              disabled={summarizeMutation.isPending || !content.trim()}
              className="w-full bg-green-600 text-white py-2 px-4 rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {summarizeMutation.isPending ? 'Summarizing...' : 'Summarize Notes'}
            </button>
          </form>

          {summarizeMutation.error && (
            <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-md">
              <p className="text-red-700 text-sm font-semibold mb-2">
                Error: {summarizeMutation.error.message}
              </p>
              {summarizeMutation.error.message.includes('timeout') ? (
                <div className="text-sm text-red-600 mt-2">
                  <p className="font-medium">Request Timeout</p>
                  <ul className="list-disc ml-5 mt-1 space-y-1">
                    <li>The content is too long to process</li>
                    <li>Try using a shorter document (under 5 pages)</li>
                    <li>Or paste only the most important sections</li>
                  </ul>
                </div>
              ) : summarizeMutation.error.message.includes('402') || 
                 summarizeMutation.error.message.includes('quota') ? (
                <div className="text-sm text-red-600 mt-2">
                  <p className="font-medium">API Quota Limit Reached</p>
                  <ul className="list-disc ml-5 mt-1 space-y-1">
                    <li>Try using a smaller document (under 10 pages)</li>
                    <li>Wait 60 seconds and try again</li>
                    <li>Or paste text directly instead of uploading</li>
                  </ul>
                </div>
              ) : null}
            </div>
          )}
        </div>
      ) : (
        <div className="bg-gray-900 p-6 rounded-lg shadow-xl border-2 border-yellow-500">
          <div className="flex justify-between items-start mb-4">
            <h2 className="text-xl font-semibold text-yellow-500">Summary</h2>
            <div className="text-sm text-gray-500">
              <span>Format: {summary.format}</span>
              <span className="mx-2">•</span>
              <span>Compression: {Math.round(summary.compression_ratio * 100)}%</span>
            </div>
          </div>

          <div className="bg-green-50 p-4 rounded-md mb-4">
            <div className="prose max-w-none">
              <div className="text-gray-700 whitespace-pre-wrap">
                {cleanMarkdown(summary.summary)}
              </div>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4 mb-4">
            <div className="bg-gray-50 p-3 rounded-md">
              <p className="text-sm text-gray-600">Original Length</p>
              <p className="text-lg font-semibold text-gray-900">{summary.original_length} chars</p>
            </div>
            <div className="bg-gray-50 p-3 rounded-md">
              <p className="text-sm text-gray-600">Summary Length</p>
              <p className="text-lg font-semibold text-gray-900">{summary.summary_length} chars</p>
            </div>
            <div className="bg-gray-50 p-3 rounded-md">
              <p className="text-sm text-gray-600">Reading Time</p>
              <p className="text-lg font-semibold text-gray-900">{summary.reading_time} min</p>
            </div>
            <div className="bg-gray-50 p-3 rounded-md">
              <p className="text-sm text-gray-600">Compression Ratio</p>
              <p className="text-lg font-semibold text-gray-900">{Math.round(summary.compression_ratio * 100)}%</p>
            </div>
          </div>

          {summary.key_terms && summary.key_terms.length > 0 && (
            <div className="mb-4">
              <h3 className="text-sm font-medium text-gray-700 mb-2">Key Terms:</h3>
              <div className="flex flex-wrap gap-2">
                {summary.key_terms.map((term, index) => (
                  <span key={index} className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm">
                    {term}
                  </span>
                ))}
              </div>
            </div>
          )}

          {summary.main_topics && summary.main_topics.length > 0 && (
            <div className="mb-4">
              <h3 className="text-sm font-medium text-gray-700 mb-2">Main Topics:</h3>
              <div className="flex flex-wrap gap-2">
                {summary.main_topics.map((topic, index) => (
                  <span key={index} className="px-3 py-1 bg-purple-100 text-purple-800 rounded-full text-sm">
                    {topic}
                  </span>
                ))}
              </div>
            </div>
          )}

          <div className="pt-4 border-t border-gray-200">
            <button
              onClick={handleNewSummary}
              className="bg-green-600 text-white py-2 px-4 rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500"
            >
              Summarize Another Document
            </button>
          </div>
        </div>
      )}
    </div>
  )
}

export default NotesPage
