const express = require('express')
const { createProxyMiddleware } = require('http-proxy-middleware')
const cors = require('cors')
const path = require('path')
const app = express()
const PORT = process.env.PORT || 3000

// Allow requests from dev frontend, and parse JSON
app.use(cors())
app.use(express.json())

// Proxy /api to the Python Flask backend running on port 5000
const PY_TARGET = process.env.PY_TARGET || 'http://127.0.0.1:5000'
app.use('/api', createProxyMiddleware({
  target: PY_TARGET,
  changeOrigin: true,
  pathRewrite: { '^/api': '/api' },
  logLevel: 'warn',
}))

// Optional: serve a small health endpoint
app.get('/health', (_, res) => res.json({ ok: true }))

app.listen(PORT, () => console.log(`Backend proxy running on http://localhost:${PORT} -> ${PY_TARGET}`))
