# 🎨 AURA Frontend - Visual Guide

Quick visual reference for all pages and features.

## 🏠 Home Page

**URL**: `http://localhost:3000/`

```
┌─────────────────────────────────────────────────────────┐
│  [Shield Icon] AURA        [Get Started] [Projects]     │
├─────────────────────────────────────────────────────────┤
│                                                          │
│           Autonomous Code Analysis                       │
│              Powered by AI                               │
│                                                          │
│   Upload your backend code and let AI-powered agents    │
│   analyze security, tests, scalability, and database    │
│                                                          │
│        [Upload Code]  [View Projects]                   │
│                                                          │
├─────────────────────────────────────────────────────────┤
│            Four Specialized AI Agents                    │
│                                                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐│
│  │ Security │  │   Test   │  │Scalability│ │ Database ││
│  │  Agent   │  │Generator │  │  Agent    │ │  Agent   ││
│  │   🛡️    │  │   🧪     │  │    ⚡     │ │   🗄️    ││
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘│
│                                                          │
├─────────────────────────────────────────────────────────┤
│                  How It Works                            │
│                                                          │
│    1. Upload     2. AI        3. View                   │
│      Code       Analysis      Results                    │
└─────────────────────────────────────────────────────────┘
```

## 📤 Upload Page

**URL**: `http://localhost:3000/upload`

```
┌─────────────────────────────────────────────────────────┐
│  [← Back to Home]                    [View Projects]    │
├─────────────────────────────────────────────────────────┤
│                                                          │
│                 Upload Your Code                         │
│    Upload a ZIP file containing your backend code       │
│                                                          │
│  ┌───────────────────────────────────────────────────┐ │
│  │                                                    │ │
│  │              📦                                    │ │
│  │                                                    │ │
│  │     Drag & drop your ZIP file here                │ │
│  │            or click to browse                     │ │
│  │                                                    │ │
│  │          [Choose File]                            │ │
│  │                                                    │ │
│  │  • Supported: Python, JavaScript, Java, Go        │ │
│  │  • Maximum file size: 50MB                        │ │
│  │  • File format: .zip only                         │ │
│  └───────────────────────────────────────────────────┘ │
│                                                          │
└─────────────────────────────────────────────────────────┘

After Upload Success:
┌─────────────────────────────────────────────────────────┐
│  ✅ Upload Successful!                                   │
│     Your code has been processed                        │
│                                                          │
│  Project Information                                     │
│  ┌───────────────────────────────────┐                 │
│  │ Project ID: 20260207_143729_abc   │                 │
│  │ Filename: backend_code.zip        │                 │
│  │ Total Files: 25                   │                 │
│  │ Code Files: 18                    │                 │
│  │ Language: Python (95% confidence) │                 │
│  │ Framework: FastAPI                │                 │
│  │ Functions: 42 | Classes: 8        │                 │
│  │ Lines of Code: 1,543              │                 │
│  └───────────────────────────────────┘                 │
│                                                          │
│       [Start Analysis]  [Upload Another]                │
└─────────────────────────────────────────────────────────┘
```

## 📁 Projects Page

**URL**: `http://localhost:3000/projects`

```
┌─────────────────────────────────────────────────────────┐
│  [← Back to Home]              [Upload New Project]     │
├─────────────────────────────────────────────────────────┤
│                                                          │
│                  Your Projects                           │
│    Manage and view analysis results for your code       │
│                                                          │
│  [🔍 Search projects...]                                │
│                                                          │
│  Showing 3 of 3 projects                                │
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │    Project   │  │    Project   │  │    Project   │ │
│  │  💻          │  │  💻          │  │  💻          │ │
│  │              │  │              │  │              │ │
│  │ 20260207...  │  │ 20260206...  │  │ 20260205...  │ │
│  │              │  │              │  │              │ │
│  │ 📅 2026-02-07│  │ 📅 2026-02-06│  │ 📅 2026-02-05│ │
│  │    14:37     │  │    10:23     │  │    16:45     │ │
│  │              │  │              │  │              │ │
│  │[View Analysis│  │[View Analysis│  │[View Analysis│ │
│  │     [🗑️]     │  │     [🗑️]     │  │     [🗑️]     │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## 📊 Analysis Dashboard

**URL**: `http://localhost:3000/dashboard/[projectId]`

