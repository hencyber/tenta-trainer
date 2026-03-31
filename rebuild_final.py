#!/usr/bin/env python3
import re, subprocess

# 1. Read pre-cases (verified working 36KB)
with open('/tmp/pre_cases.txt') as f:
    pre = f.read()

# 2. Extract 43 model answers from broken file
with open('/home/cybercore/Skrivbord/uppgiftskola2/tenta-trainer/data.js.broken') as f:
    broken = f.read()

marker = '<h5>\u2714 Exempelsvar</h5>'
parts = broken.split(marker)
ma = []
for i in range(1, len(parts)):
    raw = marker + parts[i]
    for end in ["' },", "' }\n", "' }"]:
        pos = raw.find(end)
        if pos > 0:
            raw = raw[:pos]
            break
    ma.append(raw)

print(f"Extracted {len(ma)} model answers")

def esc(s):
    """Escape for JS single-quoted string."""
    return re.sub(r"(?<!\\)'", "\\'", s)

# 3. Map: MA[0]=fleet-handoff, MA[1]=fleet-tools,
# MA[2..6]=bank(t1,t2,t3,handoff,tools), MA[7..11]=energy, MA[12..16]=recruit,
# MA[17..21]=edu, MA[22..26]=food, MA[27..31]=media, MA[32..36]=property,
# MA[37..42]=legal(t1,t2,t3,handoff,tools,gov)

def gov(case_name, risk1, risk2, hitl_point):
    return (f'<h5>\u2714 Exempelsvar</h5>'
            f'<p><strong>Tolkningsbaserade risker:</strong></p>'
            f'<ul><li>{risk1}</li><li>{risk2}</li></ul>'
            f'<p><strong>HITL:</strong> {hitl_point}</p>'
            f'<p><strong>Loggning:</strong> Alla agentbeslut loggas med tidsstämpel, konfidensniv\u00e5 och k\u00e4lldata f\u00f6r audit trail.</p>'
            f'<p><strong>Bias:</strong> Regelbunden uppf\u00f6ljning av agenternas beslut f\u00f6r att identifiera systematiska snedvridningar.</p>')

# HealthTrack rich answers
ht_t1 = esc('<h5>\u2714 Exempelsvar</h5><p><strong>Tolkningsbaserade (agent):</strong></p><ul><li>L\u00e4sa patientrapporterade symptom (fri text)</li><li>Korrelera EKG-m\u00f6nster med symptombeskrivning</li><li>Bed\u00f6ma allvarlighetsgrad</li></ul><p><strong>Klassisk automation (regelmotor):</strong></p><ul><li>Tr\u00f6skelv\u00e4rden f\u00f6r puls (&gt;120, &lt;40)</li><li>Syresm\u00e4ttning (&lt;90%)</li><li>Notifieringsregler</li></ul>')
ht_t2 = esc('<h5>\u2714 Exempelsvar</h5><p><strong>M\u00f6nster: Routing + Evaluator-Optimizer</strong></p><p>Motivering: Larmen m\u00e5ste f\u00f6rst klassificeras (routing) innan r\u00e4tt specialistagent hanterar dem. En evaluator s\u00e4kerst\u00e4ller kvalitet.</p><pre>Sensor-data -&gt; [Regelmotor: Tr\u00f6skelv\u00e4rden]\\n  -&gt; [Agent 1: Larmklassificerare]\\n  -&gt; [Agent 2: Klinisk analysagent]\\n  -&gt; [Evaluator: Kvalitetskontroll]\\n  -&gt; [HITL: Sjuksk\u00f6terska] -&gt; Patientkontakt</pre>')
ht_t3 = esc('<h5>\u2714 Exempelsvar</h5><p><strong>Agent 1: Larmklassificerare</strong></p><p><em>Varf\u00f6r beh\u00f6vs agenten:</em> M\u00e5nga larm \u00e4r falsklarm. En agent kan filtrera och prioritera baserat p\u00e5 m\u00f6nsterig\u00e4nk\u00e4nning.</p><pre>{\\n  "name": "Larmklassificerare",\\n  "system_prompt": "Du \u00e4r specialist p\u00e5 hj\u00e4rtmonitorering. Klassificera inkommande larm...",\\n  "inputs": ["ekg_data", "pulsv\u00e4rde", "syre_niva", "patienthistorik"],\\n  "outputs": ["kategori", "prioritet", "rekommendation"],\\n  "tools": ["h\u00e4mta_patienthistorik", "ekg_analys"],\\n  "r\u00e4ttigheter": "L\u00e4sr\u00e4tt patientjournal, INGEN skrivr\u00e4tt"\\n}</pre>')
ht_t4 = esc('<h5>\u2714 Exempelsvar</h5><p>Mellan Larmklassificerare \u2192 Klinisk analysagent skickas <strong>strukturerad JSON</strong>:</p><pre>{\\n  "larm_id": "LRM-2024-1547",\\n  "kategori": "potentiell_arytmi",\\n  "prioritet": "h\u00f6g",\\n  "ekg_sammanfattning": "Irregulj\u00e4r RR-intervall, m\u00f6jlig AF",\\n  "konfidens": 0.87\\n}</pre>')
ht_t5 = esc('<h5>\u2714 Exempelsvar</h5><pre>def h\u00e4mta_patienthistorik(patient_id: str) -&gt; dict:\\n    \"\"\"H\u00e4mtar patientens journaldata fr\u00e5n EHR-systemet.\\n    Input: patient_id (str)\\n    Output: dict med diagnos_historik, medicinlista, allergi_info\\n    Varf\u00f6r: Agenten beh\u00f6ver kontext f\u00f6r att bed\u00f6ma om ett larmm\u00f6nster \u00e4r nytt eller k\u00e4nt.\"\"\"\\n    return ehr_api.get(patient_id)</pre>')
ht_t6 = esc(gov('HealthTrack', 'Falskt negativ: Agent missar kritiskt larm \u2192 Livsfarligt. \u00c5tg\u00e4rd: Alla h\u00f6grisk-larm g\u00e5r alltid till HITL.', 'Hallucination: Agent fabricerar EKG-tolkning. \u00c5tg\u00e4rd: Korsvalidering mot regelmotor.', 'Obligatorisk f\u00f6r alla \u00e5tg\u00e4rder som p\u00e5verkar patientv\u00e5rd. Sjuksk\u00f6terska m\u00e5ste godk\u00e4nna kontaktf\u00f6rs\u00f6k.'))

