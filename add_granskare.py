#!/usr/bin/env python3
"""Add domain-specific Granskare agent (GODKÄNT/REVIDERA loop) to all cases."""
import re

with open('data.js') as f:
    d = f.read()

# Domain-specific Granskare for each case
GRANSKARE = {
'case-tech': ('Kvalitetsgranskare','Du ar kvalitetsgranskare for kliniska larmbedomningar.','Granska den kliniska bedomningen. Kontrollera att klassificering och rekommendation ar konsekventa och korrekt motiverade.',['Borja ALLTID med GODKANT eller REVIDERA','Ge kortfattad feedback om brister','Max 2 revideringar, sedan eskalera till manniska','Var extra strikt pa kritiska larm'],'GODKANT/REVIDERA\\nFeedback: [din feedback]','Utan kvalitetskontroll riskerar felaktiga bedomningar att na sjukskoterskan. Granskaren sakertstaller att agenternas output ar konsekvent och korrekt motiverad.','Klinisk bedomning fran Agent 2','GODKANT (till HITL) eller REVIDERA med feedback (tillbaka till Agent 2, max 2 forsok)',[],'Rattighet att skicka tillbaka for revidering','Ingen patientkontakt'),
'case-fleet': ('Kvalitetsgranskare','Du ar kvalitetsgranskare for logistikbeslut.','Granska ruttrekommendationen. Kontrollera att den ar realistisk, kostnadseffektiv och uppfyller SLA.',['Borja ALLTID med GODKANT eller REVIDERA','Kontrollera att SLA uppfylls','Verifiera att rutten ar realistisk','Max 2 revideringar'],'GODKANT/REVIDERA\\nFeedback: [din feedback]','Felaktiga ruttforslag kan kosta pengar och bryta SLA. Granskaren kontrollerar innan transportledaren ser forslaget.','Ruttalternativ fran Ruttoptimeraren','GODKANT eller REVIDERA med feedback (max 2 forsok)',[],'Rattighet att skicka tillbaka for revidering','Ingen ruttaktivering'),
'case-bank': ('Kvalitetsgranskare','Du ar kvalitetsgranskare for kreditbedomningar.','Granska riskbedomningen. Kontrollera att alla riskflaggor ar korrekt identifierade och att rekommendationen foljer policymatrisen.',['Borja ALLTID med GODKANT eller REVIDERA','Korsvalidera mot policymatris','Kontrollera att skuldkvot ar korrekt beraknad','Max 2 revideringar'],'GODKANT/REVIDERA\\nFeedback: [din feedback]','Felaktiga kreditbedomningar kan leda till daliga lan eller missade affarer. Granskaren sakertstaller konsekvent kvalitet.','Riskbedomning fran Riskbedomaren + beslutsunderlag','GODKANT eller REVIDERA med feedback (max 2 forsok)',[],'Lasakomst till policymatris','Ingen beslutsbefogenhet'),
'case-energy': ('Kvalitetsgranskare','Du ar kvalitetsgranskare for underhallsplaner.','Granska atgardsplanen. Kontrollera att prioritering ar korrekt, resurser ar rimliga och vader beaktats.',['Borja ALLTID med GODKANT eller REVIDERA','Kontrollera att riskniva matchar prioritet','Verifiera resursbehov','Max 2 revideringar'],'GODKANT/REVIDERA\\nFeedback: [din feedback]','Felaktiga underhallsplaner kan leda till onodiga kostnader eller missade akuta fel. Granskaren kontrollerar innan arbetsorder skapas.','Atgardsplan fran Underhallsplaneraren','GODKANT eller REVIDERA med feedback (max 2 forsok)',[],'Rattighet att skicka tillbaka','Ingen arbetsorderratt'),
'case-recruit': ('Kvalitetsgranskare','Du ar kvalitetsgranskare for rekryteringsbedomningar.','Granska matchresultatet. Kontrollera att bedomningen ar objektiv, evidensbaserad och fri fran bias.',['Borja ALLTID med GODKANT eller REVIDERA','Kontrollera att maste-krav bedomts korrekt','Flagga eventuell bias','Max 2 revideringar'],'GODKANT/REVIDERA\\nFeedback: [din feedback]','Utan kvalitetskontroll riskerar biased eller felaktiga matchningar att na rekryteraren. Granskaren sakertstaller objektivitet.','Matchresultat fran Matchningsagenten','GODKANT eller REVIDERA med feedback (max 2 forsok)',[],'Rattighet att skicka tillbaka','Ingen kandidatkontakt'),
'case-edu': ('Kvalitetsgranskare','Du ar tonkontrollant och kvalitetsgranskare for studentsvar.','Granska det genererade svaret. Kontrollera att det ar korrekt, vanligt formulerat och baserat pa kunskapsbasen.',['Borja ALLTID med GODKANT eller REVIDERA','Kontrollera att svaret ENBART baseras pa kunskapsbasen','Verifiera att tonen ar professionell och hjalpsam','Max 2 revideringar'],'GODKANT/REVIDERA\\nFeedback: [din feedback]','Felaktiga eller oartiga svar till studenter skadar foretaget. Granskaren sakertstaller kvalitet innan svaret skickas.','Formulerat svar fran Svarsagenten','GODKANT (svaret skickas) eller REVIDERA med feedback (max 2 forsok)',[],'Kontroll av kunskapsbas-kallor','Ingen studentkontakt'),
'case-food': ('Kvalitetsgranskare','Du ar kvalitetsgranskare for inspektionsbedomningar.','Granska riskbedomningen. Kontrollera att avvikelser klassificerats korrekt och att atgardsforslaget ar proportionerligt.',['Borja ALLTID med GODKANT eller REVIDERA','Kontrollera lagreferenser','Verifiera att historik beaktats','Max 2 revideringar'],'GODKANT/REVIDERA\\nFeedback: [din feedback]','Inkonsekvent riskbedomning ar huvudproblemet. Granskaren sakertstaller att alla inspektioner bedms lika.','Riskbedomning fran Riskbedomaren','GODKANT eller REVIDERA med feedback (max 2 forsok)',[],'Lasakomst till lagar och praxis','Ingen myndighetsbeslutsbefogenhet'),
'case-media': ('Kvalitetsgranskare','Du ar kvalitetsgranskare for moderationsbeslut.','Granska policybedomningen for grazon-kommentarer. Kontrollera att yttrandefriheten respekteras och att policyreferensen ar korrekt.',['Borja ALLTID med GODKANT eller REVIDERA','Ta hansyn till yttrandefrihet','Kontrollera att ratt policyregel refereras','Max 2 revideringar'],'GODKANT/REVIDERA\\nFeedback: [din feedback]','Felaktig moderering kan leda till overcensur eller juridiska problem. Granskaren sakertstaller balans.','Policybedomning fran Policybedomaren','GODKANT eller REVIDERA med feedback (max 2 forsok)',[],'Lasakomst till juridisk praxis','Ingen publiceringskontroll'),
'case-property': ('Kvalitetsgranskare','Du ar kvalitetsgranskare for fastighetsarenden.','Granska prioriteringen. Kontrollera att akut-flaggan ar korrekt, att ratt entreprenor valts och att SLA ar rimligt.',['Borja ALLTID med GODKANT eller REVIDERA','Dubbelkolla akut-klassificering','Verifiera entreprenorsval','Max 2 revideringar'],'GODKANT/REVIDERA\\nFeedback: [din feedback]','Felklassificering av akuta arenden ar huvudproblemet. Granskaren fangar upp missar innan arbetsorder skapas.','Prioritering fran Prioriteringsagenten','GODKANT eller REVIDERA med feedback (max 2 forsok)',[],'Kontrollera entreprenorsregister','Ingen avtalsingaende'),
'case-legal': ('Kvalitetsgranskare','Du ar kvalitetsgranskare for juridiska riskanalyser.','Granska riskanalysen. Kontrollera att alla klausuler fangats, att policyreferenserna ar korrekta och att alternativa formuleringar ar juridiskt korrekta.',['Borja ALLTID med GODKANT eller REVIDERA','Kontrollera fullstandighet - alla klausuler?','Verifiera policyreferenser','Max 2 revideringar'],'GODKANT/REVIDERA\\nFeedback: [din feedback]','Missade riskklausuler kan kosta klienten miljoner. Granskaren dubbelgranskar innan PM nar juristen.','Riskanalys fran Klausulgranskaren','GODKANT eller REVIDERA med feedback (max 2 forsok)',[],'Lasakomst till policydatabas och prejudikat','Ingen klientkontakt'),
}

