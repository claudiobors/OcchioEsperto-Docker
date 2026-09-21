import base from '../vite.config.js'
import { fileURLToPath } from 'node:url'
const root = fileURLToPath(new URL('.', import.meta.url))
const authMock = fileURLToPath(new URL('./mock-auth.js', import.meta.url))
export default {
  ...base,
  root,
  base: '/',
  publicDir: fileURLToPath(new URL('../public', import.meta.url)),
  plugins: [{name:'local-review-auth',enforce:'pre',resolveId(id) { if (id.endsWith('/context/AuthContext')) return authMock }}, ...base.plugins],
  server: {host:'127.0.0.1',port:5180,strictPort:true,fs:{allow:[fileURLToPath(new URL('..',import.meta.url))]}},
  build: {outDir: fileURLToPath(new URL('../../tmp/review-build',import.meta.url)),emptyOutDir:false},
}

