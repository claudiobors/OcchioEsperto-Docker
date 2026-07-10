import { Scale, Shield } from 'lucide-react'

export default function Terms() {
  return (
    <div className="min-h-[calc(100vh-4rem)] py-16 px-4">
      <div className="max-w-3xl mx-auto">
        <div className="text-center mb-12">
          <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-vespa-green/10 flex items-center justify-center">
            <Scale className="w-7 h-7 text-vespa-green" />
          </div>
          <h1 className="font-heading text-3xl sm:text-4xl font-bold text-vespa-black mb-4">
            Termini di Servizio
          </h1>
          <p className="text-vespa-gray text-sm">
            Ultimo aggiornamento: Giugno 2026
          </p>
        </div>

        <div className="bg-white rounded-2xl border border-vespa-cream-dark p-8 sm:p-12 space-y-8">
          {/* Disclaimer importante */}
          <div className="bg-vespa-cream/50 rounded-xl p-6 border border-vespa-cream-dark">
            <div className="flex items-start gap-3">
              <Shield className="w-6 h-6 text-vespa-green shrink-0 mt-0.5" />
              <div>
                <h2 className="font-semibold text-vespa-black mb-2">Avviso Importante</h2>
                <p className="text-sm text-vespa-gray leading-relaxed">
                  Questo servizio offre un'analisi basata su dati storici per supportare appassionati e restauratori.
                  Non costituisce un certificato ufficiale di origine e non è affiliato in alcun modo al Gruppo Piaggio.
                  Le nostre analisi si basano sulle più moderne conoscenze di intelligenza artificiale, addestrate da
                  massimi esperti del settore.
                </p>
              </div>
            </div>
          </div>

          <section>
            <h2 className="font-heading text-xl font-bold text-vespa-black mb-4">1. Accettazione dei Termini</h2>
            <p className="text-sm text-vespa-gray leading-relaxed">
              Utilizzando OcchioEsperto.it (di seguito "il Servizio"), l'utente accetta integralmente i presenti
              Termini di Servizio. Se non si accettano questi termini, non è possibile utilizzare il Servizio.
            </p>
          </section>

          <section>
            <h2 className="font-heading text-xl font-bold text-vespa-black mb-4">2. Descrizione del Servizio</h2>
            <p className="text-sm text-vespa-gray leading-relaxed">
              OcchioEsperto è un assistente digitale basato su intelligenza artificiale che fornisce analisi
              e identificazioni di modelli Vespa Piaggio (1946-oggi) basate su dati storici. Il Servizio si
              propone come supporto informativo per appassionati e restauratori e non sostituisce in alcun
              modo una perizia tecnica ufficiale o un certificato di autenticità rilasciato da enti autorizzati.
            </p>
          </section>

          <section>
            <h2 className="font-heading text-xl font-bold text-vespa-black mb-4">3. Nessuna Affiliazione</h2>
            <p className="text-sm text-vespa-gray leading-relaxed">
              OcchioEsperto non è affiliato, approvato, sponsorizzato o in alcun modo collegato al
              Gruppo Piaggio & C. S.p.A. o alle sue sussidiarie. I marchi "Vespa" e "Piaggio" sono
              di proprietà dei rispettivi titolari e vengono menzionati esclusivamente a scopo descrittivo
              del servizio offerto.
            </p>
          </section>

          <section>
            <h2 className="font-heading text-xl font-bold text-vespa-black mb-4">4. Limitazione di Responsabilità</h2>
            <p className="text-sm text-vespa-gray leading-relaxed">
              Le analisi fornite da OcchioEsperto sono basate su dati storici pubblici e algoritmi di
              intelligenza artificiale. L'accuratezza delle identificazioni non è garantita e l'utente
              riconosce che:
            </p>
            <ul className="list-disc pl-5 mt-3 space-y-2 text-sm text-vespa-gray">
              <li>Le stime di mercato sono indicative e basate su dati aggregati, non costituiscono una valutazione professionale;</li>
              <li>Le verifiche di originalità sono parziali e non sostituiscono un controllo da parte di un esperto qualificato;</li>
              <li>Il Servizio non può essere utilizzato come unico riferimento per transazioni di compravendita;</li>
              <li>L'utente esonera espressamente OcchioEsperto da qualsiasi responsabilità economica o legale derivante da decisioni basate sulle analisi fornite.</li>
            </ul>
          </section>

          <section>
            <h2 className="font-heading text-xl font-bold text-vespa-black mb-4">5. Privacy e Dati</h2>
            <p className="text-sm text-vespa-gray leading-relaxed">
              I dati personali forniti dall'utente (email, nome, foto) vengono trattati secondo la nostra
              Privacy Policy. I dati delle Vespe analizzate possono essere utilizzati in forma aggregata
              e anonima per migliorare l'accuratezza del Servizio.
            </p>
          </section>

          <section>
            <h2 className="font-heading text-xl font-bold text-vespa-black mb-4">6. Pagamenti e Rimborsi</h2>
            <p className="text-sm text-vespa-gray leading-relaxed">
              I pagamenti per i piani a pagamento vengono processati tramite Stripe. Ogni analisi viene
              acquistata singolarmente (nessun abbonamento ricorrente). Una volta completata l'analisi,
              il pagamento non è rimborsabile in quanto il servizio digitale viene erogato immediatamente.
            </p>
          </section>

          <section>
            <h2 className="font-heading text-xl font-bold text-vespa-black mb-4">7. Modifiche ai Termini</h2>
            <p className="text-sm text-vespa-gray leading-relaxed">
              Ci riserviamo il diritto di modificare questi termini in qualsiasi momento. Le modifiche
              saranno comunicate tramite aggiornamento di questa pagina. L'uso continuato del Servizio
              dopo le modifiche costituisce accettazione dei nuovi termini.
            </p>
          </section>
        </div>
      </div>
    </div>
  )
}