#!/usr/bin/env python3
"""
OcchioEsperto.it — Vespa Knowledge Base Seed Script
Crea il database SQLite pre-popolato con tutti i modelli Vespa Piaggio dal 1946 a oggi.
"""

import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "vespa_knowledge.db")

def create_schema(conn):
    """Create the database schema."""
    cursor = conn.cursor()

    cursor.executescript("""
        -- Main Vespa models table
        CREATE TABLE IF NOT EXISTS vespa_models (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            slug TEXT NOT NULL UNIQUE,
            production_start INTEGER NOT NULL,
            production_end INTEGER,
            displacement_cc TEXT NOT NULL,
            description TEXT,
            image_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- Chassis (telaio) number ranges per model
        CREATE TABLE IF NOT EXISTS vespa_chassis_numbers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model_id INTEGER NOT NULL,
            number_start TEXT NOT NULL,
            number_end TEXT,
            year_start INTEGER,
            year_end INTEGER,
            notes TEXT,
            FOREIGN KEY (model_id) REFERENCES vespa_models(id)
        );

        -- Engine number ranges per model
        CREATE TABLE IF NOT EXISTS vespa_engine_numbers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model_id INTEGER NOT NULL,
            number_start TEXT NOT NULL,
            number_end TEXT,
            year_start INTEGER,
            year_end INTEGER,
            notes TEXT,
            FOREIGN KEY (model_id) REFERENCES vespa_models(id)
        );

        -- Historical colors available per model
        CREATE TABLE IF NOT EXISTS vespa_colors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model_id INTEGER NOT NULL,
            color_name TEXT NOT NULL,
            color_hex TEXT NOT NULL,
            year_start INTEGER,
            year_end INTEGER,
            notes TEXT,
            FOREIGN KEY (model_id) REFERENCES vespa_models(id)
        );

        -- Known issues per model
        CREATE TABLE IF NOT EXISTS vespa_known_issues (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model_id INTEGER NOT NULL,
            issue TEXT NOT NULL,
            severity TEXT CHECK(severity IN ('info', 'warning', 'critical')),
            description TEXT,
            FOREIGN KEY (model_id) REFERENCES vespa_models(id)
        );

        -- Market price estimates per model per condition
        CREATE TABLE IF NOT EXISTS vespa_market_prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model_id INTEGER NOT NULL,
            condition_type TEXT NOT NULL CHECK(condition_type IN ('restored', 'good', 'fair', 'project')),
            price_min INTEGER,
            price_max INTEGER,
            currency TEXT DEFAULT 'EUR',
            last_updated DATE,
            FOREIGN KEY (model_id) REFERENCES vespa_models(id)
        );

        -- Create indexes for fast lookup
        CREATE INDEX IF NOT EXISTS idx_chassis_model ON vespa_chassis_numbers(model_id);
        CREATE INDEX IF NOT EXISTS idx_engine_model ON vespa_engine_numbers(model_id);
        CREATE INDEX IF NOT EXISTS idx_colors_model ON vespa_colors(model_id);
        CREATE INDEX IF NOT EXISTS idx_prices_model ON vespa_market_prices(model_id);
        CREATE INDEX IF NOT EXISTS idx_issues_model ON vespa_known_issues(model_id);
    """)

    conn.commit()


