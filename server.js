import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import path from 'path';
import { fileURLToPath } from 'url';

dotenv.config();

const app = express();
const __dirname = path.dirname(fileURLToPath(import.meta.url));

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, 'dist')));

// API Routes
app.post('/api/auth/signup', (req, res) => {
  const { name, email, password } = req.body;
  
  // Mock authentication - replace with real database
  if (!name || !email || !password) {
    return res.status(400).json({ message: 'All fields are required' });
  }
  
  const mockToken = 'mock_token_' + Math.random().toString(36).substring(7);
  res.json({
    token: mockToken,
    user: {
      id: 1,
      name,
      email,
      avatar: `https://api.dicebear.com/7.x/avataaars/svg?seed=${email}`,
    },
  });
});

app.post('/api/auth/login', (req, res) => {
  const { email, password } = req.body;
  
  // Mock authentication - replace with real database
  if (!email || !password) {
    return res.status(400).json({ message: 'Email and password are required' });
  }
  
  const mockToken = 'mock_token_' + Math.random().toString(36).substring(7);
  res.json({
    token: mockToken,
    user: {
      id: 1,
      name: 'User',
      email,
      avatar: `https://api.dicebear.com/7.x/avataaars/svg?seed=${email}`,
    },
  });
});

// Serve React app
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'dist', 'index.html'));
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
