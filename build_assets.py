"""Generate the theme-aware SVG assets used by the profile README.

Every SVG carries its own light palette plus a prefers-color-scheme: dark
override, so one file matches both GitHub themes. Run:  python scripts/build_assets.py
"""
from pathlib import Path
from html import escape

OUT = Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(exist_ok=True)

DISPLAY = "'Bricolage Grotesque','Segoe UI Variable Display','Segoe UI','Helvetica Neue',Arial,sans-serif"
BODY = "'IBM Plex Sans','Segoe UI','Helvetica Neue',Arial,sans-serif"
MONO = "'JetBrains Mono',ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"

STYLE = f"""
<style>
.bg{{fill:#F2F4F7}} .sf{{fill:#FFFFFF}} .s2{{fill:#E8ECF1}} .ln{{stroke:#D3DAE3}} .lnf{{fill:#D3DAE3}}
.ink{{fill:#10161D}} .mu{{fill:#566271}} .ac{{fill:#0A66C2}} .acs{{fill:#DCEAF8}} .acst{{stroke:#0A66C2}}
.mk{{fill:#C98A0B}} .mks{{fill:#FCEFC9}} .mkst{{stroke:#C98A0B}} .ok{{fill:#1F8A4C}} .onac{{fill:#FFFFFF}}
.d{{font-family:{DISPLAY}}} .b{{font-family:{BODY}}} .m{{font-family:{MONO}}}
.flow{{stroke-dasharray:4 4;animation:flow .7s linear infinite}}
.pulse{{animation:pulse 2.4s ease-out infinite;transform-origin:center;transform-box:fill-box}}
@keyframes flow{{to{{stroke-dashoffset:-16}}}}
@keyframes pulse{{0%{{opacity:.55;transform:scale(1)}}80%,100%{{opacity:0;transform:scale(2.6)}}}}
@media (prefers-color-scheme:dark){{
 .bg{{fill:#0C1117}} .sf{{fill:#131A22}} .s2{{fill:#1A232D}} .ln{{stroke:#26323F}} .lnf{{fill:#26323F}}
 .ink{{fill:#E4EAF0}} .mu{{fill:#8E9BAA}} .ac{{fill:#58A2EE}} .acs{{fill:#132B44}} .acst{{stroke:#58A2EE}}
 .mk{{fill:#F2B84B}} .mks{{fill:#3A2E12}} .mkst{{stroke:#F2B84B}} .ok{{fill:#44BD78}} .onac{{fill:#06101C}}
}}
@media (prefers-reduced-motion:reduce){{.flow,.pulse{{animation:none}}}}
</style>"""