def seed_data(conn):
    """Seed the database with comprehensive Vespa knowledge."""
    cursor = conn.cursor()

    # =========================================================
    # MODELS DATA
    # =========================================================
    models = [
        # (name, slug, start, end, displacement, description)
        ("Vespa 98", "vespa-98", 1946, 1947, "98 cc",
         "La prima Vespa della storia. Progettata da Corradino D'Ascanio, prodotta dal 1946. Motore 98cc, cambio a 3 marce. Rivoluzionaria per l'epoca con la carrozzeria portante in acciaio."),

        ("Vespa 125", "vespa-125", 1948, 1950, "125 cc",
         "Evoluzione della 98 con motore portato a 125cc. Mantiene il cambio a 3 marce. Primo vero successo commerciale Piaggio."),

        ("Vespa 125 U", "vespa-125-u", 1953, 1955, "125 cc",
         "Versione utilitaria della 125, con finiture semplificate per ridurre i costi. Nota come 'Vespa Economica'."),

        ("Vespa 150", "vespa-150", 1955, 1957, "150 cc",
         "Nuovo motore da 150cc. Prima Vespa con sospensione posteriore migliorata. Design iconico anni '50."),

        ("Vespa 150 GS (Gran Sport)", "vespa-150-gs", 1955, 1961, "150 cc",
         "La prima Vespa sportiva. Motore elaborato da 150cc, cambio a 4 marce. Velocità massima di 90 km/h. Un'icona."),

        ("Vespa 125 VM", "vespa-125-vm", 1957, 1960, "125 cc",
         "Modello aggiornato con sospensione anteriore a molla e paraurti parafango."),

        ("Vespa 150 VL", "vespa-150-vl", 1957, 1962, "150 cc",
         "Evoluzione della Vespa 150 con nuovo telaio e motore migliorato."),

        ("Vespa 160 GS (Gran Sport)", "vespa-160-gs", 1962, 1964, "160 cc",
         "Evoluzione della GS con motore 160cc. Cerchi da 10 pollici, freno a tamburo anteriore. Design più moderno."),

        ("Vespa 150 Super (VLA/VLB)", "vespa-150-super", 1965, 1970, "150 cc",
         "Modello dalla forma più squadrata. Fanale anteriore rettangolare e pedana piatta. Un classico degli anni '60."),

        ("Vespa 125 Super (VMA/VMB)", "vespa-125-super", 1966, 1973, "125 cc",
         "Versione 125cc della Super. Molto popolare in Italia come mezzo di trasporto quotidiano."),

        ("Vespa Sprint (VLA1T)", "vespa-sprint", 1965, 1971, "150 cc",
         "Versione sportiva della Super con manubrio ribassato e sella sportiva. Fanale anteriore rettangolare. Velocità 95 km/h."),

        ("Vespa Sprint Veloce (VBC)", "vespa-sprint-veloce", 1969, 1973, "125 cc",
         "Versione 125cc dello Sprint. Leggera e scattante, apprezzata dai giovani."),

        ("Vespa 180 SS (Super Sport)", "vespa-180-ss", 1964, 1968, "180 cc",
         "La regina delle Vespa classiche. Motore 180cc, cambio a 4 marce, velocità oltre 100 km/h. Cerchi da 10 pollici."),

        ("Vespa 50 (V5A1T)", "vespa-50", 1963, 1975, "50 cc",
         "La prima Vespa 50cc, pensata per i giovanissimi (patente a 14 anni). Motore 50cc 2T, cambio a 3 marce. Un fenomeno sociale."),

        ("Vespa 50 Special", "vespa-50-special", 1969, 1973, "50 cc",
         "Versione più moderna e sportiva della 50. Fanale anteriore tondo, colori vivaci. Icona giovanile."),

        ("Vespa 50 L", "vespa-50-l", 1968, 1973, "50 cc",
         "Versione più lunga e comoda della 50, con pedana più ampia e sella confortevole."),

        ("Vespa 90 (V9A)", "vespa-90", 1963, 1966, "90 cc",
         "Modello intermedio tra 50 e 125. Motore 90cc, carrozzeria simile alla 50 ma leggermente più grande."),

        ("Vespa Primavera 125 (VMA2T)", "vespa-primavera-125", 1968, 1971, "125 cc",
         "Primavera: la Vespa che ha segnato un'epoca. Linea elegante, colori pastello. Molto ricercata."),

        ("Vespa Primavera ET3 (VMB1T)", "vespa-primavera-et3", 1971, 1983, "125 cc",
         "Elettronica a 3 porte (ET3). Motore 125cc con accensione elettronica. 4 marce, 95 km/h. Tra le più amate."),

        ("Vespa 125 Nuova (VMA1T)", "vespa-nuova-125", 1971, 1978, "125 cc",
         "Nuova linea più moderna. Fanale anteriore rettangolare, indicatori di direzione integrati."),

        ("Vespa Rally 180 (VSD1T)", "vespa-rally-180", 1965, 1972, "180 cc",
         "La Vespa da rally. Motore 180cc potente, cambio a 4 marce, cruscotto con tachimetro. Velocità 105 km/h."),

        ("Vespa Rally 200 (VSE1T)", "vespa-rally-200", 1972, 1976, "200 cc",
         "Evoluzione della Rally con motore 200cc. La più potente Vespa classica. Velocità oltre 110 km/h."),

        ("Vespa PX 125 (T5)", "vespa-px-125", 1978, 2000, "125 cc",
         "La Vespa PX, icona assoluta. Telaio in acciaio, cambio a 4 marce. Prodotta per oltre 20 anni in milioni di esemplari."),

        ("Vespa PX 150", "vespa-px-150", 1978, 2000, "150 cc",
         "Versione 150cc della PX. Molto diffusa in Italia e nel mondo."),

        ("Vespa PX 200", "vespa-px-200", 1978, 2016, "200 cc",
         "Versione 200cc della PX. La più potente della serie, molto apprezzata per i lunghi viaggi. Riedizione 2011."),

        ("Vespa Cosa (Cosetta) 125", "vespa-cosa-125", 1988, 1992, "125 cc",
         "Il tentativo di Piaggio di modernizzare la PX. Nuovo telaio, freno a disco anteriore, design più aerodinamico."),

        ("Vespa Cosa 200", "vespa-cosa-200", 1989, 1994, "200 cc",
         "Versione 200cc della Cosa. Meno diffusa della PX, oggi ricercata dai collezionisti."),

        ("Vespa T5 (Pole Position)", "vespa-t5", 1985, 1995, "125 cc",
         "Versione sportiva della PX. Testa a 5 luci (da qui T5), carburatore 24mm, potenza 12 CV. Velocità 115 km/h."),

        ("Vespa PK 125", "vespa-pk-125", 1983, 1995, "125 cc",
         "Modello moderno con carrozzeria in plastica ABS, ruote da 10 pollici, avviamento elettrico."),

        ("Vespa PK 80 S", "vespa-pk-80-s", 1985, 1992, "80 cc",
         "Versione 80cc della PK, con accensione elettronica e avviamento elettrico. Design anni '80."),

        ("Vespa ET2 50", "vespa-et2-50", 1996, 2005, "50 cc",
         "Nuova era per Vespa. Motore 50cc 2T, carrozzeria in plastica, design moderno che richiama il classico."),

        ("Vespa ET4 125", "vespa-et4-125", 1996, 2005, "125 cc",
         "Prima Vespa con motore 4T. Rivoluzione tecnica. Design moderno, avviamento elettrico, freno a disco."),

        ("Vespa ET4 150", "vespa-et4-150", 1998, 2005, "150 cc",
         "Versione 150cc 4T della ET4. Più potente e versatile."),

        ("Vespa GTS 125", "vespa-gts-125", 2003, 2009, "125 cc",
         "La Granturismo Sport. Design più muscoloso, motore 4T 125cc. Successo mondiale."),

        ("Vespa GTS 250", "vespa-gts-250", 2004, 2008, "250 cc",
         "Versione 250cc della GTS. Motore potente per autostrada. ABS disponibile."),

        ("Vespa GTS 300 Super", "vespa-gts-300-super", 2006, 2015, "300 cc",
         "La Vespa più potente della storia moderna. Motore 300cc 4T, 22 CV, ABS. Velocità 130 km/h."),

        ("Vespa GTV 300", "vespa-gtv-300", 2006, 2012, "300 cc",
         "Versione retrò della GTS. Faro anteriore sul parafango come la 98 originale. Sella monoposto."),

        ("Vespa LX 125", "vespa-lx-125", 2005, 2014, "125 cc",
         "Modello entry-level moderno. Linea ispirata alla Primavera, motore 4T 125cc."),

        ("Vespa LXV 125", "vespa-lxv-125", 2006, 2012, "125 cc",
         "Versione vintage della LX. Sella marrone, faro tondo, portapacchi cromato."),

        ("Vespa S 125", "vespa-s-125", 2007, 2012, "125 cc",
         "Design ispirato alla Sprint degli anni '60. Faro quadrato, manubrio basso."),

        ("Vespa Primavera 125 (2013)", "vespa-primavera-2013", 2013, 2020, "125 cc",
         "Rinascita del nome Primavera. Design moderno che omaggia il classico. Motore 4T i-get."),

        ("Vespa Sprint 150 (2014)", "vespa-sprint-2014", 2014, 2020, "150 cc",
         "Nuova Sprint. Design sportivo, ruote da 12 pollici, motore 150cc i-get."),

        ("Vespa GTS 300 (2019)", "vespa-gts-300-2019", 2019, 2024, "300 cc",
         "GTS di ultima generazione. Motore HPE 300cc, 23.8 CV, ABS ASR, display TFT opzionale."),

        ("Vespa GTS 125 (2019)", "vespa-gts-125-2019", 2019, 2024, "125 cc",
         "GTS 125cc con motore i-get. Nuova piattaforma, connettività smartphone."),

        ("Vespa Elettrica", "vespa-elettrica", 2019, 2024, "Elettrica",
         "La prima Vespa elettrica. Motore elettrico 4kW, batteria agli ioni di litio. Autonomia 70 km (100 km con extender)."),

        ("Vespa Primavera 125 (2021)", "vespa-primavera-2021", 2021, 2024, "125 cc",
         "Restyling della Primavera. Motore i-get 125cc, fari full LED, connettività."),

        ("Vespa Sprint S 125 (2021)", "vespa-sprint-s-2021", 2021, 2024, "125 cc",
         "Versione sportiva della Sprint. Sella nera con cuciture rosse, grafiche speciali."),
    ]

    cursor.executemany(
        "INSERT OR IGNORE INTO vespa_models (name, slug, production_start, production_end, displacement_cc, description) VALUES (?, ?, ?, ?, ?, ?)",
        models
    )
    conn.commit()

    # Get model IDs by slug
    cursor.execute("SELECT id, slug FROM vespa_models")
    model_ids = {row[1]: row[0] for row in cursor.fetchall()}

    # =========================================================
    # CHASSIS NUMBERS
    # =========================================================
    chassis_data = [
        # (slug, start, end, year_start, year_end, notes)
        ("vespa-98", "1001", "10000", 1946, 1947, "Serie iniziale"),
        ("vespa-98", "10001", "20000", 1947, 1947, "Seconda serie"),
        ("vespa-125", "20001", "60000", 1948, 1950, "Telaio 125 prima serie"),
        ("vespa-125-u", "60001", "90000", 1953, 1955, "Telaio 125 U"),
        ("vespa-150", "90001", "150000", 1955, 1957, "Telaio 150 prima serie"),
        ("vespa-150-gs", "1", "50000", 1955, 1961, "Telaio GS 150"),
        ("vespa-125-vm", "100001", "200000", 1957, 1960, "Telaio 125 VM"),
        ("vespa-150-vl", "200001", "400000", 1957, 1962, "Telaio 150 VL"),
        ("vespa-160-gs", "10001", "50000", 1962, 1964, "Telaio GS 160"),
        ("vespa-150-super", "1", "200000", 1965, 1970, "Telaio VLA/VLB"),
        ("vespa-125-super", "1", "350000", 1966, 1973, "Telaio VMA/VMB"),
        ("vespa-sprint", "100001", "350000", 1965, 1971, "Telaio Sprint VLA1T"),
        ("vespa-sprint-veloce", "1", "150000", 1969, 1973, "Telaio VBC"),
        ("vespa-180-ss", "10001", "80000", 1964, 1968, "Telaio 180 SS"),
        ("vespa-50", "1", "500000", 1963, 1975, "Telaio V5A1T"),
        ("vespa-50-special", "500001", "750000", 1969, 1973, "Telaio 50 Special"),
        ("vespa-50-l", "100001", "300000", 1968, 1973, "Telaio 50 L"),
        ("vespa-90", "1", "150000", 1963, 1966, "Telaio V9A"),
        ("vespa-primavera-125", "1", "200000", 1968, 1971, "Telaio VMA2T"),
        ("vespa-primavera-et3", "1", "400000", 1971, 1983, "Telaio VMB1T"),
        ("vespa-nuova-125", "1", "250000", 1971, 1978, "Telaio VMA1T"),
        ("vespa-rally-180", "10001", "80000", 1965, 1972, "Telaio VSD1T"),
        ("vespa-rally-200", "1", "120000", 1972, 1976, "Telaio VSE1T"),
        ("vespa-px-125", "100001", "1200000", 1978, 2000, "Telaio PX125"),
        ("vespa-px-150", "100001", "800000", 1978, 2000, "Telaio PX150"),
        ("vespa-px-200", "100001", "600000", 1978, 2016, "Telaio PX200"),
        ("vespa-cosa-125", "10001", "60000", 1988, 1992, "Telaio Cosa125"),
        ("vespa-cosa-200", "10001", "30000", 1989, 1994, "Telaio Cosa200"),
        ("vespa-t5", "10001", "75000", 1985, 1995, "Telaio T5 Pole Position"),
        ("vespa-pk-125", "100001", "450000", 1983, 1995, "Telaio PK125"),
        ("vespa-pk-80-s", "100001", "200000", 1985, 1992, "Telaio PK80 S"),
        ("vespa-et2-50", "ZAPM0401", "ZAPM04099999", 1996, 2005, "Telaio ET2 50"),
        ("vespa-et4-125", "ZAPM0501", "ZAPM05099999", 1996, 2005, "Telaio ET4 125"),
        ("vespa-et4-150", "ZAPM0501", "ZAPM05099999", 1998, 2005, "Telaio ET4 150"),
    ]

    chassis_values = []
    for slug, start, end, y_start, y_end, notes in chassis_data:
        if slug in model_ids:
            chassis_values.append((model_ids[slug], start, end, y_start, y_end, notes))

    cursor.executemany(
        "INSERT INTO vespa_chassis_numbers (model_id, number_start, number_end, year_start, year_end, notes) VALUES (?, ?, ?, ?, ?, ?)",
        chassis_values
    )
    conn.commit()

    # =========================================================
    # ENGINE NUMBERS
    # =========================================================
    engine_data = [
        # (slug, start, end, year_start, year_end, notes)
        ("vespa-98", "1001", "10000", 1946, 1947, "Motore V1T"),
        ("vespa-125", "20001", "60000", 1948, 1950, "Motore VM1T"),
        ("vespa-125-u", "60001", "90000", 1953, 1955, "Motore VM1T"),
        ("vespa-150", "90001", "150000", 1955, 1957, "Motore VL1T"),
        ("vespa-150-gs", "1", "50000", 1955, 1961, "Motore VGS1"),
        ("vespa-160-gs", "10001", "50000", 1962, 1964, "Motore VGS2"),
        ("vespa-150-super", "VLA1M", "VLA999999", 1965, 1970, "Motore VLA"),
        ("vespa-125-super", "VMA1M", "VMA999999", 1966, 1973, "Motore VMA"),
        ("vespa-sprint", "VLA1M", "VLA999999", 1965, 1971, "Motore VLA Sprint"),
        ("vespa-sprint-veloce", "VBC1M", "VBC999999", 1969, 1973, "Motore VBC"),
        ("vespa-180-ss", "VSD1M", "VSD999999", 1964, 1968, "Motore VSD"),
        ("vespa-50", "V5A1M", "V5A999999", 1963, 1975, "Motore V5A"),
        ("vespa-50-special", "V5B1M", "V5B999999", 1969, 1973, "Motore V5B"),
        ("vespa-90", "V9A1M", "V9A999999", 1963, 1966, "Motore V9A"),
        ("vespa-primavera-125", "VMA2M", "VMA2999999", 1968, 1971, "Motore VMA2"),
        ("vespa-primavera-et3", "VMB1M", "VMB999999", 1971, 1983, "Motore VMB ET3"),
        ("vespa-rally-180", "VSD1M", "VSD999999", 1965, 1972, "Motore VSD Rally"),
        ("vespa-rally-200", "VSE1M", "VSE999999", 1972, 1976, "Motore VSE Rally 200"),
        ("vespa-px-125", "PX125M1", "PX125M999999", 1978, 2000, "Motore PX125"),
        ("vespa-px-150", "PX150M1", "PX150M999999", 1978, 2000, "Motore PX150"),
        ("vespa-px-200", "PX200M1", "PX200M999999", 1978, 2016, "Motore PX200"),
        ("vespa-t5", "T5M1", "T5M99999", 1985, 1995, "Motore T5 5 porte"),
        ("vespa-cosa-125", "COSA125M1", "COSA125M99999", 1988, 1992, "Motore Cosa125"),
        ("vespa-cosa-200", "COSA200M1", "COSA200M99999", 1989, 1994, "Motore Cosa200"),
        ("vespa-pk-125", "PK125M1", "PK125M999999", 1983, 1995, "Motore PK125"),
        ("vespa-et4-125", "M0401M", "M0409999999", 1996, 2005, "Motore ET4 125 4T LEADER"),
        ("vespa-et4-150", "M0501M", "M0509999999", 1998, 2005, "Motore ET4 150 4T LEADER"),
    ]

    engine_values = []
    for slug, start, end, y_start, y_end, notes in engine_data:
        if slug in model_ids:
            engine_values.append((model_ids[slug], start, end, y_start, y_end, notes))

    cursor.executemany(
        "INSERT INTO vespa_engine_numbers (model_id, number_start, number_end, year_start, year_end, notes) VALUES (?, ?, ?, ?, ?, ?)",
        engine_values
    )
    conn.commit()

    # =========================================================
    # REAL VERIFIED CHASSIS NUMBER RANGES
    # Fonte: registro storico fornito dall'utente (dati "certi"), con
    # nomenclatura dei modelli incrociata su scooterhelp.com/serial/.
    # A differenza delle stime sopra, questi sono range documentati
    # anno per anno. Aggiunti come modelli distinti per non alterare
    # il comportamento di matching esistente.
    # =========================================================
    real_models = [
        # (name, slug, start, end, displacement, description)
        ("Vespa 50 N", "vespa-50-n", 1963, 1971, "50 cc",
         "Prima Vespa 50cc, telaio V5A1T. Numeri di telaio documentati anno per anno."),
        ("Vespa 50 R", "vespa-50-r", 1969, 1983, "50 cc",
         "Variante 'R' della Vespa 50, telaio V5A1T con numerazione dedicata (700001+), distinta dalla 50 N."),
        ("Vespa 50 Special", "vespa-50-special-verificata", 1969, 1983, "50 cc",
         "Vespa 50 Special, telai V5A2T/V5B1T/V5B3T secondo l'anno."),
        ("Vespa 50 Elestart", "vespa-50-elestart", 1969, 1977, "50 cc",
         "Versione con avviamento elettrico della Vespa 50, telai V5A3T/V5B2T/V5B4T secondo l'anno."),
        ("Vespa 50 S", "vespa-50-s", 1963, 1972, "50 cc",
         "Vespa 50 S, telaio V5SA1T."),
        ("Vespa 50 SS", "vespa-50-ss", 1965, 1972, "50 cc",
         "Vespa 50 SS sportiva, telaio V5SS1T."),
        ("Vespa 50 Sprinter (50SR)", "vespa-50-sprinter", 1971, 1979, "50 cc",
         "Vespa 50 Sprinter / 50SR, telaio V5SS2T."),
        ("Vespa PX 80 Arcobaleno Elestart", "vespa-px-80-arcobaleno", 1984, 1984, "80 cc",
         "Serie Arcobaleno PX80 Elestart, telaio V8X1T. Solo numero di partenza documentato."),
        ("Vespa 90 SS", "vespa-90-ss", 1965, 1971, "90 cc",
         "Vespa 90 SS, telaio V9SS1T."),
        ("Vespa 90 Racer", "vespa-90-racer", 1971, 1974, "90 cc",
         "Vespa 90 Racer, telaio V9SS2T."),
        ("Vespa 100", "vespa-100-verificata", 1978, 1983, "100 cc",
         "Vespa 100, telaio V9B1T."),
        ("Vespa PX 100 E", "vespa-px-100-e", 1983, 1984, "100 cc",
         "Vespa PX100E, telaio VIX1T."),

        # --- Vespa 125, serie storiche 1948-1969 (una per ciascuna evoluzione di telaio) ---
        ("Vespa 125 (V1T-V15T)", "vespa-125-v1t-v15t", 1948, 1950, "125 cc",
         "Prima serie Vespa 125, telai V1T-V15T."),
        ("Vespa 125 (V30T-V33T)", "vespa-125-v30t-v33t", 1950, 1952, "125 cc",
         "Evoluzione della prima serie 125, telai V30T-V33T."),
        ("Vespa 125 (VM1T)", "vespa-125-vm1t", 1952, 1953, "125 cc",
         "Vespa 125, telaio VM1T."),
        ("Vespa 125 U (VU1T)", "vespa-125-u-vu1t", 1953, 1953, "125 cc",
         "Vespa 125 U (economica), telaio VU1T."),
        ("Vespa 125 (VM2T)", "vespa-125-vm2t", 1953, 1954, "125 cc",
         "Vespa 125, telaio VM2T."),
        ("Vespa 125 (VN1T)", "vespa-125-vn1t", 1954, 1955, "125 cc",
         "Vespa 125, telaio VN1T."),
        ("Vespa 125 (VN2T)", "vespa-125-vn2t", 1956, 1957, "125 cc",
         "Vespa 125, telaio VN2T."),
        ("Vespa 125 (VNA1T)", "vespa-125-vna1t", 1957, 1958, "125 cc",
         "Vespa 125, telaio VNA1T."),
        ("Vespa 125 (VNA2T)", "vespa-125-vna2t", 1958, 1959, "125 cc",
         "Vespa 125, telaio VNA2T."),
        ("Vespa 125 (VNB1T)", "vespa-125-vnb1t", 1959, 1961, "125 cc",
         "Vespa 125, telaio VNB1T."),
        ("Vespa 125 (VNB2T)", "vespa-125-vnb2t", 1961, 1961, "125 cc",
         "Vespa 125, telaio VNB2T."),
        ("Vespa 125 (VNB3T)", "vespa-125-vnb3t", 1961, 1962, "125 cc",
         "Vespa 125, telaio VNB3T."),
        ("Vespa 125 (VNB4T)", "vespa-125-vnb4t", 1962, 1963, "125 cc",
         "Vespa 125, telaio VNB4T."),
        ("Vespa 125 (VNB5T)", "vespa-125-vnb5t", 1963, 1964, "125 cc",
         "Vespa 125, telaio VNB5T."),
        ("Vespa 125 (VNB6T)", "vespa-125-vnb6t", 1964, 1966, "125 cc",
         "Vespa 125, telaio VNB6T."),
        ("Vespa 125 Super (VNC1T)", "vespa-125-super-vnc1t", 1965, 1969, "125 cc",
         "Vespa 125 Super, telaio VNC1T (non va confusa con la successiva 'Vespa 125 Super VMA/VMB')."),

        ("Vespa 125 GT / Sprint (VNL2T)", "vespa-125-gt-sprint", 1966, 1973, "125 cc",
         "Vespa 125 GT e Sprint, telaio VNL2T (numerazione dedicata, distinta dalla GTR)."),
        ("Vespa 125 GTR (VNL2T)", "vespa-125-gtr", 1968, 1982, "125 cc",
         "Vespa 125 GTR, telaio VNL2T con numerazione dedicata (100001+), distinta da GT/Sprint."),
        ("Vespa 125 TS", "vespa-125-ts-verificata", 1975, 1978, "125 cc",
         "Vespa 125 TS, telaio VNL3T."),
        ("Vespa P125X (VNX1T)", "vespa-p125x", 1977, 1982, "125 cc",
         "Vespa P125X, telaio VNX1T, predecessore della PX125E."),
        ("Vespa PX 125 E / EFL (VNX2T)", "vespa-px125e", 1981, 1987, "125 cc",
         "Vespa PX125E e versione Arcobaleno, telaio VNX2T."),
        ("Vespa PX 125 E Arcobaleno Elestart", "vespa-px125e-arcobaleno-elestart", 1984, 1984, "125 cc",
         "Vespa PX125E Arcobaleno con avviamento elettrico, telaio VNX2T. Solo numero di partenza documentato."),
        ("Vespa PX 125 T5 (VNX5T)", "vespa-px125-t5-verificata", 1985, 1986, "125 cc",
         "Vespa PX125 T5, telaio VNX5T. Solo numeri di partenza documentati."),

        ("Vespa Allstate (USA, Sears)", "vespa-allstate-usa", 1951, 1965, "125-150 cc",
         "Vespa venduta negli USA con marchio Sears Allstate. Corrispondenza anno/telaio/numero di catalogo Sears "
         "nota (VA1T 1951 - VA14T 1965), ma senza range seriali numerici documentati."),
        ("Vespa S (VNS1T-VNS6T)", "vespa-s-vns", 1959, 1965, "125-150 cc",
         "Serie poco documentata; nota la corrispondenza anno/telaio (VNS1T 1959 - VNS6T 1965) ma senza range "
         "seriali numerici documentati."),

        ("Vespa 150 (VL/VB/VBA/VBB)", "vespa-150-classic-verificata", 1954, 1965, "150 cc",
         "Evoluzione della Vespa 150 attraverso i telai VL1T, VL2T, VL3T, VB1T, VBA1T, VBB1T, VBB2T."),
        ("Vespa 150 Super (VBC1T)", "vespa-150-super-vbc1t", 1965, 1979, "150 cc",
         "Vespa 150 Super, telaio VBC1T, prodotta per 15 anni con numerazione continua."),
        ("Vespa 150 GL / Sprint (VGL-VLB1T)", "vespa-150-gl-sprint-verificata", 1957, 1974, "150 cc",
         "Evoluzione dalla GL alla Sprint: telai VGL1T, VGLA1T, VGLB1T, VLA1T, VLB1T (dal 050001 al 051523 il "
         "prefisso è eccezionalmente VLB2T)."),
        ("Vespa 150 Sprint Veloce (VLB1T)", "vespa-150-sprint-veloce-verificata", 1969, 1979, "150 cc",
         "Vespa 150 Sprint Veloce, telaio VLB1T con numerazione dedicata (0150001+), distinta dalla Sprint standard."),
        ("Vespa P150S (VBX1T)", "vespa-p150s", 1978, 1984, "150 cc",
         "Vespa P150S, telaio VBX1T."),
        ("Vespa P150X, gamma completa (VBX1T)", "vespa-p150x-full", 1978, 1990, "150 cc",
         "Vespa P150X, telaio VBX1T, numerazione complessiva 1978-1990."),
        ("Vespa P150X / PX150E / Arcobaleno EFL (VLX1T)", "vespa-p150x-px150e", 1978, 1984, "150 cc",
         "Vespa P150X, PX150E e versione Arcobaleno EFL, telaio VLX1T."),
        ("Vespa PX 150 Arcobaleno Elestart (VLX1T)", "vespa-px150-arcobaleno-elestart", 1984, 1984, "150 cc",
         "Vespa PX150 Arcobaleno con avviamento elettrico, telaio VLX1T. Solo numero di partenza documentato."),

        ("Vespa 150 GS - 160 GS (VS1T-VS5T, VSB1T)", "vespa-150gs-160gs-verificata", 1955, 1964, "150-160 cc",
         "Evoluzione della GS 150 (VS1T-VS5T) e successiva GS 160 (VSB1T)."),
        ("Vespa 180 SS (VSC1T)", "vespa-180-ss-vsc1t", 1964, 1968, "180 cc",
         "Vespa 180 Super Sport, telaio VSC1T."),
        ("Vespa 180 Rally (VSD1T)", "vespa-180-rally-verificata", 1968, 1973, "180 cc",
         "Vespa 180 Rally, telaio VSD1T."),
        ("Vespa 200 Rally (VSE1T)", "vespa-200-rally-verificata", 1972, 1979, "200 cc",
         "Vespa 200 Rally, telaio VSE1T."),
        ("Vespa P200X / PX200E / Arcobaleno EFL (VSX1T)", "vespa-p200x-px200e", 1977, 1986, "200 cc",
         "Vespa P200X, PX200E e versione Arcobaleno EFL, telaio VSX1T. Dal 1984 al 1986 numerazione 184911-195545 "
         "più una seconda serie aperta da 312000 in poi."),
        ("Vespa PX 200 E Arcobaleno Elestart (VSX1T)", "vespa-px200e-arcobaleno-elestart", 1981, 1990, "200 cc",
         "Vespa PX200E Arcobaleno con avviamento elettrico, telaio VSX1T."),
    ]

    cursor.executemany(
        "INSERT OR IGNORE INTO vespa_models (name, slug, production_start, production_end, displacement_cc, description) VALUES (?, ?, ?, ?, ?, ?)",
        real_models
    )
    conn.commit()
    cursor.execute("SELECT id, slug FROM vespa_models")
    model_ids.update({row[1]: row[0] for row in cursor.fetchall()})

    real_chassis_data = [
        # (slug, start, end, year_start, year_end, notes)

        # Vespa 50 N (V5A1T)
        ("vespa-50-n", "1001", "6960", 1963, 1963, "Telaio V5A1T"),
        ("vespa-50-n", "6961", "61346", 1964, 1964, "Telaio V5A1T"),
        ("vespa-50-n", "61347", "92876", 1965, 1965, "Telaio V5A1T"),
        ("vespa-50-n", "92877", "101576", 1965, 1965, "Telaio V5A1T"),
        ("vespa-50-n", "101577", "155460", 1966, 1966, "Telaio V5A1T"),
        ("vespa-50-n", "155461", "190977", 1967, 1967, "Telaio V5A1T"),
        ("vespa-50-n", "200001", "213546", 1967, 1967, "Telaio V5A1T"),
        ("vespa-50-n", "213547", "248333", 1968, 1968, "Telaio V5A1T"),
        ("vespa-50-n", "248334", "275620", 1969, 1969, "Telaio V5A1T"),
        ("vespa-50-n", "275621", "280997", 1970, 1970, "Telaio V5A1T"),
        ("vespa-50-n", "280998", "283299", 1971, 1971, "Telaio V5A1T"),

        # Vespa 50 R (V5A1T, numerazione dedicata)
        ("vespa-50-r", "700001", "702503", 1969, 1969, "Telaio V5A1T (serie 50/R)"),
        ("vespa-50-r", "702504", "735716", 1970, 1970, "Telaio V5A1T (serie 50/R)"),
        ("vespa-50-r", "735717", "769612", 1971, 1971, "Telaio V5A1T (serie 50/R)"),
        ("vespa-50-r", "769613", "938761", 1972, 1983, "Telaio V5A1T (serie 50/R)"),

        # Vespa 50 Special (V5A2T / V5B1T / V5B3T)
        ("vespa-50-special-verificata", "1001", "2015", 1969, 1969, "Telaio V5A2T"),
        ("vespa-50-special-verificata", "2016", "34257", 1970, 1970, "Telaio V5A2T"),
        ("vespa-50-special-verificata", "34258", "96013", 1971, 1971, "Telaio V5A2T"),
        ("vespa-50-special-verificata", "1001", "95671", 1972, 1975, "Telaio V5B1T"),
        ("vespa-50-special-verificata", "1001", "565056", 1975, 1983, "Telaio V5B3T"),

        # Vespa 50 Elestart (V5A3T / V5B2T / V5B4T)
        ("vespa-50-elestart", "1001", "1020", 1969, 1969, "Telaio V5A3T"),
        ("vespa-50-elestart", "1021", "3696", 1970, 1970, "Telaio V5A3T"),
        ("vespa-50-elestart", "3697", "4833", 1971, 1971, "Telaio V5A3T"),
        ("vespa-50-elestart", "4834", "5708", 1972, 1972, "Telaio V5B2T"),
        ("vespa-50-elestart", "1001", "3667", 1972, 1977, "Telaio V5B4T"),

        # Vespa 50 S (V5SA1T)
        ("vespa-50-s", "1101", "2104", 1963, 1963, "Telaio V5SA1T"),
        ("vespa-50-s", "2105", "10479", 1964, 1964, "Telaio V5SA1T"),
        ("vespa-50-s", "10480", "15001", 1965, 1965, "Telaio V5SA1T"),
        ("vespa-50-s", "15002", "15324", 1966, 1966, "Telaio V5SA1T"),
        ("vespa-50-s", "15325", "20424", 1966, 1966, "Telaio V5SA1T"),
        ("vespa-50-s", "20425", "30964", 1967, 1967, "Telaio V5SA1T"),
        ("vespa-50-s", "30965", "31000", 1968, 1968, "Telaio V5SA1T"),
        ("vespa-50-s", "31001", "35604", 1968, 1968, "Telaio V5SA1T"),
        ("vespa-50-s", "35605", "40250", 1969, 1969, "Telaio V5SA1T"),
        ("vespa-50-s", "40251", "45599", 1970, 1970, "Telaio V5SA1T"),
        ("vespa-50-s", "45600", "48980", 1971, 1971, "Telaio V5SA1T"),
        ("vespa-50-s", "48981", "148270", 1972, 1972, "Telaio V5SA1T"),

        # Vespa 50 SS (V5SS1T)
        ("vespa-50-ss", "1001", "1192", 1965, 1965, "Telaio V5SS1T"),
        ("vespa-50-ss", "1193", "2207", 1966, 1966, "Telaio V5SS1T"),
        ("vespa-50-ss", "2208", "2397", 1967, 1967, "Telaio V5SS1T"),
        ("vespa-50-ss", "2398", "2793", 1968, 1968, "Telaio V5SS1T"),
        ("vespa-50-ss", "2794", "3089", 1969, 1969, "Telaio V5SS1T"),
        ("vespa-50-ss", "3090", "3422", 1970, 1970, "Telaio V5SS1T"),
        ("vespa-50-ss", "3423", "3525", 1971, 1971, "Telaio V5SS1T"),
        ("vespa-50-ss", "3526", "4525", 1972, 1972, "Telaio V5SS1T"),

        # Vespa 50 Sprinter / 50SR (V5SS2T)
        ("vespa-50-sprinter", "4001", "4160", 1971, 1971, "Telaio V5SS2T"),
        ("vespa-50-sprinter", "4161", "4515", 1972, 1972, "Telaio V5SS2T"),
        ("vespa-50-sprinter", "4516", "10579", 1973, 1979, "Telaio V5SS2T"),

        # Vespa PX 80 Arcobaleno Elestart (V8X1T) - solo inizio noto
        ("vespa-px-80-arcobaleno", "3000001", None, 1984, 1984, "Telaio V8X1T, fine range non documentata"),

        # Vespa 90 (V9A1T)
        ("vespa-90", "1001", "2984", 1963, 1963, "Telaio V9A1T"),
        ("vespa-90", "2985", "17549", 1964, 1964, "Telaio V9A1T"),
        ("vespa-90", "17550", "21544", 1965, 1965, "Telaio V9A1T"),
        ("vespa-90", "21545", "24130", 1966, 1966, "Telaio V9A1T"),
        ("vespa-90", "24131", "25000", 1967, 1967, "Telaio V9A1T"),
        ("vespa-90", "25001", "28000", 1967, 1967, "Telaio V9A1T"),
        ("vespa-90", "28001", "28382", 1967, 1967, "Telaio V9A1T"),
        ("vespa-90", "28383", "32255", 1968, 1968, "Telaio V9A1T"),
        ("vespa-90", "32256", "36966", 1969, 1969, "Telaio V9A1T"),
        ("vespa-90", "36967", "44721", 1970, 1970, "Telaio V9A1T"),
        ("vespa-90", "44722", "52905", 1971, 1971, "Telaio V9A1T"),
        ("vespa-90", "52906", "300026", 1972, 1978, "Telaio V9A1T"),

        # Vespa 90 SS (V9SS1T)
        ("vespa-90-ss", "1001", "2262", 1965, 1965, "Telaio V9SS1T"),
        ("vespa-90-ss", "2263", "4876", 1966, 1966, "Telaio V9SS1T"),
        ("vespa-90-ss", "4877", "5026", 1967, 1967, "Telaio V9SS1T"),
        ("vespa-90-ss", "5027", "5401", 1968, 1968, "Telaio V9SS1T"),
        ("vespa-90-ss", "5402", "5678", 1969, 1969, "Telaio V9SS1T"),
        ("vespa-90-ss", "5679", "6138", 1970, 1970, "Telaio V9SS1T"),
        ("vespa-90-ss", "6139", "6309", 1971, 1971, "Telaio V9SS1T"),

        # Vespa 90 Racer (V9SS2T)
        ("vespa-90-racer", "7001", "7360", 1971, 1971, "Telaio V9SS2T"),
        ("vespa-90-racer", "7361", "10516", 1972, 1974, "Telaio V9SS2T"),

        # Vespa 98 (V98) - integra il modello esistente con il range reale documentato
        ("vespa-98", "01", "18079", 1946, 1947, "Telaio V98 (range reale documentato)"),

        # Vespa 100 (V9B1T)
        ("vespa-100-verificata", "1101", "28904", 1978, 1983, "Telaio V9B1T"),

        # Vespa PX 100 E (VIX1T)
        ("vespa-px-100-e", "1101", "11104", 1983, 1983, "Telaio VIX1T"),
        ("vespa-px-100-e", "11105", None, 1984, 1984, "Telaio VIX1T, fine range non documentata"),

        # Vespa 125 Nuova (VMA1T) - integra il modello esistente
        ("vespa-nuova-125", "01001", "08392", 1965, 1965, "Telaio VMA1T (range reale documentato)"),
        ("vespa-nuova-125", "08393", "014781", 1966, 1966, "Telaio VMA1T (range reale documentato)"),
        ("vespa-nuova-125", "014782", "018100", 1967, 1967, "Telaio VMA1T (range reale documentato)"),

        # Vespa 125 Primavera (VMA2T) - integra il modello esistente
        ("vespa-primavera-125", "020001", "022874", 1967, 1967, "Telaio VMA2T (range reale documentato)"),
        ("vespa-primavera-125", "022875", "031548", 1968, 1968, "Telaio VMA2T (range reale documentato)"),
        ("vespa-primavera-125", "031549", "036266", 1969, 1969, "Telaio VMA2T (range reale documentato)"),
        ("vespa-primavera-125", "036267", "042299", 1970, 1970, "Telaio VMA2T (range reale documentato)"),
        ("vespa-primavera-125", "042300", "049703", 1971, 1971, "Telaio VMA2T (range reale documentato)"),
        ("vespa-primavera-125", "049704", "0240329", 1972, 1983, "Telaio VMA2T (range reale documentato)"),

        # Vespa 125 Primavera ET3 (VMB1T) - integra il modello esistente
        ("vespa-primavera-et3", "1101", "150143", 1976, 1983, "Telaio VMB1T (range reale documentato)"),

        # Vespa 125, serie storiche 1948-1969
        ("vespa-125-v1t-v15t", "01", "104096", 1948, 1950, "Telaio V1T-V15T"),
        ("vespa-125-v30t-v33t", "104097", "251820", 1950, 1952, "Telaio V30T-V33T"),
        ("vespa-125-vm1t", "01001", "08830", 1952, 1952, "Telaio VM1T"),
        ("vespa-125-vm1t", "08831", "085870", 1953, 1953, "Telaio VM1T"),
        ("vespa-125-u-vu1t", "1001", "7001", 1953, 1953, "Telaio VU1T (Vespa U)"),
        ("vespa-125-vm2t", "085871", "0100619", 1953, 1953, "Telaio VM2T"),
        ("vespa-125-vm2t", "0100620", "0176014", 1954, 1954, "Telaio VM2T"),
        ("vespa-125-vn1t", "01001", "023000", 1954, 1954, "Telaio VN1T"),
        ("vespa-125-vn1t", "023001", "050100", 1955, 1955, "Telaio VN1T"),
        ("vespa-125-vn2t", "050101", "096569", 1956, 1956, "Telaio VN2T"),
        ("vespa-125-vn2t", "096570", "0125600", 1957, 1957, "Telaio VN2T"),
        ("vespa-125-vna1t", "01001", "010300", 1957, 1957, "Telaio VNA1T"),
        ("vespa-125-vna1t", "010301", "068031", 1958, 1958, "Telaio VNA1T"),
        ("vespa-125-vna2t", "068032", "0107007", 1958, 1958, "Telaio VNA2T"),
        ("vespa-125-vna2t", "0107008", "0116431", 1959, 1959, "Telaio VNA2T"),
        ("vespa-125-vnb1t", "01001", "016275", 1959, 1959, "Telaio VNB1T"),
        ("vespa-125-vnb1t", "016276", "080686", 1960, 1960, "Telaio VNB1T"),
        ("vespa-125-vnb1t", "080687", "089850", 1961, 1961, "Telaio VNB1T"),
        ("vespa-125-vnb2t", "01001", "038699", 1961, 1961, "Telaio VNB2T"),
        ("vespa-125-vnb3t", "034700", "054414", 1961, 1961, "Telaio VNB3T"),
        ("vespa-125-vnb3t", "054415", "090395", 1962, 1962, "Telaio VNB3T"),
        ("vespa-125-vnb4t", "090396", "099700", 1962, 1962, "Telaio VNB4T"),
        ("vespa-125-vnb4t", "099701", "0136485", 1963, 1963, "Telaio VNB4T"),
        ("vespa-125-vnb5t", "01001", "07070", 1963, 1963, "Telaio VNB5T"),
        ("vespa-125-vnb5t", "07071", "043240", 1964, 1964, "Telaio VNB5T"),
        ("vespa-125-vnb6t", "01001", "07455", 1964, 1964, "Telaio VNB6T"),
        ("vespa-125-vnb6t", "07456", "035439", 1965, 1965, "Telaio VNB6T"),
        ("vespa-125-vnb6t", "035440", "037028", 1966, 1966, "Telaio VNB6T (trascrizione originale ambigua: 'VNB67')"),
        ("vespa-125-super-vnc1t", "01001", "04420", 1965, 1965, "Telaio VNC1T (Super)"),
        ("vespa-125-super-vnc1t", "04421", "019044", 1966, 1966, "Telaio VNC1T (Super)"),
        ("vespa-125-super-vnc1t", "019045", "023745", 1967, 1967, "Telaio VNC1T (Super)"),
        ("vespa-125-super-vnc1t", "023746", "025076", 1968, 1968, "Telaio VNC1T (Super)"),
        ("vespa-125-super-vnc1t", "025077", "025146", 1969, 1969, "Telaio VNC1T (Super)"),

        # Vespa 125 GT / Sprint (VNL2T)
        ("vespa-125-gt-sprint", "30001", "35763", 1966, 1966, "Telaio VNL2T (GT/Sprint)"),
        ("vespa-125-gt-sprint", "35764", "54602", 1967, 1967, "Telaio VNL2T (GT/Sprint)"),
        ("vespa-125-gt-sprint", "54603", "65401", 1968, 1968, "Telaio VNL2T (GT/Sprint)"),
        ("vespa-125-gt-sprint", "65402", "69847", 1969, 1969, "Telaio VNL2T (GT/Sprint)"),
        ("vespa-125-gt-sprint", "69848", "73613", 1970, 1970, "Telaio VNL2T (GT/Sprint)"),
        ("vespa-125-gt-sprint", "73614", "75821", 1971, 1971, "Telaio VNL2T (GT/Sprint)"),
        ("vespa-125-gt-sprint", "75822", "81582", 1972, 1973, "Telaio VNL2T (GT/Sprint)"),

        # Vespa 125 GTR (VNL2T, numerazione dedicata 100001+)
        ("vespa-125-gtr", "100001", "100751", 1968, 1968, "Telaio VNL2T (GTR)"),
        ("vespa-125-gtr", "100752", "107340", 1969, 1969, "Telaio VNL2T (GTR)"),
        ("vespa-125-gtr", "107341", "112897", 1970, 1970, "Telaio VNL2T (GTR)"),
        ("vespa-125-gtr", "112898", "117898", 1971, 1971, "Telaio VNL2T (GTR)"),
        ("vespa-125-gtr", "117899", "151788", 1972, 1982, "Telaio VNL2T (GTR)"),

        # Vespa 125 TS (VNL3T)
        ("vespa-125-ts-verificata", "1101", "29804", 1975, 1978, "Telaio VNL3T"),

        # Vespa P125X (VNX1T)
        ("vespa-p125x", "1101", "5004", 1977, 1977, "Telaio VNX1T"),
        ("vespa-p125x", "5005", "32785", 1978, 1978, "Telaio VNX1T"),
        ("vespa-p125x", "32786", "74935", 1979, 1979, "Telaio VNX1T"),
        ("vespa-p125x", "74936", "130379", 1980, 1980, "Telaio VNX1T"),
        ("vespa-p125x", "130380", "195563", 1981, 1981, "Telaio VNX1T"),
        ("vespa-p125x", "195564", "198248", 1982, 1982, "Telaio VNX1T"),

        # Vespa PX 125 E / EFL (VNX2T)
        ("vespa-px125e", "1101", "11295", 1981, 1981, "Telaio VNX2T"),
        ("vespa-px125e", "11296", "87953", 1982, 1982, "Telaio VNX2T"),
        ("vespa-px125e", "87954", "135401", 1983, 1983, "Telaio VNX2T"),
        ("vespa-px125e", "200001", "214890", 1983, 1983, "Telaio VNX2T (serie Arcobaleno)"),
        ("vespa-px125e", "214891", "243846", 1984, 1984, "Telaio VNX2T (serie Arcobaleno)"),
        ("vespa-px125e", "243847", "264193", 1985, 1985, "Telaio VNX2T (serie Arcobaleno)"),
        ("vespa-px125e", "264194", "278043", 1986, 1986, "Telaio VNX2T (serie Arcobaleno)"),
        ("vespa-px125e", "278044", "281514", 1987, 1987, "Telaio VNX2T (serie Arcobaleno)"),

        # Vespa PX 125 E Arcobaleno Elestart (VNX2T) - solo inizio noto
        ("vespa-px125e-arcobaleno-elestart", "3000001", None, 1984, 1984, "Telaio VNX2T, fine range non documentata"),

        # Vespa PX 125 T5 (VNX5T) - solo inizio noto
        ("vespa-px125-t5-verificata", "1101", None, 1985, 1985, "Telaio VNX5T (trascrizione originale ambigua: 'VNXST'), fine range non documentata"),
        ("vespa-px125-t5-verificata", "3000001", None, 1986, 1986, "Telaio VNX5T (Elestart), fine range non documentata"),

        # Vespa 150 (VL1T, VL2T, VL3T, VB1T, VBA1T, VBB1T, VBB2T)
        ("vespa-150-classic-verificata", "1001", "8173", 1954, 1954, "Telaio VL1T"),
        ("vespa-150-classic-verificata", "8174", "17000", 1955, 1955, "Telaio VL1T"),
        ("vespa-150-classic-verificata", "17001", "64970", 1955, 1955, "Telaio VL2T"),
        ("vespa-150-classic-verificata", "64971", "93101", 1956, 1956, "Telaio VL2T"),
        ("vespa-150-classic-verificata", "93102", "130693", 1956, 1956, "Telaio VL3T"),
        ("vespa-150-classic-verificata", "130694", "132737", 1957, 1957, "Telaio VL3T"),
        ("vespa-150-classic-verificata", "1001", "55375", 1957, 1957, "Telaio VB1T"),
        ("vespa-150-classic-verificata", "55376", "99700", 1958, 1958, "Telaio VB1T"),
        ("vespa-150-classic-verificata", "1001", "16515", 1958, 1958, "Telaio VBA1T"),
        ("vespa-150-classic-verificata", "16516", "88519", 1959, 1959, "Telaio VBA1T"),
        ("vespa-150-classic-verificata", "88520", "125040", 1960, 1960, "Telaio VBA1T"),
        ("vespa-150-classic-verificata", "1001", "16070", 1960, 1960, "Telaio VBB1T"),
        ("vespa-150-classic-verificata", "16071", "96683", 1961, 1961, "Telaio VBB1T"),
        ("vespa-150-classic-verificata", "96684", "146000", 1962, 1962, "Telaio VBB1T"),
        ("vespa-150-classic-verificata", "146001", "155712", 1962, 1962, "Telaio VBB2T"),
        ("vespa-150-classic-verificata", "155713", "198232", 1963, 1963, "Telaio VBB2T"),
        ("vespa-150-classic-verificata", "198233", "240757", 1964, 1964, "Telaio VBB2T"),
        ("vespa-150-classic-verificata", "240758", "273260", 1965, 1965, "Telaio VBB2T"),

        # Vespa 150 Super (VBC1T)
        ("vespa-150-super-vbc1t", "1001", "4295", 1965, 1965, "Telaio VBC1T"),
        ("vespa-150-super-vbc1t", "4296", "43413", 1966, 1966, "Telaio VBC1T"),
        ("vespa-150-super-vbc1t", "43414", "61496", 1967, 1967, "Telaio VBC1T"),
        ("vespa-150-super-vbc1t", "61497", "80740", 1968, 1968, "Telaio VBC1T"),
        ("vespa-150-super-vbc1t", "80741", "100493", 1969, 1969, "Telaio VBC1T"),
        ("vespa-150-super-vbc1t", "100494", "125619", 1970, 1970, "Telaio VBC1T"),
        ("vespa-150-super-vbc1t", "125620", "151299", 1971, 1971, "Telaio VBC1T"),
        ("vespa-150-super-vbc1t", "151300", "182205", 1972, 1972, "Telaio VBC1T"),
        ("vespa-150-super-vbc1t", "182206", "221194", 1973, 1973, "Telaio VBC1T"),
        ("vespa-150-super-vbc1t", "221195", "280314", 1974, 1974, "Telaio VBC1T"),
        ("vespa-150-super-vbc1t", "280315", "351374", 1975, 1975, "Telaio VBC1T"),
        ("vespa-150-super-vbc1t", "351375", "409392", 1976, 1976, "Telaio VBC1T"),
        ("vespa-150-super-vbc1t", "409393", "476737", 1977, 1977, "Telaio VBC1T"),
        ("vespa-150-super-vbc1t", "476738", "550121", 1978, 1978, "Telaio VBC1T"),
        ("vespa-150-super-vbc1t", "550122", "554808", 1979, 1979, "Telaio VBC1T"),

        # Vespa 150 GL / Sprint (VGL1T, VGLA1T, VGLB1T, VLA1T, VLB1T)
        ("vespa-150-gl-sprint-verificata", "01001", "010842", 1957, 1957, "Telaio VGL1T"),
        ("vespa-150-gl-sprint-verificata", "010843", "016610", 1958, 1958, "Telaio VGL1T"),
        ("vespa-150-gl-sprint-verificata", "01001", "016000", 1959, 1959, "Telaio VGLA1T"),
        ("vespa-150-gl-sprint-verificata", "016001", "031227", 1960, 1960, "Telaio VGLA1T"),
        ("vespa-150-gl-sprint-verificata", "031228", "035267", 1961, 1961, "Telaio VGLA1T"),
        ("vespa-150-gl-sprint-verificata", "035268", "043000", 1961, 1961, "Telaio VGLB1T"),
        ("vespa-150-gl-sprint-verificata", "043001", "048294", 1962, 1962, "Telaio VGLB1T"),
        ("vespa-150-gl-sprint-verificata", "01001", "05958", 1962, 1962, "Telaio VLA1T"),
        ("vespa-150-gl-sprint-verificata", "05959", "057103", 1963, 1963, "Telaio VLA1T"),
        ("vespa-150-gl-sprint-verificata", "057104", "078009", 1964, 1964, "Telaio VLA1T"),
        ("vespa-150-gl-sprint-verificata", "078010", "080855", 1965, 1965, "Telaio VLA1T"),
        ("vespa-150-gl-sprint-verificata", "01001", "026478", 1965, 1965, "Telaio VLB1T (inizio Sprint)"),
        ("vespa-150-gl-sprint-verificata", "026479", "039230", 1966, 1966, "Telaio VLB1T"),
        ("vespa-150-gl-sprint-verificata", "039231", "063336", 1967, 1967, "Telaio VLB1T (dal 050001 al 051523 il prefisso è VLB2T)"),
        ("vespa-150-gl-sprint-verificata", "063337", "089260", 1968, 1968, "Telaio VLB1T"),
        ("vespa-150-gl-sprint-verificata", "089261", "0108325", 1969, 1969, "Telaio VLB1T"),
        ("vespa-150-gl-sprint-verificata", "0108326", "0132259", 1970, 1970, "Telaio VLB1T"),
        ("vespa-150-gl-sprint-verificata", "0132260", "1150937", 1971, 1971, "Telaio VLB1T"),
        ("vespa-150-gl-sprint-verificata", "1150937", "1205477", 1972, 1974, "Telaio VLB1T"),

        # Vespa 150 Sprint Veloce (VLB1T, numerazione dedicata 0150001+)
        ("vespa-150-sprint-veloce-verificata", "0150001", "0154384", 1969, 1969, "Telaio VLB1T (Sprint Veloce)"),
        ("vespa-150-sprint-veloce-verificata", "0154385", "0159754", 1970, 1970, "Telaio VLB1T (Sprint Veloce)"),
        ("vespa-150-sprint-veloce-verificata", "0159755", "0164041", 1971, 1971, "Telaio VLB1T (Sprint Veloce)"),
        ("vespa-150-sprint-veloce-verificata", "164042", "169331", 1972, 1972, "Telaio VLB1T (Sprint Veloce)"),
        ("vespa-150-sprint-veloce-verificata", "169332", "173345", 1973, 1973, "Telaio VLB1T (Sprint Veloce)"),
        ("vespa-150-sprint-veloce-verificata", "173346", "213336", 1974, 1974, "Telaio VLB1T (Sprint Veloce)"),
        ("vespa-150-sprint-veloce-verificata", "213337", "248469", 1975, 1975, "Telaio VLB1T (Sprint Veloce)"),
        ("vespa-150-sprint-veloce-verificata", "248470", "294169", 1976, 1976, "Telaio VLB1T (Sprint Veloce)"),
        ("vespa-150-sprint-veloce-verificata", "294170", "349628", 1977, 1977, "Telaio VLB1T (Sprint Veloce)"),
        ("vespa-150-sprint-veloce-verificata", "349629", "367672", 1978, 1978, "Telaio VLB1T (Sprint Veloce)"),
        ("vespa-150-sprint-veloce-verificata", "367673", "368119", 1979, 1979, "Telaio VLB1T (Sprint Veloce)"),

        # Vespa P150S (VBX1T)
        ("vespa-p150s", "1101", "10819", 1978, 1978, "Telaio VBX1T"),
        ("vespa-p150s", "10280", "52138", 1979, 1979, "Telaio VBX1T"),
        ("vespa-p150s", "52139", "85966", 1980, 1980, "Telaio VBX1T"),
        ("vespa-p150s", "85967", "170765", 1981, 1981, "Telaio VBX1T"),
        ("vespa-p150s", "170766", "203818", 1982, 1982, "Telaio VBX1T"),
        ("vespa-p150s", "203819", "230729", 1983, 1983, "Telaio VBX1T"),
        ("vespa-p150s", "230730", None, 1984, 1984, "Telaio VBX1T, fine range non documentata"),

        # Vespa P150X, gamma completa (VBX1T)
        ("vespa-p150x-full", "1001", "299155", 1978, 1990, "Telaio VBX1T"),

        # Vespa P150X / PX150E / Arcobaleno EFL (VLX1T)
        ("vespa-p150x-px150e", "1101", "67627", 1978, 1978, "Telaio VLX1T"),
        ("vespa-p150x-px150e", "67628", "135880", 1979, 1979, "Telaio VLX1T"),
        ("vespa-p150x-px150e", "135881", "240136", 1980, 1980, "Telaio VLX1T"),
        ("vespa-p150x-px150e", "240137", "346402", 1981, 1981, "Telaio VLX1T"),
        ("vespa-p150x-px150e", "346403", "363301", 1981, 1981, "Telaio VLX1T"),
        ("vespa-p150x-px150e", "363302", "455339", 1982, 1982, "Telaio VLX1T"),
        ("vespa-p150x-px150e", "455340", "503132", 1983, 1983, "Telaio VLX1T"),
        ("vespa-p150x-px150e", "503133", None, 1984, 1984, "Telaio VLX1T, fine range non documentata"),
        ("vespa-p150x-px150e", "600001", "605007", 1983, 1983, "Telaio VLX1T (serie Arcobaleno)"),
        ("vespa-p150x-px150e", "605008", None, 1984, 1984, "Telaio VLX1T (serie Arcobaleno), fine range non documentata"),

        # Vespa PX 150 Arcobaleno Elestart (VLX1T) - solo inizio noto
        ("vespa-px150-arcobaleno-elestart", "3000001", None, 1984, 1984, "Telaio VLX1T, fine range non documentata"),

        # Vespa 150 GS - 160 GS (VS1T-VS5T, VSB1T)
        ("vespa-150gs-160gs-verificata", "001001", "0013300", 1955, 1955, "Telaio VS1T (inizio 150)"),
        ("vespa-150gs-160gs-verificata", "0013301", "0023310", 1956, 1956, "Telaio VS2T"),
        ("vespa-150gs-160gs-verificata", "0023311", "0035310", 1957, 1957, "Telaio VS3T"),
        ("vespa-150gs-160gs-verificata", "0035311", "0047350", 1958, 1958, "Telaio VS4T"),
        ("vespa-150gs-160gs-verificata", "0047351", "0052363", 1958, 1958, "Telaio VS5T"),
        ("vespa-150gs-160gs-verificata", "0052364", "0070128", 1959, 1959, "Telaio VS5T"),
        ("vespa-150gs-160gs-verificata", "0070129", "00104731", 1960, 1960, "Telaio VS5T"),
        ("vespa-150gs-160gs-verificata", "00104732", "00127350", 1961, 1961, "Telaio VS5T"),
        ("vespa-150gs-160gs-verificata", "001001", "0029970", 1962, 1962, "Telaio VSB1T (inizio 160)"),
        ("vespa-150gs-160gs-verificata", "0029971", "00482501", 1963, 1963, "Telaio VSB1T"),
        ("vespa-150gs-160gs-verificata", "0048251", "0061000", 1964, 1964, "Telaio VSB1T"),

        # Vespa 180 SS (VSC1T)
        ("vespa-180-ss-vsc1t", "001001", "003120", 1964, 1964, "Telaio VSC1T"),
        ("vespa-180-ss-vsc1t", "003121", "0019720", 1965, 1965, "Telaio VSC1T"),
        ("vespa-180-ss-vsc1t", "0019721", "0025673", 1966, 1966, "Telaio VSC1T"),
        ("vespa-180-ss-vsc1t", "0025674", "0032632", 1967, 1967, "Telaio VSC1T"),
        ("vespa-180-ss-vsc1t", "0032633", "0036700", 1968, 1968, "Telaio VSC1T"),

        # Vespa 180 Rally (VSD1T)
        ("vespa-180-rally-verificata", "001001", "005328", 1968, 1968, "Telaio VSD1T"),
        ("vespa-180-rally-verificata", "005329", "0011537", 1969, 1969, "Telaio VSD1T"),
        ("vespa-180-rally-verificata", "0011538", "0017810", 1970, 1970, "Telaio VSD1T"),
        ("vespa-180-rally-verificata", "0017811", "0023348", 1971, 1971, "Telaio VSD1T"),
        ("vespa-180-rally-verificata", "0023348", "0027495", 1972, 1973, "Telaio VSD1T"),

        # Vespa 200 Rally (VSE1T)
        ("vespa-200-rally-verificata", "001001", "0042275", 1972, 1979, "Telaio VSE1T"),

        # Vespa P200X / PX200E / Arcobaleno EFL (VSX1T)
        ("vespa-p200x-px200e", "100", "1700", 1977, 1977, "Telaio VSX1T"),
        ("vespa-p200x-px200e", "1101", "2041", 1977, 1977, "Telaio VSX1T"),
        ("vespa-p200x-px200e", "2042", "15227", 1978, 1978, "Telaio VSX1T"),
        ("vespa-p200x-px200e", "15228", "36559", 1979, 1979, "Telaio VSX1T"),
        ("vespa-p200x-px200e", "36560", "73334", 1980, 1980, "Telaio VSX1T"),
        ("vespa-p200x-px200e", "73335", "116614", 1981, 1981, "Telaio VSX1T"),
        ("vespa-p200x-px200e", "116615", "160000", 1982, 1982, "Telaio VSX1T"),
        ("vespa-p200x-px200e", "160001", "165842", 1982, 1982, "Telaio VSX1T"),
        ("vespa-p200x-px200e", "165843", "184910", 1983, 1983, "Telaio VSX1T"),
        ("vespa-p200x-px200e", "184911", "195545", 1984, 1986, "Telaio VSX1T (esiste anche una seconda serie aperta da 312000 in poi)"),
        ("vespa-p200x-px200e", "300001", "304224", 1983, 1983, "Telaio VSX1T (serie Arcobaleno)"),
        ("vespa-p200x-px200e", "304225", None, 1984, 1984, "Telaio VSX1T (serie Arcobaleno), fine range non documentata"),

        # Vespa PX 200 E Arcobaleno Elestart (VSX1T)
        ("vespa-px200e-arcobaleno-elestart", "3000001", "3022538", 1981, 1990, "Telaio VSX1T"),
    ]

    real_chassis_values = []
    for slug, start, end, y_start, y_end, notes in real_chassis_data:
        if slug in model_ids:
            real_chassis_values.append((model_ids[slug], start, end, y_start, y_end, notes))

    cursor.executemany(
        "INSERT INTO vespa_chassis_numbers (model_id, number_start, number_end, year_start, year_end, notes) VALUES (?, ?, ?, ?, ?, ?)",
        real_chassis_values
    )
    conn.commit()

    # =========================================================
    # COLORS
    # =========================================================
    colors_data = [
        # (slug, color_name, hex, year_start, year_end, notes)
        ("vespa-98", "Grigio", "#B0B0B0", 1946, 1947, "Grigio militare originale"),
        ("vespa-98", "Verde", "#3A5F3A", 1946, 1947, "Verde militare"),
        ("vespa-125", "Grigio", "#C0C0C0", 1948, 1950, "Grigio chiaro"),
        ("vespa-125", "Marrone", "#6B3A2A", 1948, 1950, "Marrone scuro"),
        ("vespa-150-gs", "Celeste", "#87CEEB", 1955, 1958, "Celeste Pastello"),
        ("vespa-150-gs", "Rosso", "#CC0000", 1955, 1961, "Rosso GS"),
        ("vespa-150-gs", "Marrone", "#8B5A2B", 1955, 1958, "Marrone scuro"),
        ("vespa-150-gs", "Beige", "#F5F5DC", 1959, 1961, "Beige chiaro"),
        ("vespa-160-gs", "Blu", "#00008B", 1962, 1964, "Blu scuro"),
        ("vespa-160-gs", "Grigio Chiaro", "#D3D3D3", 1962, 1964, "Grigio chiaro metallizzato"),
        ("vespa-160-gs", "Rosso", "#FF0000", 1962, 1964, "Rosso corsa"),
        ("vespa-150-super", "Bianco", "#FFFFFF", 1965, 1970, "Bianco"),
        ("vespa-150-super", "Celeste", "#ADD8E6", 1965, 1970, "Celeste chiaro"),
        ("vespa-150-super", "Arancione", "#FF8C00", 1968, 1970, "Arancione"),
        ("vespa-sprint", "Rosso Sprint", "#E31837", 1965, 1971, "Rosso Sprint classico"),
        ("vespa-sprint", "Celeste Sprint", "#5BA4CF", 1965, 1971, "Celeste Sprint"),
        ("vespa-sprint", "Bianco", "#FFFFFF", 1965, 1971, "Bianco"),
        ("vespa-sprint", "Nero", "#000000", 1969, 1971, "Nero"),
        ("vespa-180-ss", "Rosso", "#CC0000", 1964, 1968, "Rosso SS"),
        ("vespa-180-ss", "Blu Scuro", "#1A1A5E", 1964, 1968, "Blu notte"),
        ("vespa-180-ss", "Argento", "#C0C0C0", 1965, 1968, "Argento metallizzato"),
        ("vespa-50", "Celeste", "#87CEEB", 1963, 1975, "Celeste"),
        ("vespa-50", "Bianco", "#FFFFFF", 1963, 1975, "Bianco"),
        ("vespa-50", "Rosso", "#CC0000", 1963, 1975, "Rosso"),
        ("vespa-50", "Azzurro", "#4F94CD", 1968, 1975, "Azzurro"),
        ("vespa-50-special", "Celeste", "#00BFFF", 1969, 1973, "Celeste Special"),
        ("vespa-50-special", "Arancione", "#FF6347", 1969, 1973, "Arancione Special"),
        ("vespa-50-special", "Verde Mela", "#98FB98", 1970, 1973, "Verde mela"),
        ("vespa-50-special", "Giallo", "#FFD700", 1969, 1973, "Giallo"),
        ("vespa-50-special", "Viola", "#8B008B", 1971, 1973, "Viola metallizzato"),
        ("vespa-primavera-et3", "Azzurro Primavera", "#5B9BD5", 1971, 1975, "Azzurro pastello"),
        ("vespa-primavera-et3", "Verde Primavera", "#7CBA7C", 1971, 1975, "Verde pastello"),
        ("vespa-primavera-et3", "Rosa", "#FFB6C1", 1971, 1975, "Rosa Primavera"),
        ("vespa-primavera-et3", "Bianco", "#FFFFFF", 1971, 1983, "Bianco"),
        ("vespa-primavera-et3", "Giallo", "#F4D03F", 1976, 1983, "Giallo"),
        ("vespa-primavera-et3", "Marrone", "#8B4513", 1976, 1983, "Marrone metallizzato"),
        ("vespa-rally-180", "Rosso Rally", "#DC143C", 1965, 1972, "Rosso Rally classico"),
        ("vespa-rally-180", "Blu Notte", "#191970", 1965, 1972, "Blu notte metallizzato"),
        ("vespa-rally-200", "Argento", "#C0C0C0", 1972, 1976, "Argento metallizzato"),
        ("vespa-rally-200", "Verde Scuro", "#006400", 1972, 1976, "Verde scuro"),
        ("vespa-rally-200", "Rosso", "#DC143C", 1972, 1976, "Rosso Rally"),
        ("vespa-px-125", "Bianco", "#FFFFFF", 1978, 2000, "Bianco PX"),
        ("vespa-px-125", "Rosso", "#E31837", 1978, 2000, "Rosso PX"),
        ("vespa-px-125", "Blu", "#1E90FF", 1978, 2000, "Blu"),
        ("vespa-px-125", "Nero", "#000000", 1978, 2000, "Nero"),
        ("vespa-px-125", "Arancione", "#FF4500", 1985, 1995, "Arancione PX"),
        ("vespa-px-125", "Verde", "#228B22", 1985, 2000, "Verde PX"),
        ("vespa-px-200", "Bianco", "#FFFFFF", 1978, 2016, "Bianco"),
        ("vespa-px-200", "Nero", "#000000", 1978, 2016, "Nero"),
        ("vespa-px-200", "Bordeaux", "#800020", 1995, 2000, "Bordeaux"),
        ("vespa-px-200", "Azzurro Metallizzato", "#5B9BD5", 2000, 2016, "Azzurro metallizzato"),
        ("vespa-t5", "Rosso T5", "#E32636", 1985, 1995, "Rosso T5"),
        ("vespa-t5", "Bianco Perlato", "#F5F5F5", 1985, 1995, "Bianco perlato"),
        ("vespa-t5", "Blu T5", "#000080", 1985, 1995, "Blu T5"),
        ("vespa-t5", "Nero", "#000000", 1985, 1995, "Nero"),
        ("vespa-et4-125", "Bianco", "#FFFFFF", 1996, 2005, "Bianco"),
        ("vespa-et4-125", "Blu ET4", "#4169E1", 1996, 2005, "Blu metallizzato"),
        ("vespa-et4-125", "Rosso", "#CC0000", 1996, 2005, "Rosso"),
        ("vespa-et4-125", "Verde", "#2E8B57", 1998, 2005, "Verde"),
        ("vespa-et4-125", "Giallo", "#FFD700", 1996, 2005, "Giallo"),
        ("vespa-gts-300-super", "Nero", "#000000", 2006, 2015, "Nero"),
        ("vespa-gts-300-super", "Bianco", "#FFFFFF", 2006, 2015, "Bianco"),
        ("vespa-gts-300-super", "Rosso", "#CC0000", 2006, 2015, "Rosso GTS"),
        ("vespa-gts-300-super", "Azzurro", "#5B9BD5", 2008, 2015, "Azzurro metallizzato"),
        ("vespa-gts-300-super", "Grigio", "#808080", 2010, 2015, "Grigio metallizzato"),
        ("vespa-gts-300-super", "Marrone", "#8B4513", 2012, 2015, "Marrone"),
        ("vespa-gtv-300", "Verde GTV", "#2E4A2E", 2006, 2012, "Verde scuro metallizzato"),
        ("vespa-gtv-300", "Beige", "#D2B48C", 2006, 2012, "Beige"),
        ("vespa-gtv-300", "Bordeaux", "#800020", 2006, 2012, "Bordeaux"),
        ("vespa-primavera-2013", "Bianco", "#FFFFFF", 2013, 2020, "Bianco"),
        ("vespa-primavera-2013", "Azzurro", "#87CEEB", 2013, 2020, "Azzurro Primavera"),
        ("vespa-primavera-2013", "Rosso", "#CC0000", 2013, 2020, "Rosso"),
        ("vespa-primavera-2013", "Giallo", "#FFD700", 2013, 2020, "Giallo"),
        ("vespa-primavera-2013", "Verde", "#228B22", 2015, 2020, "Verde"),
        ("vespa-primavera-2013", "Grigio", "#A9A9A9", 2016, 2020, "Grigio"),
        ("vespa-sprint-2014", "Bianco", "#FFFFFF", 2014, 2020, "Bianco"),
        ("vespa-sprint-2014", "Rosso Sprint", "#E31837", 2014, 2020, "Rosso Sprint"),
        ("vespa-sprint-2014", "Nero", "#000000", 2014, 2020, "Nero"),
        ("vespa-sprint-2014", "Grigio", "#A9A9A9", 2014, 2020, "Grigio"),
        ("vespa-sprint-2014", "Blu", "#00008B", 2016, 2020, "Blu notte"),
        ("vespa-gts-300-2019", "Bianco", "#FFFFFF", 2019, 2024, "Bianco"),
        ("vespa-gts-300-2019", "Nero", "#000000", 2019, 2024, "Nero"),
        ("vespa-gts-300-2019", "Grigio", "#808080", 2019, 2024, "Grigio metallizzato"),
        ("vespa-gts-300-2019", "Azzurro", "#5B9BD5", 2019, 2024, "Azzurro"),
        ("vespa-gts-300-2019", "Beige", "#D2B48C", 2019, 2024, "Beige Sabbia"),
        ("vespa-gts-300-2019", "Verde", "#2E4A2E", 2020, 2024, "Verde"),
        ("vespa-gts-300-2019", "Rosso", "#CC0000", 2019, 2024, "Rosso 916"),
        ("vespa-elettrica", "Bianco", "#FFFFFF", 2019, 2024, "Bianco"),
        ("vespa-elettrica", "Nero", "#000000", 2019, 2024, "Nero"),
        ("vespa-elettrica", "Azzurro", "#87CEEB", 2019, 2024, "Azzurro"),
        ("vespa-elettrica", "Giallo", "#FFD700", 2019, 2024, "Giallo"),
    ]

    colors_values = []
    for slug, color, hex_code, y_start, y_end, notes in colors_data:
        if slug in model_ids:
            colors_values.append((model_ids[slug], color, hex_code, y_start, y_end, notes))

    cursor.executemany(
        "INSERT INTO vespa_colors (model_id, color_name, color_hex, year_start, year_end, notes) VALUES (?, ?, ?, ?, ?, ?)",
        colors_values
    )
    conn.commit()

    # =========================================================
    # KNOWN ISSUES
    # =========================================================
    issues_data = [
        # (slug, issue, severity, description)
        ("vespa-98", "Frizione a bagno d'olio usurata", "warning", "La frizione a bagno d'olio tende a usurarsi. Controllare i dischi."),
        ("vespa-98", "Cuscinetti ruota posteriore", "critical", "Cuscinetti sottodimensionati, tendono a grippare. Sostituire con ricambi moderni."),
        ("vespa-125", "Cambio 3 marce rumoroso", "info", "Il cambio a 3 marce è rumoroso di suo, non è un difetto."),
        ("vespa-125", "Guarnizioni carburatore", "warning", "Le guarnizioni in gomma originale si deteriorano con l'età."),
        ("vespa-150-gs", "Testata motore", "warning", "La testata può deformarsi se surriscaldata. Controllare piano di testata."),

        ("vespa-150-super", "Cuscinetti albero motore", "warning", "I cuscinetti originali vanno controllati e sostituiti dopo 40.000 km."),
        ("vespa-150-super", "Pompa carburante", "warning", "La pompa a depressione può perdere tenuta."),
        ("vespa-sprint", "Frizione slitta", "warning", "La frizione tende a slittare su riprese decise. Verificare molle."),
        ("vespa-sprint", "Ammortizzatore posteriore", "info", "Ammortizzatore originale poco efficiente. Upgrade consigliato."),
        ("vespa-180-ss", "Surriscaldamento motore", "warning", "Il motore 180cc tende a surriscaldarsi nel traffico. Controllare raffreddamento."),
        ("vespa-180-ss", "Cuscinetti ruota", "critical", "Cuscinetti ruota da controllare frequentemente. Sostituire con ricambi SKF."),

        ("vespa-50", "Cilindro in alluminio", "warning", "Il cilindro in alluminio si usura più velocemente della versione in ghisa."),
        ("vespa-50", "Carburatore SHA 14/12", "info", "Il carburatore SHA è delicato. Pulizia frequente necessaria."),
        ("vespa-50-special", "Accensione a puntine", "warning", "Le puntine si usurano e richiedono regolazione periodica."),
        ("vespa-primavera-et3", "Valvola lamellare", "warning", "La valvola lamellare può rompersi. Sostituire con ricambi Mallossi."),
        ("vespa-primavera-et3", "Testata 3 porte", "info", "La testata ET3 è specifica. Usare candela NGK B10ES."),

        ("vespa-rally-180", "Carburatore SI 20/20", "warning", "Il carburatore SI 20/20 è delicato. Usare getti originali."),
        ("vespa-rally-200", "Albero motore", "critical", "Albero motore può rompersi su esemplari molto sollecitati. Verificare gioco."),
        ("vespa-rally-200", "Puntine spinterogeno", "warning", "Puntine da controllare ogni 3000 km."),
        ("vespa-px-125", "Change rod flexion", "warning", "La leva del cambio può piegarsi. Sostituire con rinforzata."),
        ("vespa-px-125", "Frizione originale", "warning", "Frizione originale poco resistente all'uso intenso."),
        ("vespa-px-125", "Supporto motore posteriore", "info", "Il silentbloc del supporto motore si usura nel tempo."),
        ("vespa-px-200", "Rottura mozzo ruota posteriore", "critical", "Il mozzo ruota posteriore può rompersi su PX200 molto spinte. Verificare."),
        ("vespa-px-200", "Frizione rinforzata", "info", "Su PX200 consigliata frizione rinforzata per uso intenso."),
        ("vespa-t5", "Testata 5 luci fragile", "critical", "La testata 5 luci tende a rompersi tra le luci di travaso."),
        ("vespa-t5", "Carburatore 24mm", "info", "Il carburatore Dell'Orto SI 24/24E è specifico T5."),

        ("vespa-cosa-125", "Cambio a 4 marce debole", "warning", "Il cambio della Cosa ha rapporti delicati. Usare olio specifico."),
        ("vespa-cosa-125", "Freno a disco anteriore", "warning", "Il freno a disco originale ha problemi di spurgo aria."),
        ("vespa-pk-125", "Carter motore in alluminio", "warning", "Il carter motore in alluminio può filettarsi facilmente."),
        ("vespa-pk-125", "Impianto elettrico", "warning", "L'impianto elettrico PK125 è delicato. Verificare massa e connettori."),
        ("vespa-et4-125", "Variatore usurato", "warning", "Il variatore del cambio CVT si usura ogni 15.000 km."),
        ("vespa-et4-125", "Bobina di accensione", "info", "La bobina originale può cedere. Sintomo: accensione intermittente."),

        ("vespa-gts-300-super", "Cuscinetti reggispinta", "warning", "Cuscinetti reggispinta del motore da controllare dopo 30.000 km."),
        ("vespa-gts-300-super", "Pompa acqua", "warning", "Pompa acqua può perdere dopo 40.000 km. Controllare liquido."),
        ("vespa-gts-300-super", "Cinghia servizi", "info", "Cinghia servizi da sostituire ogni 20.000 km."),
        ("vespa-gts-300-2019", "Sensore ABS", "warning", "Sensore ABS posteriore può dare falsi contatti con sporco."),
        ("vespa-gts-300-2019", "Batteria", "info", "Batteria originale ha durata limitata (2-3 anni)."),
        ("vespa-elettrica", "Batteria agli ioni di litio", "warning", "La batteria perde capacità nel tempo. Ricambio costoso."),
        ("vespa-elettrica", "Motore elettrico", "info", "Il motore elettrico è molto affidabile, nessun problema noto."),
    ]

    issues_values = []
    for slug, issue, severity, desc in issues_data:
        if slug in model_ids:
            issues_values.append((model_ids[slug], issue, severity, desc))

    cursor.executemany(
        "INSERT INTO vespa_known_issues (model_id, issue, severity, description) VALUES (?, ?, ?, ?)",
        issues_values
    )
    conn.commit()

    # =========================================================
    # MARKET PRICES
    # =========================================================
    prices_data = [
        # (slug, condition, min, max)
        # --- 98 ---
        ("vespa-98", "restored", 15000, 25000),
        ("vespa-98", "good", 8000, 15000),
        ("vespa-98", "fair", 4000, 8000),
        ("vespa-98", "project", 1500, 4000),
        # --- 125 ---
        ("vespa-125", "restored", 6000, 12000),
        ("vespa-125", "good", 3500, 6000),
        ("vespa-125", "fair", 1500, 3500),
        ("vespa-125", "project", 500, 1500),
        # --- 150 GS ---
        ("vespa-150-gs", "restored", 10000, 18000),
        ("vespa-150-gs", "good", 5500, 10000),
        ("vespa-150-gs", "fair", 2500, 5500),
        ("vespa-150-gs", "project", 1000, 2500),
        # --- 160 GS ---
        ("vespa-160-gs", "restored", 8000, 15000),
        ("vespa-160-gs", "good", 4500, 8000),
        ("vespa-160-gs", "fair", 2000, 4500),
        ("vespa-160-gs", "project", 800, 2000),
        # --- 150 Super ---
        ("vespa-150-super", "restored", 4000, 7000),
        ("vespa-150-super", "good", 2000, 4000),
        ("vespa-150-super", "fair", 1000, 2000),
        ("vespa-150-super", "project", 300, 1000),
        # --- 125 Super ---
        ("vespa-125-super", "restored", 3500, 6000),
        ("vespa-125-super", "good", 1800, 3500),
        ("vespa-125-super", "fair", 800, 1800),
        ("vespa-125-super", "project", 300, 800),
        # --- Sprint ---
        ("vespa-sprint", "restored", 6000, 10000),
        ("vespa-sprint", "good", 3000, 6000),
        ("vespa-sprint", "fair", 1200, 3000),
        ("vespa-sprint", "project", 500, 1200),
        # --- Sprint Veloce ---
        ("vespa-sprint-veloce", "restored", 5000, 9000),
        ("vespa-sprint-veloce", "good", 2500, 5000),
        ("vespa-sprint-veloce", "fair", 1000, 2500),
        ("vespa-sprint-veloce", "project", 400, 1000),
        # --- 180 SS ---
        ("vespa-180-ss", "restored", 12000, 22000),
        ("vespa-180-ss", "good", 6000, 12000),
        ("vespa-180-ss", "fair", 3000, 6000),
        ("vespa-180-ss", "project", 1000, 3000),
        # --- 50 ---
        ("vespa-50", "restored", 2500, 4500),
        ("vespa-50", "good", 1200, 2500),
        ("vespa-50", "fair", 600, 1200),
        ("vespa-50", "project", 200, 600),
        # --- 50 Special ---
        ("vespa-50-special", "restored", 3500, 6000),
        ("vespa-50-special", "good", 1800, 3500),
        ("vespa-50-special", "fair", 800, 1800),
        ("vespa-50-special", "project", 300, 800),
        # --- 50 L ---
        ("vespa-50-l", "restored", 2000, 3500),
        ("vespa-50-l", "good", 1000, 2000),
        ("vespa-50-l", "fair", 400, 1000),
        ("vespa-50-l", "project", 150, 400),
        # --- 90 ---
        ("vespa-90", "restored", 3000, 5500),
        ("vespa-90", "good", 1500, 3000),
        ("vespa-90", "fair", 600, 1500),
        ("vespa-90", "project", 250, 600),
        # --- Primavera 125 ---
        ("vespa-primavera-125", "restored", 4000, 7000),
        ("vespa-primavera-125", "good", 2000, 4000),
        ("vespa-primavera-125", "fair", 1000, 2000),
        ("vespa-primavera-125", "project", 300, 1000),
        # --- Primavera ET3 ---
        ("vespa-primavera-et3", "restored", 5000, 9000),
        ("vespa-primavera-et3", "good", 2500, 5000),
        ("vespa-primavera-et3", "fair", 1000, 2500),
        ("vespa-primavera-et3", "project", 400, 1000),
        # --- Rally 180 ---
        ("vespa-rally-180", "restored", 8000, 14000),
        ("vespa-rally-180", "good", 4000, 8000),
        ("vespa-rally-180", "fair", 2000, 4000),
        ("vespa-rally-180", "project", 800, 2000),
        # --- Rally 200 ---
        ("vespa-rally-200", "restored", 10000, 18000),
        ("vespa-rally-200", "good", 5000, 10000),
        ("vespa-rally-200", "fair", 2500, 5000),
        ("vespa-rally-200", "project", 1000, 2500),
        # --- PX 125 ---
        ("vespa-px-125", "restored", 3000, 5000),
        ("vespa-px-125", "good", 1500, 3000),
        ("vespa-px-125", "fair", 700, 1500),
        ("vespa-px-125", "project", 300, 700),
        # --- PX 150 ---
        ("vespa-px-150", "restored", 3500, 5500),
        ("vespa-px-150", "good", 1800, 3500),
        ("vespa-px-150", "fair", 800, 1800),
        ("vespa-px-150", "project", 300, 800),
        # --- PX 200 ---
        ("vespa-px-200", "restored", 5000, 9000),
        ("vespa-px-200", "good", 2500, 5000),
        ("vespa-px-200", "fair", 1200, 2500),
        ("vespa-px-200", "project", 500, 1200),
        # --- T5 ---
        ("vespa-t5", "restored", 6000, 10000),
        ("vespa-t5", "good", 3000, 6000),
        ("vespa-t5", "fair", 1500, 3000),
        ("vespa-t5", "project", 600, 1500),
        # --- Cosa 125 ---
        ("vespa-cosa-125", "restored", 3000, 5000),
        ("vespa-cosa-125", "good", 1500, 3000),
        ("vespa-cosa-125", "fair", 600, 1500),
        ("vespa-cosa-125", "project", 200, 600),
        # --- Cosa 200 ---
        ("vespa-cosa-200", "restored", 4000, 7000),
        ("vespa-cosa-200", "good", 2000, 4000),
        ("vespa-cosa-200", "fair", 1000, 2000),
        ("vespa-cosa-200", "project", 400, 1000),
        # --- PK 125 ---
        ("vespa-pk-125", "restored", 2000, 3500),
        ("vespa-pk-125", "good", 1000, 2000),
        ("vespa-pk-125", "fair", 400, 1000),
        ("vespa-pk-125", "project", 150, 400),
        # --- ET4 125 ---
        ("vespa-et4-125", "restored", 2000, 3500),
        ("vespa-et4-125", "good", 1200, 2000),
        ("vespa-et4-125", "fair", 600, 1200),
        ("vespa-et4-125", "project", 300, 600),
        # --- ET4 150 ---
        ("vespa-et4-150", "restored", 2500, 4000),
        ("vespa-et4-150", "good", 1500, 2500),
        ("vespa-et4-150", "fair", 800, 1500),
        ("vespa-et4-150", "project", 400, 800),
        # --- GTS 125 ---
        ("vespa-gts-125", "restored", 3000, 4500),
        ("vespa-gts-125", "good", 2000, 3000),
        ("vespa-gts-125", "fair", 1200, 2000),
        ("vespa-gts-125", "project", 600, 1200),
        # --- GTS 250 ---
        ("vespa-gts-250", "restored", 3500, 5500),
        ("vespa-gts-250", "good", 2200, 3500),
        ("vespa-gts-250", "fair", 1400, 2200),
        ("vespa-gts-250", "project", 700, 1400),
        # --- GTS 300 Super ---
        ("vespa-gts-300-super", "restored", 4000, 6500),
        ("vespa-gts-300-super", "good", 2500, 4000),
        ("vespa-gts-300-super", "fair", 1500, 2500),
        ("vespa-gts-300-super", "project", 800, 1500),
        # --- GTV 300 ---
        ("vespa-gtv-300", "restored", 4500, 7000),
        ("vespa-gtv-300", "good", 2800, 4500),
        ("vespa-gtv-300", "fair", 1800, 2800),
        ("vespa-gtv-300", "project", 900, 1800),
        # --- LX 125 ---
        ("vespa-lx-125", "restored", 2000, 3500),
        ("vespa-lx-125", "good", 1200, 2000),
        ("vespa-lx-125", "fair", 600, 1200),
        ("vespa-lx-125", "project", 300, 600),
        # --- LXV 125 ---
        ("vespa-lxv-125", "restored", 2500, 4000),
        ("vespa-lxv-125", "good", 1500, 2500),
        ("vespa-lxv-125", "fair", 800, 1500),
        ("vespa-lxv-125", "project", 400, 800),
        # --- S 125 ---
        ("vespa-s-125", "restored", 2200, 3500),
        ("vespa-s-125", "good", 1300, 2200),
        ("vespa-s-125", "fair", 700, 1300),
        ("vespa-s-125", "project", 300, 700),
        # --- Primavera 2013 ---
        ("vespa-primavera-2013", "restored", 3000, 4500),
        ("vespa-primavera-2013", "good", 2000, 3000),
        ("vespa-primavera-2013", "fair", 1200, 2000),
        ("vespa-primavera-2013", "project", 600, 1200),
        # --- Sprint 2014 ---
        ("vespa-sprint-2014", "restored", 3200, 4800),
        ("vespa-sprint-2014", "good", 2000, 3200),
        ("vespa-sprint-2014", "fair", 1300, 2000),
        ("vespa-sprint-2014", "project", 700, 1300),
        # --- GTS 300 2019 ---
        ("vespa-gts-300-2019", "restored", 5500, 8000),
        ("vespa-gts-300-2019", "good", 4000, 5500),
        ("vespa-gts-300-2019", "fair", 2800, 4000),
        ("vespa-gts-300-2019", "project", 1500, 2800),
        # --- GTS 125 2019 ---
        ("vespa-gts-125-2019", "restored", 4000, 6000),
        ("vespa-gts-125-2019", "good", 2800, 4000),
        ("vespa-gts-125-2019", "fair", 1800, 2800),
        ("vespa-gts-125-2019", "project", 1000, 1800),
        # --- Elettrica ---
        ("vespa-elettrica", "restored", 5000, 7000),
        ("vespa-elettrica", "good", 3500, 5000),
        ("vespa-elettrica", "fair", 2000, 3500),
        ("vespa-elettrica", "project", 1000, 2000),
        # --- Primavera 2021 ---
        ("vespa-primavera-2021", "restored", 4000, 5500),
        ("vespa-primavera-2021", "good", 3000, 4000),
        ("vespa-primavera-2021", "fair", 2000, 3000),
        ("vespa-primavera-2021", "project", 1200, 2000),
        # --- Sprint S 2021 ---
        ("vespa-sprint-s-2021", "restored", 4200, 5800),
        ("vespa-sprint-s-2021", "good", 3200, 4200),
        ("vespa-sprint-s-2021", "fair", 2200, 3200),
        ("vespa-sprint-s-2021", "project", 1300, 2200),
    ]

    prices_values = []
    for slug, condition, min_price, max_price in prices_data:
        if slug in model_ids:
            prices_values.append((model_ids[slug], condition, min_price, max_price, "EUR", "2025-06-01"))

    cursor.executemany(
        "INSERT INTO vespa_market_prices (model_id, condition_type, price_min, price_max, currency, last_updated) VALUES (?, ?, ?, ?, ?, ?)",
        prices_values
    )
    conn.commit()

    print(f"✅ Database creato con successo: {DB_PATH}")
    print(f"📊 Totale modelli: {len(models)}")
    print(f"🎨 Colori inseriti: {len(colors_values)}")
    print(f"🔧 Problemi noti: {len(issues_values)}")
    print(f"💰 Fasce di prezzo: {len(prices_values)}")
    print(f"🔢 Range telai: {len(chassis_values)}")
    print(f"🔢 Range motori: {len(engine_values)}")


