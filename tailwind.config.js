export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'green-ge': '#007A33',
        'green-light': '#E8F5E9',
        'green-dark': '#006028',
        'blue-ge': '#0055A4',
        'blue-light': '#E3F2FD',
        'red-ge': '#CE1126',
        'red-light': '#FFEBEE',
        'gold-ge': '#FFD700',
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        display: ['Poppins', 'sans-serif'],
      },
      boxShadow: {
        'soft': '0 4px 20px rgba(0, 0, 0, 0.08)',
        'medium': '0 8px 30px rgba(0, 0, 0, 0.12)',
        'strong': '0 15px 40px rgba(0, 0, 0, 0.15)',
      },
      borderRadius: {
        'xl': '1rem',
        '2xl': '1.5rem',
        '3xl': '2rem',
      },
    },
  },
  plugins: [],
}