# FleetOps - tasks 1,2,3 missing + governance missing
fl_t1 = esc('<h5>\u2714 Exempelsvar</h5><p><strong>Tolkningsbaserade (agent):</strong></p><ul><li>Tolka trafikrapporter och v\u00e4derprognoser (fri text)</li><li>Bed\u00f6ma om f\u00f6rsening kr\u00e4ver omdirigering</li></ul><p><strong>Klassisk automation:</strong></p><ul><li>GPS-sp\u00e5rning och ETA-ber\u00e4kning</li><li>SLA-kontroll mot avtalade leveranstider</li></ul>')
fl_t2 = esc('<h5>\u2714 Exempelsvar</h5><p><strong>M\u00f6nster: Routing + Parallellization</strong></p><p>Motivering: Flera datak\u00e4llor (v\u00e4der, trafik, kundkrav) m\u00e5ste analyseras parallellt, sedan dirigeras \u00e4rendet.</p><pre>F\u00f6rseningslarm -&gt; [Parallell: V\u00e4deragent + Trafikagent]\\n  -&gt; [Router: Beslutspunkt]\\n  -&gt; [Agent: Omdirigerare]\\n  -&gt; [HITL: Transportledare] -&gt; Godk\u00e4nn ny rutt</pre>')
fl_t3 = esc('<h5>\u2714 Exempelsvar</h5><p><strong>Agent 1: Klassificerare</strong></p><pre>{\\n  "name": "F\u00f6rseningsklassificerare",\\n  "system_prompt": "Du \u00e4r logistikexpert. Klassificera f\u00f6rseningar efter orsak...",\\n  "inputs": ["fordons-id", "position", "rutt", "v\u00e4derdata"],\\n  "outputs": ["orsak", "f\u00f6rv\u00e4ntad_f\u00f6rsening_min", "rekommendation"],\\n  "tools": ["check_sla", "h\u00e4mta_alternativ_rutt"]\\n}</pre>')
fl_t4 = esc(ma[0]) if len(ma) > 0 else ''
fl_t5 = esc(ma[1]) if len(ma) > 1 else ''
fl_t6 = esc(gov('FleetOps', 'Felaktig omdirigering: Agent v\u00e4ljer l\u00e4ngre rutt \u2192 \u00f6kade kostnader.', 'Hallucination: Agent fabricerar v\u00e4gdata. \u00c5tg\u00e4rd: Validering mot Google Maps API.', 'Transportledare godk\u00e4nner alla ruttf\u00f6r\u00e4ndringar som p\u00e5verkar SLA.'))

