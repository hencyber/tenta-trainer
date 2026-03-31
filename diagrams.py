DIAGRAMS = {
'case-tech': """flowchart TD
    A["📡 Sensor-data"] --> B["⚙️ Regelmotor\\nTröskelvärden"]
    B --> C["🤖 Agent 1:\\nLarmklassificerare"]
    C -->|"hamta_patienthistorik()"| D[("🔧 EHR-system")]
    D -->|"patientdata"| C
    C -->|"klassificering"| E["🤖 Agent 2:\\nKlinisk Analysagent"]
    E -->|"rekommendation"| F["✅ Evaluator:\\nKvalitetskontroll"]
    F -->|"GODKÄNT"| G["👩‍⚕️ HITL:\\nSjuksköterska"]
    F -->|"REVIDERA"| E
    G --> H["📞 Patientkontakt"]
    style A fill:#6b7280
    style C fill:#4f8ef7
    style E fill:#f59e0b
    style F fill:#ef4444
    style G fill:#10b981
    style D fill:#8b5cf6""",
'case-fleet': """flowchart TD
    A["🚨 Förseningslarm\\nGPS"] --> B["🤖 Agent 1:\\nFörseningsklassificerare"]
    B -->|"check_sla()"| C[("🔧 SLA-databas")]
    C -->|"sla_status"| B
    B -->|"förseningsrapport"| D["🤖 Agent 2:\\nRuttoptimerare"]
    D -->|"hamta_rutt()"| E[("🔧 Maps API")]
    E -->|"ruttalternativ"| D
    D -->|"rekommendation"| F["👷 HITL:\\nTransportledare"]
    F --> G["✅ Ny rutt aktiverad"]
    style A fill:#6b7280
    style B fill:#4f8ef7
    style D fill:#f59e0b
    style F fill:#10b981
    style C fill:#8b5cf6
    style E fill:#8b5cf6""",
'case-bank': """flowchart TD
    A["📄 Låneansökan"] --> B["🤖 Agent 1:\\nDokumenttolkare"]
    B -->|"extrahera_pdf()"| C[("🔧 PDF-parser")]
    C -->|"lönedata"| B
    B -->|"strukturerad data"| D["⚙️ Regelmotor:\\nUC + Skuldkvot"]
    D --> E["🤖 Agent 2:\\nRiskbedömare"]
    E -->|"hamta_kreditupplysning()"| F[("🔧 UC API")]
    F -->|"kreditdata"| E
    E -->|"riskbedömning"| G["🤖 Agent 3:\\nSammanfattare"]
    G --> H["👨‍💼 HITL:\\nKredithandläggare"]
    H --> I["✅ Beslut"]
    style A fill:#6b7280
    style B fill:#4f8ef7
    style D fill:#6b7280
    style E fill:#f59e0b
    style G fill:#4f8ef7
    style H fill:#10b981
    style C fill:#8b5cf6
    style F fill:#8b5cf6""",
'case-energy': """flowchart TD
    A["⚡ SCADA-larm"] --> B["🤖 Agent 1:\\nFelanalysagent"]
    B -->|"hamta_underhallshistorik()"| C[("🔧 SAP PM")]
    C -->|"historik"| B
    B -->|"felanalys"| D["🤖 Agent 2:\\nUnderhållsplanerare"]
    D -->|"kolla_vader()"| E[("🔧 Väder-API")]
    E -->|"väderprogrnos"| D
    D -->|"åtgärdsplan"| F["👷 HITL:\\nDrifttekniker"]
    F --> G["✅ Arbetsorder"]
    style A fill:#6b7280
    style B fill:#4f8ef7
    style D fill:#f59e0b
    style F fill:#10b981
    style C fill:#8b5cf6
    style E fill:#8b5cf6""",
'case-recruit': """flowchart TD
    A["📄 CV inkommer"] --> B["🤖 Agent 1:\\nCV-Parser"]
    B -->|"extrahera_cv()"| C[("🔧 Dokumentparser")]
    C -->|"CV-data"| B
    B -->|"strukturerad data"| D["🤖 Agent 2:\\nMatchningsagent"]
    D -->|"matchresultat"| E["✅ Evaluator:\\nKvalitetskontroll"]
    E -->|"GODKÄNT"| F["👔 HITL:\\nRekryterare"]
    E -->|"REVIDERA"| D
    F --> G["📋 Kortlista till kund"]
    style A fill:#6b7280
    style B fill:#4f8ef7
    style D fill:#f59e0b
    style E fill:#ef4444
    style F fill:#10b981
    style C fill:#8b5cf6""",
'case-edu': """flowchart TD
    A["📩 Studentfråga"] --> B["🤖 Agent 1:\\nFrågeklassificerare"]
    B -->|"hamta_studentinfo()"| C[("🔧 LMS/Canvas")]
    C -->|"studentdata"| B
    B -->|"kategori + HITL-flagga"| D{"HITL krävs?"}
    D -->|"Nej"| E["🤖 Agent 2:\\nSvarsagent (RAG)"]
    D -->|"Ja (betyg/undantag)"| F["👩‍🏫 HITL: Lärare"]
    E -->|"search_kunskapsbas()"| G[("🔧 FAQ-databas")]
    G -->|"svar"| E
    E -->|"formulerat svar"| H["✅ Tonkontroll"]
    H --> I["📤 Svar till student"]
    style A fill:#6b7280
    style B fill:#4f8ef7
    style E fill:#f59e0b
    style F fill:#10b981
    style H fill:#ef4444
    style C fill:#8b5cf6
    style G fill:#8b5cf6""",
'case-food': """flowchart TD
    A["📋 Inspektionsdata"] --> B["🤖 Agent 1:\\nRapportanalysagent"]
    B -->|"hamta_inspektionshistorik()"| C[("🔧 Inspektionssystem")]
    C -->|"historik"| B
    B -->|"avvikelseanalys"| D["🤖 Agent 2:\\nRiskbedömare"]
    D -->|"riskbedömning"| E["👨‍🔬 HITL:\\nInspektör"]
    E --> F["✅ Myndighetsbeslut"]
    style A fill:#6b7280
    style B fill:#4f8ef7
    style D fill:#f59e0b
    style E fill:#10b981
    style C fill:#8b5cf6""",
'case-media': """flowchart TD
    A["💬 Kommentar publiceras"] --> B["⚙️ Regelmotor:\\nOrdfilter + Spam"]
    B --> C["🤖 Agent 1:\\nKontextanalysagent"]
    C -->|"bedömning"| D{"Konfidens?"}
    D -->|"Över 95%: ta bort"| E["🗑️ Automatisk borttagning"]
    D -->|"50-90%: gråzon"| F["🤖 Agent 2:\\nPolicybedömare"]
    D -->|"Under 50%: godkänn"| G["✅ Publicerad"]
    F -->|"hamta_publiceringsregler()"| H[("🔧 Policyregelverk")]
    H -->|"regler"| F
    F --> I["👨‍💻 HITL: Moderator"]
    I --> J["✅ Slutgiltigt beslut"]
    style A fill:#6b7280
    style B fill:#6b7280
    style C fill:#4f8ef7
    style F fill:#f59e0b
    style I fill:#10b981
    style H fill:#8b5cf6""",
'case-property': """flowchart TD
    A["📱 Felanmälan"] --> B["🤖 Agent 1:\\nÄrendeklassificerare"]
    B -->|"analysera_bild()"| C[("🔧 Bildanalys-API")]
    C -->|"skadetyp"| B
    B -->|"klassificering"| D["🤖 Agent 2:\\nPrioriteringsagent"]
    D -->|"sok_entreprenor()"| E[("🔧 Entreprenörsregister")]
    E -->|"förslag"| D
    D -->|"akut?"| F{"Prioritet?"}
    F -->|"Akut"| G["👷 HITL: Fastighetsskötare"]
    F -->|"Rutin"| H["✅ Automatisk bokning"]
    G --> I["✅ Arbetsorder"]
    style A fill:#6b7280
    style B fill:#4f8ef7
    style D fill:#f59e0b
    style G fill:#10b981
    style C fill:#8b5cf6
    style E fill:#8b5cf6""",
'case-legal': """flowchart TD
    A["📄 Avtal-PDF"] --> B["🤖 Agent 1:\\nAvtalstolkare"]
    B -->|"extrahera_pdf()"| C[("🔧 DMS/iManage")]
    C -->|"avtalstext"| B
    B -->|"avtalsextrakt"| D["🤖 Agent 2:\\nKlausulgranskare"]
    D -->|"sok_policy()"| E[("🔧 Policydatabas")]
    E -->|"regler"| D
    D -->|"riskanalys"| F["🔍 Critic-agent:\\nKvalitetskontroll"]
    F -->|"GODKÄNT"| G["👨‍⚖️ HITL: Jurist"]
    F -->|"REVIDERA + feedback"| D
    G --> H["✅ Signerat PM"]
    style A fill:#6b7280
    style B fill:#4f8ef7
    style D fill:#f59e0b
    style F fill:#ef4444
    style G fill:#10b981
    style C fill:#8b5cf6
    style E fill:#8b5cf6"""
}