def svg(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-label="{escape(title)}"><title>{escape(title)}</title>{STYLE}{body}</svg>\n')


def t(x, y, s, cls, size, weight=400, anchor="start", extra=""):
    return (f'<text x="{x}" y="{y}" class="{cls}" font-size="{size}" font-weight="{weight}" '
            f'text-anchor="{anchor}" {extra}>{escape(s)}</text>')


def write(name, content):
    (OUT / name).write_text(content, encoding="utf-8")


def mono_w(s, size):  # monospace advance is ~0.6em
    return len(s) * size * 0.6


# ------------------------------------------------------------------ hero
def hero():
    W, H = 1200, 440
    b = [f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="18" class="bg ln" stroke-width="1"/>']
    # status pill
    pill = "Open to full-time roles · Bhopal, India"
    pw = mono_w(pill, 13) + 44
    b.append(f'<rect x="48" y="44" width="{pw}" height="32" rx="16" class="sf ln" stroke-width="1"/>')
    b.append('<circle cx="66" cy="60" r="4.5" class="ok pulse"/><circle cx="66" cy="60" r="4.5" class="ok"/>')
    b.append(t(80, 64.5, pill, "ink m", 13, 500))
    # name
    b.append(t(44, 160, "Ratneshwar", "ink d", 86, 800, extra='letter-spacing="-3"'))
    b.append(t(44, 242, "Pandey", "ac d", 86, 800, extra='letter-spacing="-3"'))
    # lead with highlighter
    b.append(f'<rect x="119" y="279" width="436" height="11" class="mks"/>')
    b.append(t(48, 288, "I build", "mu b", 20, extra='textLength="64" lengthAdjust="spacingAndGlyphs"'))
    b.append(t(121, 288, "multi-agent AI systems that cite their sources", "ink b", 20, 500,
               extra='textLength="432" lengthAdjust="spacingAndGlyphs"'))
    b.append(t(48, 318, "— and the full-stack and cloud plumbing that", "mu b", 20))
    b.append(t(48, 348, "gets them to production.", "mu b", 20))
    # facts
    facts = [("LAST ROLE", "SWE Intern, KPMG"), ("DEGREE", "B.Tech CSE · 7.98"),
             ("DSA", "700+ solved"), ("HACKATHON", "1st, Infenion")]
    b.append(f'<line x1="48" y1="372" x2="592" y2="372" class="ln" stroke-width="1"/>')
    for i, (k, v) in enumerate(facts):
        x = 48 + i * 140
        b.append(t(x, 396, k, "mu m", 11, 500, extra='letter-spacing="1"'))
        b.append(t(x, 418, v, "ink b", 14.5, 500))

    # agent card
    cx, cy, cw, ch = 640, 40, 512, 360
    b.append(f'<rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" rx="14" class="sf ln" stroke-width="1"/>')
    b.append(t(cx + 20, cy + 36, "Ask my portfolio", "ink d", 20, 700))
    b.append(t(cx + cw - 20, cy + 35, "SUPERVISOR → INDEXES → CITATIONS", "mu m", 10.5, 500, "end", 'letter-spacing="0.8"'))
    b.append(f'<rect x="{cx+20}" y="{cy+52}" width="{cw-110}" height="40" rx="9" class="bg ln" stroke-width="1"/>')
    b.append(t(cx + 34, cy + 77, "Which project shows production AI work?", "ink b", 15))
    b.append(f'<rect x="{cx+cw-82}" y="{cy+52}" width="62" height="40" rx="9" class="ac"/>')
    b.append(t(cx + cw - 51, cy + 77, "Run", "onac b", 15, 600, "middle"))
    # graph (site geometry scaled 0.86, offset)
    gx, gy, s = cx + 20, cy + 106, 0.86
    def R(x, y, w=96, h=34):
        return x * s + gx, y * s + gy, w * s, h * s
    nodes = [("question", 10, 68, "on"), ("supervisor", 118, 68, "on"), ("projects", 226, 14, "hit"),
             ("stack", 226, 68, ""), ("profile", 226, 122, ""), ("citations", 334, 68, "on"), ("answer", 442, 68, "on")]
    edges = [("M106 85 H118", True), ("M214 85 C220 85 220 31 226 31", True), ("M214 85 H226", False),
             ("M214 85 C220 85 220 139 226 139", False), ("M322 31 C328 31 328 85 334 85", True),
             ("M322 85 H334", False), ("M322 139 C328 139 328 85 334 85", False), ("M430 85 H442", True)]
    b.append(f'<g transform="translate({gx} {gy}) scale({s})">')
    for d, on in edges:
        b.append(f'<path d="{d}" fill="none" stroke-width="1.6" class="{"acst flow" if on else "ln"}"/>')
    for label, x, y, st in nodes:
        fill = {"on": "acs", "hit": "mks", "": "sf"}[st]
        stroke = {"on": "acst", "hit": "mkst", "": "ln"}[st]
        b.append(f'<rect x="{x}" y="{y}" width="96" height="34" rx="7" class="{fill} {stroke}" stroke-width="1.3"/>')
        b.append(t(x + 48, y + 21.5, label, ("ink" if st else "mu") + " m", 12, 500, "middle"))
    b.append('</g>')
    # answer
    ay = cy + 262
    b.append(t(cx + 20, ay, "GROUNDED ANSWER", "mu m", 10.5, 500, extra='letter-spacing="0.8"'))
    b.append(t(cx + cw - 20, ay, "3 SOURCES", "mu m", 10.5, 500, "end", 'letter-spacing="0.8"'))
    b.append(t(cx + 20, ay + 24, "The Government Gazette Intelligence Agent sends each", "ink b", 14.5))
    b.append(t(cx + 20, ay + 45, "question through a supervisor to search, OCR and", "ink b", 14.5))
    b.append(t(cx + 20, ay + 66, "citation agents — every answer cites the source PDF.", "ink b", 14.5))
    b.append(f'<rect x="{cx+cw-44}" y="{ay+53}" width="22" height="18" rx="4" class="mks"/>')
    b.append(t(cx + cw - 33, ay + 66, "1", "ink m", 11, 600, "middle"))
    b.append(t(cx + 20, cy + ch + 26, "▶ Try it live — ratneshwarpandey12220865.github.io", "ac m", 13, 500))
    write("hero.svg", svg(W, H, "".join(b), "Ratneshwar Pandey — builds multi-agent AI systems that cite their sources. Open to full-time roles."))


# ------------------------------------------------------------------ section headers
def section(name, title, sub):
    W, H = 1200, 92
    b = [t(0, 50, title, "ink d", 40, 750, extra='letter-spacing="-1"'),
         t(0, 80, sub, "mu b", 16)]
    write(f"section-{name}.svg", svg(W, H, "".join(b), f"{title} — {sub}"))


# ------------------------------------------------------------------ project cards
PROJECTS = [
    ("gazette", "AI AGENTS · OCR · CITATIONS", "Government Gazette Intelligence Agent",
     ["Searches, OCRs and extracts Indian state + national gazettes,", "then answers questions with verified citations."],
     ["Python", "FastAPI", "DeepSeek", "Tesseract", "PyMuPDF", "Next.js"], "7 + 1", "specialist agents + supervisor"),
    ("taskpilot", "AGENTS · HUMAN-IN-THE-LOOP", "TaskPilot",
     ["An autonomous agent that plans, acts, and pauses for a", "human's approval before anything risky."],
     ["LangGraph", "MCP", "FastAPI", "SQLite", "Pytest"], "plan → gate → act", "risky steps wait for a human"),
    ("router", "LLM COST · EVALUATION", "Hybrid SLM + LLM Router",
     ["Answers most queries on a local 3B model, escalates only", "what needs a frontier model — and proves the savings."],
     ["Python", "Ollama", "Groq", "qwen2.5:3b", "38 tests"], "3B → 120B", "escalate only on low confidence"),
    ("documind", "RAG · PAGE CITATIONS", "DocuMind RAG",
     ["Ask your PDFs anything and get answers with clickable", "page citations, rendered on the spot."],
     ["FastAPI", "Next.js", "Qdrant", "Ollama", "DeepSeek", "Docker"], "hybrid + rerank", "retrieval before generation"),
    ("research", "MULTI-AGENT · SERVERLESS", "Multi-Agent Research Assistant",
     ["Four LangGraph agents research, summarise, fact-check and", "write the report, streaming progress over SSE."],
     ["LangGraph", "FastAPI", "React", "PostgreSQL", "Celery", "Lambda"], "~60%", "less manual research time"),
    ("resume", "RAG · CAREER COACH", "AI Resume Analyzer",
     ["A six-step LangGraph pipeline: skills, gaps for 8 target", "roles via RAG, and a prioritised improvement plan."],
     ["LangGraph", "ChromaDB", "DeepSeek", "FastAPI", "React", "Docker"], "~85%", "user-reported relevance"),
    ("ecommerce", "JAVA · MICROSERVICES", "E-Commerce Platform",
     ["Five Spring Boot services behind an API gateway, with a", "Next.js storefront and a Dockerised local stack."],
     ["Java 17", "Spring Boot", "PostgreSQL", "Redis", "Next.js", "Docker"], "320 → 45 ms", "catalog query time"),
    ("pm", "FULL-STACK · REAL-TIME", "Project Management Platform",
     ["Jira/Notion-style workspaces: GraphQL kanban boards,", "live notifications and role-based teams."],
     ["Next.js", "GraphQL", "FastAPI", "PostgreSQL", "Redis", "Celery"], "kanban + RBAC", "live updates via Redis pub/sub"),
]


def card(pid, doms, title, lines, tags, metric, mlabel):
    W, H = 590, 260
    b = [f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="14" class="sf ln" stroke-width="1"/>',
         t(26, 38, doms, "mu m", 11.5, 500, extra='letter-spacing="0.9"'),
         t(W - 26, 38, "open ↗", "ac m", 12, 500, "end"),
         t(26, 76, title, "ink d", 23, 700, extra='letter-spacing="-0.3"'),
         t(26, 106, lines[0], "mu b", 15), t(26, 128, lines[1], "mu b", 15)]
    x, y = 26, 150
    for tg in tags:
        w = mono_w(tg, 12) + 16
        if x + w > W - 26:
            x, y = 26, y + 30
        b.append(f'<rect x="{x}" y="{y}" width="{w}" height="24" rx="5" class="s2"/>')
        b.append(t(x + 8, y + 16.5, tg, "ink m", 12, 500))
        x += w + 6
    b.append(f'<line x1="26" y1="{H-58}" x2="{W-26}" y2="{H-58}" class="ln" stroke-width="1"/>')
    b.append(t(26, H - 22, metric, "ink d", 27, 750, extra='letter-spacing="-0.5"'))
    b.append(t(W - 26, H - 26, mlabel, "mu b", 13.5, 400, "end"))
    write(f"card-{pid}.svg", svg(W, H, "".join(b), f"{title}: {' '.join(lines)} {metric} {mlabel}"))


# ------------------------------------------------------------------ stack explorer
STACK = [
    ("AI / LLM", [("HF Transformers", 5), ("LangGraph", 3), ("LangChain", 3), ("OpenAI SDK", 3), ("Tesseract / OCR", 3), ("Ollama", 1), ("Qdrant", 1), ("ChromaDB", 1)]),
    ("Backend", [("FastAPI", 9), ("Express", 4), ("SQLAlchemy", 3), ("Celery", 2), ("Spring Boot", 1), ("Django", 1), ("GraphQL", 1)]),
    ("Frontend", [("React", 12), ("Tailwind CSS", 8), ("Next.js", 5), ("Zustand", 2), ("Streamlit", 2)]),
    ("Data", [("PostgreSQL", 4), ("MongoDB", 4), ("Redis", 3)]),
    ("Ship & test", [("Docker", 7), ("Pytest", 3), ("Playwright", 3), ("GitHub Actions", 3), ("AWS Lambda", 1)]),
]


def stack():
    W = 1200
    colw = W / 5
    rows = max(len(i) for _, i in STACK)
    H = 58 + rows * 32 + 44
    mx = max(c for _, i in STACK for _, c in i)
    b = []
    for ci, (g, items) in enumerate(STACK):
        x = ci * colw
        b.append(t(x, 22, g.upper(), "mu m", 12, 600, extra='letter-spacing="1"'))
        for ri, (name, n) in enumerate(items):
            y = 58 + ri * 32
            b.append(t(x, y, name, "ink b", 15))
            bw = max(6, n / mx * 60)
            b.append(f'<rect x="{x + colw - 44 - bw}" y="{y - 9}" width="{bw}" height="6" rx="3" class="ac"/>')
            b.append(t(x + colw - 24, y, str(n), "mu m", 12, 500, "end"))
    b.append(t(0, H - 8, "Bars = how many of my 20 most recently updated repos list it as a dependency.", "mu b", 13))
    write("stack.svg", svg(W, H, "".join(b), "Tech stack, counted from dependency files across my 20 most recent repositories"))


# ------------------------------------------------------------------ experience
def experience():
    W = 1200
    rows = [
        ("Now", "Looking for my first full-time role", "AI/ML engineering · Full-stack · Cloud & DevOps",
         ["Shipping agent projects — TaskPilot, Hybrid Router, Gazette Agent — while I interview."], True),
        ("Jan – Jul 2026", "Software Engineer Intern", "KPMG",
         ["Built full-stack enterprise apps with React and FastAPI in Agile/Scrum sprints.",
          "Wrote Playwright test automation that streamlined regression testing.",
          "Built web-scraping pipelines that automated data collection for project teams."], False),
        ("Sep 2022 – Jul 2026", "B.Tech, Computer Science & Engineering", "Lovely Professional University · CGPA 7.98 / 10", [], False),
    ]
    b, y = [], 30
    for i, (when, title, org, bullets, now) in enumerate(rows):
        if i:
            b.append(f'<line x1="0" y1="{y-30}" x2="{W}" y2="{y-30}" class="ln" stroke-width="1"/>')
        b.append(t(0, y, when, "mu m", 13.5, 500))
        b.append(t(210, y, title, ("ok" if now else "ink") + " d", 21, 700))
        b.append(t(210, y + 26, org, "mu b", 15))
        yy = y + 54
        for bl in bullets:
            b.append(f'<circle cx="216" cy="{yy-5}" r="2.5" class="ac"/>')
            b.append(t(228, yy, bl, "ink b", 15))
            yy += 24
        y = yy + (34 if bullets else 8) + 12
    H = y - 20
    write("experience.svg", svg(W, H, "".join(b), "Experience: KPMG Software Engineer Intern 2026; B.Tech CSE LPU 2022–2026; open to full-time roles"))


# ------------------------------------------------------------------ recognition
def recognition():
    W, H = 1200, 250
    b = [t(0, 20, "ACHIEVEMENTS", "mu m", 12, 600, extra='letter-spacing="1"'),
         t(620, 20, "CERTIFICATIONS", "mu m", 12, 600, extra='letter-spacing="1"')]
    ach = [("1st", "Infenion Hackathon — “Defend the Kingdom”", "Real-time strategy solution shipped in 24 hours."),
           ("700+", "Competitive programming", "Problems solved on LeetCode, CodeChef and HackerRank.")]
    for i, (big, h, s) in enumerate(ach):
        y = 78 + i * 92
        b.append(t(0, y + 6, big, "mk d", 44, 800))
        b.append(t(118, y - 8, h, "ink b", 16, 600))
        b.append(t(118, y + 16, s, "mu b", 15))
    certs = ["Cloud Computing — NPTEL, IIT Kharagpur", "Prompt Engineering for LLMs — Coursera",
             "Supervised ML: Regression & Classification — Coursera", "Generative AI for Everyone — DeepLearning.AI"]
    for i, c in enumerate(certs):
        y = 62 + i * 46
        if i:
            b.append(f'<line x1="620" y1="{y-28}" x2="{W}" y2="{y-28}" class="ln" stroke-width="1"/>')
        b.append(t(620, y, "2024", "mu m", 13, 500))
        b.append(t(680, y, c, "ink b", 15.5))
    write("recognition.svg", svg(W, H, "".join(b), "Recognition: 1st place Infenion Hackathon; 700+ DSA problems; four 2024 certifications"))


# ------------------------------------------------------------------ contact
def contact():
    W, H = 1200, 250
    b = [f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="18" class="bg ln" stroke-width="1"/>',
         t(48, 86, "Hiring for AI, full-stack", "ink d", 50, 800, extra='letter-spacing="-1.5"'),
         t(48, 142, "or cloud work?", "ink d", 50, 800, extra='letter-spacing="-1.5"'),
         t(48, 180, "I reply to every email. A short note about the role and team is plenty.", "mu b", 17)]
    mail = "pandeyratneshwar1@gmail.com"
    b.append(t(48, 222, mail, "ink m", 20, 600))
    b.append(f'<rect x="48" y="229" width="{mono_w(mail, 20)}" height="2.5" class="ac"/>')
    b.append(f'<rect x="{W-230}" y="196" width="182" height="40" rx="9" class="ac"/>')
    b.append(t(W - 139, 221, "Email me  →", "onac b", 15, 600, "middle"))
    write("contact.svg", svg(W, H, "".join(b), "Hiring for AI, full-stack or cloud work? Email pandeyratneshwar1@gmail.com"))


if __name__ == "__main__":
    hero()
    section("projects", "Projects", "Eight systems, each with the number I'd defend in an interview. Click a card for the repo.")
    section("stack", "Stack", "What my recent repos are actually built with.")
    section("experience", "Experience", "Internship, degree, and what I'm doing now.")
    section("recognition", "Recognition", "Hackathon, problem solving, certifications.")
    section("stats", "Activity", "Live from GitHub.")
    for p in PROJECTS:
        card(*p)
    stack()
    experience()
    recognition()
    contact()
    print("wrote", len(list(OUT.glob("*.svg"))), "svgs to", OUT)
