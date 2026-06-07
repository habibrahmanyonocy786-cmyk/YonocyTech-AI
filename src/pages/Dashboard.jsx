import { motion } from 'framer-motion';
import { useAuthStore } from '../store/authStore';
import { Code2, Zap, Clock, TrendingUp } from 'lucide-react';

function Dashboard() {
  const { user } = useAuthStore();

  const stats = [
    { icon: Code2, label: 'Code Generated', value: '2,847 lines', color: 'from-blue-500 to-cyan-500' },
    { icon: Zap, label: 'Processing Power', value: '94%', color: 'from-purple-500 to-pink-500' },
    { icon: Clock, label: 'Avg Response', value: '87ms', color: 'from-green-500 to-emerald-500' },
    { icon: TrendingUp, label: 'Productivity Boost', value: '3.2x', color: 'from-orange-500 to-red-500' },
  ];

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
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <motion.div
        initial="hidden"
        animate="visible"
        variants={containerVariants}
      >
        <motion.div variants={itemVariants} className="mb-12">
          <h1 className="text-4xl font-bold text-white mb-2">
            Welcome back, {user?.name}! 👋
          </h1>
          <p className="text-slate-400">Here's what's happening with your AI coding assistant today.</p>
        </motion.div>

        {/* Stats Grid */}
        <motion.div
          variants={containerVariants}
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12"
        >
          {stats.map((stat, index) => {
            const Icon = stat.icon;
            return (
              <motion.div
                key={index}
                variants={itemVariants}
                className="p-6 rounded-xl bg-gradient-to-br from-slate-800/50 to-slate-900/50 border border-blue-900/30 hover:border-blue-500/50 transition-all hover:shadow-lg hover:shadow-blue-500/10"
              >
                <div className={`w-12 h-12 rounded-lg bg-gradient-to-br ${stat.color} p-3 mb-4`}>
                  <Icon className="w-full h-full text-white" />
                </div>
                <p className="text-slate-400 text-sm mb-2">{stat.label}</p>
                <p className="text-2xl font-bold text-white">{stat.value}</p>
              </motion.div>
            );
          })}
        </motion.div>

        {/* Recent Activity */}
        <motion.div variants={itemVariants} className="bg-slate-900/50 backdrop-blur-xl border border-blue-900/30 rounded-xl p-8">
          <h2 className="text-2xl font-bold text-white mb-6">Recent Activity</h2>
          <div className="space-y-4">
            {[
              { action: 'Generated React component', time: '2 minutes ago' },
              { action: 'Fixed TypeScript errors', time: '15 minutes ago' },
              { action: 'Optimized database query', time: '1 hour ago' },
              { action: 'Created API endpoint', time: '3 hours ago' },
            ].map((item, index) => (
              <div key={index} className="flex items-center justify-between p-4 rounded-lg bg-slate-800/30 border border-slate-700/30 hover:border-blue-500/30 transition-colors">
                <span className="text-slate-300">{item.action}</span>
                <span className="text-slate-500 text-sm">{item.time}</span>
              </div>
            ))}
          </div>
        </motion.div>
      </motion.div>
    </div>
  );
}

export default Dashboard;