# Build Granskare HTML block
def granskare_html(case_id, agent_num=3):
    g = GRANSKARE[case_id]
    nm,ro,up,rl,fm,mo,inp,out,_,perm1,perm2 = g
    h = f'<h4>Agent {agent_num}: {nm} (Evaluator)</h4>'
    h += '<p><strong>Systeminstruktion:</strong></p><pre>'
    h += f'# Roll\\n{ro}\\n\\n# Uppgift\\n{up}\\n\\n# Regler\\n'
    for r in rl: h += f'- {r}\\n'
    h += f'\\n# Format\\n{fm}</pre>'
    h += f'<p><strong>Varfor behovs agenten?</strong> {mo}</p>'
    h += f'<p><strong>Input:</strong> {inp}</p>'
    h += f'<p><strong>Output:</strong> {out}</p>'
    h += f'<p><strong>Rattigheter:</strong></p><ul><li>{perm1}</li><li>{perm2}</li></ul>'
    return h

# For each case, inject the Granskare into task 3 model answer
for case_id in GRANSKARE:
    # Find case block
    marker = f"id: '{case_id}'"
    idx = d.find(marker)
    if idx < 0: continue
    
    # Count existing agents in task 3
    t3_start = d.find('Agent-specifikation', idx)
    next_task = d.find('4. Kommunikation', idx)
    block = d[t3_start:next_task]
    agent_count = block.count('<h4>Agent ')
    
    # Find the END of the last agent's </ul> in task 3
    # We need to insert BEFORE the closing of the model answer
    # Strategy: find the modelAnswer for task 3 and append before the closing quote
    
    # Find "Agent-specifikation" task's modelAnswer
    ma_search_start = d.find("Agent-specifikation", idx)
    # Find the modelAnswer value start
    ma_start = d.find("modelAnswer: '", ma_search_start)
    if ma_start < 0: continue
    ma_start += len("modelAnswer: '")
    
    # Find the end of this modelAnswer (the closing ' })
    # Need to find the matching single quote, accounting for escaped quotes
    pos = ma_start
    while pos < len(d):
        if d[pos] == "'" and d[pos-1] != '\\':
            break
        pos += 1
    
    # Insert Granskare HTML before the closing quote
    granskare = granskare_html(case_id, agent_count + 1)
    # Escape for JS single-quoted string
    granskare = granskare.replace("'", "\\'")
    d = d[:pos] + granskare + d[pos:]

# Write back
with open('data.js', 'w') as f:
    f.write(d)

import subprocess
r = subprocess.run(['node', '--check', 'data.js'], capture_output=True, text=True)
if r.returncode == 0:
    print(f'SUCCESS: Granskare added to all 10 cases ({len(d)} bytes), syntax OK')
else:
    print(f'ERROR: {r.stderr}')
