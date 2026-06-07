import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { useAuthStore } from '../store/authStore';
import { Mail, Lock, Eye, EyeOff, Github, ArrowRight } from 'lucide-react';

function LoginPage() {
  const navigate = useNavigate();
  const { login, loading, error } = useAuthStore();
  const [showPassword, setShowPassword] = useState(false);
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    rememberMe: false,
  });
  const [validationErrors, setValidationErrors] = useState({});

  const handleChange = (e) => {
    const { name, value, checked, type } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }));
    if (validationErrors[name]) {
      setValidationErrors((prev) => ({
        ...prev,
        [name]: '',
      }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const errors = {};

    if (!formData.email.match(/^[^\s@]+@[^\s@]+\.[^\s@]+$/)) {
      errors.email = 'Valid email is required';
    }
    if (formData.password.length < 8) {
      errors.password = 'Password must be at least 8 characters';
    }

    if (Object.keys(errors).length > 0) {
      setValidationErrors(errors);
      return;
    }

    try {
      await login({
        email: formData.email,
        password: formData.password,
      });
      navigate('/dashboard');
    } catch (err) {
      setValidationErrors({ submit: err.message });
    }
  };

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
        delayChildren: 0.2,
      },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: { duration: 0.6, ease: 'easeOut' },
    },
  };

  return (
    <div className="min-h-screen flex items-center justify-center px-4 py-12">
      <motion.div
        initial="hidden"
        animate="visible"
        variants={containerVariants}
        className="w-full max-w-md"
      >
        <motion.div variants={itemVariants} className="text-center mb-8">
          <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent mb-2">
            Welcome Back
          </h1>
          <p className="text-slate-400">Sign in to your YonocyTech account</p>
        </motion.div>

        <motion.div
          variants={itemVariants}
          className="bg-slate-900/50 backdrop-blur-xl border border-blue-900/30 rounded-2xl p-8 shadow-2xl"
        >
          {/* Social Login */}
          <div className="mb-6">
            <button className="w-full flex items-center justify-center space-x-2 bg-slate-800 hover:bg-slate-700 text-white font-semibold py-3 rounded-lg transition-colors">
              <Github size={20} />
              <span>Sign in with GitHub</span>
            </button>
          </div>

          <div className="flex items-center gap-4 mb-6">
            <div className="flex-1 h-px bg-blue-900/30" />
            <span className="text-slate-500 text-sm">or</span>
            <div className="flex-1 h-px bg-blue-900/30" />
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-4">
            {/* Email Field */}
            <motion.div variants={itemVariants}>
              <label className="block text-sm font-medium text-slate-300 mb-2">Email Address</label>
              <div className="relative">
                <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-500" size={18} />
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  placeholder="you@example.com"
                  className={`w-full pl-10 pr-4 py-3 bg-slate-800/50 border rounded-lg focus:outline-none transition-all ${
                    validationErrors.email
                      ? 'border-red-500/50 focus:border-red-500'
                      : 'border-blue-900/30 focus:border-blue-500'
                  }`}
                />
              </div>
              {validationErrors.email && (
                <p className="text-red-400 text-sm mt-1">{validationErrors.email}</p>
              )}
            </motion.div>

            {/* Password Field */}
            <motion.div variants={itemVariants}>
              <label className="block text-sm font-medium text-slate-300 mb-2">Password</label>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-500" size={18} />
                <input
                  type={showPassword ? 'text' : 'password'}
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  placeholder="Enter your password"
                  className={`w-full pl-10 pr-12 py-3 bg-slate-800/50 border rounded-lg focus:outline-none transition-all ${
                    validationErrors.password
                      ? 'border-red-500/50 focus:border-red-500'
                      : 'border-blue-900/30 focus:border-blue-500'
                  }`}
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 transform -translate-y-1/2 text-slate-500 hover:text-slate-300"
                >
                  {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                </button>
              </div>
              {validationErrors.password && (
                <p className="text-red-400 text-sm mt-1">{validationErrors.password}</p>
              )}
            </motion.div>

            {/* Remember Me & Forgot Password */}
            <motion.div variants={itemVariants} className="flex items-center justify-between">
              <label className="flex items-center space-x-2 cursor-pointer">
                <input
                  type="checkbox"
                  name="rememberMe"
                  checked={formData.rememberMe}
                  onChange={handleChange}
                  className="w-4 h-4 rounded border-blue-500"
                />
                <span className="text-sm text-slate-400">Remember me</span>
              </label>
              <a href="#" className="text-sm text-blue-400 hover:text-blue-300">
                Forgot password?
              </a>
            </motion.div>

            {/* Error Message */}
            {(error || validationErrors.submit) && (
              <motion.div
                variants={itemVariants}
                className="p-3 bg-red-900/20 border border-red-500/30 rounded-lg text-red-400 text-sm"
              >
                {error || validationErrors.submit}
              </motion.div>
            )}

            {/* Submit Button */}
            <motion.button
              variants={itemVariants}
              type="submit"
              disabled={loading}
              className="w-full py-3 bg-gradient-to-r from-blue-600 to-cyan-600 text-white font-semibold rounded-lg hover:shadow-lg hover:shadow-blue-500/50 transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center group"
            >
              {loading ? (
                <span>Signing in...</span>
              ) : (
                <>
                  Sign In
                  <ArrowRight className="ml-2 group-hover:translate-x-1 transition-transform" size={18} />
                </>
              )}
            </motion.button>
          </form>

          {/* Signup Link */}
          <motion.p variants={itemVariants} className="text-center text-slate-400 mt-6">
            Don't have an account?{' '}
            <a href="/signup" className="text-blue-400 hover:text-blue-300 font-semibold">
              Create one
            </a>
          </motion.p>
        </motion.div>
      </motion.div>
    </div>
  );
}

export default LoginPage;
