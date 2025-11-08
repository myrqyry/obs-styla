import { defineConfig, loadEnv } from 'vite'
import path from 'path'
import svgr from 'vite-plugin-svgr'

// Assumptions:
// - During development we proxy `/api` requests to a backend running locally.
// - Prefer the Node proxy at http://127.0.0.1:3000 (if present). You can override
//   the target by setting VITE_API_PROXY_TARGET in an env file (e.g. .env.development)
//   or in the shell before starting Vite.
// Example .env.development content:
// VITE_API_PROXY_TARGET=http://127.0.0.1:3000

export default defineConfig(({ mode }) => {
  // Load env vars so VITE_* variables are available here.
  const env = loadEnv(mode, process.cwd(), '')

  // Vite only exposes env vars that start with VITE_. Use VITE_API_PROXY_TARGET
  // to change the proxy target without editing this file.
  const apiProxyTarget = env.VITE_API_PROXY_TARGET || 'http://127.0.0.1:3000'

  return {
    // Helpful dev server defaults. The port can be changed by Vite CLI args.
    server: {
      port: 5173,
      open: false,
      proxy: {
        // Proxy API requests to the backend during development. This keeps
        // same-origin in the browser and avoids CORS issues while developing.
        '/api': {
          target: apiProxyTarget,
          changeOrigin: true,
          secure: false,
          ws: true,
          // Keep the path as-is; if your backend expects a different base
          // path you can rewrite it here.
          rewrite: (p) => p,
        },
      },
    },

    // Nice-to-have alias so imports can use `@/...` to refer to `src/`
    resolve: {
      alias: {
        '@': path.resolve(__dirname, 'src'),
      },
    },
    plugins: [svgr()],
  }
})