def verify_database(conn):
    """Verify the database content."""
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM vespa_models")
    models_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM vespa_colors")
    colors_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM vespa_known_issues")
    issues_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM vespa_market_prices")
    prices_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM vespa_chassis_numbers")
    chassis_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM vespa_engine_numbers")
    engine_count = cursor.fetchone()[0]

    print(f"\n📋 Verifica database:")
    print(f"   - Modelli: {models_count}")
    print(f"   - Colori: {colors_count}")
    print(f"   - Problemi noti: {issues_count}")
    print(f"   - Fasce prezzo: {prices_count}")
    print(f"   - Range telai: {chassis_count}")
    print(f"   - Range motori: {engine_count}")

    print("\n🏍️  Modelli presenti:")
    cursor.execute("SELECT name, production_start, production_end, displacement_cc FROM vespa_models ORDER BY production_start")
    for row in cursor.fetchall():
        end_str = f"oggi" if row[2] is None or row[2] >= 2024 else str(row[2])
        print(f"   - {row[0]} ({row[1]}-{end_str}, {row[3]})")


def main():
    print("🚀 OcchioEsperto.it — Vespa Knowledge Base Database\n")

    if os.path.exists(DB_PATH):
        print(f"⚠️  Database esistente trovato: {DB_PATH}")
        import sys
        confirm = input("Sovrascrivere? (s/N): ")
        if confirm.lower() != 's':
            print("Operazione annullata.")
            return

    conn = sqlite3.connect(DB_PATH)

    print("📦 Creazione schema...")
    create_schema(conn)

    print("🌱 Inserimento dati...")
    seed_data(conn)

    verify_database(conn)

    conn.close()
    print("\n✅ Operazione completata con successo!")


if __name__ == "__main__":
    main()