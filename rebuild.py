#!/usr/bin/env python3
"""Rebuild data.js - extracts content from broken file and writes clean JS."""
import re

# Read pre-cases (verified working)
with open('/tmp/pre_cases.txt', 'r') as f:
    pre = f.read()

# Read broken file
with open('/home/cybercore/Skrivbord/uppgiftskola2/tenta-trainer/data.js.broken', 'r') as f:
    broken = f.read()

# Extract ALL model answer HTML blocks using the marker pattern
marker = '<h5>✔ Exempelsvar</h5>'
parts = broken.split(marker)
# parts[0] = before first answer, parts[1..n] = answer content + trailing junk
answers = []
for i in range(1, len(parts)):
    raw = marker + parts[i]
    # Find where the answer ends: look for next "' }," or "' }" 
    for end in ["' },", "' }\n", "' }"]:
        pos = raw.find(end)
        if pos > 0:
            raw = raw[:pos]
            break
    answers.append(raw)

print(f"Total answers extracted: {len(answers)}")

# Extract case metadata from broken file
# companyInfo strings
ci = re.findall(r"companyInfo: '(.*?)',\s*$", broken, re.MULTILINE)
pi = re.findall(r"processInput: '(.*?)',\s*$", broken, re.MULTILINE)
print(f"CompanyInfos: {len(ci)}, ProcessInputs: {len(pi)}")

# Since metadata was also collapsed, let me extract differently
# Search for specific patterns
def extract_between(text, start_pat, end_pat):
    s = text.find(start_pat)
    if s == -1: return None
    s += len(start_pat)
    e = text.find(end_pat, s)
    if e == -1: return None
    return text[s:e]

# For each case, the intro/companyInfo/etc are all on collapsed lines
# Let me find them by searching for the case IDs
case_ids = ['case-tech', 'case-fleet', 'case-bank', 'case-energy', 'case-recruit',
            'case-edu', 'case-food', 'case-media', 'case-property', 'case-legal']

# Find the position of each case
case_positions = {}
for cid in case_ids:
    pos = broken.find(f"id: '{cid}'")
    if pos >= 0:
        case_positions[cid] = pos
        
print(f"Found {len(case_positions)} case positions")

# Since the broken file has everything on long collapsed lines,
# let me extract the FULL line containing each case ID
case_lines = {}
for cid, pos in case_positions.items():
    # Find the line containing this position
    line_start = broken.rfind('\n', 0, pos) + 1
    line_end = broken.find('\n', pos)
    if line_end == -1: line_end = len(broken)
    case_lines[cid] = broken[line_start:line_end]

# Check how much data is on each case's line
for cid in case_ids:
    if cid in case_lines:
        print(f"  {cid}: {len(case_lines[cid])} chars")
    else:
        print(f"  {cid}: NOT FOUND")

# Now, from these long lines, extract metadata
def safe_extract(line, key):
    """Extract a value from key: 'value' pattern."""
    pat = key + ": '"
    start = line.find(pat)
    if start == -1: return ''
    start += len(pat)
    # Find matching closing quote - handle escaped quotes
    depth = 0
    i = start
    while i < len(line):
        if line[i] == '\\' and i+1 < len(line):
            i += 2  # skip escaped char
            continue
        if line[i] == "'":
            return line[start:i]
        i += 1
    return line[start:start+100]

cases_meta = {}
for cid in case_ids:
    if cid not in case_lines:
        continue
    line = case_lines[cid]
    meta = {
        'title': safe_extract(line, 'title'),
        'intro': safe_extract(line, 'intro'),
        'companyInfo': safe_extract(line, 'companyInfo'),
        'processInput': safe_extract(line, 'processInput'),
    }
    # Extract currentFlow array
    cf_start = line.find("currentFlow: [")
    if cf_start >= 0:
        cf_end = line.find("]", cf_start)
        if cf_end >= 0:
            cf_raw = line[cf_start+14:cf_end]
            meta['currentFlow'] = cf_raw
    
    cases_meta[cid] = meta
    print(f"  {cid} title: {meta['title'][:50]}")

print("\nAll metadata extracted. Now building data.js...")

# The case_lines for case-tech contains EVERYTHING (all 10 cases)
# because they were all collapsed into one mega-line.
# That's why only case-tech was found (it's the first case).

