document.addEventListener('DOMContentLoaded', () => {
    // State
    const state = {
        currentView: 'home',
        topicsCompleted: 0,
        quizScore: 0,
        quizIndex: 0,
        currentQuiz: [],
        answeredQuestions: new Set()
    };

    // DOM Elements
    const navBtns = document.querySelectorAll('.nav-btn');
    const views = document.querySelectorAll('.view');
    
    // Init App
    initNav();
    renderTopics();
    updateStats();
    
    // Setup Navigation
    function initNav() {
        navBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                const viewId = e.target.dataset.view;
                switchView(viewId);
            });
        });
    }

    // Switch View Helper (global scope for inline onclicks)
    window.switchView = (viewId) => {
        // Update Nav
        navBtns.forEach(btn => btn.classList.remove('active'));
        const targetBtn = document.querySelector(`.nav-btn[data-view="${viewId}"]`);
        if(targetBtn) targetBtn.classList.add('active');

        // Update View
        views.forEach(v => v.classList.remove('active'));
        document.getElementById(`view-${viewId}`).classList.add('active');
        
        // Handle specific view logical load
        if(viewId === 'quiz') startQuiz();
        if(viewId === 'case') renderCase();
        if(viewId === 'cheatsheet') renderCheatsheet();
        
        window.scrollTo(0,0);
    };

    // Render Topics Grid
    function renderTopics() {
        const grid = document.getElementById('topicsGrid');
        if(!grid) return;
        
        grid.innerHTML = examData.topics.map((t, index) => `
            <div class="topic-card" onclick="openTopic('${t.id}')">
                <div class="topic-num">Område ${index + 1}</div>
                <div class="topic-title">${t.title}</div>
                <div class="topic-desc">${t.desc}</div>
                <spån class="topic-tag tag-${t.level}">${t.level.toUpperCase()}</spån>
            </div>
        `).join('');
    }

    // Open Specific Topic
    window.openTopic = (topicId) => {
        const t = examData.topics.find(c => c.id === topicId);
        if(!t) return;
        
        const container = document.getElementById('topicContent');
        
        // Find practice questions for this topic
        const pqs = (examData.practiceQuestions || []).filter(p => p.topicId === topicId);
        let pqHtml = '';
        pqs.forEach((pq, i) => {
            pqHtml += `
                <div class="practice-q">
                    <h4>Övningsfråga: ${pq.title}</h4>
                    <p>${pq.question}</p>
                    <textarea class="answer-area" placeholder="Skriv ditt svar här..."></textarea>
                    <button class="btn-reveal" onclick="toggleAnswer('pq-${topicId}-${i}')">👁️ Visa facit</button>
                    <div id="pq-${topicId}-${i}" class="model-answer">
                        <h5>✔ Exempelsvar / Facit</h5>
                        <pre style="white-space:pre-wrap;font-family:inherit;">${pq.modelAnswer}</pre>
                    </div>
                </div>
            `;
        });

        container.innerHTML = `
            <h2>${t.title}</h2>
            <spån class="topic-tag tag-${t.level}" style="margin-bottom: 24px;">NIVÅ ${t.level.toUpperCase()}</spån>
            
            <div class="theory-section">
                <h3>📚 Teori</h3>
                <ul>
                    ${t.theory.map(item => `<li>${item}</li>`).join('')}
                </ul>
            </div>
            
            <div class="theory-section">
                <h3>🔑 Nyckelbegrepp</h3>
                ${t.keyConcepts.map(c => `<div class="key-concept">${c}</div>`).join('')}
            </div>

            ${pqHtml ? '<h3 style="margin:24px 0 12px;">✍️ Övningsfrågor</h3>' + pqHtml : ''}
            
            <button class="btn-mark-done" onclick="markTopicDone(this, '${t.id}')">✅ Markera som läst</button>
        `;
        
        // Hide Topics, show Detail
        views.forEach(v => v.classList.remove('active'));
        document.getElementById('view-topic-detail').classList.add('active');
        window.scrollTo(0,0);
    };

    window.markTopicDone = (btn, id) => {
        btn.classList.add('done');
        btn.innerText = 'Läst';
        
        // Find card and add check
        const cards = document.querySelectorAll('.topic-card');
        const index = examData.topics.findIndex(t => t.id === id);
        if(cards[index]) cards[index].classList.add('completed');
        
        state.topicsCompleted++;
        updateProgress();
    };

    // Stats and Progress Hook
    function updateStats() {
        const total = examData.quiz.length + (examData.practiceQuestions || []).length;
        document.getElementById('totalQuestions').innerText = total;
    }

    function updateProgress() {
        const total = examData.topics.length;
        const p = Math.round((state.topicsCompleted / total) * 100) || 0;
        
        document.getElementById('progressText').innerText = p + '%';
        const ring = document.getElementById('progressRing');
        const offset = 100 - p;
        ring.style.strokeDasharray = `${p}, 100`;
    }

    // Mini Quiz System
    function startQuiz() {
        // Simple randomizer for demo
        state.currentQuiz = [...examData.quiz].sort(() => Math.random() - 0.5);
        state.quizIndex = 0;
        state.quizScore = 0;
        renderQuizQuestion();
    }

    function renderQuizQuestion() {
        const container = document.getElementById('quizArea');
        if(state.quizIndex >= state.currentQuiz.length) {
            container.innerHTML = `
                <div class="quiz-score">
                    <h3>Quiz Avslutat!</h3>
                    <div class="score-num">${state.quizScore} / ${state.currentQuiz.length}</div>
                    <p style="color:var(--text-dim);margin-top:16px;">Bra jobbat! Caset väntar på dig.</p>
                    <button class="btn-primary" style="margin-top:24px;" onclick="switchView('case')">Kör Case-övning</button>
                </div>
            `;
            return;
        }

        const q = state.currentQuiz[state.quizIndex];
        const letters = ['A', 'B', 'C', 'D'];
        
        container.innerHTML = `
            <div class="quiz-card">
                <div class="quiz-meta">
                    <spån class="quiz-badge" style="background:var(--accent-glow);color:var(--accent-light);">Fråga</spån>
                    <spån class="quiz-counter">${state.quizIndex + 1} av ${state.currentQuiz.length}</spån>
                </div>
                <div class="quiz-question">${q.question}</div>
                <div class="quiz-options">
                    ${q.options.map((opt, i) => `
                        <div class="quiz-option" onclick="handleQuizAnswer(this, ${opt.isCorrect})">
                            <span class="option-letter">${letters[i]}</span>
                            <span>${opt.text}</span>
                        </div>
                    `).join('')}
                </div>
                <div id="quizExplain" class="quiz-explanation">
                    <strong>Förklaring:</strong> ${q.explanation}
                </div>
                <div class="quiz-nav">
                    <button id="nextQuizBtn" class="btn-quiz-next" style="display:none;" onclick="nextQuiz()">Nästa fråga →</button>
                </div>
            </div>
        `;
    }

    window.handleQuizAnswer = (elem, isCorrect) => {
        // Disable others
        const options = document.querySelectorAll('.quiz-option');
        options.forEach(o => o.classList.add('disabled'));
        
        // Show correct / wrong
        if(isCorrect) {
            elem.classList.add('correct');
            state.quizScore++;
        } else {
            elem.classList.add('wrong');
            // Find correct one
            const q = state.currentQuiz[state.quizIndex];
            const correctIndex = q.options.findIndex(o => o.isCorrect);
            options[correctIndex].classList.add('correct');
        }
        
        // Show explanation
        document.getElementById('quizExplain').classList.add('visible');
        document.getElementById('nextQuizBtn').style.display = 'block';
        
        // Update stats top nav
        state.answeredQuestions.add(state.quizIndex);
        document.getElementById('answeredQuestions').innerText = state.answeredQuestions.size;
    };

    window.nextQuiz = () => {
        state.quizIndex++;
        renderQuizQuestion();
    };

    // Case System
    function renderCase() {
        const container = document.getElementById('caseArea');
        const icons = ['🏥','🚛','🏦','⚡','👔','🎓','🍽️','📰','🏠','⚖️'];
        // Show case picker
        let html = `<div class="case-picker">`;
        examData.cases.forEach((c, idx) => {
            const icon = icons[idx] || '📋';
            html += `
                <div class="case-pick-card" onclick="openCase(${idx})">
                    <div class="case-pick-icon">${icon}</div>
                    <h3>${c.title}</h3>
                    <p>${c.intro.substring(0, 120)}...</p>
                    <spån class="case-pick-count">${c.tasks.length} uppgifter</spån>
                </div>
            `;
        });
        html += `</div>`;
        container.innerHTML = html;
    }

    window.openCase = (caseIdx) => {
        const container = document.getElementById('caseArea');
        const c = examData.cases[caseIdx];
        
        let html = `
            <button class="btn-back" onclick="renderCaseAndShow()">← Tillbaka till case-val</button>
            <div class="case-intro">
                <h3>${c.title}</h3>
                <p>${c.intro}</p>
                ${c.companyInfo ? `
                <div class="case-company-grid">
                    ${c.companyInfo}
                </div>` : ''}
                ${c.processInput ? `
                <div class="process-input-section"><strong>📥 Input:</strong> ${c.processInput}</div>` : ''}
                ${c.currentFlow ? `
                <div class="case-current-flow">
                    <h4>📋 Nuvarande flöde (manuellt):</h4>
                    <ol>${c.currentFlow.map(s => `<li>${s}</li>`).join('')}</ol>
                </div>` : ''}
                ${c.diagram ? `
                <div class="case-diagram-section">
                    <h4>🔀 Agentflöde (visuellt):</h4>
                    <div class="mermaid-container"><pre class="mermaid">${c.diagram.replace(/\\n/g, '\n')}</pre></div>
                </div>` : ''}
            </div>
        `;
        
        c.tasks.forEach((t, index) => {
            const ansId = `case-ans-${caseIdx}-${index}`;
            html += `
                <div class="practice-q">
                    <h4>${t.title}</h4>
                    <p>${t.question}</p>
                    <textarea class="answer-area" placeholder="Skriv ditt svar här..."></textarea>
                    <button class="btn-reveal" onclick="toggleAnswer('${ansId}')">👁️ Visa rätt svar / Facit</button>
                    <div id="${ansId}" class="model-answer">
                        <h5>✔ Exempelsvar / Facit:</h5>
                        ${t.modelAnswer}
                    </div>
                </div>
            `;
        });
        
        container.innerHTML = html;
        if(c.diagram && typeof mermaid !== 'undefined') {
            mermaid.run({nodes: container.querySelectorAll('.mermaid')});
        }
        window.scrollTo(0, 0);
    };

    window.renderCaseAndShow = () => {
        renderCase();
        window.scrollTo(0, 0);
    };

    window.toggleAnswer = (id) => {
        const el = document.getElementById(id);
        if(el) el.classList.toggle('visible');
    };

    // Cheatsheet
    function renderCheatsheet() {
        const el = document.getElementById('cheatsheetArea');
        el.innerHTML = `
        <div class="cheat-section">
            <h3>Nyckelbegrepp</h3>
            <table class="cheat-table">
                <tr><th>Begrepp</th><th>Definition</th></tr>
                <tr><td>Autoregressiv</td><td>Genererar en token i taget baserat på allt före</td></tr>
                <tr><td>Context window</td><td>Modellens arbetsminne</td></tr>
                <tr><td>Hallucination</td><td>Modellen hittar på trovärdiga men felaktiga säker</td></tr>
                <tr><td>Temperature</td><td>Låg = stabilt, hög = kreativt</td></tr>
                <tr><td>RAG</td><td>Retrieval-Augmented Generation: hämta → infoga → generera</td></tr>
                <tr><td>Embeddings</td><td>Text som vektor för semantisk sökning</td></tr>
                <tr><td>Tool</td><td>Extern funktion modellen ber systemet köra</td></tr>
                <tr><td>MCP</td><td>Model Context Protocol – standardiserar verktyg</td></tr>
                <tr><td>Prompt injection</td><td>Extern data manipulerar agentens beteende</td></tr>
                <tr><td>Least privilege</td><td>Minsta möjliga behörighet</td></tr>
                <tr><td>HITL</td><td>Human-in-the-loop: människa godkänner vid risk</td></tr>
                <tr><td>Definition of Done</td><td>Tydliga kriterier för "färdigt"</td></tr>
                <tr><td>Governance</td><td>Policy → beteende → logg → förbättring</td></tr>
                <tr><td>Varians</td><td>Icke-deterministiskt beteende – kontrollera var det är tillåtet</td></tr>
                <tr><td>Tokenisering</td><td>Text → subword-tokens → numeriska ID:n. Påverkar context window + kostnad</td></tr>
                <tr><td>RLHF</td><td>Reinforcement Learning from Human Feedback – människor rankar svar → modellen lär sig</td></tr>
                <tr><td>Chain-of-Thought</td><td>Be modellen resonera steg-för-steg → bättre logik/matematik</td></tr>
                <tr><td>Role confusion</td><td>Agent blandar roller (planner kodar, critic skriver om text)</td></tr>
                <tr><td>Cascading errors</td><td>Tidigt fel förstärks i kedjan ("viskleken")</td></tr>
                <tr><td>Gemensam ärendefil</td><td>Delad state (JSON/YAML) som agenter uppdaterar stegvis</td></tr>
            </table>
        </div>
        <div class="cheat-section">
            <h3>Multi-agent-mönster</h3>
            <table class="cheat-table">
                <tr><th>Mönster</th><th>Beskrivning</th><th>Bäst för</th></tr>
                <tr><td>Handoff</td><td>A→B→C stafettpinne</td><td>Linjära flöden</td></tr>
                <tr><td>Supervisor</td><td>Manager väljer expert-agenter</td><td>Dynamiska val</td></tr>
                <tr><td>Planner-Doer-Critic</td><td>Plan → Utför → Granska</td><td>Kvalitetssäkring</td></tr>
                <tr><td>Hybrid</td><td>if/else + LLM</td><td>Regelstyrt + tolkning</td></tr>
                <tr><td>HITL</td><td>Människa godkänner</td><td>Högriskbeslut</td></tr>
            </table>
        </div>
        <div class="cheat-section">
            <h3>Systeminstruktion – Mall</h3>
            <pre style="color:var(--green);background:rgba(0,0,0,0.3);padding:16px;border-radius:8px;font-size:0.85rem;">
# Roll
[Vem är agenten?]

# Uppgift
[Vad ska den göra exakt?]

# Regler
- [Begränsning 1]
- [Begränsning 2]

# Format
[Hur ska output se ut? JSON/Markdown/etc]
            </pre>
        </div>
        <div class="cheat-section">
            <h3>Case-mall (Vad du ska göra på tentan)</h3>
            <ol style="color:var(--text-dim);font-size:0.9rem;">
                <li><strong>Analysera processen</strong> – Vad är tolkningsbaserat? Regelbaserat? HITL?</li>
                <li><strong>Välj mönster</strong> – Handoff/Supervisor/PDC/Hybrid + motivera</li>
                <li><strong>Designa agenter (minst 3)</strong> – Roll/Uppgift/Regler/Format + input/output</li>
                <li><strong>Rita diagram</strong> – Agenter, pilar, verktyg, feedback-loop, HITL</li>
                <li><strong>Beskriv verktyg</strong> – Minst 1 funktionsanrop med input/output</li>
                <li><strong>Risker (minst 3)</strong> – Hallucination, GDPR, loop-risk + åtgärder</li>
            </ol>
        </div>
        <div class="cheat-section">
            <h3>Promptramverk (COSTAR & MEEPO)</h3>
            <table class="cheat-table">
                <tr><th>COSTAR</th><th>Beskrivning</th></tr>
                <tr><td>C - Context</td><td>Bakgrund och situation</td></tr>
                <tr><td>O - Objective</td><td>Vad ska uppnås?</td></tr>
                <tr><td>S - Style</td><td>Vilken ton/stil?</td></tr>
                <tr><td>T - Tone</td><td>Formell, informell, teknisk?</td></tr>
                <tr><td>A - Audience</td><td>Vem läser resultatet?</td></tr>
                <tr><td>R - Response</td><td>Format (JSON, lista, mejl)?</td></tr>
            </table>
            <table class="cheat-table" style="margin-top:16px;">
                <tr><th>MEEPO</th><th>Beskrivning</th></tr>
                <tr><td>M - Mission</td><td>Uppdraget / målet</td></tr>
                <tr><td>E - Examples</td><td>Few-shot-exempel</td></tr>
                <tr><td>E - Execution</td><td>Steg-för-steg-instruktioner</td></tr>
                <tr><td>P - Persona</td><td>Vilken roll/karaktär?</td></tr>
                <tr><td>O - Output</td><td>Önskat format</td></tr>
            </table>
            <p style="color:var(--text-dim);font-size:0.85rem;margin-top:12px;">💡 <strong>Roll/Uppgift/Regler/Format</strong> som vi använt är en förenkling av dessa ramverk. Alla fungerar — det viktiga är att ha <em>tydlig struktur</em>.</p>
        </div>
        <div class="cheat-section">
            <h3>Guardrails & Kontrollmekanismer</h3>
            <table class="cheat-table">
                <tr><th>Mekanism</th><th>Vad det gör</th></tr>
                <tr><td>Temperature/Top-p</td><td>Kontrollerar kreativitet vs determinism. Låg temp = stabilt.</td></tr>
                <tr><td>Output-schema</td><td>Tvinga JSON-format → förhindrar fri text (minskar hallucinering)</td></tr>
                <tr><td>Max tokens</td><td>Begränsar svarslängd → förhindrar "rambling"</td></tr>
                <tr><td>Middleware</td><td>Sanerar input/output mellan agenter (PII-maskning, schema-validering)</td></tr>
                <tr><td>Stoppvillkor</td><td>Max antal loopar, timeout, Definition of Done</td></tr>
                <tr><td>Fallback</td><td>Om agent misslyckas → eskalera till människa</td></tr>
            </table>
        </div>
        <div class="cheat-section">
            <h3>Processdesign: Use-Case Discovery</h3>
            <p style="color:var(--text-dim);font-size:0.9rem;margin-bottom:12px;">Hur hittar du processer som lämpar sig för agenter?</p>
            <ol style="color:var(--text-dim);font-size:0.85rem;">
                <li><strong>Hög volym + repetitivt</strong> — "Vi gör detta 500 gånger/dag"</li>
                <li><strong>Ostrukturerad input</strong> — Fri text (mejl, PDF:er, chat)</li>
                <li><strong>Kräver tolkning</strong> — "Det beror på vad kunden menar"</li>
                <li><strong>Många undantag</strong> — If/else klarar inte alla varianter</li>
                <li><strong>Kvalitetsproblem</strong> — Inkonsekvent resultat mellan handläggare</li>
            </ol>
            <p style="color:var(--text-dim);font-size:0.85rem;margin-top:12px;">❌ <strong>Använd INTE agent för:</strong> Rent regelbaserat (bokföring), lagkrav på determinism, enkel trigger→action (SMS vid statusändring).</p>
        </div>
        `;
    }
});
