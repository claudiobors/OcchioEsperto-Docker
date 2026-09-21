export default function AuthLayout({ children }) {
  return <div className="auth-layout"><aside className="auth-editorial"><img src={`${import.meta.env.BASE_URL}images/collector-studio.webp`} alt="Scooter storico in atelier, immagine generata con AI" width="1536" height="1024" /><div><h2>Le passioni belle<br />meritano un posto<br /><em>tutto loro.</em></h2><p>Il tuo garage, le tue scoperte.<br />Un dettaglio alla volta.</p></div><small>Scena illustrativa generata con AI</small></aside><section className="auth-content">{children}</section></div>
}

