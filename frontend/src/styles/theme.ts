// Black & Gold Theme Configuration
export const theme = {
  colors: {
    primary: {
      gold: '#FFD700',
      goldDark: '#DAA520',
      goldLight: '#FFF8DC',
    },
    background: {
      black: '#000000',
      darkGray: '#1a1a1a',
      cardBg: '#1f1f1f',
    },
    text: {
      gold: '#FFD700',
      goldLight: '#FFF8DC',
      white: '#FFFFFF',
      gray: '#9CA3AF',
    },
    border: {
      gold: '#FFD700',
      darkGold: '#DAA520',
    }
  },
  
  // Common class combinations
  card: 'bg-gray-900 border-2 border-yellow-500 rounded-lg shadow-xl',
  cardHover: 'hover:border-yellow-400 hover:shadow-2xl',
  button: 'bg-yellow-500 text-black font-bold hover:bg-yellow-400',
  buttonSecondary: 'bg-gray-800 text-yellow-500 border-2 border-yellow-500 hover:bg-gray-700',
  input: 'bg-gray-800 border-2 border-yellow-500 text-yellow-100 focus:border-yellow-400',
  label: 'text-yellow-400 font-medium',
  title: 'text-yellow-500 font-bold',
  text: 'text-yellow-100',
  textMuted: 'text-gray-400',
}
