import { Link } from 'react-router-dom';
import { ArrowRight, Zap, Shield, Cpu, Github } from 'lucide-react';
import { motion } from 'framer-motion';

function Homepage() {
  const features = [
    {
      icon: Zap,
      title: 'Lightning Fast',
      description: 'AI-powered code generation with millisecond response times',
    },
    {
      icon: Shield,
      title: 'Secure & Private',
      description: 'Your code stays yours. Enterprise-grade encryption guaranteed.',
    },
    {
      icon: Cpu,
      title: 'Advanced AI',
      description: 'State-of-the-art models for intelligent code assistance',
    },
  ];

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.2,
        delayChildren: 0.3,
      },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: { duration: 0.8, ease: 'easeOut' },
    },
  };

  return (
    <div className="min-h-screen pt-20 pb-16">
      {/* Hero Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial="hidden"
          animate="visible"
          variants={containerVariants}
          className="text-center mb-20"
        >
          <motion.div variants={itemVariants}>
            <h1 className="text-5xl md:text-7xl font-bold mb-6 bg-gradient-to-r from-blue-400 via-cyan-400 to-blue-300 bg-clip-text text-transparent leading-tight">
              Code with Intelligence
            </h1>
          </motion.div>

          <motion.p variants={itemVariants} className="text-xl text-slate-400 mb-8 max-w-3xl mx-auto">
            YonocyTech AI is your intelligent coding assistant. Write better code, faster.
            Powered by advanced AI models designed for developers.
          </motion.p>

          <motion.div variants={itemVariants} className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              to="/signup"
              className="inline-flex items-center justify-center px-8 py-4 bg-gradient-to-r from-blue-600 to-cyan-600 text-white font-semibold rounded-lg hover:shadow-lg hover:shadow-blue-500/50 transition-all group"
            >
              Get Started Free
              <ArrowRight className="ml-2 group-hover:translate-x-1 transition-transform" size={20} />
            </Link>
            <a
              href="https://github.com/habibrahmanyonocy786-cmyk"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center justify-center px-8 py-4 bg-slate-800 hover:bg-slate-700 text-white font-semibold rounded-lg transition-colors group"
            >
              <Github className="mr-2" size={20} />
              GitHub
            </a>
          </motion.div>
        </motion.div>

        {/* Features Grid */}
        <motion.div
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true }}
          variants={containerVariants}
          className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-20"
        >
          {features.map((feature, index) => {
            const Icon = feature.icon;
            return (
              <motion.div
                key={index}
                variants={itemVariants}
                className="p-6 rounded-xl bg-gradient-to-br from-slate-800/50 to-slate-900/50 border border-blue-900/30 hover:border-blue-500/50 transition-all hover:shadow-lg hover:shadow-blue-500/10"
              >
                <Icon className="w-12 h-12 mb-4 text-blue-400" />
                <h3 className="text-xl font-semibold mb-2 text-white">{feature.title}</h3>
                <p className="text-slate-400">{feature.description}</p>
              </motion.div>
            );
          })}
        </motion.div>

        {/* Stats Section */}
        <motion.div
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true }}
          variants={containerVariants}
          className="grid grid-cols-1 md:grid-cols-3 gap-8 text-center"
        >
          {[
            { label: 'Active Users', value: '10K+' },
            { label: 'Code Lines Generated', value: '1M+' },
            { label: 'Response Time', value: '<100ms' },
          ].map((stat, index) => (
            <motion.div key={index} variants={itemVariants}>
              <p className="text-3xl font-bold text-blue-400 mb-2">{stat.value}</p>
              <p className="text-slate-400">{stat.label}</p>
            </motion.div>
          ))}
        </motion.div>
      </div>
    </div>
  );
}

export default Homepage;
