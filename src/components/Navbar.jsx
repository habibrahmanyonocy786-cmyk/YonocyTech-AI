import { useState } from 'react';
import { Link } from 'react-router-dom';
import { Menu, X, LogOut, User } from 'lucide-react';
import { useAuthStore } from '../store/authStore';

function Navbar() {
  const [isOpen, setIsOpen] = useState(false);
  const { logout, user } = useAuthStore();

  const handleLogout = () => {
    logout();
    setIsOpen(false);
  };

  return (
    <nav className="sticky top-0 z-50 bg-slate-950/80 backdrop-blur-md border-b border-blue-900/30">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2 group">
            <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-lg flex items-center justify-center group-hover:shadow-lg group-hover:shadow-blue-500/50 transition-all">
              <span className="text-white font-bold text-sm">YT</span>
            </div>
            <span className="text-xl font-bold bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">YonocyTech</span>
          </Link>

          {/* Desktop Menu */}
          <div className="hidden md:flex items-center space-x-8">
            <Link to="/" className="text-slate-300 hover:text-white transition-colors">Home</Link>
            {user && (
              <>
                <Link to="/dashboard" className="text-slate-300 hover:text-white transition-colors">Dashboard</Link>
              </>
            )}
          </div>

          {/* User Menu / Mobile Menu Button */}
          <div className="flex items-center space-x-4">
            {user && (
              <div className="hidden md:flex items-center space-x-3">
                <img
                  src={user.avatar || 'https://api.dicebear.com/7.x/avataaars/svg?seed=' + user.email}
                  alt="Avatar"
                  className="w-8 h-8 rounded-full border border-blue-500/50"
                />
                <span className="text-sm text-slate-300">{user.name}</span>
                <button
                  onClick={handleLogout}
                  className="p-2 hover:bg-slate-800 rounded-lg transition-colors"
                >
                  <LogOut size={18} />
                </button>
              </div>
            )}
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="md:hidden p-2 hover:bg-slate-800 rounded-lg transition-colors"
            >
              {isOpen ? <X size={24} /> : <Menu size={24} />}
            </button>
          </div>
        </div>

        {/* Mobile Menu */}
        {isOpen && (
          <div className="md:hidden pb-4 border-t border-blue-900/30">
            <Link
              to="/"
              className="block px-4 py-2 text-slate-300 hover:bg-slate-800 rounded-lg transition-colors"
              onClick={() => setIsOpen(false)}
            >
              Home
            </Link>
            {user && (
              <>
                <Link
                  to="/dashboard"
                  className="block px-4 py-2 text-slate-300 hover:bg-slate-800 rounded-lg transition-colors"
                  onClick={() => setIsOpen(false)}
                >
                  Dashboard
                </Link>
                <button
                  onClick={handleLogout}
                  className="w-full text-left px-4 py-2 text-slate-300 hover:bg-slate-800 rounded-lg transition-colors flex items-center space-x-2"
                >
                  <LogOut size={18} />
                  <span>Logout</span>
                </button>
              </>
            )}
          </div>
        )}
      </div>
    </nav>
  );
}

export default Navbar;