# Cases 3-10: use extracted MAs (indices 2-42)
def case_ma(base_idx, governance_text):
    """Get 6 MAs for a case starting at base_idx in the ma list."""
    return [
        esc(ma[base_idx]) if base_idx < len(ma) else '',
        esc(ma[base_idx+1]) if base_idx+1 < len(ma) else '',
        esc(ma[base_idx+2]) if base_idx+2 < len(ma) else '',
        esc(ma[base_idx+3]) if base_idx+3 < len(ma) else '',
        esc(ma[base_idx+4]) if base_idx+4 < len(ma) else '',
        esc(governance_text),
    ]

bank_gov = gov('NordicBank', 'Felaktig kreditbed\u00f6mning: Agent missar riskflaggor i l\u00f6nespec \u2192 D\u00e5liga l\u00e5n.', 'Diskriminering: Systematisk bias mot vissa inkomsttyper. \u00c5tg\u00e4rd: A/B-testning.', 'Kredithandl\u00e4ggare godk\u00e4nner ALLA l\u00e5nebeslut. Lagstadgat krav.')
energy_gov = gov('GreenEnergy', 'Missad kritisk felkod: Agent nedprioriterar allvarligt turbin-fel.', 'Hallucination: Agent fabricerar underh\u00e5llshistorik. \u00c5tg\u00e4rd: Validering mot SCADA-data.', 'F\u00e4lttekniker bekr\u00e4ftar \u00e5tg\u00e4rdsplan innan arbetsorder skickas.')
recruit_gov = gov('TechRecruit', 'Diskrimineringsbias: Agent nedv\u00e4rderar CV fr\u00e5n vissa l\u00e4ros\u00e4ten systematiskt.', 'GDPR-risk: Modellen memorerar persondata fr\u00e5n CV.', 'Rekryterare granskar ALLA kandidatlistor innan de skickas till kund.')
edu_gov = gov('EduLearn', 'Felaktig information: Agent ger fel svar p\u00e5 kursfr\u00e5gor.', 'Eskaleringsmiss: Agent missar att studenten beh\u00f6ver m\u00e4nsklig hj\u00e4lp.', 'L\u00e4rare godk\u00e4nner \u00e4ndring av betyg eller kursinformation.')
food_gov = gov('FoodSafe', 'Missad h\u00e4lsorisk: Agent klassificerar allvarlig avvikelse som l\u00e5gprioritet.', 'Bias: Systematisk underbed\u00f6mning av vissa restaurangtyper.', 'Inspekt\u00f6r signerar ALLA \u00e5tg\u00e4rdsf\u00f6rel\u00e4gganden. Myndighetsbeslut kr\u00e4ver m\u00e4nniska.')
media_gov = gov('MediaHouse', '\u00d6vercensur: Agent tar bort legitima \u00e5sikter \u2192 Yttrandefrihetsproblem.', 'Undercensur: Agent missar hatretorik \u2192 Juridisk risk.', 'Redakt\u00f6r granskar alla modererings\u00e4renden i gr\u00e5zonen (konfidens 50-90%).')
property_gov = gov('PropertyCare', 'Felklassificering: Agent bed\u00f6mer vattenl\u00e4cka som l\u00e5gprio \u2192 Vattenskada.', 'Hallucination: Agent fabricerar \u00e5tg\u00e4rdsf\u00f6rslag.', 'Fastighetsf\u00f6rvaltare godk\u00e4nner alla arbetsordrar \u00f6ver 5000 kr.')

bank_answers = case_ma(2, bank_gov)
energy_answers = case_ma(7, energy_gov)
recruit_answers = case_ma(12, recruit_gov)
edu_answers = case_ma(17, edu_gov)
food_answers = case_ma(22, food_gov)
media_answers = case_ma(27, media_gov)
property_answers = case_ma(32, property_gov)
legal_answers = [esc(ma[i]) for i in range(37, min(43, len(ma)))]
# Pad legal if needed
while len(legal_answers) < 6:
    legal_answers.append('')

