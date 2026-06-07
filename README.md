# YonocyTech AI - Setup Guide

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- npm or yarn

### Development Setup

1. **Install dependencies**
   ```bash
   npm install
   ```

2. **Start development server**
   ```bash
   npm run dev
   ```

3. **Start backend server** (in another terminal)
   ```bash
   npm start
   ```

4. **Open browser**
   ```
   http://localhost:5173
   ```

### Build for Production

```bash
npm run build
```

### Docker Deployment

```bash
docker-compose up
```

## 📁 Project Structure

```
├── src/
│   ├── components/        # React components
│   ├── pages/            # Page components
│   ├── store/            # Zustand stores
│   ├── App.jsx           # Main App component
│   ├── main.jsx          # React entry point
│   └── index.css         # Global styles
├── dist/                 # Build output
├── server.js             # Express backend
├── vite.config.js        # Vite configuration
├── tailwind.config.js    # Tailwind configuration
└── package.json          # Dependencies
```

## 🎨 Features

- ✨ Modern Copilot-inspired UI
- 🔐 Secure authentication system
- 📱 Fully responsive design
- 🎭 Smooth animations with Framer Motion
- 🎯 Beautiful signup/login pages
- 📊 Dashboard with statistics
- 🚀 Production-ready code

## 🔧 Tech Stack

- **Frontend**: React 18, Vite, Tailwind CSS
- **Animations**: Framer Motion
- **Icons**: Lucide React
- **State Management**: Zustand
- **Backend**: Express.js
- **Deployment**: Docker

## 📝 Environment Variables

Create `.env` file:

```
VITE_API_URL=http://localhost:3000
VITE_APP_NAME=YonocyTech AI
PORT=3000
NODE_ENV=development
```

## 🌐 Deployment Options

### Vercel
```bash
vercel deploy
```

### Heroku
```bash
heroku create
heroku push
```

### Railway/Render
Connect your GitHub repo for automatic deployments.

### Self-hosted with Docker
```bash
docker build -t yonocytech-ai .
docker run -p 3000:3000 yonocytech-ai
```

## 📚 Learn More

- [React Documentation](https://react.dev)
- [Tailwind CSS](https://tailwindcss.com)
- [Framer Motion](https://www.framer.com/motion)
- [Zustand](https://github.com/pmndrs/zustand)

## 📄 License

MIT License - feel free to use this project!
