import { Lock, Eye, Trash2 } from 'lucide-react'

export default function Privacy() {
  return (
    <div className="min-h-[calc(100vh-4rem)] py-16 px-4">
      <div className="max-w-3xl mx-auto">
        <div className="text-center mb-12">
          <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-vespa-green/10 flex items-center justify-center">
            <Lock className="w-7 h-7 text-vespa-green" />
          </div>
          <h1 className="font-heading text-3xl sm:text-4xl font-bold text-vespa-black mb-4">
            Privacy Policy
          </h1>
          <p className="text-vespa-gray text-sm">
            Ultimo aggiornamento: Giugno 2026
          </p>
        </div>

        <div className="bg-white rounded-2xl border border-vespa-cream-dark p-8 sm:p-12 space-y-8">
          <section>
            <h2 className="font-heading text-xl font-bold text-vespa-black mb-4">1. Titolare del Trattamento</h2>
            <p className="text-sm text-vespa-gray leading-relaxed">
              Il titolare del trattamento dei dati è OcchioEsperto. Per qualsiasi richiesta relativa
              ai tuoi dati personali, puoi contattarci all'indirizzo email: privacy@occhioesperto.it.
            </p>
          </section>

          <section>
            <h2 className="font-heading text-xl font-bold text-vespa-black mb-4">2. Dati Raccolti</h2>
            <p className="text-sm text-vespa-gray leading-relaxed mb-4">
              Durante l'utilizzo del Servizio, raccogliamo i seguenti dati:
            </p>
            <div className="space-y-3">
              <div className="flex items-start gap-3">
                <Eye className="w-5 h-5 text-vespa-green shrink-0 mt-0.5" />
                <div>
                  <h3 className="font-semibold text-vespa-black text-sm">Dati di Registrazione</h3>
                  <p className="text-xs text-vespa-gray">Nome, indirizzo email e password (crittografata).</p>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <Eye className="w-5 h-5 text-vespa-green shrink-0 mt-0.5" />
                <div>
                  <h3 className="font-semibold text-vespa-black text-sm">Dati delle Analisi</h3>
                  <p className="text-xs text-vespa-gray">Numeri di telaio, motore, foto e descrizioni delle Vespa inserite dall'utente.</p>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <Eye className="w-5 h-5 text-vespa-green shrink-0 mt-0.5" />
                <div>
                  <h3 className="font-semibold text-vespa-black text-sm">Dati di Pagamento</h3>
                  <p className="text-xs text-vespa-gray">I pagamenti sono gestiti da Stripe. Non memorizziamo dati di carte di credito.</p>
                </div>
              </div>
            </div>
          </section>

          <section>
            <h2 className="font-heading text-xl font-bold text-vespa-black mb-4">3. Finalità del Trattamento</h2>
            <p className="text-sm text-vespa-gray leading-relaxed">
              I dati raccolti vengono utilizzati per:
            </p>
            <ul className="list-disc pl-5 mt-3 space-y-2 text-sm text-vespa-gray">
              <li>Fornire il servizio di identificazione e analisi delle Vespa;</li>
              <li>Migliorare l'accuratezza degli algoritmi di analisi (dati aggregati e anonimi);</li>
              <li>Gestire pagamenti e fatture tramite Stripe;</li>
              <li>Comunicare con l'utente in merito al servizio richiesto;</li>
              <li>Rispettare obblighi di legge.</li>
            </ul>
          </section>

          <section>
            <h2 className="font-heading text-xl font-bold text-vespa-black mb-4">4. Base Giuridica</h2>
            <p className="text-sm text-vespa-gray leading-relaxed">
              Il trattamento dei dati è basato sul consenso dell'utente (art. 6 par. 1 lett. a GDPR)
              e sull'esecuzione del contratto di servizio (art. 6 par. 1 lett. b GDPR).
            </p>
          </section>

          <section>
            <h2 className="font-heading text-xl font-bold text-vespa-black mb-4">5. Conservazione dei Dati</h2>
            <p className="text-sm text-vespa-gray leading-relaxed">
              I dati vengono conservati per tutta la durata dell'account utente. In caso di richiesta
              di cancellazione dell'account, tutti i dati associati vengono eliminati entro 30 giorni.
              I dati di pagamento vengono conservati per 10 anni come richiesto dalla normativa fiscale.
            </p>
          </section>

          <section>
            <h2 className="font-heading text-xl font-bold text-vespa-black mb-4">6. Diritti dell'Utente</h2>
            <p className="text-sm text-vespa-gray leading-relaxed mb-4">
              Ai sensi del GDPR, l'utente ha diritto a:
            </p>
            <ul className="list-disc pl-5 space-y-2 text-sm text-vespa-gray">
              <li>Accedere ai propri dati personali;</li>
              <li>Richiedere la rettifica o cancellazione dei dati;</li>
              <li>Limitare il trattamento dei dati;</li>
              <li>Opporsi al trattamento dei dati;</li>
              <li>Richiedere la portabilità dei dati;</li>
              <li>Revocare il consenso in qualsiasi momento.</li>
            </ul>
          </section>

          <section>
            <h2 className="font-heading text-xl font-bold text-vespa-black mb-4">7. Sicurezza</h2>
            <p className="text-sm text-vespa-gray leading-relaxed">
              I dati vengono trasmessi su connessione crittografata (HTTPS). Le password sono
              crittografate con algoritmo bcrypt. I pagamenti sono gestiti da Stripe, conformi
              agli standard PCI DSS.
            </p>
          </section>

          <section>
            <div className="flex items-start gap-3 bg-vespa-cream/50 rounded-xl p-6 border border-vespa-cream-dark">
              <Trash2 className="w-6 h-6 text-vespa-green shrink-0 mt-0.5" />
              <div>
                <h2 className="font-semibold text-vespa-black mb-2">Cancellazione Account</h2>
                <p className="text-sm text-vespa-gray leading-relaxed">
                  Puoi richiedere la cancellazione del tuo account e di tutti i dati associati
                  in qualsiasi momento scrivendo a privacy@occhioesperto.it. Provvederemo entro 30 giorni.
                </p>
              </div>
            </div>
          </section>
        </div>
      </div>
    </div>
  )
}