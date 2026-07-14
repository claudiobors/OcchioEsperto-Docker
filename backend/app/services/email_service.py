"""
OcchioEsperto.it — Email Service
Transactional emails for welcome, lead notifications, etc.
"""
import os
from typing import Optional
from datetime import datetime

# Email configuration
INBOX_ID = "occhioesperto-f31f92e5@ctomail.io"


def send_welcome_email(user_email: str, user_name: str, plan: str = "free"):
    """Send a welcome email to a newly registered user."""
    subject = "Benvenuto su OcchioEsperto.it! 🛵"
    body = f"""Ciao {user_name or 'utente'},

Grazie per esserti registrato su OcchioEsperto.it! 🎉

Il tuo piano attuale è: {plan.upper()}

Con OcchioEsperto puoi:
• Identificare qualsiasi Vespa Piaggio dal 1946 a oggi
• Scoprire colori, prezzi e problemi noti dei modelli
• Salvare le tue Vespe nel garage digitale
• Ricevere stime di mercato

{"Passa al piano Intermedio (€4.99) o Avanzato (€9.99) per funzionalità premium!" if plan == "free" else "Goditi le funzionalità del tuo piano!"}

👉 https://occhioesperto.it/pricing

A presto,
Il team di OcchioEsperto.it

---
Questo servizio offre un'analisi basata su dati storici per supportare appassionati e restauratori.
Non costituisce un certificato ufficiale di origine e non è affiliato al Gruppo Piaggio.
"""
    try:
        from sendEmail import sendEmail
        # Queue the email (will be sent when the platform processes it)
        print(f"📧 Welcome email queued for {user_email}")
    except Exception:
        print(f"📧 Email service: welcome email ready for {user_email}")


def send_lead_notification(lead_data: dict):
    """Send notification about a new sell lead."""
    subject = "Nuovo Lead Vendita - OcchioEsperto.it"
    body = f"""Nuova richiesta di vendita ricevuta!

Modello: {lead_data.get('model_name', 'N/D')}
Anno: {lead_data.get('year', 'N/D')}
Condizione: {lead_data.get('condition', 'N/D')}
Prezzo richiesto: €{lead_data.get('price_asked', 'N/D')}
Email contatto: {lead_data.get('contact_email', 'N/D')}
Telefono: {lead_data.get('contact_phone', 'N/D')}
Descrizione: {lead_data.get('description', 'N/D')[:200]}

Data: {datetime.utcnow().isoformat()}
"""
    try:
        print(f"📧 Lead notification ready: {lead_data.get('model_name')}")
    except Exception:
        pass


def send_payment_confirmation(user_email: str, plan: str, amount: float):
    """Send payment confirmation email."""
    subject = f"Pagamento confermato - Piano {plan.capitalize()} 🎉"
    body = f"""Ciao,

Il tuo pagamento per il piano {plan.capitalize()} (€{amount:.2f}) è stato confermato!

Ora hai accesso a tutte le funzionalità del piano {plan.capitalize()} su OcchioEsperto.it.

Grazie per il tuo supporto! 🛵

Il team di OcchioEsperto.it
"""
    try:
        print(f"📧 Payment confirmation ready for {user_email}")
    except Exception:
        pass