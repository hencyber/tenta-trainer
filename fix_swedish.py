#!/usr/bin/env python3
"""
COMPREHENSIVE Swedish character fixer.
Uses a complete dictionary of ASCII→Swedish word mappings.
Handles word boundaries to avoid false replacements.
"""
import re, sys

# Complete dictionary: ASCII version → correct Swedish
# Format: (pattern, replacement, whole_word_only)
DICT = [
    # === Å-ord ===
    (r'\bpa\b', 'på', True),
    (r'\bgar\b', 'går', True),
    (r'\bfar\b', 'får', True),
    (r'\bnar\b', 'när', True),
    (r'\bhar\b', 'har', False),  # 'har' is correct!
    (r'\bnar\b', 'når', False),  # context dependent
    (r'\bstar\b', 'står', True),
    (r'\bat\b', 'åt', False),    # context dependent, skip
    (r'\bra\b', 'rå', False),    # skip - ambiguous
    ('atkomst', 'åtkomst'),
    ('atgard', 'åtgärd'),
    ('aterkom', 'återkom'),
    ('aterkoppl', 'återkoppl'),
    ('aterfall', 'återfall'),
    ('aterstall', 'återställ'),
    ('atagande', 'åtagande'),
    ('atminstone', 'åtminstone'),
    ('arsrapport', 'årsrapport'),
    ('arlig', 'årlig'),
    ('malgrupp', 'målgrupp'),
    ('malsattning', 'målsättning'),
    ('sparbar', 'spårbar'),
    ('sparning', 'spårning'),
    ('gradvis', 'gradvis'),  # correct
    ('hallbar', 'hållbar'),
    ('hallbart', 'hållbart'),
    ('haller', 'håller'),
    ('innehall', 'innehåll'),
    ('underhall', 'underhåll'),
    ('avstaende', 'avståend'),
    
    # === Ä-ord ===
    (r'\bar\b', 'är', True),
    ('aven', 'även'),
    ('varfor', 'varför'),
    ('darfor', 'därför'),
    ('darefter', 'därefter'),
    ('namner', 'nämner'),
    ('nagon', 'någon'),
    ('nagot', 'något'),
    ('nagra', 'några'),
    ('bedomning', 'bedömning'),
    ('bedomare', 'bedömare'),
    ('bedomts', 'bedömts'),
    ('bedoms', 'bedöms'),
    ('bedomd', 'bedömd'),
    ('berakna', 'beräkna'),
    ('beraknad', 'beräknad'),
    ('behov', 'behöv'),  # behövs, behöver, behövlig
    ('atgardsforslag', 'åtgärdsförslag'),  # compound first
    ('formagor', 'förmågor'),
    ('formaga', 'förmåga'),
    ('forslag', 'förslag'),
    ('forsok', 'försök'),
    ('forsening', 'försening'),
    ('forsenings', 'försenings'),
    ('forsta', 'första'),
    ('forstar', 'förstår'),
    ('forklaring', 'förklaring'),
    ('forklarar', 'förklarar'),
    ('forandring', 'förändring'),
    ('forbattring', 'förbättring'),
    ('forbattra', 'förbättra'),
    ('fortroende', 'förtroende'),
    ('fortydliga', 'förtydliga'),
    ('forhandling', 'förhandling'),
    ('forfarande', 'förfarande'),
    ('foreskrift', 'föreskrift'),
    ('forvanta', 'förvänta'),
    ('foretag', 'företag'),
    ('forvaltn', 'förvaltn'),
    ('losning', 'lösning'),
    ('mojlig', 'möjlig'),
    ('nodvandig', 'nödvändig'),
    ('sakerstall', 'säkerställ'),
    ('sakerhet', 'säkerhet'),
    ('sakert', 'säkert'),
    ('sarskilt', 'särskilt'),
    ('sarskild', 'särskild'),
    ('hansyn', 'hänsyn'),
    ('handelse', 'händelse'),
    ('gallande', 'gällande'),
    ('tillgang', 'tillgång'),
    ('tillgangl', 'tillgängl'),
    ('tillrackl', 'tillräckl'),
    ('tillforlitl', 'tillförlitl'),
    ('rattighet', 'rättighet'),
    ('Rattighet', 'Rättighet'),
    ('rattsakerhet', 'rättssäkerhet'),
    ('lasakomst', 'läsåtkomst'),
    ('Lasakomst', 'Läsåtkomst'),
    ('lakemedel', 'läkemedel'),
    ('Lakemedel', 'Läkemedel'),
    ('lamplig', 'lämplig'),
    ('lampar', 'lämpar'),
    ('lagre', 'lägre'),
    ('langre', 'längre'),
    ('vardefull', 'värdefull'),
    ('vagledning', 'vägledning'),
    ('valjer', 'väljer'),
    ('valja', 'välja'),
    ('avgorande', 'avgörande'),
    ('avgora', 'avgöra'),
    ('mansklig', 'mänsklig'),
    ('manniska', 'människa'),
    ('overlamning', 'överlämning'),
    ('overlamna', 'överlämna'),
    ('overvakning', 'övervakning'),
    ('overcensur', 'övercensur'),
    ('fullstandig', 'fullständig'),
    ('standig', 'ständig'),
    ('kanslig', 'känslig'),
    ('kansla', 'känsla'),
    ('hamta', 'hämta'),
    ('Hamta', 'Hämta'),
    ('hjalp', 'hjälp'),
    ('halso', 'hälso'),
    ('halsa', 'hälsa'),
    ('hjart', 'hjärt'),
    ('bradskande', 'brådskande'),
    ('Bradskande', 'Brådskande'),
    ('igenkanning', 'igenkänning'),
    ('radgivare', 'rådgivare'),
    ('monsterig', 'mönsterig'),
    ('Monsterig', 'Mönsterig'),
    ('ordinationsratt', 'ordinationsrätt'),
    ('skrivrakomst', 'skrivåtkomst'),
    ('irreguljar', 'irreguljär'),
    ('Irreguljar', 'Irreguljär'),
    ('anmalan', 'anmälan'),
    ('Anmalan', 'Anmälan'),
    ('arende', 'ärende'),
    ('Arende', 'Ärende'),
    ('uppfoljning', 'uppföljning'),
    ('leverantor', 'leverantör'),
    ('Leverantor', 'Leverantör'),
    ('entreprenor', 'entreprenör'),
    ('Entreprenor', 'Entreprenör'),
    ('fragestallning', 'frågeställning'),
    ('fragekategori', 'frågekategori'),
    ('Fragekategori', 'Frågekategori'),
    ('frageklassificerare', 'frågeklassificerare'),
    ('Frageklassificerare', 'Frågeklassificerare'),
    ('grazon', 'gråzon'),
    ('Grazon', 'Gråzon'),
    ('paverka', 'påverka'),
    ('paverkan', 'påverkan'),
    ('omrade', 'område'),
    ('stodjer', 'stödjer'),
    ('stammer', 'stämmer'),
    ('flodet', 'flödet'),
    ('genomfor', 'genomför'),
    ('maste', 'måste'),
    ('stanga', 'stänga'),
    ('stanger', 'stänger'),
    ('saknar', 'saknar'),  # correct!
    
    # === Ö-ord ===
    ('gora', 'göra'),
    (r'\bgor\b', 'gör', True),
    (r'\bbor\b', 'bör', True),
    ('okar', 'ökar'),
    ('oppna', 'öppna'),
    ('oppen', 'öppen'),
    ('overens', 'överens'),
    ('hogre', 'högre'),
    ('hogsta', 'högsta'),
    ('okad', 'ökad'),
    ('ovrig', 'övrig'),
    ('nodiga', 'nödiga'),
    ('onodiga', 'onödiga'),
    ('utfor', 'utför'),
    ('utvardera', 'utvärdera'),
    ('forklara', 'förklara'),
    
    # === GODKÄNT/REVIDERA ===
    ('GODKANT', 'GODKÄNT'),
    
    # === Kontext-specifika fraser ===
    (' for att ', ' för att '),
    (' for den ', ' för den '),
    (' for varje ', ' för varje '),
    (' for detta ', ' för detta '),
    (' over ', ' över '),
    (' fran ', ' från '),
    (' fran.', ' från.'),
    (' fran,', ' från,'),
    ('(fran ', '(från '),
    (' nar ', ' när '),
    (' aven ', ' även '),
    (' dar ', ' där '),
    (' ar ', ' är '),
    (' ar,', ' är,'),
    (' ar.', ' är.'),
    (' pa ', ' på '),
    (' pa.', ' på.'),
    (' pa,', ' på,'),
    (' gar ', ' går '),
    (' gar.', ' går.'),
    (' far ', ' får '),
    (' far.', ' får.'),
    (' far,', ' får,'),
    (' bor ', ' bör '),
    (' bor.', ' bör.'),
    (' gor ', ' gör '),
    (' gor.', ' gör.'),
    (' gor,', ' gör,'),
    (' na ', ' nå '),
    (' kant ', ' känt '),
    (' kant.', ' känt.'),
    (' kant,', ' känt,'),
    # Fix common phrase patterns
    ('Borja', 'Börja'),
    ('kvalitetsgranskare for ', 'kvalitetsgranskare för '),
    ('Kvalitetsgranskare for ', 'Kvalitetsgranskare för '),
]

