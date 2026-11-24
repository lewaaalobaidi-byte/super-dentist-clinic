module.exports = {
  content: ['./*.html', './site.js'],
  theme: {
    extend: {
      fontFamily: { sans: ['"Noto Sans Arabic"', 'Inter', 'sans-serif'] },
      colors: {
        navyBlue: '#1a365d', iceBlue: '#00e5ff', deepBlue: '#0077ff',
        whatsapp: '#15803D', whatsappDark: '#166534'
      },
      boxShadow: {
        glass: '0 8px 32px 0 rgba(255, 255, 255, 0.2)',
        glow: '0 0 20px rgba(21, 128, 61, 0.35)',
        cta: '0 1px 2px rgba(0,0,0,.08), 0 6px 16px rgba(21,128,61,.28)'
      }
    }
  }
}
