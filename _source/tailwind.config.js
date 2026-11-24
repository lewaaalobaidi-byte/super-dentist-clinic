module.exports = {
  content: ['./*.html', './site.js'],
  theme: {
    extend: {
      fontFamily: { sans: ['"Noto Sans Arabic"', 'Inter', 'sans-serif'] },
      colors: {
        navyBlue: '#1a365d', iceBlue: '#00e5ff', deepBlue: '#0077ff',
        whatsapp: '#25D366', whatsappDark: '#128C7E'
      },
      boxShadow: {
        glass: '0 8px 32px 0 rgba(255, 255, 255, 0.2)',
        glow: '0 0 20px rgba(37, 211, 102, 0.5)'
      }
    }
  }
}