# Read file
path = '/home/cybercore/Skrivbord/uppgiftskola2/tenta-trainer/data.js'
with open(path, encoding='utf-8') as f:
    d = f.read()

original_len = len(d)
total = 0

for item in DICT:
    if isinstance(item, tuple) and len(item) == 3:
        pattern, replacement, whole_word = item
        if whole_word:
            # Use regex word boundary
            count_before = len(re.findall(pattern, d))
            if count_before > 0:
                d = re.sub(pattern, replacement, d)
                total += count_before
                print(f"  regex '{pattern}' → '{replacement}' ({count_before}x)")
    elif isinstance(item, tuple) and len(item) == 2:
        old, new = item
        if old != new and old in d:
            c = d.count(old)
            d = d.replace(old, new)
            total += c
            if c > 0:
                print(f"  '{old}' → '{new}' ({c}x)")

# Avoid double-fixes (e.g. "föför" from fixing "for" twice)
# Fix common double-replacement artifacts
double_fixes = [
    ('föför', 'för'),
    ('åtåt', 'åt'),
    ('äränd', 'ärend'),
    ('övöver', 'över'),
    ('ärende', 'ärende'),
]
for old, new in double_fixes:
    if old in d:
        c = d.count(old)
        if c > 0:
            d = d.replace(old, new)
            print(f"  DOUBLE-FIX: '{old}' → '{new}' ({c}x)")

with open(path, 'w', encoding='utf-8') as f:
    f.write(d)

print(f"\n✅ Total: {total} ersättningar")
print(f"   Filstorlek: {original_len} → {len(d)} bytes")
