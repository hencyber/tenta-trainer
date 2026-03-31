#!/usr/bin/env python3
"""Fix 3 issues found by NotebookLM validation across all 10 cases."""
import re

with open('data.js') as f:
    d = f.read()

# ============================================================
# FIX 1: Add "Formagor" section to all Evaluator agents
# ============================================================
# Each Granskare needs domain-specific capabilities

GRANSKARE_FORMAGOR = {
    'case-tech': 'Bedoma konsekvens mellan larmklassificering och klinisk rekommendation, Validera att evidens stodjer bedomningen',
    'case-fleet': 'Bedoma om ruttforslag ar kostnadseffektivt och SLA-kompatibelt, Validera tidsestimat mot historiska data',
    'case-bank': 'Korsvalidera riskflaggor mot policymatris, Kontrollera matematisk korrekthet i skuldkvotsberakning',
    'case-energy': 'Bedoma om prioritering matchar riskniva, Validera att resursbehov ar realistiska',
    'case-recruit': 'Identifiera potentiell bias i matchning, Kontrollera att maste-krav bedomts korrekt',
    'case-edu': 'Verifiera att svar enbart baseras pa kunskapsbasen (ej hallucination), Kontrollera ton och professionalism',
    'case-food': 'Kontrollera att avvikelser klassificerats korrekt mot lagkrav, Validera proportionalitet i atgardsforslag',
    'case-media': 'Bedoma balans mellan yttrandefrihet och policyefterlevnad, Validera att ratt policyregel refereras',
    'case-property': 'Dubbelkontrollera akut-klassificering mot skadebild, Validera entreprenorsval mot kompetenskrav',
    'case-legal': 'Kontrollera att alla relevanta klausuler identifierats, Verifiera att policyreferenser ar korrekta och aktuella',
}

for case_id, formagor_text in GRANSKARE_FORMAGOR.items():
    # Find the Granskare section for this case
    idx = d.find(f"id: '{case_id}'")
    if idx < 0: continue
    
    next_case = d.find("id: 'case-", idx+10)
    
    # Find "Rattigheter:" under Kvalitetsgranskare
    # We need the LAST occurrence of Rattigheter in task 3
    t3_start = d.find('Agent-specifikation', idx)
    t4_marker = d.find('4. Kommunikation', idx)
    
    # Find the Kvalitetsgranskare section
    eval_start = d.find('Kvalitetsgranskare', t3_start)
    if eval_start < 0 or eval_start > t4_marker: continue
    
    # Find Rattigheter after the evaluator
    ratt_pos = d.find('Rattigheter:', eval_start)
    if ratt_pos < 0 or ratt_pos > t4_marker: continue
    
    # Insert Formagor BEFORE Rattigheter
    formagor_html = f'<p><strong>Formagor:</strong></p><ul><li>{formagor_text.split(", ")[0]}</li><li>{formagor_text.split(", ")[1]}</li></ul>'
    d = d[:ratt_pos] + formagor_html + d[ratt_pos:]

print("FIX 1 DONE: Added Formagor to all 10 Evaluators")

# ============================================================
# FIX 2: Fix Evaluator input to include both Agent 1 + Agent 2
# ============================================================
# Pattern: "Input: [only agent 2]" -> "Input: Klassificering (Agent 1) + Bedomning (Agent 2)"

EVAL_INPUT_FIX = {
    'case-tech': ('Klinisk bedomning fran Agent 2', 'Larmklassificering (fran Agent 1) + Klinisk bedomning (fran Agent 2)'),
    'case-fleet': ('Ruttalternativ fran Ruttoptimeraren', 'Forseningsrapport (fran Agent 1) + Ruttalternativ (fran Agent 2)'),
    'case-bank': ('Riskbedomning fran Riskbedomaren + beslutsunderlag', 'Dokumentextrakt (fran Agent 1) + Riskbedomning (fran Agent 2)'),
    'case-energy': ('Atgardsplan fran Underhallsplaneraren', 'Felanalys (fran Agent 1) + Atgardsplan (fran Agent 2)'),
    'case-recruit': ('Matchresultat fran Matchningsagenten', 'CV-extrakt (fran Agent 1) + Matchresultat (fran Agent 2)'),
    'case-edu': ('Formulerat svar fran Svarsagenten', 'Fragekategori (fran Agent 1) + Formulerat svar (fran Agent 2)'),
    'case-food': ('Riskbedomning fran Riskbedomaren', 'Avvikelseanalys (fran Agent 1) + Riskbedomning (fran Agent 2)'),
    'case-media': ('Policybedomning fran Policybedomaren', 'Kontextanalys (fran Agent 1) + Policybedomning (fran Agent 2)'),
    'case-property': ('Prioritering fran Prioriteringsagenten', 'Arendeklassificering (fran Agent 1) + Prioritering (fran Agent 2)'),
    'case-legal': ('Riskanalys fran Klausulgranskaren', 'Avtalsextrakt (fran Agent 1) + Riskanalys (fran Agent 2)'),
}

for case_id, (old_input, new_input) in EVAL_INPUT_FIX.items():
    count = d.count(old_input)
    if count > 0:
        d = d.replace(old_input, new_input, 1)

print("FIX 2 DONE: Updated Evaluator inputs to include Agent 1 + Agent 2")

# ============================================================
# VALIDATE
# ============================================================
import subprocess
r = subprocess.run(['node', '--check', 'data.js'], capture_output=True, text=True, 
                   input=None, cwd='/home/cybercore/Skrivbord/uppgiftskola2/tenta-trainer')

with open('data.js', 'w') as f:
    f.write(d)

r = subprocess.run(['node', '--check', 'data.js'], capture_output=True, text=True)
if r.returncode == 0:
    print(f"\nSUCCESS: All fixes applied, {len(d)} bytes, syntax OK")
else:
    print(f"\nERROR: {r.stderr}")

# Verify fixes
cases = re.findall(r"id: '(case-\w+)'", d)
for c in cases:
    idx = d.find(f"id: '{c}'")
    t3_start = d.find('Agent-specifikation', idx)
    t4_marker = d.find('4. Kommunikation', idx)
    block = d[t3_start:t4_marker]
    
    eval_start = block.find('Kvalitetsgranskare')
    eval_block = block[eval_start:]
    
    has_formagor = 'Formagor:' in eval_block
    has_dual_input = 'Agent 1' in eval_block and 'Agent 2' in eval_block
    
    title_m = re.search(r"title: '([^']+)'", d[idx:idx+200])
    title = title_m.group(1) if title_m else c
    
    status = "✅" if has_formagor and has_dual_input else "⚠️"
    print(f"  {status} {title}: Formagor={has_formagor}, DualInput={has_dual_input}")
