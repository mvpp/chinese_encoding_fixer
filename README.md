脚本加入了苹果字符重组（NFC）和容错机制
在终端运行它：

```Bash
python3 final_fix.py
```
📊 Architecture & Features (系统架构与核心特性)

<div align="center">
<table>
<tr>
<td align="center">🎯 <b>Dual-Tier Themes</b>



Canonical (固定分类) + Open (自由形态)</td>
<td align="center">🧠 <b>Smart SEC Parsing</b>



基于 Token 预算的动态截断分配</td>
<td align="center">🤖 <b>3-Layer LLM Engine</b>



主题发现 + TF-IDF 打分 + 市场叙事</td>
<td align="center">🗄️ <b>Unified Output</b>



开箱即用的 SQLite 统一查询层</td>
</tr>
</table>
</div>

🏗️ System Flow (系统处理流)

flowchart TB
    %% Definitions
    classDef core fill:#f8fafc,stroke:#94a3b8,stroke-width:1px,color:#0f172a,rx:6px
    classDef extract fill:#eff6ff,stroke:#60a5fa,stroke-width:2px,color:#1e3a8a,rx:6px
    classDef llm fill:#faf5ff,stroke:#c084fc,stroke-width:2px,color:#6b21a8,rx:6px
    classDef db fill:#f0fdf4,stroke:#4ade80,stroke-width:2px,color:#14532d,rx:8px
    classDef output fill:#fff7ed,stroke:#fb923c,stroke-width:2px,color:#9a3412,rx:6px

    subgraph Pipeline ["📡 1. Data Pipeline (Two-Pass Data Collection)"]
        direction TB
        subgraph Pass1 ["Pass 1: Core Providers"]
            YF[Yahoo Finance<br/>Fundamentals]:::core
            SEC[SEC EDGAR<br/>10-K / 10-Q / S-1]:::core
        end
        subgraph Pass2 ["Pass 2: Enrichment (Ticker Dependent)"]
            FH[Finnhub News]:::core
            GD[GDELT Themes]:::core
            PV[PatentsView CPC]:::core
            ST[StockTwits Social]:::core
        end
        Pass1 --> Pass2
    end

    subgraph Parsing ["⚙️ 2. Smart Parsing"]
        SE[Smart SEC Extractor<br/>Item 1, 7 & 1A (70/30 Truncation)]:::extract
        DN[News/Patents Deduplication<br/>& Text Normalization]:::extract
        SEC --> SE
        Pass2 --> DN
    end

    subgraph ThemeEngine ["🧠 3. Theme Extraction Engine (3 Layers)"]
        direction TB
        L1["Layer 1: LLM Discovery<br/>(Extract Themes & Map to Canonical)"]:::llm
        L2["Layer 2: BM25 Corpus Scoring<br/>(TF-IDF Distinctiveness Filter)"]:::llm
        L3["Layer 3: Market Narrative<br/>(LLM Perception from News)"]:::llm
    end

    subgraph Storage ["🎯 4. Unified Output Database"]
        direction LR
        DB[(SQLite DB<br/>Query Layer)]:::db
        CT[Tier 1: Canonical Themes<br/>~200 Fixed Taxonomy]:::output
        OT[Tier 2: Open Themes<br/>Distinctive & Free-form]:::output
        NT[Tier 3: Narrative Themes<br/>Market Perception]:::output
    end

    %% Routing
    SE --> L1
    L1 -- Mapped --> CT
    L1 -- Unmapped --> OT
    L1 -. Trigger .-> L2
    L2 -- Score Filter --> OT
    DN --> L3
    L3 --> NT

    CT --> DB
    OT --> DB
    NT --> DB


🔍 Deep Dive: The 3-Layer Extraction Engine

该项目最核心的亮点在于其多层主题提炼机制，确保提取出的主题既标准又具有股票独特性：

Layer

Component

Mechanism (运行机制)

Outcome (产出结果)

Layer 1

LLM Theme Discovery

智能分配 100K Tokens 预算读取 SEC 报告提取主题。通过 Alias lookup (别名映射) 和 Cosine Similarity (向量相似度 ≥ 0.60) 将其归一化。

归入 Canonical Themes（如: Cloud Computing）。未匹配项降级为 Open Themes。

Layer 2

BM25 Corpus Scoring

建立所有 SEC 文件的全局 TF-IDF 矩阵。对 Open Themes 进行“词频-逆文档频率”打分，过滤掉 "Cloud computing" 等烂大街词汇。

产出高价值的 Open Themes（如: Peptide Vaccine），解决长尾主题问题。

Layer 3

Market Narrative

使用独立 LLM 处理汇总后的新闻头条和社交情绪（StockTwits），提取外界对该公司的“贴标签”行为。

产出 Narrative Themes（如: Meme stock, AI Winner, Tariff Risk）。
