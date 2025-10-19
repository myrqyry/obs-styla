import './style.css'
import axios from 'axios'

const root = document.getElementById('root')!

root.innerHTML = `
  <div class="app">
    <header>
      <h1>OBS Styla — Validator</h1>
      <div class="controls">
            <div class="left-controls">
              <button id="validate">Refresh</button>
              <input id="search" placeholder="Search filenames / messages" />
              <label class="checkbox"><input id="errorsOnly" type="checkbox"/> Errors only</label>
            </div>
            <div class="right-controls">
              <button id="export">Export JSON</button>
              <span id="status" class="muted">idle</span>
            </div>
          </div>
    </header>
    <main>
      <div id="panel" class="panel">No data yet. Click Refresh.</div>
    </main>
  </div>
`

let lastData: any = null

function filterAndRender() {
  const q = (document.getElementById('search') as HTMLInputElement).value.trim().toLowerCase()
  const errorsOnly = (document.getElementById('errorsOnly') as HTMLInputElement).checked
  if (!lastData) return
  const filtered = { validations: lastData.validations.filter((entry: any) => {
    const name = (entry.name || '').toLowerCase()
    const reportString = JSON.stringify(entry.report || {}).toLowerCase()
    if (q && !(name.includes(q) || reportString.includes(q))) return false
    if (errorsOnly) {
      const errs = (entry.report && entry.report.summary && entry.report.summary.errors) || 0
      return errs > 0
    }
    return true
  }) }
  renderReport(filtered)
}

function renderReport(data: any) {
  const panel = document.getElementById('panel')!
  if (!data || !Array.isArray(data.validations)) {
    panel.innerHTML = `<div class="error">Invalid response</div>`
    return
  }

  const list = document.createElement('div')
  list.className = 'report-list'

  data.validations.forEach((entry: any) => {
    const box = document.createElement('div')
    box.className = 'report-item'

    const header = document.createElement('div')
    header.className = 'report-header'
    const name = document.createElement('div')
    name.className = 'report-name'
    name.textContent = entry.name || 'unknown'
    const counts = document.createElement('div')
    counts.className = 'report-counts'
    const errors = (entry.report && entry.report.summary && entry.report.summary.errors) || 0
    const warnings = (entry.report && entry.report.summary && entry.report.summary.warnings) || 0
    counts.innerHTML = `<span class="err">Errors: ${errors}</span> <span class="warn">Warnings: ${warnings}</span>`

    header.appendChild(name)
    header.appendChild(counts)

    const body = document.createElement('div')
    body.className = 'report-body'
    body.style.display = 'none'

    if (entry.report) {
      const errs = entry.report.errors || []
      const warns = entry.report.warnings || []

      const makeList = (items: any[], cls: string) => {
        const ul = document.createElement('ul')
        ul.className = cls
        items.forEach(it => {
          const li = document.createElement('li')
          li.textContent = it.message || JSON.stringify(it)
          ul.appendChild(li)
        })
        return ul
      }

      if (errs.length) {
        const h = document.createElement('h4')
        h.textContent = `Errors (${errs.length})`
        body.appendChild(h)
        body.appendChild(makeList(errs, 'errors'))
      }
      if (warns.length) {
        const h = document.createElement('h4')
        h.textContent = `Warnings (${warns.length})`
        body.appendChild(h)
        body.appendChild(makeList(warns, 'warnings'))
      }
      if (!errs.length && !warns.length) {
        body.textContent = 'No issues found.'
      }
    } else {
      body.textContent = 'No report available.'
    }

    header.addEventListener('click', () => {
      body.style.display = body.style.display === 'none' ? 'block' : 'none'
    })

    box.appendChild(header)
    box.appendChild(body)
    list.appendChild(box)
  })

  panel.innerHTML = ''
  panel.appendChild(list)
}

async function fetchAndRender() {
  const status = document.getElementById('status')!
  status.textContent = 'loading...'
  try {
    const r = await axios.get('/api/validate')
    lastData = r.data
    renderReport(r.data)
    // wire filters/export
    ;(document.getElementById('search') as HTMLInputElement).addEventListener('input', filterAndRender)
    ;(document.getElementById('errorsOnly') as HTMLInputElement).addEventListener('change', filterAndRender)
    ;(document.getElementById('export') as HTMLButtonElement).addEventListener('click', () => {
      const blob = new Blob([JSON.stringify(lastData, null, 2)], { type: 'application/json' })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = 'validation-report.json'
      document.body.appendChild(a)
      a.click()
      a.remove()
      URL.revokeObjectURL(url)
    })
    status.textContent = 'last updated'
  } catch (e: any) {
    const panel = document.getElementById('panel')!
    panel.innerHTML = `<div class="error">${String(e)}</div>`
    status.textContent = 'error'
  }
}

document.getElementById('validate')!.addEventListener('click', fetchAndRender)

// Auto-fetch on load
fetchAndRender()