# 4. Build cases array
cases_data = [
    ('case-tech', 'HealthTrack Nordic AB', 'Optimera larmhantering fr\u00e5n b\u00e4rbara hj\u00e4rtmonitorer med AI-agenter.',
     '<strong>Bransch:</strong> E-h\u00e4lsa/MedTech<br><strong>Storlek:</strong> 120 anst\u00e4llda, 30 000 aktiva anv\u00e4ndare<br><strong>Utmaning:</strong> 2000+ larm/dag varav 85% \u00e4r falsklarm',
     'Datastr\u00f6mmar fr\u00e5n EKG-sensorer, pulsklockor och syrem\u00e4tare. Patientrapporterade symptom i fritext. Journaldata fr\u00e5n EHR-system.',
     [ht_t1, ht_t2, ht_t3, ht_t4, ht_t5, ht_t6]),
    ('case-fleet', 'FleetOps Logistics AB', 'AI-agentifiering av omdirigering vid f\u00f6rseningar.',
     '<strong>Bransch:</strong> Transport/Logistik<br><strong>Storlek:</strong> 500 lastbilar, 85 anst\u00e4llda<br><strong>Utmaning:</strong> 40 f\u00f6rseningar/dag kr\u00e4ver manuell omplanering',
     'Ruttdata, v\u00e4derrapporter, kundens ETA-krav, trafikinformation i realtid, SLA-avtal.',
     [fl_t1, fl_t2, fl_t3, fl_t4, fl_t5, fl_t6]),
    ('case-bank', 'NordicBank - Kredithantering', 'Automation av l\u00e5nebed\u00f6mningar f\u00f6r privatl\u00e5n.',
     '<strong>Bransch:</strong> Finans<br><strong>Storlek:</strong> Mellanstor nischbank, 800 ans\u00f6kningar/vecka<br><strong>Utmaning:</strong> 5-7 dagars handl\u00e4ggningstid',
     'L\u00e5neans\u00f6kan, kreditupplysning (UC), l\u00f6nespecifikation (PDF) och kontoutdrag.',
     bank_answers),
    ('case-energy', 'GreenEnergy - Vindkraftsservice', 'Optimering av underh\u00e5ll f\u00f6r vindkraftverk.',
     '<strong>Bransch:</strong> Energi<br><strong>Storlek:</strong> 200 turbiner, 60 anst\u00e4llda<br><strong>Utmaning:</strong> 3000 larm/m\u00e5nad fr\u00e5n SCADA-system',
     'SCADA-sensordata, felkoder, textrapporter fr\u00e5n f\u00e4lttekniker, underh\u00e5llshistorik.',
     energy_answers),
    ('case-recruit', 'TechRecruit - CV-Matchning', 'Generativ AI f\u00f6r initial kandidatgallring.',
     '<strong>Bransch:</strong> Rekrytering/HR-tech<br><strong>Storlek:</strong> 25 anst\u00e4llda, 1200 CV/m\u00e5nad<br><strong>Utmaning:</strong> Manuell gallring tar 15 min/CV',
     'CV (PDF/Word), personligt brev, kravprofil fr\u00e5n kund med m\u00e5ste-krav och meriterande.',
     recruit_answers),
    ('case-edu', 'EduLearn - Studentst\u00f6d', 'Supervisory agent f\u00f6r inkommande studentfr\u00e5gor.',
     '<strong>Bransch:</strong> EdTech/Utbildning<br><strong>Storlek:</strong> 8000 studenter, 200 kurser<br><strong>Utmaning:</strong> 500 supportmeddelanden/dag med 48h svarstid',
     'Mejl/meddelanden fr\u00e5n studenter med fr\u00e5gor om schema, uppgifter, betyg och tekniska problem.',
     edu_answers),
    ('case-food', 'FoodSafe - Livsmedelskontroll', 'Analys av inspektionsrapporter fr\u00e5n restauranger.',
     '<strong>Bransch:</strong> Myndighet/Livsmedel<br><strong>Storlek:</strong> 120 inspekt\u00f6rer, 15 000 inspektioner/\u00e5r<br><strong>Utmaning:</strong> Inkonsekvent riskbed\u00f6mning',
     'Granskningsprotokoll (fritext), foton p\u00e5 avvikelser, tidigare inspektionshistorik.',
     food_answers),
    ('case-media', 'MediaHouse - Moderering', 'Hybridfl\u00f6de f\u00f6r inneh\u00e5llsmoderering av kommentarer.',
     '<strong>Bransch:</strong> Media<br><strong>Storlek:</strong> 200 000 kommentarer/dag<br><strong>Utmaning:</strong> Balans mellan yttrandefrihet och trygghet',
     'Anv\u00e4ndarkommentarer, anm\u00e4lningsorsak, anv\u00e4ndarhistorik, artikelkontext.',
     media_answers),
    ('case-property', 'PropertyCare - Felanm\u00e4lan', 'Automatiserad hantering av hyresg\u00e4sters felanm\u00e4lningar.',
     '<strong>Bransch:</strong> Fastighetsf\u00f6rvaltning<br><strong>Storlek:</strong> 12 000 l\u00e4genheter, 800 felanm\u00e4lningar/m\u00e5nad<br><strong>Utmaning:</strong> Felklassificering av akuta \u00e4renden',
     'Fritext i formul\u00e4r, foton, adresser, hyresg\u00e4sthistorik fr\u00e5n fastighetssystem.',
     property_answers),
    ('case-legal', 'LegalAssist - Avtalsgranskning', 'Agent f\u00f6r identifiering av riskfyllda klausuler.',
     '<strong>Bransch:</strong> Juridik<br><strong>Storlek:</strong> 45 jurister, 200 avtal/m\u00e5nad<br><strong>Utmaning:</strong> 4h/avtal manuell granskning',
     'PDF-avtal p\u00e5 10-50 sidor, checklista \u00f6ver riskparametrar, tidigare avtalsbed\u00f6mningar.',
     legal_answers),
]

