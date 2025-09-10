import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Plus, Bot, Play, Pause, Settings, Trash2, Clock, CheckCircle, XCircle } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import { agentsAPI } from '../utils/api';
import { Agent } from '../types';
import toast from 'react-hot-toast';

const Dashboard: React.FC = () => {
  const { user } = useAuth();
  const [agents, setAgents] = useState<Agent[]>([]);
  const [loading, setLoading] = useState(true);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [executingAgent, setExecutingAgent] = useState<string | null>(null);

  useEffect(() => {
    fetchAgents();
  }, []);

  const fetchAgents = async () => {
    try {
      const response = await agentsAPI.list();
      setAgents(response.data);
    } catch (error) {
      toast.error('Failed to load agents');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateAgent = async (agentData: {
    name: string;
    description: string;
    type: string;
  }) => {
    try {
      const response = await agentsAPI.create(agentData);
      setAgents([...agents, response.data]);
      setShowCreateModal(false);
      toast.success('Agent created successfully');
    } catch (error) {
      toast.error('Failed to create agent');
    }
  };

  const handleExecuteAgent = async (agentId: string) => {
    setExecutingAgent(agentId);
    try {
      const response = await agentsAPI.execute(agentId, {
        type: 'test',
        data: { message: 'Test execution from dashboard' }
      });
      toast.success('Agent executed successfully');
      await fetchAgents(); // Refresh to get updated execution count
    } catch (error) {
      toast.error('Failed to execute agent');
    } finally {
      setExecutingAgent(null);
    }
  };

  const handleDeleteAgent = async (agentId: string) => {
    if (window.confirm('Are you sure you want to delete this agent?')) {
      try {
        await agentsAPI.delete(agentId);
        setAgents(agents.filter(agent => agent.id !== agentId));
        toast.success('Agent deleted successfully');
      } catch (error) {
        toast.error('Failed to delete agent');
      }
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'text-green-400';
      case 'inactive': return 'text-aether-gray-400';
      case 'error': return 'text-red-400';
      default: return 'text-aether-gray-400';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'active': return <CheckCircle className="h-4 w-4 text-green-400" />;
      case 'error': return <XCircle className="h-4 w-4 text-red-400" />;
      default: return <Clock className="h-4 w-4 text-aether-gray-400" />;
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-aether-blue"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-aether-dark py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <motion.div
          className="mb-8"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-white">
                Welcome back, {user?.full_name || user?.email}
              </h1>
              <p className="text-aether-gray-300 mt-1">
                Manage your AI agents and monitor their performance
              </p>
            </div>
            <button
              onClick={() => setShowCreateModal(true)}
              className="btn-primary flex items-center space-x-2"
            >
              <Plus className="h-5 w-5" />
              <span>Create Agent</span>
            </button>
          </div>
        </motion.div>

        {/* Stats */}
        <motion.div
          className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1, duration: 0.6 }}
        >
          <div className="card">
            <div className="flex items-center">
              <Bot className="h-8 w-8 text-aether-blue" />
              <div className="ml-4">
                <div className="text-2xl font-bold text-white">{agents.length}</div>
                <div className="text-aether-gray-300 text-sm">Total Agents</div>
              </div>
            </div>
          </div>
          
          <div className="card">
            <div className="flex items-center">
              <CheckCircle className="h-8 w-8 text-green-400" />
              <div className="ml-4">
                <div className="text-2xl font-bold text-white">
                  {agents.filter(a => a.status === 'active').length}
                </div>
                <div className="text-aether-gray-300 text-sm">Active Agents</div>
              </div>
            </div>
          </div>
          
          <div className="card">
            <div className="flex items-center">
              <Play className="h-8 w-8 text-aether-purple" />
              <div className="ml-4">
                <div className="text-2xl font-bold text-white">
                  {agents.reduce((sum, agent) => sum + agent.execution_count, 0)}
                </div>
                <div className="text-aether-gray-300 text-sm">Total Executions</div>
              </div>
            </div>
          </div>
          
          <div className="card">
            <div className="flex items-center">
              <Clock className="h-8 w-8 text-aether-blue" />
              <div className="ml-4">
                <div className="text-2xl font-bold text-white">500</div>
                <div className="text-aether-gray-300 text-sm">Tasks Remaining</div>
              </div>
            </div>
          </div>
        </motion.div>

        {/* Agents Grid */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2, duration: 0.6 }}
        >
          <h2 className="text-xl font-semibold text-white mb-6">Your Agents</h2>
          
          {agents.length === 0 ? (
            <div className="card text-center py-12">
              <Bot className="h-16 w-16 text-aether-gray-600 mx-auto mb-4" />
              <h3 className="text-xl font-semibold text-white mb-2">No agents yet</h3>
              <p className="text-aether-gray-300 mb-6">
                Create your first AI agent to get started with automation
              </p>
              <button
                onClick={() => setShowCreateModal(true)}
                className="btn-primary"
              >
                Create Your First Agent
              </button>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {agents.map((agent) => (
                <motion.div
                  key={agent.id}
                  className="card hover:border-aether-blue/50 transition-all duration-200"
                  whileHover={{ scale: 1.02 }}
                >
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex items-center space-x-3">
                      <div className="w-10 h-10 bg-gradient-to-r from-aether-blue to-aether-purple rounded-lg flex items-center justify-center">
                        <Bot className="h-5 w-5 text-white" />
                      </div>
                      <div>
                        <h3 className="font-semibold text-white">{agent.name}</h3>
                        <div className="flex items-center space-x-1">
                          {getStatusIcon(agent.status)}
                          <span className={`text-sm ${getStatusColor(agent.status)}`}>
                            {agent.status}
                          </span>
                        </div>
                      </div>
                    </div>
                    <div className="flex space-x-1">
                      <button className="p-1 text-aether-gray-400 hover:text-white">
                        <Settings className="h-4 w-4" />
                      </button>
                      <button
                        onClick={() => handleDeleteAgent(agent.id)}
                        className="p-1 text-aether-gray-400 hover:text-red-400"
                      >
                        <Trash2 className="h-4 w-4" />
                      </button>
                    </div>
                  </div>

                  <p className="text-aether-gray-300 text-sm mb-4">
                    {agent.description || 'No description provided'}
                  </p>

                  <div className="flex items-center justify-between text-sm text-aether-gray-400 mb-4">
                    <span>Type: {agent.type}</span>
                    <span>Executions: {agent.execution_count}</span>
                  </div>

                  <button
                    onClick={() => handleExecuteAgent(agent.id)}
                    disabled={executingAgent === agent.id}
                    className="w-full btn-primary text-sm disabled:opacity-50"
                  >
                    {executingAgent === agent.id ? 'Executing...' : 'Execute Agent'}
                  </button>
                </motion.div>
              ))}
            </div>
          )}
        </motion.div>
      </div>

      {/* Create Agent Modal */}
      {showCreateModal && (
        <CreateAgentModal
          onClose={() => setShowCreateModal(false)}
          onCreate={handleCreateAgent}
        />
      )}
    </div>
  );
};

