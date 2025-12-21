# 🛡️ Sentinel: Agentic Tech Surveillance System

**Sentinel** is a local, autonomous AI agent designed to keep Master Software Engineers and Architects "in the know." 

Unlike standard RSS feeds or newsletters, Sentinel uses **LangGraph** to build a cyclic agentic workflow that reads, filters, analyzes, and synthesizes high-signal intelligence from **ArXiv**, **GitHub**, and **Hacker News**.

It is specifically tuned to filter noise and prioritize:
* **Generative AI & LLM Architectures** (RAG, Agents)
* **Enterprise Software Engineering** (.NET, Microservices)
* **LegalTech & Digital Forensics**

---

## 🚀 Features

* **🧠 Semantic Gatekeeper:** Uses LLMs (Claude 3.5 Sonnet or Gemini 1.5 Pro) to grade papers on a 1-10 scale based on a custom "Interest Constitution."
* **🕵️ Code Hunter:** Automatically scrapes ArXiv abstract pages to find and verify official GitHub implementations.
* **📡 Multi-Source Monitoring:**
    * **ArXiv:** Scans `cs.SE`, `cs.AI`, `cs.CR`, `cs.CL`.
    * **GitHub Trending:** Monitors C# and Python repos.
    * **Hacker News:** Filters for high-impact tech discussions.
* **💾 Long-Term Memory:** Uses SQLite to deduplicate findings (never reads the same paper twice).
* **📰 Daily Briefing:** Generates a clean, Obsidian-friendly Markdown report in `Daily_Briefings/`.

---

## 🏗️ Architecture

The system runs on **LangGraph** with the following cyclic node structure:

`Monitor` (Ingestion) -> `Industry_Monitor` (Git/HN) -> `Gatekeeper` (LLM Filter) -> `Analyst` (Code Search) -> `Journalist` (Report Gen)

---

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone [https://github.com/abahjat/sentinel.git](https://github.com/abahjat/sentinel.git)
cd sentinel