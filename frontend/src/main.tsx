import './style.css'
import axios from 'axios'

const root = document.getElementById('root')!

root.innerHTML = `
  <div class="app">
    <header>
      <h1>OBS Styla</h1>
      <nav class="tabs">
        <button id="tab-gen" class="active">Generator</button>
        <button id="tab-val">Validator</button>
      </nav>
    </header>
    <main>
      <section id="gen" class="panel">
        <div class="controls">
          <button id="generate">Run Generation</button>
          <button id="refresh-themes">Refresh Themes</button>
          <span id="gen-status" class="muted">idle</span>
        </div>
        <div id="gen-output" class="panel-inner">No generation run yet.</div>
        <h3>Generated Themes</h3>
        <ul id="themes-list"></ul>
      </section>

      <section id="val" class="panel" style="display:none">
        <div class="controls">
          <button id="validate">Run Validation</button>
          <span id="val-status" class="muted">idle</span>
        </div>
        <div id="val-output" class="panel-inner">No validation run yet.</div>
      </section>
    </main>
  </div>
`

// Tab switching
document.getElementById('tab-gen')!.addEventListener('click', () => {
  (document.getElementById('tab-gen') as HTMLElement).classList.add('active')
  (document.getElementById('tab-val') as HTMLElement).classList.remove('active')
  (document.getElementById('gen') as HTMLElement).style.display = 'block'
  (document.getElementById('val') as HTMLElement).style.display = 'none'
})
document.getElementById('tab-val')!.addEventListener('click', () => {
  (document.getElementById('tab-val') as HTMLElement).classList.add('active')
  (document.getElementById('tab-gen') as HTMLElement).classList.remove('active')
  (document.getElementById('gen') as HTMLElement).style.display = 'none'
  (document.getElementById('val') as HTMLElement).style.display = 'block'
})

async function listThemes() {
  const list = document.getElementById('themes-list')!
  list.innerHTML = 'Loading...'
  try {
    const r = await axios.get('/api/themes')
    const themes = r.data.themes || []
    list.innerHTML = ''
    themes.forEach((t: any) => {
      const li = document.createElement('li')
      const a = document.createElement('a')
      a.href = `/api/themes/${encodeURIComponent(t.name)}`
      a.textContent = `${t.name} (${t.size} bytes)`
      a.target = '_blank'
      li.appendChild(a)
      list.appendChild(li)
    })
    if (themes.length === 0) list.innerHTML = '<li>No themes found</li>'
  } catch (e: any) {
    list.innerHTML = `<li class="error">Error listing themes: ${String(e)}</li>`
  }
}

document.getElementById('refresh-themes')!.addEventListener('click', listThemes)

document.getElementById('generate')!.addEventListener('click', async () => {
  const out = document.getElementById('gen-output')!
  const status = document.getElementById('gen-status')!
  status.textContent = 'running...'
  out.textContent = 'Running generation scripts...'
  try {
    const r = await axios.post('/api/generate')
    out.innerHTML = ''
    const results = r.data.results || []
    results.forEach((res: any) => {
      const pre = document.createElement('pre')
      pre.textContent = `${res.script} -> exit ${res.returncode}\nstdout:\n${res.stdout}\nstderr:\n${res.stderr}`
      out.appendChild(pre)
    })
    await listThemes()
    status.textContent = 'done'
  } catch (e: any) {
    out.innerHTML = `<div class="error">Generation failed: ${String(e)}</div>`
    status.textContent = 'error'
  }
})

// Validator: reuse existing validation UI but simpler
document.getElementById('validate')!.addEventListener('click', async () => {
  const out = document.getElementById('val-output')!
  const status = document.getElementById('val-status')!
  status.textContent = 'running...'
  out.textContent = 'Running validation...'
  try {
    const r = await axios.get('/api/validate')
    out.innerHTML = '<pre>' + JSON.stringify(r.data, null, 2) + '</pre>'
    status.textContent = 'done'
  } catch (e: any) {
    out.innerHTML = `<div class="error">Validation failed: ${String(e)}</div>`
    status.textContent = 'error'
  }
})

// Auto-load themes on start
listThemes()


