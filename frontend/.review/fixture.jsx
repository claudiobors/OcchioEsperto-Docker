import React from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import App from '../src/App'
import '../src/index.css'
createRoot(document.getElementById('root')).render(<BrowserRouter><div style={{padding:'10px 20px',background:'#e8d6af',color:'#20372f',fontSize:12}}>AMBIENTE DI VERIFICA — Dati sintetici locali. Nessuna richiesta o transazione reale.</div><App /></BrowserRouter>)

