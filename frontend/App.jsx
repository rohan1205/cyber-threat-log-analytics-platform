import { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { AreaChart, Area, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';

const API_URL = import.meta.env.VITE_API_URL || 'https://cyber-threat-log-analytics-platform.onrender.com';

function App() {
  const [alerts, setAlerts] = useState([]);
  const [logs, setLogs] = useState([]);
  const [severityCounts, setSeverityCounts] = useState([]);
  const [timeSeriesData, setTimeSeriesData] = useState([]);
  const [topThreats, setTopThreats] = useState([]);
  const [token, setToken] = useState(localStorage.getItem('token') || '');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLoggedIn, setIsLoggedIn] = useState(!!token);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('dashboard');
  const [attackType, setAttackType] = useState('dos');
  const consoleRef = useRef(null);

  // Fetch alerts from Supabase/PostgreSQL
  const fetchAlerts = async () => {
    if (!token) return;
    
    try {
      const response = await fetch(`${API_URL}/alerts`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      
      if (response.ok) {
        const data = await response.json();
        setAlerts(data);
      }
    } catch (error) {
      console.error('Error fetching alerts:', error);
    }
  };

  // Fetch logs
  const fetchLogs = async () => {
    if (!token) return;
    
    try {
      const response = await fetch(`${API_URL}/logs`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      
      if (response.ok) {
        const data = await response.json();
        setLogs(data);
      }
    } catch (error) {
      console.error('Error fetching logs:', error);
    }
  };

  // Fetch severity counts
  const fetchSeverityCounts = async () => {
    if (!token) return;
    
    try {
      const response = await fetch(`${API_URL}/analytics/severity-count`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      
      if (response.ok) {
        const data = await response.json();
        setSeverityCounts(data);
      }
    } catch (error) {
      console.error('Error fetching severity counts:', error);
    }
  };

  // Fetch time series data
  const fetchTimeSeries = async () => {
    if (!token) return;
    
    try {
      const response = await fetch(`${API_URL}/analytics/time-series?hours=24`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      
      if (response.ok) {
        const data = await response.json();
        setTimeSeriesData(data.map(item => ({
          time: new Date(item._id).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' }),
          count: item.count,
          avgScore: Math.round(item.avg_score || 0)
        })));
      }
    } catch (error) {
      console.error('Error fetching time series:', error);
    }
  };

  // Fetch top threats
  const fetchTopThreats = async () => {
    if (!token) return;
    
    try {
      const response = await fetch(`${API_URL}/analytics/top-threats?limit=10`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      
      if (response.ok) {
        const data = await response.json();
        setTopThreats(data);
      }
    } catch (error) {
      console.error('Error fetching top threats:', error);
    }
  };

  // Login function
  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      // First try to login
      const loginResponse = await fetch(`${API_URL}/auth/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });

      if (loginResponse.ok) {
        const data = await loginResponse.json();
        const newToken = data.access_token;
        setToken(newToken);
        localStorage.setItem('token', newToken);
        setIsLoggedIn(true);
        setLoading(false);
        fetchAllData();
        return;
      }

      // If login fails (401), try to register
      let errorData;
      try {
        errorData = await loginResponse.json();
      } catch {
        errorData = { detail: 'Invalid credentials' };
      }
      console.log('Login failed:', errorData);
      
      // Try to register
      const registerResponse = await fetch(`${API_URL}/auth/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });

      if (registerResponse.ok) {
        // Registration successful, now try to login
        const loginResponse2 = await fetch(`${API_URL}/auth/auth/login`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, password })
        });

        if (loginResponse2.ok) {
          const data = await loginResponse2.json();
          const newToken = data.access_token;
          setToken(newToken);
          localStorage.setItem('token', newToken);
          setIsLoggedIn(true);
          setLoading(false);
          fetchAllData();
        } else {
          const errorData2 = await loginResponse2.json().catch(() => ({ detail: 'Login after registration failed' }));
          alert(`Registration successful but login failed: ${errorData2.detail || 'Unknown error'}`);
          setLoading(false);
        }
      } else {
        // Registration failed
        let regErrorData;
        try {
          regErrorData = await registerResponse.json();
        } catch {
          regErrorData = { detail: 'Registration failed - unable to parse response' };
        }
        console.log('Registration failed:', regErrorData, 'Status:', registerResponse.status);
        
        if (registerResponse.status === 400 && regErrorData.detail?.includes('already exists')) {
          // User already exists, but login failed - wrong password?
          alert('User already exists. Please check your password or try a different email.');
        } else {
          alert(`Registration failed (Status ${registerResponse.status}): ${regErrorData.detail || 'Unknown error'}\n\nBackend URL: ${API_URL}\n\nCheck browser console (F12) for more details.`);
        }
        setLoading(false);
      }
    } catch (error) {
      console.error('Error:', error);
      alert(`Network error: ${error.message}\n\nMake sure the backend is running at ${API_URL}`);
      setLoading(false);
    }
  };

  const fetchAllData = () => {
    fetchAlerts();
    fetchLogs();
    fetchSeverityCounts();
    fetchTimeSeries();
    fetchTopThreats();
  };

  // Simulate Attack function - CRITICAL: Sends JWT token
  const simulateAttack = async () => {
    if (!token) {
      alert('Please login first');
      return;
    }

    setLoading(true);
    
    let attackLogs = [];
    
    switch(attackType) {
      case 'dos':
        // DoS Attack: >10 logs from one IP in 10 seconds
        attackLogs = Array.from({ length: 12 }, () => ({
          event: 'Connection Request',
          source_ip: '192.168.1.100',
          destination_port: 80
        }));
        break;
      case 'portscan':
        // Port Scan: One IP hitting 5+ different ports in 1 minute
        attackLogs = [80, 443, 22, 3389, 3306, 5432, 8080, 9090].map(port => ({
          event: 'Port Connection Attempt',
          source_ip: '10.0.0.50',
          destination_port: port
        }));
        break;
      case 'bruteforce':
        // Brute Force: 3+ 'Failed Login' events
        attackLogs = Array.from({ length: 5 }, () => ({
          event: 'Failed Login Attempt',
          source_ip: '172.16.0.25',
          destination_port: 22
        }));
        break;
      case 'mixed':
        attackLogs = [
          ...Array.from({ length: 5 }, () => ({ event: 'Failed Login Attempt', source_ip: '192.168.1.50', destination_port: 22 })),
          ...Array.from({ length: 8 }, () => ({ event: 'Connection Request', source_ip: '10.0.0.100', destination_port: 80 })),
          ...Array.from({ length: 6 }, () => ({ event: 'Port Connection Attempt', source_ip: '172.16.0.75', destination_port: null })).map((log, i) => ({
            ...log,
            destination_port: [443, 22, 3389, 3306, 5432, 8080][i]
          }))
        ];
        break;
    }

    try {
      for (const log of attackLogs) {
        const response = await fetch(`${API_URL}/logs`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify(log)
        });

        if (response.ok) {
          const result = await response.json();
          addConsoleLog(`[${new Date().toLocaleTimeString()}] ${log.event} from ${log.source_ip} - Score: ${result.analysis?.score || 0}`);
        }
        
        await new Promise(resolve => setTimeout(resolve, 300));
      }

      await fetchAllData();
      addConsoleLog(`[${new Date().toLocaleTimeString()}] Attack simulation completed. ${attackLogs.length} logs sent.`);
    } catch (error) {
      console.error('Error simulating attack:', error);
      addConsoleLog(`[${new Date().toLocaleTimeString()}] ERROR: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const consoleLogs = useRef([]);
  
  const addConsoleLog = (message) => {
    consoleLogs.current = [...consoleLogs.current.slice(-49), message];
    if (consoleRef.current) {
      consoleRef.current.scrollTop = consoleRef.current.scrollHeight;
    }
  };

  useEffect(() => {
    if (isLoggedIn && token) {
      fetchAllData();
      
      const interval = setInterval(() => {
        fetchAlerts();
        fetchLogs();
        fetchTimeSeries();
      }, 5000);
      
      return () => clearInterval(interval);
    }
  }, [isLoggedIn, token]);

  if (!isLoggedIn) {
    return (
      <div className="min-h-screen bg-cyber-dark flex items-center justify-center p-4">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="glass rounded-2xl p-8 w-full max-w-md"
        >
          <h1 className="text-3xl font-bold mb-2 bg-gradient-to-r from-cyber-cyan to-cyber-neon bg-clip-text text-transparent">
            Cyber Threat Command Center
          </h1>
          <p className="text-gray-400 mb-6">Enter your credentials to access</p>
          <form onSubmit={handleLogin}>
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-300 mb-2">Email</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                className="w-full px-4 py-3 bg-black/30 border border-white/10 rounded-lg focus:outline-none focus:ring-2 focus:ring-cyber-cyan text-white"
                placeholder="user@example.com"
              />
            </div>
            <div className="mb-6">
              <label className="block text-sm font-medium text-gray-300 mb-2">Password</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className="w-full px-4 py-3 bg-black/30 border border-white/10 rounded-lg focus:outline-none focus:ring-2 focus:ring-cyber-cyan text-white"
                placeholder="••••••••"
              />
            </div>
            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 bg-gradient-to-r from-cyber-blue to-cyber-purple rounded-lg font-semibold hover:opacity-90 transition-opacity disabled:opacity-50"
            >
              {loading ? 'Loading...' : 'Login / Register'}
            </button>
          </form>
        </motion.div>
      </div>
    );
  }

  const severityColors = {
    CRITICAL: 'text-red-400 glow-red',
    HIGH: 'text-orange-400',
    MEDIUM: 'text-yellow-400',
    LOW: 'text-green-400',
    UNKNOWN: 'text-gray-400'
  };

  const severityBgColors = {
    CRITICAL: 'bg-red-500/20 border-red-500/50',
    HIGH: 'bg-orange-500/20 border-orange-500/50',
    MEDIUM: 'bg-yellow-500/20 border-yellow-500/50',
    LOW: 'bg-green-500/20 border-green-500/50',
    UNKNOWN: 'bg-gray-500/20 border-gray-500/50'
  };

  return (
    <div className="min-h-screen bg-cyber-dark flex">
      {/* Command Sidebar */}
      <motion.div
        initial={{ x: -300 }}
        animate={{ x: 0 }}
        className="w-64 glass-dark p-4 flex flex-col"
      >
        <div className="mb-8">
          <h1 className="text-xl font-bold bg-gradient-to-r from-cyber-cyan to-cyber-neon bg-clip-text text-transparent">
            🛡️ Command Center
          </h1>
          <p className="text-xs text-gray-400 mt-1">v2.0.0</p>
        </div>

        <nav className="flex-1 space-y-2">
          <button
            onClick={() => setActiveTab('dashboard')}
            className={`w-full text-left px-4 py-3 rounded-lg transition-all ${
              activeTab === 'dashboard'
                ? 'bg-cyber-blue/30 border border-cyber-blue/50 text-white'
                : 'text-gray-400 hover:bg-white/5 hover:text-white'
            }`}
          >
            📊 Dashboard
          </button>
          <button
            onClick={() => setActiveTab('threats')}
            className={`w-full text-left px-4 py-3 rounded-lg transition-all ${
              activeTab === 'threats'
                ? 'bg-cyber-blue/30 border border-cyber-blue/50 text-white'
                : 'text-gray-400 hover:bg-white/5 hover:text-white'
            }`}
          >
            ⚠️ Top Threats
          </button>
          <button
            onClick={() => setActiveTab('console')}
            className={`w-full text-left px-4 py-3 rounded-lg transition-all ${
              activeTab === 'console'
                ? 'bg-cyber-blue/30 border border-cyber-blue/50 text-white'
                : 'text-gray-400 hover:bg-white/5 hover:text-white'
            }`}
          >
            💻 Live Console
          </button>
        </nav>

        <div className="mt-auto space-y-4">
          <div className="glass rounded-lg p-4">
            <label className="block text-sm font-medium text-gray-300 mb-2">Simulate Attack</label>
            <select
              value={attackType}
              onChange={(e) => setAttackType(e.target.value)}
              className="w-full px-3 py-2 bg-black/30 border border-white/10 rounded-lg text-white text-sm mb-2"
            >
              <option value="dos">DoS Attack</option>
              <option value="portscan">Port Scan</option>
              <option value="bruteforce">Brute Force</option>
              <option value="mixed">Mixed Attack</option>
            </select>
            <button
              onClick={simulateAttack}
              disabled={loading}
              className="w-full py-2 bg-red-600 hover:bg-red-700 rounded-lg font-semibold text-sm transition-colors disabled:opacity-50 disabled:cursor-not-allowed glow-red"
            >
              {loading ? '⚡ Simulating...' : '🔥 Launch Attack'}
            </button>
          </div>

          <button
            onClick={() => {
              localStorage.removeItem('token');
              setToken('');
              setIsLoggedIn(false);
            }}
            className="w-full py-2 bg-gray-700 hover:bg-gray-600 rounded-lg font-semibold text-sm transition-colors"
          >
            🚪 Logout
          </button>
        </div>
      </motion.div>

      {/* Main Content */}
      <div className="flex-1 overflow-y-auto">
        {/* Alert Ticker */}
        {alerts.length > 0 && (
          <motion.div
            initial={{ y: -100 }}
            animate={{ y: 0 }}
            className="bg-red-900/30 border-b border-red-500/50 p-4"
          >
            <div className="flex items-center space-x-4 overflow-x-auto">
              <span className="text-red-400 font-bold whitespace-nowrap">🚨 CRITICAL ALERTS:</span>
              <div className="flex space-x-4">
                {alerts.slice(0, 5).map((alert, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    className="glass-dark rounded-lg px-4 py-2 whitespace-nowrap border border-red-500/30"
                  >
                    <span className="text-red-400 font-semibold">{alert.alert_type}</span>
                    <span className="text-gray-400 ml-2">from {alert.source_ip}</span>
                  </motion.div>
                ))}
              </div>
            </div>
          </motion.div>
        )}

        <div className="p-6 space-y-6">
          {/* Dashboard Tab */}
          {activeTab === 'dashboard' && (
            <>
              {/* Stats Cards */}
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                {severityCounts.map((item, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: index * 0.1 }}
                    className={`glass rounded-xl p-6 ${severityBgColors[item._id] || severityBgColors.UNKNOWN}`}
                  >
                    <div className="text-sm text-gray-400 mb-2">{item._id || 'UNKNOWN'}</div>
                    <div className={`text-4xl font-bold ${severityColors[item._id] || severityColors.UNKNOWN}`}>
                      {item.count}
                    </div>
                  </motion.div>
                ))}
              </div>

              {/* Time Series Chart */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="glass rounded-xl p-6"
              >
                <h2 className="text-xl font-bold mb-4 text-white">Traffic Over Time (24h)</h2>
                <ResponsiveContainer width="100%" height={300}>
                  <AreaChart data={timeSeriesData}>
                    <defs>
                      <linearGradient id="colorCount" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#06b6d4" stopOpacity={0.8}/>
                        <stop offset="95%" stopColor="#06b6d4" stopOpacity={0}/>
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                    <XAxis dataKey="time" stroke="#9ca3af" />
                    <YAxis stroke="#9ca3af" />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: '#1a1f3a',
                        border: '1px solid rgba(255, 255, 255, 0.1)',
                        borderRadius: '8px',
                        color: '#fff'
                      }}
                    />
                    <Area
                      type="monotone"
                      dataKey="count"
                      stroke="#06b6d4"
                      fillOpacity={1}
                      fill="url(#colorCount)"
                    />
                  </AreaChart>
                </ResponsiveContainer>
              </motion.div>

              {/* Severity Distribution */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="glass rounded-xl p-6"
              >
                <h2 className="text-xl font-bold mb-4 text-white">Severity Distribution</h2>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={severityCounts}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                    <XAxis dataKey="_id" stroke="#9ca3af" />
                    <YAxis stroke="#9ca3af" />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: '#1a1f3a',
                        border: '1px solid rgba(255, 255, 255, 0.1)',
                        borderRadius: '8px',
                        color: '#fff'
                      }}
                    />
                    <Bar dataKey="count" fill="#2563eb" radius={[8, 8, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </motion.div>

              {/* Recent Alerts */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="glass rounded-xl p-6"
              >
                <h2 className="text-xl font-bold mb-4 text-white">Recent Alerts</h2>
                <div className="space-y-3 max-h-96 overflow-y-auto">
                  <AnimatePresence>
                    {alerts.slice(0, 10).map((alert, index) => (
                      <motion.div
                        key={index}
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        exit={{ opacity: 0, x: 20 }}
                        className={`glass-dark rounded-lg p-4 border ${severityBgColors[alert.severity] || severityBgColors.UNKNOWN}`}
                      >
                        <div className="flex items-center justify-between">
                          <div>
                            <div className="flex items-center space-x-2">
                              <span className={`font-bold ${severityColors[alert.severity] || severityColors.UNKNOWN}`}>
                                {alert.alert_type}
                              </span>
                              <span className="text-xs text-gray-400">{alert.severity}</span>
                            </div>
                            <p className="text-sm text-gray-300 mt-1">{alert.description}</p>
                            <p className="text-xs text-gray-500 mt-1">
                              {alert.source_ip} • {new Date(alert.created_at).toLocaleString()}
                            </p>
                          </div>
                        </div>
                      </motion.div>
                    ))}
                  </AnimatePresence>
                  {alerts.length === 0 && (
                    <div className="text-center text-gray-400 py-8">No alerts detected</div>
                  )}
                </div>
              </motion.div>
            </>
          )}

          {/* Top Threats Tab */}
          {activeTab === 'threats' && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="glass rounded-xl p-6"
            >
              <h2 className="text-2xl font-bold mb-6 text-white">Top Security Threats</h2>
              <div className="space-y-4">
                <AnimatePresence>
                  {topThreats.map((threat, index) => (
                    <motion.div
                      key={index}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: index * 0.1 }}
                      className={`glass-dark rounded-lg p-5 border ${severityBgColors[threat.severity] || severityBgColors.UNKNOWN}`}
                    >
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <div className="flex items-center space-x-3 mb-2">
                            <span className={`text-lg font-bold ${severityColors[threat.severity] || severityColors.UNKNOWN}`}>
                              {threat.event}
                            </span>
                            <span className={`px-3 py-1 rounded-full text-xs font-semibold ${severityBgColors[threat.severity] || severityBgColors.UNKNOWN} ${severityColors[threat.severity] || severityColors.UNKNOWN}`}>
                              {threat.severity}
                            </span>
                            <span className="text-cyber-cyan font-bold">Score: {threat.score}</span>
                          </div>
                          <p className="text-gray-300 text-sm mb-2">Source: {threat.source_ip}</p>
                          {threat.reasons && threat.reasons.length > 0 && (
                            <div className="flex flex-wrap gap-2 mt-2">
                              {threat.reasons.map((reason, i) => (
                                <span key={i} className="px-2 py-1 bg-cyber-blue/20 text-cyber-cyan text-xs rounded">
                                  {reason}
                                </span>
                              ))}
                            </div>
                          )}
                          <p className="text-xs text-gray-500 mt-2">
                            {new Date(threat.timestamp).toLocaleString()}
                          </p>
                        </div>
                      </div>
                    </motion.div>
                  ))}
                </AnimatePresence>
                {topThreats.length === 0 && (
                  <div className="text-center text-gray-400 py-12">No high-priority threats detected</div>
                )}
              </div>
            </motion.div>
          )}

          {/* Live Console Tab */}
          {activeTab === 'console' && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="glass rounded-xl p-6"
            >
              <h2 className="text-2xl font-bold mb-4 text-white">Live System Console</h2>
              <div
                ref={consoleRef}
                className="bg-black/40 rounded-lg p-4 font-mono text-sm h-96 overflow-y-auto border border-cyber-neon/30"
                style={{ scrollbarWidth: 'thin' }}
              >
                {consoleLogs.current.length === 0 ? (
                  <div className="text-cyber-neon">[System Ready] Waiting for events...</div>
                ) : (
                  consoleLogs.current.map((log, index) => (
                    <div key={index} className="text-cyber-neon mb-1">
                      {log}
                    </div>
                  ))
                )}
              </div>
              
              {/* Recent Logs Table */}
              <div className="mt-6">
                <h3 className="text-lg font-bold mb-4 text-white">Recent Logs</h3>
                <div className="glass-dark rounded-lg overflow-hidden">
                  <div className="max-h-96 overflow-y-auto">
                    <table className="w-full">
                      <thead className="bg-black/30 sticky top-0">
                        <tr>
                          <th className="px-4 py-3 text-left text-xs font-semibold text-gray-400 uppercase">Time</th>
                          <th className="px-4 py-3 text-left text-xs font-semibold text-gray-400 uppercase">Event</th>
                          <th className="px-4 py-3 text-left text-xs font-semibold text-gray-400 uppercase">Source IP</th>
                          <th className="px-4 py-3 text-left text-xs font-semibold text-gray-400 uppercase">Severity</th>
                          <th className="px-4 py-3 text-left text-xs font-semibold text-gray-400 uppercase">Score</th>
                        </tr>
                      </thead>
                      <tbody>
                        <AnimatePresence>
                          {logs.slice(0, 50).map((log, index) => (
                            <motion.tr
                              key={index}
                              initial={{ opacity: 0 }}
                              animate={{ opacity: 1 }}
                              className="border-t border-white/5 hover:bg-white/5"
                            >
                              <td className="px-4 py-3 text-sm text-gray-400">
                                {log.timestamp ? new Date(log.timestamp).toLocaleTimeString() : 'N/A'}
                              </td>
                              <td className="px-4 py-3 text-sm text-white">{log.event}</td>
                              <td className="px-4 py-3 text-sm text-cyber-cyan">{log.source_ip}</td>
                              <td className="px-4 py-3">
                                <span className={`px-2 py-1 rounded text-xs font-semibold ${severityColors[log.severity] || severityColors.UNKNOWN}`}>
                                  {log.severity}
                                </span>
                              </td>
                              <td className="px-4 py-3 text-sm text-white">{log.score || 0}</td>
                            </motion.tr>
                          ))}
                        </AnimatePresence>
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            </motion.div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
