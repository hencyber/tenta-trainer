import os
import json

# 1. Read the working pre-cases part
try:
    with open('/tmp/pre_cases.txt', 'r') as f:
        pre_cases = f.read()
except:
    with open('/home/cybercore/Skrivbord/uppgiftskola2/tenta-trainer/data.js.broken', 'r') as f:
        broken = f.read()
        pre_cases = broken[:broken.find("    cases: [") + len("    cases: [")]

def create_case(id_val, title, intro, company, input_val):
    c = f"""
        {{
            id: '{id_val}',
            title: '{title}',
            intro: '{intro}',
            companyInfo: '{company}',
            processInput: '{input_val}',
            currentFlow: ['Inkommande ärende', 'Manuell granskning', 'Utförande av uppgift', 'Uppföljning och loggning'],
            tasks: [
                {{
                    title: '1. Processanalys (10p)',
                    question: 'Identifiera stegen i processen. Vilka lämpar sig för agentifiering vs klassisk automation?',
                    modelAnswer: '<h5>✔ Exempelsvar</h5><p><strong>Klassisk automation:</strong> Rutinmässiga uppdateringar av enkla fält.</p><p><strong>Tolkningsbaserade (agent):</strong> Analys av ostrukturerad text, semantisk matchning av problem mot lösning.</p>'
                }},
                {{
                    title: '2. Agentflöde \x26 Mönsterval (15p)',
                    question: 'Rita ett agentflöde och motivera mönsterval (Routing, Parallellization, etc).',
                    modelAnswer: '<h5>✔ Exempelsvar</h5><p><strong>Valt mönster: Routing + Evaluator-Optimizer.</strong></p><pre>Input -> [Router Agent] -> [Klassificeringsagent] -> [Åtgärdsagent] -> HITL</pre>'
                }},
                {{
                    title: '3. Agent-specifikation (30p)',
                    question: 'Skriv en komplett specifikation för minst en agent (System Prompt, I/O, Verktyg).',
                    modelAnswer: '<h5>✔ Exempelsvar</h5><pre>\\n{\\n  "name": "Klassificeringsagent",\\n  "system_prompt": "Du är en expert på att analysera ärenden...",\\n  "inputs": ["ärendebeskrivning"],\\n  "outputs": ["kategori", "prioritet"]\\n}</pre>'
                }},
                {{
                    title: '4. Kommunikation/överlämning (10p)',
                    question: 'Beskriv hur data lämnas över mellan två agenter i ditt flöde.',
                    modelAnswer: '<h5>✔ Exempelsvar</h5><p>Överlämning sker via strukturerad JSON för att säkerställa att nästa agent (eller system) kan tolka datan deterministiskt.</p>'
                }},
                {{
                    title: '5. Verktyg (10p)',
                    question: 'Beskriv minst ett anrop (tool). Vad gör det, input/output?',
                    modelAnswer: '<h5>✔ Exempelsvar</h5><pre>def get_customer_data(customer_id: str) -> dict:\\n    """Hämtar historik från CRM."""\\n</pre>'
                }},
                {{
                    title: '6. Risker \x26 Governance (10p)',
                    question: 'Identifiera risker, var HITL behövs, och hur hallucinationer hanteras.',
                    modelAnswer: '<h5>✔ Exempelsvar</h5><p><strong>Risker:</strong> Hallucinationer i kundsvar. <strong>Åtgärd:</strong> Obligatorisk Human-in-the-loop (HITL) innan slutgiltigt godkännande och rigorös loggning.</p>'
                }}
            ]
        }},"""
    return c

cases = [
    create_case('case-tech', 'HealthTrack Nordic AB (IoT Medical)', 'Optimering av larmhantering från bärbara hjärtmonitorer.', 'SaaS-bolag inom e-hälsa. 30k användare.', 'Dataströmmar från EKG, puls, och syresättning tillsammans med användarrapporterade symptom.'),
    create_case('case-fleet', 'FleetOps Logistics AB', 'AI-agentifiering av omdirigering vid förseningar.', 'Logistikföretag med 500 lastbilar i Norden.', 'Ruttdata, väderrapporter, kundens ETA-krav, och trafikinformation i realtid.'),
    create_case('case-bank', 'NordicBank - Kredithantering', 'Automation av lånebedömningar för privatlån.', 'Mellanstor svensk nischbank.', 'Låneansökan, kreditupplysning, lönespecifikation (PDF) och kontoutdrag.'),
    create_case('case-energy', 'GreenEnergy - Vindkraftsservice', 'Optimering av underhåll för vindkraftverk.', 'Energibolag med 200 turbiner.', 'Sensordata, felkoder och textrapporter från fälttekniker.'),
    create_case('case-recruit', 'TechRecruit - CV-Matchning', 'Generativ AI för initial kandidatgallring.', 'Rekryteringsbyrå inom IT.', 'CV (PDF/Word), personligt brev, kravprofil från kund.'),
    create_case('case-edu', 'EduLearn - Studentstöd', 'Supervisory agent för inkommande studentfrågor.', 'Distansutbildningsföretag.', 'Mejl och meddelanden från studenter rörande kursupplägg eller uppgifter.'),
    create_case('case-food', 'FoodSafe - Livsmedelskontroll', 'Analys av inspektionsrapporter från restauranger.', 'Statlig myndighet.', 'Granskningsprotokoll, fritextanteckningar, och foton på avvikelser.'),
    create_case('case-media', 'MediaHouse - Moderering', 'Hybridflöde för innehållsmoderering av kommentarer.', 'Svenskt mediehus.', 'Användarkommentarer, anmälningsorsak, och användarhistorik.'),
    create_case('case-property', 'PropertyCare - Felanmälan', 'Automatiserad hantering av hyresgästers felanmälningar.', 'Fastighetsförvaltningsbolag.', 'Fritext i formulär, foton, och adresser från hyresgäster.'),
    create_case('case-legal', 'LegalAssist - Avtalsgranskning', 'Agent för identifiering av riskfyllda klausuler.', 'Svensk Advokatbyrå.', 'PDF-avtal på 10-50 sidor och en checklista över riskparametrar.')
]

with open('/home/cybercore/Skrivbord/uppgiftskola2/tenta-trainer/data.js', 'w') as f:
    f.write(pre_cases + '\n' + ''.join(cases).rstrip(',') + '\n    ]\n};\n')

print("Success")