const CreateAgentModal: React.FC<{
  onClose: () => void;
  onCreate: (data: { name: string; description: string; type: string }) => void;
}> = ({ onClose, onCreate }) => {
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [type, setType] = useState('workflow');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onCreate({ name, description, type });
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <motion.div
        className="bg-aether-gray-800 rounded-lg p-6 w-full max-w-md mx-4"
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.3 }}
      >
        <h3 className="text-xl font-semibold text-white mb-4">Create New Agent</h3>
        
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-aether-gray-300 mb-1">
              Agent Name
            </label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="input-field"
              placeholder="My AI Agent"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-aether-gray-300 mb-1">
              Description
            </label>
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="input-field h-20 resize-none"
              placeholder="Describe what this agent does..."
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-aether-gray-300 mb-1">
              Agent Type
            </label>
            <select
              value={type}
              onChange={(e) => setType(e.target.value)}
              className="input-field"
            >
              <option value="workflow">Workflow Agent</option>
              <option value="customer_support">Customer Support</option>
              <option value="coding">Coding Assistant</option>
              <option value="data_analysis">Data Analysis</option>
              <option value="content_creation">Content Creation</option>
            </select>
          </div>

          <div className="flex space-x-3 pt-4">
            <button type="button" onClick={onClose} className="btn-secondary flex-1">
              Cancel
            </button>
            <button type="submit" className="btn-primary flex-1">
              Create Agent
            </button>
          </div>
        </form>
      </motion.div>
    </div>
  );
};

export default Dashboard;