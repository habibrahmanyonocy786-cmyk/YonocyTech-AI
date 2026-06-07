import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { useAuthStore } from '../store/authStore';
import { Eye, EyeOff, Mail, Lock, User, Github, ArrowRight } from 'lucide-react';

function SignupPage() {
  const navigate = useNavigate();
  const { signup, loading, error } = useAuthStore();
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
    agreeToTerms: false,
  });
  const [validationErrors, setValidationErrors] = useState({});

  const validateForm = () => {
    const errors = {};

    if (!formData.name.trim()) errors.name = 'Name is required';
    if (!formData.email.match(/^[^\s@]+@[^\s@]+\.[^\s@]+$/)) {
      errors.email = 'Valid email is required';
    }
    if (formData.password.length < 8) {
      errors.password = 'Password must be at least 8 characters';
    }
    if (formData.password !== formData.confirmPassword) {
      errors.confirmPassword = 'Passwords do not match';
    }
    if (!formData.agreeToTerms) {
      errors.agreeToTerms = 'You must agree to the terms';
    }

    return errors;
  };

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
    const errors = validateForm();

    if (Object.keys(errors).length > 0) {
      setValidationErrors(errors);
      return;
    }

    try {
      await signup({
        name: formData.name,
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
        {/* Animated Background Gradient */}
        <div className="absolute inset-0 bg-gradient-to-br from-blue-600/10 via-cyan-600/10 to-slate-900/10 blur-3xl -z-10" />

        <motion.div
          variants={itemVariants}
          className="text-center mb-8"
        >
          <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent mb-2">
            Welcome to YonocyTech
          </h1>
          <p className="text-slate-400">Join thousands of developers using AI-powered coding</p>
        </motion.div>

        <motion.div
          variants={itemVariants}
          className="bg-slate-900/50 backdrop-blur-xl border border-blue-900/30 rounded-2xl p-8 shadow-2xl"
        >
          {/* Social Sign Up */}
          <div className="mb-6">
            <button className="w-full flex items-center justify-center space-x-2 bg-slate-800 hover:bg-slate-700 text-white font-semibold py-3 rounded-lg transition-colors group">
              <Github size={20} />
              <span>Sign up with GitHub</span>
            </button>
          </div>

          <div className="flex items-center gap-4 mb-6">
            <div className="flex-1 h-px bg-blue-900/30" />
            <span className="text-slate-500 text-sm">or</span>
            <div className="flex-1 h-px bg-blue-900/30" />
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-4">
            {/* Name Field */}
            <motion.div variants={itemVariants}>
              <label className="block text-sm font-medium text-slate-300 mb-2">Full Name</label>
              <div className="relative">
                <User className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-500" size={18} />
                <input
                  type="text"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  placeholder="Enter your name"
                  className={`w-full pl-10 pr-4 py-3 bg-slate-800/50 border rounded-lg focus:outline-none transition-all ${
                    validationErrors.name
                      ? 'border-red-500/50 focus:border-red-500'
                      : 'border-blue-900/30 focus:border-blue-500'
                  }`}
                />
              </div>
              {validationErrors.name && (
                <p className="text-red-400 text-sm mt-1">{validationErrors.name}</p>
              )}
            </motion.div>

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
                  placeholder="At least 8 characters"
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

            {/* Confirm Password Field */}
            <motion.div variants={itemVariants}>
              <label className="block text-sm font-medium text-slate-300 mb-2">Confirm Password</label>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-500" size={18} />
                <input
                  type={showConfirmPassword ? 'text' : 'password'}
                  name="confirmPassword"
                  value={formData.confirmPassword}
                  onChange={handleChange}
                  placeholder="Confirm your password"
                  className={`w-full pl-10 pr-12 py-3 bg-slate-800/50 border rounded-lg focus:outline-none transition-all ${
                    validationErrors.confirmPassword
                      ? 'border-red-500/50 focus:border-red-500'
                      : 'border-blue-900/30 focus:border-blue-500'
                  }`}
                />
                <button
                  type="button"
                  onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                  className="absolute right-3 top-1/2 transform -translate-y-1/2 text-slate-500 hover:text-slate-300"
                >
                  {showConfirmPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                </button>
              </div>
              {validationErrors.confirmPassword && (
                <p className="text-red-400 text-sm mt-1">{validationErrors.confirmPassword}</p>
              )}
            </motion.div>

            {/* Terms Checkbox */}
            <motion.div variants={itemVariants}>
              <label className="flex items-center space-x-2 cursor-pointer">
                <input
                  type="checkbox"
                  name="agreeToTerms"
                  checked={formData.agreeToTerms}
                  onChange={handleChange}
                  className="w-4 h-4 rounded border-blue-500 text-blue-600 focus:ring-blue-500"
                />
                <span className="text-sm text-slate-400">
                  I agree to the{' '}
                  <a href="#" className="text-blue-400 hover:text-blue-300">
                    Terms of Service
                  </a>
                  {' '}and{' '}
                  <a href="#" className="text-blue-400 hover:text-blue-300">
                    Privacy Policy
                  </a>
                </span>
              </label>
              {validationErrors.agreeToTerms && (
                <p className="text-red-400 text-sm mt-1">{validationErrors.agreeToTerms}</p>
              )}
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
                <span>Creating Account...</span>
              ) : (
                <>
                  Create Account
                  <ArrowRight className="ml-2 group-hover:translate-x-1 transition-transform" size={18} />
                </>
              )}
            </motion.button>
          </form>

          {/* Login Link */}
          <motion.p variants={itemVariants} className="text-center text-slate-400 mt-6">
            Already have an account?{' '}
            <a href="/login" className="text-blue-400 hover:text-blue-300 font-semibold">
              Sign in
            </a>
          </motion.p>
        </motion.div>
      </motion.div>
    </div>
  );
}

export default SignupPage;
