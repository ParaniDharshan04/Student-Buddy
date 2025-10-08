import { useState, useRef, useEffect } from 'react'
import { useVoiceChat } from '../hooks/useVoiceChat'

interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
}

const VoiceAssistantPage = () => {
  const [messages, setMessages] = useState<Message[]>([])
  const [isListening, setIsListening] = useState(false)
  const [isSpeaking, setIsSpeaking] = useState(false)
  const [transcript, setTranscript] = useState('')
  const [textInput, setTextInput] = useState('')
  const [conversationMode, setConversationMode] = useState<'practice' | 'interview' | 'presentation'>('practice')
  
  const recognitionRef = useRef<any>(null)
  const synthesisRef = useRef<SpeechSynthesisUtterance | null>(null)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  
  const voiceChatMutation = useVoiceChat()

  const handleUserMessage = async (text: string) => {
    if (!text.trim()) return

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: text,
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setTranscript('')

    try {
      const response = await voiceChatMutation.mutateAsync({
        message: text,
        conversation_mode: conversationMode,
        conversation_history: messages.map(m => ({
          role: m.role,
          content: m.content
        }))
      })

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response.response,
        timestamp: new Date()
      }

      setMessages(prev => [...prev, assistantMessage])
      
      // Speak the response
      speakText(response.response)
    } catch (error) {
      console.error('Error getting AI response:', error)
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date()
      }
      setMessages(prev => [...prev, errorMessage])
    }
  }

  const speakText = (text: string) => {
    try {
      console.log('=== SPEAK TEXT CALLED ===')
      console.log('Text to speak:', text.substring(0, 100))
      
      if (!('speechSynthesis' in window)) {
        alert('Text-to-speech is not supported in your browser. Please use Chrome or Edge.')
        return
      }
      
      // Only cancel if currently speaking
      if (window.speechSynthesis.speaking) {
        console.log('Cancelling previous speech...')
        window.speechSynthesis.cancel()
      }
      
      // Create utterance
      const utterance = new SpeechSynthesisUtterance(text)
      utterance.lang = 'en-US'
      utterance.rate = 0.9
      utterance.pitch = 1
      utterance.volume = 1
      
      utterance.onstart = () => {
        console.log('🔊 AI is speaking NOW! Check your volume!')
        setIsSpeaking(true)
      }
      
      utterance.onend = () => {
        console.log('✓ AI finished speaking')
        setIsSpeaking(false)
      }
      
      utterance.onerror = (event) => {
        console.error('❌ Speech error:', event.error)
        if (event.error !== 'interrupted') {
          alert(`Speech error: ${event.error}`)
        }
        setIsSpeaking(false)
      }
      
      synthesisRef.current = utterance
      
      // Speak immediately
      console.log('Starting speech...')
      window.speechSynthesis.speak(utterance)
      
      // Debug check
      setTimeout(() => {
        console.log('Status check:', {
          speaking: window.speechSynthesis.speaking,
          pending: window.speechSynthesis.pending,
          paused: window.speechSynthesis.paused
        })
      }, 500)
      
    } catch (error) {
      console.error('❌ Error in speakText:', error)
      setIsSpeaking(false)
    }
  }

  useEffect(() => {
    // Initialize Speech Recognition
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = (window as any).webkitSpeechRecognition || (window as any).SpeechRecognition
      recognitionRef.current = new SpeechRecognition()
      recognitionRef.current.continuous = false
      recognitionRef.current.interimResults = true
      recognitionRef.current.lang = 'en-US'

      recognitionRef.current.onresult = (event: any) => {
        const current = event.resultIndex
        const transcriptText = event.results[current][0].transcript
        setTranscript(transcriptText)
        
        if (event.results[current].isFinal) {
          handleUserMessage(transcriptText)
        }
      }

      recognitionRef.current.onerror = (event: any) => {
        console.error('Speech recognition error:', event.error)
        
        let errorMessage = ''
        let shouldRetry = false
        
        switch (event.error) {
          case 'network':
            errorMessage = 'Network error detected. This is usually temporary. Click the microphone again to retry.'
            shouldRetry = true
            break
          case 'not-allowed':
            errorMessage = 'Microphone access denied. Please:\n1. Click the lock icon in address bar\n2. Allow microphone access\n3. Refresh the page'
            break
          case 'no-speech':
            // Don't show alert for no-speech, just stop listening
            setIsListening(false)
            return
          case 'aborted':
            // Don't show alert for aborted
            setIsListening(false)
            return
          case 'audio-capture':
            errorMessage = 'No microphone found. Please connect a microphone and try again.'
            break
          case 'service-not-allowed':
            errorMessage = 'Speech recognition service not available. Please check your internet connection.'
            shouldRetry = true
            break
          default:
            errorMessage = `Speech recognition error: ${event.error}. Click microphone to try again.`
            shouldRetry = true
        }
        
        if (errorMessage) {
          alert(errorMessage)
        }
        
        setIsListening(false)
      }

      recognitionRef.current.onend = () => {
        setIsListening(false)
      }
    } else {
      console.error('Speech recognition not supported')
      alert('Speech recognition is not supported in your browser. Please use Chrome or Edge.')
    }

    return () => {
      if (recognitionRef.current) {
        try {
          recognitionRef.current.stop()
        } catch (e) {
          // Ignore errors on cleanup
        }
      }
      window.speechSynthesis.cancel()
    }
  }, [])

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const startListening = () => {
    if (!recognitionRef.current) {
      alert('Speech recognition not initialized. Please refresh the page.')
      return
    }
    
    if (!isListening) {
      try {
        setTranscript('')
        // Reset recognition to clear any previous errors
        recognitionRef.current.abort()
        setTimeout(() => {
          try {
            recognitionRef.current.start()
            setIsListening(true)
          } catch (e) {
            console.error('Error starting recognition:', e)
            alert('Could not start microphone. Please check permissions and internet connection.')
          }
        }, 100)
      } catch (error) {
        console.error('Error starting recognition:', error)
        alert('Could not start microphone. Please check permissions.')
      }
    }
  }

  const stopListening = () => {
    if (recognitionRef.current && isListening) {
      try {
        recognitionRef.current.stop()
        setIsListening(false)
      } catch (error) {
        console.error('Error stopping recognition:', error)
      }
    }
  }

  const stopSpeaking = () => {
    console.log('Stopping speech...')
    window.speechSynthesis.cancel()
    setIsSpeaking(false)
  }

  const clearConversation = () => {
    setMessages([])
    setTranscript('')
    stopSpeaking()
  }

  const getModeDescription = () => {
    switch (conversationMode) {
      case 'practice':
        return 'Casual conversation practice to improve fluency'
      case 'interview':
        return 'Mock interview practice with professional questions'
      case 'presentation':
        return 'Practice presenting ideas clearly and confidently'
    }
  }

  return (
    <div className="max-w-6xl mx-auto">
      <div className="mb-8">
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-yellow-500 mb-2">Voice Assistant</h1>
            <p className="text-gray-400">Practice your communication skills with AI</p>
          </div>
          <button
            onClick={() => {
              const test = 'Hello! This is a test. Can you hear me speaking?'
              console.log('Testing voice...')
              speakText(test)
            }}
            className="px-4 py-2 bg-yellow-500 text-black font-semibold rounded-lg hover:bg-yellow-600"
          >
            🔊 Test Voice
          </button>
        </div>
      </div>

      {/* Mode Selection */}
      <div className="bg-gray-800 p-6 rounded-lg shadow-xl border-2 border-yellow-500 mb-6">
        <h2 className="text-xl font-semibold text-yellow-400 mb-4">Conversation Mode</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
          <button
            onClick={() => setConversationMode('practice')}
            className={`p-4 rounded-lg border-2 transition-all ${
              conversationMode === 'practice'
                ? 'border-yellow-500 bg-gray-700'
                : 'border-gray-600 hover:border-yellow-400'
            }`}
          >
            <div className="text-2xl mb-2">💬</div>
            <div className="font-semibold text-yellow-400">Casual Practice</div>
            <div className="text-sm text-gray-400 mt-1">Improve fluency</div>
          </button>
          
          <button
            onClick={() => setConversationMode('interview')}
            className={`p-4 rounded-lg border-2 transition-all ${
              conversationMode === 'interview'
                ? 'border-yellow-500 bg-gray-700'
                : 'border-gray-600 hover:border-yellow-400'
            }`}
          >
            <div className="text-2xl mb-2">👔</div>
            <div className="font-semibold text-yellow-400">Interview Practice</div>
            <div className="text-sm text-gray-400 mt-1">Professional skills</div>
          </button>
          
          <button
            onClick={() => setConversationMode('presentation')}
            className={`p-4 rounded-lg border-2 transition-all ${
              conversationMode === 'presentation'
                ? 'border-yellow-500 bg-gray-700'
                : 'border-gray-600 hover:border-yellow-400'
            }`}
          >
            <div className="text-2xl mb-2">🎤</div>
            <div className="font-semibold text-yellow-400">Presentation</div>
            <div className="text-sm text-gray-400 mt-1">Public speaking</div>
          </button>
        </div>
        <p className="text-sm text-gray-400">{getModeDescription()}</p>
      </div>

      {/* Chat Area */}
      <div className="bg-gray-800 rounded-lg shadow-xl border-2 border-yellow-500 mb-6">
        <div className="h-96 overflow-y-auto p-6 space-y-4">
          {messages.length === 0 ? (
            <div className="text-center text-gray-500 mt-20">
              <div className="text-6xl mb-4">🎙️</div>
              <p className="text-lg">Click the microphone to start speaking</p>
              <p className="text-sm mt-2">The AI will respond and help you practice</p>
            </div>
          ) : (
            messages.map((message) => (
              <div
                key={message.id}
                className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-[70%] p-4 rounded-lg ${
                    message.role === 'user'
                      ? 'bg-yellow-500 text-black'
                      : 'bg-gray-700 text-yellow-100'
                  }`}
                >
                  <div className="flex items-start gap-2">
                    <span className="text-2xl">
                      {message.role === 'user' ? '👤' : '🤖'}
                    </span>
                    <div className="flex-1">
                      <p className="whitespace-pre-wrap">{message.content}</p>
                      <div className="flex items-center justify-between mt-2">
                        <p className="text-xs opacity-70">
                          {message.timestamp.toLocaleTimeString()}
                        </p>
                        {message.role === 'assistant' && (
                          <button
                            onClick={() => speakText(message.content)}
                            className="text-xs px-2 py-1 bg-yellow-500/20 hover:bg-yellow-500/30 rounded flex items-center gap-1"
                            title="Speak this message"
                          >
                            🔊 Speak
                          </button>
                        )}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ))
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Transcript Display */}
        {transcript && (
          <div className="px-6 py-3 bg-gray-900 border-t border-gray-700">
            <p className="text-sm text-gray-400">Listening: <span className="text-yellow-400">{transcript}</span></p>
          </div>
        )}

        {/* Controls */}
        <div className="p-6 bg-gray-900 border-t border-gray-700 rounded-b-lg">
          <div className="flex items-center justify-center gap-4">
            {/* Microphone Button */}
            <button
              onClick={isListening ? stopListening : startListening}
              disabled={isSpeaking}
              className={`w-16 h-16 rounded-full flex items-center justify-center transition-all ${
                isListening
                  ? 'bg-red-500 hover:bg-red-600 animate-pulse'
                  : 'bg-yellow-500 hover:bg-yellow-600'
              } disabled:opacity-50 disabled:cursor-not-allowed`}
            >
              {isListening ? (
                <svg className="w-8 h-8 text-white" fill="currentColor" viewBox="0 0 20 20">
                  <rect x="6" y="6" width="8" height="8" />
                </svg>
              ) : (
                <svg className="w-8 h-8 text-black" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M7 4a3 3 0 016 0v6a3 3 0 11-6 0V4z" />
                  <path d="M5.5 9.643a.75.75 0 00-1.5 0V10c0 3.06 2.29 5.585 5.25 5.954V17.5h-1.5a.75.75 0 000 1.5h4.5a.75.75 0 000-1.5h-1.5v-1.546A6.001 6.001 0 0016 10v-.357a.75.75 0 00-1.5 0V10a4.5 4.5 0 01-9 0v-.357z" />
                </svg>
              )}
            </button>

            {/* Stop Speaking Button */}
            {isSpeaking && (
              <button
                onClick={stopSpeaking}
                className="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600"
              >
                Stop Speaking
              </button>
            )}

            {/* Clear Button */}
            {messages.length > 0 && (
              <button
                onClick={clearConversation}
                className="px-4 py-2 bg-gray-700 text-yellow-400 rounded-lg hover:bg-gray-600 border border-yellow-500"
              >
                Clear Chat
              </button>
            )}
          </div>

          <div className="mt-4 text-center">
            <p className="text-sm text-gray-400">
              {isListening ? '🎤 Listening...' : isSpeaking ? '🔊 Speaking...' : '💡 Click microphone to speak or type below'}
            </p>
          </div>

          {/* Text Input Fallback */}
          <div className="mt-4">
            <div className="flex gap-2">
              <input
                type="text"
                value={textInput}
                onChange={(e) => setTextInput(e.target.value)}
                onKeyPress={(e) => {
                  if (e.key === 'Enter' && textInput.trim()) {
                    handleUserMessage(textInput)
                    setTextInput('')
                  }
                }}
                placeholder="Or type your message here..."
                className="flex-1 px-4 py-2 bg-gray-800 border border-gray-600 rounded-lg text-yellow-100 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-yellow-500"
                disabled={isListening || isSpeaking}
              />
              <button
                onClick={() => {
                  if (textInput.trim()) {
                    handleUserMessage(textInput)
                    setTextInput('')
                  }
                }}
                disabled={!textInput.trim() || isListening || isSpeaking}
                className="px-6 py-2 bg-yellow-500 text-black font-semibold rounded-lg hover:bg-yellow-600 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Send
              </button>
            </div>
            <p className="text-xs text-gray-500 mt-2 text-center">
              💡 Tip: If microphone doesn't work, you can type your messages
            </p>
          </div>
        </div>
      </div>

      {/* Tips */}
      <div className="bg-gray-800 p-6 rounded-lg border border-yellow-500/30">
        <h3 className="text-lg font-semibold text-yellow-400 mb-3">💡 Tips for Better Practice</h3>
        <ul className="space-y-2 text-gray-300 text-sm">
          <li>• Speak clearly and at a moderate pace</li>
          <li>• Use complete sentences to practice proper grammar</li>
          <li>• Try different conversation modes to practice various scenarios</li>
          <li>• Listen to the AI's pronunciation and try to mimic it</li>
          <li>• Practice regularly to build confidence and fluency</li>
        </ul>
      </div>
    </div>
  )
}

export default VoiceAssistantPage
