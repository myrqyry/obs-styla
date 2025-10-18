const express = require('express')
const { execFile } = require('child_process')
const path = require('path')
const cors = require('cors')
const app = express()
const PORT = process.env.PORT || 3000

// allow Vite dev server origin by default
app.use(cors({ origin: (origin, cb) => cb(null, true) }))
app.use(express.json())

// Simple proxy: call python validator script (we'll create a small wrapper)
app.get('/api/validate', (req, res) => {
  const py = path.join(__dirname, '..', 'app', 'server.py')
  // The existing app/server.py exposes /api/validate when run as a Flask app.
  // For now call the Flask server endpoint if running; fallback to executing a helper script `app/validate_cli.py`.
  const cli = path.join(__dirname, '..', 'app', 'validate_cli.py')
  execFile('python3', [cli], { cwd: path.join(__dirname, '..') }, (err, stdout, stderr) => {
    if (err) {
      return res.status(500).json({ error: String(err), stderr: stderr })
    }
    try {
      const data = JSON.parse(stdout)
      res.json(data)
    } catch (e) {
      res.status(500).json({ error: 'Failed to parse Python output', raw: stdout })
    }
  })
})

app.listen(PORT, () => console.log(`Backend running on http://localhost:${PORT}`))
