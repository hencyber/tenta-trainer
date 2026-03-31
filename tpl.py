import re
def esc(s):
    return re.sub(r"(?<!\\)'", "\\'", s)
def co(b,s,k,v,c,t,p):
    return f'<strong>Bransch:</strong> {b}<br><strong>Storlek:</strong> {s}<br><strong>Kunder:</strong> {k}<br><strong>Volym:</strong> {v}<br><strong>Compliance:</strong> {c}<br><strong>Teknisk miljo:</strong> {t}<br><strong>Stort problem:</strong> {p}'
def t1(ag,au):
    h='<h5>V Exempelsvar</h5><p><strong>Tolkningsbaserade steg (agenter):</strong></p><ul>'+''.join(f'<li>{s}</li>' for s in ag)+'</ul><p><strong>Klassisk automation/regelmotor:</strong></p><ul>'+''.join(f'<li>{s}</li>' for s in au)+'</ul>'
    return h
def t2(mot,pat,pw,fl):
    return f'<h5>V Exempelsvar</h5><p><strong>Varfor bor detta flode implementeras?</strong> {mot}</p><p><strong>Monster: {pat}</strong></p><p>Motivering: {pw}</p><pre>{fl}</pre>'
def t3(agents):
    h='<h5>V Exempelsvar</h5>'
    for i,(nm,ro,up,rl,fm,mo,inp,out,ca,pe) in enumerate(agents):
        h+=f'<h4>Agent {i+1}: {nm}</h4><p><strong>Systeminstruktion:</strong></p><pre># Roll\\n{ro}\\n\\n# Uppgift\\n{up}\\n\\n# Regler\\n'+''.join(f'- {r}\\n' for r in rl)+f'\\n# Format\\n{fm}</pre><p><strong>Varfor behovs agenten?</strong> {mo}</p><p><strong>Input:</strong> {inp}</p><p><strong>Output:</strong> {out}</p>'
        if ca: h+='<p><strong>Formagor:</strong></p><ul>'+''.join(f'<li>{c}</li>' for c in ca)+'</ul>'
        h+='<p><strong>Rattigheter:</strong></p><ul>'+''.join(f'<li>{p}</li>' for p in pe)+'</ul>'
    return h
def t4(af,at,flds,w):
    h=f'<h5>V Exempelsvar</h5><p>Mellan <strong>{af}</strong> -> <strong>{at}</strong> sker overlamning via strukturerad JSON:</p><pre>{{\\n'
    for k,d in flds: h+=f'  \\"{k}\\": \\"{d}\\",\\n'
    return h+f'}}</pre><p><strong>Varfor denna struktur?</strong> {w}</p>'
def t5(fn,dc,inp,out,w):
    return f'<h5>V Exempelsvar</h5><pre>def {fn}({inp}) -> dict:\\n    \\\"\\\"\\\"{dc}\\n    Input: {inp}\\n    Output: {out}\\\"\\\"\\\"</pre><p><strong>Varfor behovs verktyget?</strong> {w}</p>'
def t6(risks,hitl):
    h='<h5>V Exempelsvar</h5><p><strong>Identifierade risker:</strong></p><ul>'+''.join(f'<li><strong>{r}:</strong> {m}</li>' for r,m in risks)+f'</ul><p><strong>HITL-punkter:</strong> {hitl}</p><p><strong>Loggning:</strong> Alla agentbeslut loggas med tidstampel och kalldata for audit trail.</p>'
    return h
