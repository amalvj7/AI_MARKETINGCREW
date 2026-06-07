# 🚀 Marketing Agent — CrewAI Multi-Agent System

An **AI marketing team in a box**. In the real world, launching a marketing
campaign for a product needs *at least four different specialists*. This project
replaces that four-person team with **four collaborating AI agents** that
research the market, build a strategy, write the content, and optimize it for
search — end to end, automatically.

---

## 👥 The Real-World Team → The AI Crew

In a real company you would hire (and pay) **4 people** to do this work:

| Real-world role | What they do | 🤖 AI Agent in this project |
| --- | --- | --- |
| **Marketing Head / Strategist** | Studies the market, sizes up competitors, and writes the marketing strategy | `marketing_head` |
| **Social Media Content Writer** | Plans the content calendar, writes posts, captions & reel scripts | `social_media_content_writer` |
| **Blog Content Writer** | Researches topics and writes long-form blog articles | `blog_content_writer` |
| **SEO Specialist** | Finds keywords and optimizes everything for search engines | `seo_specialist` |

These four agents work **sequentially** (one hands its output to the next),
coordinated by CrewAI — exactly how a real marketing team passes work down the
line.

---

## 🧠 How It Works

The crew runs **9 tasks** in order, mirroring a real campaign workflow:

```
1. Market Research          ──►  marketing_head
2. Marketing Strategy       ──►  marketing_head
3. Social Content Research  ──►  social_media_content_writer
4. Content Calendar         ──►  social_media_content_writer
5. Social Media Drafts      ──►  social_media_content_writer
6. Reel Scripts             ──►  social_media_content_writer
7. Blog Content Research    ──►  blog_content_writer
8. Blog Draft               ──►  blog_content_writer
9. SEO Optimization         ──►  seo_specialist
```

Each agent is equipped with real tools so it can actually *do* the work, not
just talk about it:

- 🔎 **SerperDevTool** — live Google search
- 🌐 **ScrapeWebsiteTool** — read competitor / reference websites
- 📄 **FileReadTool / FileWriterTool** — read and save deliverables
- 📁 **DirectoryReadTool** — browse generated files

The crew uses **Google Gemini 2.0 Flash** as its reasoning engine and runs with
`planning=True`, so it plans the whole campaign before executing.

---

## 📂 Project Structure

```
MarketingAgent_CrewAI/
├── crew.py              # Defines the 4 agents, 9 tasks, and the crew
├── config/
│   ├── agent.yaml       # Role / goal / backstory for each agent
│   └── task.yaml        # Description & expected output for each task
├── .env                 # API keys (NEVER commit this!)
└── README.md            # You are here
```

---

## ⚙️ Setup

### 1. Install dependencies

```bash
pip install crewai crewai-tools python-dotenv pydantic
```

### 2. Add your API keys

Create a `.env` file in the project folder:

```env
GEMINI_API_KEY=your_gemini_api_key_here
SERPER_API_KEY=your_serper_api_key_here
```

> ⚠️ **Both keys are required.**
> - `GEMINI_API_KEY` → powers the agents' reasoning (get it from [Google AI Studio](https://aistudio.google.com/)).
> - `SERPER_API_KEY` → powers the `SerperDevTool` web search (get it from [serper.dev](https://serper.dev/)). The crew will fail at runtime without it.

### 3. Run the crew

```bash
python crew.py
```

---

## 🎯 Customizing the Campaign

The product being marketed is defined in the `inputs` dictionary at the bottom of
[`crew.py`](crew.py). Change these to market *your own* product:

```python
inputs = {
    "product_name": "AI Powered Excel Automation Tool",
    "target_audience": "Small and Medium Enterprises (SMEs)",
    "product_description": "A tool that automates repetitive tasks in Excel using AI...",
    "budget": "Rs. 50,000",
    "current_date": datetime.now().strftime("%Y-%m-%d"),
}
```

These values are injected into the task prompts in `config/task.yaml` via
`{product_name}`, `{target_audience}`, `{product_description}`, and `{budget}`.

---

## 🔐 Security Note

Your real `GEMINI_API_KEY` is currently sitting in `.env`. **Do not commit
`.env` to git** — add it to `.gitignore`. If this key has ever been shared or
pushed publicly, **rotate it** in Google AI Studio.

```gitignore
.env
```

---

## 🧰 Tech Stack

- [CrewAI](https://www.crewai.com/) — multi-agent orchestration
- [Google Gemini 2.0 Flash](https://aistudio.google.com/) — LLM
- [Serper.dev](https://serper.dev/) — web search API
- Python 3.10+
