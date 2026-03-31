#!/usr/bin/env python3
import sys,re,subprocess
sys.path.insert(0,'/home/cybercore/Skrivbord/uppgiftskola2/tenta-trainer')
from tpl import esc
from cases_1_3 import C
from cases_4_7 import C2
from cases_8_10 import C3
from diagrams import DIAGRAMS
ALL=C+C2+C3
TASKS=[
('1. Processanalys (10p)','Identifiera stegen. Vilka lampar sig for agentifiering vs klassisk automation? Motivera.'),
('2. Agentflode och Monsterval (15p)','Rita/beskriv ett agentflode. Motivera monsterval. Inkludera 2-4 meningars motivering till varfor flodet bor implementeras.'),
('3. Agent-specifikation (30p)','Skriv en fullstandig specifikation per agent: Systeminstruktion (# Roll, # Uppgift, # Regler, # Format), motivering, Input/Output, Formagor/verktyg, Rattigheter.'),
('4. Kommunikation/overlamning (10p)','Beskriv hur data lamnas over mellan tva agenter. Visa JSON-struktur och motivera varfor informationen behovs.'),
('5. Verktyg (10p)','Beskriv minst ett funktionsanrop/tool: funktionsnamn, docstring, input, output. Motivera.'),
('6. Risker och Governance (10p)','Identifiera risker (hallucinering, bias, loops, GDPR). Var bor manniska vara i loopen (HITL)?'),
]
with open('/home/cybercore/Skrivbord/uppgiftskola2/tenta-trainer/data.js.backup_pre_cases','r') as f:
    pre=f.read()
if not pre:
    # fallback: read current data.js and extract pre_cases
    with open('/home/cybercore/Skrivbord/uppgiftskola2/tenta-trainer/data.js','r') as f:
        full=f.read()
    idx=full.find('cases: [')
    if idx>0:
        # find the matching line start
        line_start=full.rfind('\n',0,idx)
        pre=full[:line_start+1]
out=pre.rstrip()+'\n    cases: [\n'
for ci,(cid,title,intro,company,pinput,cflow,answers) in enumerate(ALL):
    out+=f"        {{\n            id: '{esc(cid)}',\n            title: '{esc(title)}',\n"
    out+=f"            intro: '{esc(intro)}',\n"
    out+=f"            companyInfo: '{esc(company)}',\n"
    out+=f"            processInput: '{esc(pinput)}',\n"
    out+=f"            currentFlow: [{','.join(repr(s) for s in cflow)}],\n"
    diag=DIAGRAMS.get(cid,'')
    if diag:
        diag_esc=esc(diag.replace('\n','\\n'))
        out+=f"            diagram: '{diag_esc}',\n"
    out+=f"            tasks: [\n"
    for ti in range(6):
        tname,tq=TASKS[ti]
        ans=answers[ti] if ti<len(answers) else '<h5>V Exempelsvar</h5><p>Se facit.</p>'
        out+=f"                {{ title: '{esc(tname)}', question: '{esc(tq)}', modelAnswer: '{esc(ans)}' }}"
        out+=',\n' if ti<5 else '\n'
    out+=f"            ]\n        }}"
    out+=',\n' if ci<len(ALL)-1 else '\n'
out+='    ]\n};\n'
outpath='/home/cybercore/Skrivbord/uppgiftskola2/tenta-trainer/data.js'
with open(outpath,'w') as f:
    f.write(out)
r=subprocess.run(['node','--check',outpath],capture_output=True,text=True)
if r.returncode==0:
    print(f'SUCCESS: data.js written ({len(out)} bytes), {len(ALL)} cases, syntax OK')
else:
    print(f'ERROR: {r.stderr}')
    sys.exit(1)