# Let me re-extract by splitting the mega-line at case boundaries
mega = case_lines.get('case-tech', '')
if mega:
    # Split at each "id: 'case-" pattern
    case_blocks = re.split(r"(?=id: 'case-)", mega)
    print(f"\nFound {len(case_blocks)} case blocks in mega-line")
    for block in case_blocks:
        cid_match = re.search(r"id: '(case-\w+)'", block)
        if cid_match:
            cid = cid_match.group(1)
            meta = {
                'title': safe_extract(block, 'title'),
                'intro': safe_extract(block, 'intro'),
                'companyInfo': safe_extract(block, 'companyInfo'),
                'processInput': safe_extract(block, 'processInput'),
            }
            cf_start = block.find("currentFlow: [")
            if cf_start >= 0:
                cf_end = block.find("]", cf_start)
                if cf_end >= 0:
                    meta['currentFlow'] = block[cf_start+14:cf_end]
            
            cases_meta[cid] = meta
            print(f"  {cid}: title='{meta['title'][:40]}' intro_len={len(meta['intro'])}")

# Now extract the answers for each case from the blocks
# Each block contains modelAnswer strings
case_answers = {}
for block in case_blocks:
    cid_match = re.search(r"id: '(case-\w+)'", block)
    if not cid_match:
        continue
    cid = cid_match.group(1)
    # Find all modelAnswer strings in this block
    ma_parts = block.split(marker)
    case_ma = []
    for i in range(1, len(ma_parts)):
        raw = marker + ma_parts[i]
        for end in ["' },", "' }\n", "' }"]:
            pos = raw.find(end)
            if pos > 0:
                raw = raw[:pos]
                break
        case_ma.append(raw)
    case_answers[cid] = case_ma
    print(f"  {cid}: {len(case_ma)} model answers")

# Now extract questions for each case
case_questions = {}
for block in case_blocks:
    cid_match = re.search(r"id: '(case-\w+)'", block)
    if not cid_match:
        continue
    cid = cid_match.group(1)
    questions = re.findall(r"question: '(.*?)',", block)
    case_questions[cid] = questions
    print(f"  {cid}: {len(questions)} questions")

# Now extract task titles for each case
case_titles = {}
for block in case_blocks:
    cid_match = re.search(r"id: '(case-\w+)'", block)
    if not cid_match:
        continue
    cid = cid_match.group(1)
    titles = re.findall(r"title: '(\d+\. .*?)'", block)
    case_titles[cid] = titles

# BUILD THE OUTPUT
def js_str(s):
    """Escape a string for use in JS single quotes."""
    s = s.replace('\\', '\\\\')
    s = s.replace("'", "\\'")
    s = s.replace('\n', '\\n')
    s = s.replace('\r', '')
    return s

output = pre + '\n'

for cid in case_ids:
    meta = cases_meta.get(cid, {})
    if not meta.get('title'):
        print(f"WARNING: No metadata for {cid}, skipping")
        continue
    
    ma_list = case_answers.get(cid, [])
    q_list = case_questions.get(cid, [])
    t_list = case_titles.get(cid, [])
    
    cf = meta.get('currentFlow', '')
    
    output += f"""        {{
            id: '{cid}',
            title: '{js_str(meta["title"])}',
            intro: '{js_str(meta["intro"])}',
            companyInfo: '{js_str(meta["companyInfo"])}',
            processInput: '{js_str(meta["processInput"])}',
            currentFlow: [{cf}],
            tasks: [\n"""
    
    # Write tasks
    num_tasks = min(len(t_list), len(q_list), len(ma_list))
    for i in range(num_tasks):
        comma = ',' if i < num_tasks - 1 else ''
        output += f"                {{ title: '{js_str(t_list[i])}', question: '{js_str(q_list[i])}',\n"
        output += f"                  modelAnswer: '{js_str(ma_list[i])}' }}{comma}\n"
    
    output += """            ]
        },
"""

# Close the structure
output = output.rstrip().rstrip(',') + '\n'
output += """    ]
};
"""

# Write the file
with open('/home/cybercore/Skrivbord/uppgiftskola2/tenta-trainer/data.js', 'w') as f:
    f.write(output)

print(f"\nWrote {len(output)} chars to data.js")

# Validate
import subprocess
result = subprocess.run(['node', '--check', '/home/cybercore/Skrivbord/uppgiftskola2/tenta-trainer/data.js'],
                       capture_output=True, text=True)
if result.returncode == 0:
    print("✅ JavaScript syntax is VALID!")
else:
    print(f"❌ JS Error: {result.stderr[:200]}")