```
┌─────────────────────────────────────────────────────────┐
│  [← Back to Projects]      [🔍 RAG Search] [📥 Export]  │
├─────────────────────────────────────────────────────────┤
│                                                          │
│         Analysis Dashboard                               │
│  Project ID: 20260207_143729_a1b2c3d4                   │
│                                                          │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐│
│  │ Total  │ │Critical│ │  High  │ │ Medium │ │  Low   ││
│  │   30   │ │   2    │ │   8    │ │   15   │ │   5    ││
│  └────────┘ └────────┘ └────────┘ └────────┘ └────────┘│
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   Security   │  │     Test     │  │ Scalability  │ │
│  │    Agent     │  │  Generator   │  │    Agent     │ │
│  │     🛡️      │  │     🧪       │  │     ⚡       │ │
│  │              │  │              │  │              │ │
│  │ 8 Findings   │  │ 12 Findings  │  │ 6 Findings   │ │
│  │  3.45s       │  │  2.15s       │  │  1.87s       │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
│                                                          │
│  ┌──────────────┐                                       │
│  │   Database   │                                       │
│  │    Agent     │                                       │
│  │     🗄️      │                                       │
│  │              │                                       │
│  │ 4 Findings   │                                       │
│  │  1.92s       │                                       │
│  └──────────────┘                                       │
│                                                          │
├─────────────────────────────────────────────────────────┤
│  [All (30)] [Security (8)] [Test Gen (12)] [......]    │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Findings Table                                          │
│  ┌─────────────────────────────────────────────────┐   │
│  │ [🔍 Search] [Filter ▾] [Sort by ▾]             │   │
│  ├─────────┬──────────────┬────────┬──────────────┤   │
│  │Severity │ Title        │ Agent  │ Location     │   │
│  ├─────────┼──────────────┼────────┼──────────────┤   │
│  │CRITICAL │SQL Injection │Security│api/users.py:45│  │
│  │   RED   │              │        │  [View Code] │   │
│  ├─────────┼──────────────┼────────┼──────────────┤   │
│  │  HIGH   │Missing Test  │Test Gen│api/auth.py  │   │
│  │ ORANGE  │              │        │  [View Code] │   │
│  └─────────┴──────────────┴────────┴──────────────┘   │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## 🔍 Code Viewer Modal

```
┌─────────────────────────────────────────────────────────┐
│  CRITICAL  Security                              [✕]    │
│                                                          │
│  Potential SQL Injection                                │
│  api/users.py:45                                        │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Description                                             │
│  Detected potential sql_injection vulnerability         │
│  pattern in database query construction                 │
│                                                          │
│  Code Snippet                                            │
│  ┌───────────────────────────────────────────────────┐ │
│  │ 43  def get_user(user_id):                        │ │
│  │ 44      cursor = conn.cursor()                    │ │
│  │ 45      cursor.execute(f"SELECT * FROM users     │ │
│  │                WHERE id={user_id}")               │ │
│  │ 46      return cursor.fetchone()                  │ │
│  └───────────────────────────────────────────────────┘ │
│                                                          │
│  Recommendation                                          │
│  ┌───────────────────────────────────────────────────┐ │
│  │ Use parameterized queries or ORMs. Never          │ │
│  │ concatenate user input into SQL queries.          │ │
│  │ Example: cursor.execute("SELECT * FROM users      │ │
│  │ WHERE id=?", (user_id,))                          │ │
│  └───────────────────────────────────────────────────┘ │
│                                                          │
│                    [Close]                               │
└─────────────────────────────────────────────────────────┘
```

## 🔎 RAG Search Page

**URL**: `http://localhost:3000/search/[projectId]`

```
┌─────────────────────────────────────────────────────────┐
│  [← Back to Dashboard]        ✨ RAG-Powered Search     │
├─────────────────────────────────────────────────────────┤
│                                                          │
│            Semantic Code Search                          │
│   Use AI-powered semantic search to find code snippets  │
│                                                          │
│  ┌───────────────────────────────────────────────────┐ │
│  │ Search Query                                       │ │
│  │ [🔍 Find authentication logic, SQL queries...]    │ │
│  │                                                    │ │
│  │ Strategy: [Multi-Query ▾]  Results: [5]           │ │
│  │                                                    │ │
│  │ ☑ Use Reranking  ☑ Include Context                │ │
│  │                                                    │ │
│  │            [Search Code]                           │ │
│  └───────────────────────────────────────────────────┘ │
│                                                          │
├─────────────────────────────────────────────────────────┤
│  Found 5 results - Strategy: multi_query [Reranked]    │
│                                                          │
│  AI-Generated Query Variations:                         │
│  [user login] [access control] [JWT validation]        │
│                                                          │
├─────────────────────────────────────────────────────────┤
│  Result 1                                                │
│  ┌───────────────────────────────────────────────────┐ │
│  │ 💻 api/auth.py         [function] Score: 94.2%   │ │
│  ├───────────────────────────────────────────────────┤ │
│  │ Context Before: (grayed)                          │ │
│  │   import jwt                                      │ │
│  │   from datetime import datetime                   │ │
│  ├───────────────────────────────────────────────────┤ │
│  │ def authenticate_user(username, password):        │ │
│  │     user = db.get_user(username)                  │ │
│  │     if user and verify_password(password):        │ │
│  │         return generate_token(user)               │ │
│  │     return None                                   │ │
│  ├───────────────────────────────────────────────────┤ │
│  │ Context After: (grayed)                           │ │
│  │   def generate_token(user):                       │ │
│  │       return jwt.encode({...})                    │ │
│  └───────────────────────────────────────────────────┘ │
│                                                          │
│  [More results...]                                       │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## 🎨 Color Scheme

```
Primary Colors:
- Blue: #0ea5e9 (buttons, accents)
- Purple: #a855f7 (gradients)

Severity Colors:
- Critical: Red (#dc2626)
- High: Orange (#ea580c)
- Medium: Yellow (#ca8a04)
- Low: Blue (#2563eb)

Background:
- Gradient: Blue-50 → White → Purple-50
- Cards: White with subtle shadows
- Headers: White with backdrop blur

Text:
- Primary: Gray-900
- Secondary: Gray-600
- Muted: Gray-500
```

## 📱 Responsive Breakpoints

```
Mobile:    < 768px   (1 column)
Tablet:    768px     (2 columns)
Desktop:   1024px    (3-4 columns)
Wide:      1280px+   (4+ columns)
```

## 🎭 Interactive Elements

### Buttons
```
Primary:   Blue background, white text, hover scales
Secondary: White background, border, hover bg changes
Danger:    Red background for delete actions
```

### Cards
```
Default:   White with shadow, hover increases shadow
Agent:     Gradient header, white body, icon
Finding:   Expandable rows, syntax highlighted code
```

### Inputs
```
Text:      Border, focus ring (blue)
File:      Dashed border, drag-active changes color
Select:    Styled dropdown, consistent with theme
```

## ✨ Animations

- **Hover**: Scale 1.05, shadow increase
- **Loading**: Spin animation for loaders
- **Transitions**: 200-300ms for smooth effects
- **Fade-in**: Content appears smoothly

---

**Happy Building! 🚀**
