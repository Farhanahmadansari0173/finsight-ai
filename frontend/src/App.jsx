import { useState, useEffect } from "react"
import axios from "axios"
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer, BarChart, Bar, XAxis, YAxis } from "recharts"
import { MessageCircle, TrendingUp, AlertTriangle, List, Send, Bot, User } from "lucide-react"

const API = "https://finsight-ai-backend-vris.onrender.com"

const COLORS = ["#6366f1", "#22c55e", "#f59e0b", "#ef4444", "#3b82f6", "#ec4899", "#14b8a6"]

export default function App() {
  const [messages, setMessages] = useState([
    { role: "bot", text: "👋 Hi! I'm FinSight AI, your personal finance agent. Ask me anything about your spending!" }
  ])
  const [input, setInput] = useState("")
  const [loading, setLoading] = useState(false)
  const [activeTab, setActiveTab] = useState("chat")
  const [summary, setSummary] = useState([])
  const [transactions, setTransactions] = useState([])
  const [anomalies, setAnomalies] = useState("")
  const [forecast, setForecast] = useState("")

  useEffect(() => {
    axios.get(`${API}/summary`).then(r => setSummary(r.data.spending_by_category))
    axios.get(`${API}/transactions`).then(r => setTransactions(r.data.transactions))
    axios.get(`${API}/anomalies`).then(r => setAnomalies(r.data.anomalies))
    axios.get(`${API}/forecast`).then(r => setForecast(r.data.forecast))
  }, [])

  const sendMessage = async () => {
    if (!input.trim()) return
    const question = input
    setInput("")
    setMessages(prev => [...prev, { role: "user", text: question }])
    setLoading(true)
    try {
      const res = await axios.post(`${API}/ask`, { question })
      setMessages(prev => [...prev, { role: "bot", text: res.data.answer }])
    } catch {
      setMessages(prev => [...prev, { role: "bot", text: "Sorry, something went wrong. Please try again." }])
    }
    setLoading(false)
  }

  return (
    <div className="min-h-screen bg-gray-950 text-white">
      {/* Header */}
      <div className="bg-gray-900 border-b border-gray-800 px-6 py-4 flex items-center gap-3">
        <div className="w-10 h-10 bg-indigo-600 rounded-xl flex items-center justify-center">
          <TrendingUp size={20} />
        </div>
        <div>
          <h1 className="text-xl font-bold">FinSight AI</h1>
          <p className="text-xs text-gray-400">Personal Finance Agent • Powered by MongoDB + LLaMA</p>
        </div>
        <div className="ml-auto flex items-center gap-2">
          <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
          <span className="text-xs text-gray-400">Live</span>
        </div>
      </div>

      {/* Tabs */}
      <div className="bg-gray-900 border-b border-gray-800 px-6 flex gap-1">
        {[
          { id: "chat", icon: <MessageCircle size={16} />, label: "Chat" },
          { id: "dashboard", icon: <TrendingUp size={16} />, label: "Dashboard" },
          { id: "anomalies", icon: <AlertTriangle size={16} />, label: "Anomalies" },
          { id: "transactions", icon: <List size={16} />, label: "Transactions" },
        ].map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`flex items-center gap-2 px-4 py-3 text-sm border-b-2 transition-colors ${
              activeTab === tab.id
                ? "border-indigo-500 text-indigo-400"
                : "border-transparent text-gray-400 hover:text-gray-200"
            }`}
          >
            {tab.icon}{tab.label}
          </button>
        ))}
      </div>

      <div className="max-w-6xl mx-auto p-6">
        {/* Chat Tab */}
        {activeTab === "chat" && (
          <div className="flex flex-col h-[70vh]">
            <div className="flex-1 overflow-y-auto space-y-4 mb-4">
              {messages.map((msg, i) => (
                <div key={i} className={`flex gap-3 ${msg.role === "user" ? "flex-row-reverse" : ""}`}>
                  <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${
                    msg.role === "bot" ? "bg-indigo-600" : "bg-gray-700"
                  }`}>
                    {msg.role === "bot" ? <Bot size={16} /> : <User size={16} />}
                  </div>
                  <div className={`max-w-2xl px-4 py-3 rounded-2xl text-sm whitespace-pre-wrap ${
                    msg.role === "bot"
                      ? "bg-gray-800 text-gray-100"
                      : "bg-indigo-600 text-white"
                  }`}>
                    {msg.text}
                  </div>
                </div>
              ))}
              {loading && (
                <div className="flex gap-3">
                  <div className="w-8 h-8 bg-indigo-600 rounded-full flex items-center justify-center">
                    <Bot size={16} />
                  </div>
                  <div className="bg-gray-800 px-4 py-3 rounded-2xl">
                    <div className="flex gap-1">
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay:"0.1s"}}></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay:"0.2s"}}></div>
                    </div>
                  </div>
                </div>
              )}
            </div>
            <div className="flex gap-3">
              <input
                value={input}
                onChange={e => setInput(e.target.value)}
                onKeyDown={e => e.key === "Enter" && sendMessage()}
                placeholder="Ask about your finances..."
                className="flex-1 bg-gray-800 border border-gray-700 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-indigo-500"
              />
              <button
                onClick={sendMessage}
                className="bg-indigo-600 hover:bg-indigo-700 px-4 py-3 rounded-xl transition-colors"
              >
                <Send size={18} />
              </button>
            </div>
          </div>
        )}

        {/* Dashboard Tab */}
        {activeTab === "dashboard" && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-gray-900 rounded-2xl p-6 border border-gray-800">
              <h2 className="text-lg font-semibold mb-4">Spending by Category</h2>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie data={summary} dataKey="total" nameKey="category" cx="50%" cy="50%" outerRadius={100} label={({category}) => category}>
                    {summary.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
                  </Pie>
                  <Tooltip formatter={(v) => `₹${v}`} />
                </PieChart>
              </ResponsiveContainer>
            </div>
            <div className="bg-gray-900 rounded-2xl p-6 border border-gray-800">
              <h2 className="text-lg font-semibold mb-4">Category Breakdown</h2>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={summary}>
                  <XAxis dataKey="category" tick={{fontSize:11}} />
                  <YAxis tick={{fontSize:11}} />
                  <Tooltip formatter={(v) => `₹${v}`} />
                  <Bar dataKey="total" fill="#6366f1" radius={[4,4,0,0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
            <div className="bg-gray-900 rounded-2xl p-6 border border-gray-800 md:col-span-2">
              <h2 className="text-lg font-semibold mb-4">📈 Forecast</h2>
              <p className="text-gray-300 text-sm whitespace-pre-wrap">{forecast}</p>
            </div>
          </div>
        )}

        {/* Anomalies Tab */}
        {activeTab === "anomalies" && (
          <div className="bg-gray-900 rounded-2xl p-6 border border-gray-800">
            <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
              <AlertTriangle size={20} className="text-yellow-500" /> Detected Anomalies
            </h2>
            <p className="text-gray-300 text-sm whitespace-pre-wrap">{anomalies}</p>
          </div>
        )}

        {/* Transactions Tab */}
        {activeTab === "transactions" && (
          <div className="bg-gray-900 rounded-2xl border border-gray-800 overflow-hidden">
            <table className="w-full text-sm">
              <thead className="bg-gray-800">
                <tr>
                  <th className="text-left px-4 py-3 text-gray-400">Description</th>
                  <th className="text-left px-4 py-3 text-gray-400">Category</th>
                  <th className="text-left px-4 py-3 text-gray-400">Date</th>
                  <th className="text-right px-4 py-3 text-gray-400">Amount</th>
                </tr>
              </thead>
              <tbody>
                {transactions.map((t, i) => (
                  <tr key={i} className="border-t border-gray-800 hover:bg-gray-800 transition-colors">
                    <td className="px-4 py-3">{t.description}</td>
                    <td className="px-4 py-3">
                      <span className="bg-gray-700 px-2 py-1 rounded-full text-xs">{t.category}</span>
                    </td>
                    <td className="px-4 py-3 text-gray-400">{t.date}</td>
                    <td className={`px-4 py-3 text-right font-medium ${t.amount > 0 ? "text-green-400" : "text-red-400"}`}>
                      {t.amount > 0 ? "+" : ""}₹{Math.abs(t.amount)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  )
}