import { Link, useLocation } from 'react-router-dom'

const navigation = [
  { name: 'Home', href: '/', icon: '🏠' },
  { name: 'Ask Question', href: '/question', icon: '❓' },
  { name: 'Take Quiz', href: '/quiz', icon: '📝' },
  { name: 'Summarize Notes', href: '/notes', icon: '📄' },
  { name: 'Voice Assistant', href: '/voice-assistant', icon: '🎙️' },
]

const Sidebar = () => {
  const location = useLocation()

  return (
    <div className="w-64 bg-black shadow-lg border-r-2 border-yellow-500 min-h-screen">
      <nav className="mt-8 px-4">
        <ul className="space-y-2">
          {navigation.map((item) => {
            const isActive = location.pathname === item.href
            return (
              <li key={item.name}>
                <Link
                  to={item.href}
                  className={`flex items-center px-4 py-3 text-sm font-medium rounded-lg transition-all ${
                    isActive
                      ? 'bg-yellow-500 text-black border-l-4 border-yellow-600 shadow-lg'
                      : 'text-yellow-400 hover:bg-gray-900 hover:text-yellow-300'
                  }`}
                >
                  <span className="mr-3 text-lg">{item.icon}</span>
                  {item.name}
                </Link>
              </li>
            )
          })}
        </ul>
      </nav>
    </div>
  )
}

export default Sidebar