task_titles = [
    '1. Processanalys (10p)',
    '2. Agentfl\u00f6de & M\u00f6nsterval (15p)',
    '3. Agent-specifikation (30p)',
    '4. Kommunikation/\u00f6verl\u00e4mning (10p)',
    '5. Verktyg (10p)',
    '6. Risker & Governance (10p)',
]
task_questions = [
    'Identifiera stegen i processen. Vilka l\u00e4mpar sig f\u00f6r agentifiering vs klassisk automation? Motivera.',
    'Rita/beskriv ett agentfl\u00f6de. Motivera m\u00f6nsterval (Routing, Parallellization, Orchestrator-Worker, Evaluator-Optimizer).',
    'Skriv en komplett specifikation f\u00f6r minst en agent: System Prompt, I/O, Verktyg, R\u00e4ttigheter. Motivera varf\u00f6r agenten beh\u00f6vs.',
    'Beskriv hur data l\u00e4mnas \u00f6ver mellan tv\u00e5 agenter. Visa JSON-struktur och motivera varf\u00f6r denna information beh\u00f6vs.',
    'Beskriv minst ett funktionsanrop/tool. Vad g\u00f6r det, input/output, varf\u00f6r beh\u00f6vs det?',
    'Identifiera risker i ditt system. Var b\u00f6r m\u00e4nniska vara i loopen (HITL)? Hur hanteras hallucinationer och bias?',
]

out = pre + '\n'
for idx, (cid, title, intro, company, pinput, answers) in enumerate(cases_data):
    comma = ',' if idx < len(cases_data) - 1 else ''
    out += f"        {{\n"
    out += f"            id: '{cid}',\n"
    out += f"            title: '{esc(title)}',\n"
    out += f"            intro: '{esc(intro)}',\n"
    out += f"            companyInfo: '{esc(company)}',\n"
    out += f"            processInput: '{esc(pinput)}',\n"
    out += f"            currentFlow: ['Inkommande data', 'Klassificering', 'Agentbearbetning', 'HITL-granskning', 'Beslut/\u00e5tg\u00e4rd'],\n"
    out += f"            tasks: [\n"
    for t in range(6):
        tc = ',' if t < 5 else ''
        out += f"                {{ title: '{esc(task_titles[t])}',\n"
        out += f"                  question: '{esc(task_questions[t])}',\n"
        out += f"                  modelAnswer: '{answers[t]}' }}{tc}\n"
    out += f"            ]\n"
    out += f"        }}{comma}\n"

out += "    ]\n};\n"

with open('/home/cybercore/Skrivbord/uppgiftskola2/tenta-trainer/data.js', 'w') as f:
    f.write(out)

print(f"Wrote {len(out)} chars")
r = subprocess.run(['node', '--check', '/home/cybercore/Skrivbord/uppgiftskola2/tenta-trainer/data.js'],
                   capture_output=True, text=True)
if r.returncode == 0:
    print("JS syntax VALID!")
else:
    print(f"ERROR: {r.stderr[:300]}")
