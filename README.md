脚本加入了苹果字符重组（NFC）和容错机制
在终端运行它：

```Bash
python3 final_fix.py
```
```mermaid
flowchart TB
    %% Definitions
    classDef core fill:#f8fafc,stroke:#94a3b8,stroke-width:1px,color:#0f172a,rx:6px
    classDef extract fill:#eff6ff,stroke:#60a5fa,stroke-width:2px,color:#1e3a8a,rx:6px
    classDef llm fill:#faf5ff,stroke:#c084fc,stroke-width:2px,color:#6b21a8,rx:6px
    classDef db fill:#f0fdf4,stroke:#4ade80,stroke-width:2px,color:#14532d,rx:8px
    classDef output fill:#fff7ed,stroke:#fb923c,stroke-width:2px,color:#9a3412,rx:6px

    subgraph Pipeline ["📡 1. Data Pipeline (Two-Pass)"]
        direction TB
        subgraph Pass1 ["Pass 1: Core Providers"]
            YF[Yahoo Finance<br/>Fundamentals]:::core
            SEC[SEC EDGAR<br/>10-K / 10-Q / S-1]:::core
        end
        subgraph Pass2 ["Pass 2: Enrichment"]
            FH[Finnhub News]:::core
            GD[GDELT Themes]:::core
            PV[PatentsView CPC]:::core
            ST[StockTwits Social]:::core
        end
        Pass1 --> Pass2
    end

    subgraph Parsing ["⚙️ 2. Smart Parsing"]
        SE[Smart SEC Extractor<br/>Item 1, 7 & 1A]:::extract
        DN[Deduplication<br/>& Normalization]:::extract
        SEC --> SE
        Pass2 --> DN
    end

    subgraph ThemeEngine ["🧠 3. Theme Engine (3 Layers)"]
        direction TB
        L1["Layer 1: LLM Discovery<br/>(Extract & Map)"]:::llm
        L2["Layer 2: BM25 Corpus Scoring<br/>(TF-IDF Filter)"]:::llm
        L3["Layer 3: Market Narrative<br/>(News Perception)"]:::llm
    end

    subgraph Storage ["🎯 4. Unified Output DB"]
        direction LR
        DB[(SQLite DB)]:::db
        CT[Tier 1: Canonical<br/>~200 Fixed Taxonomy]:::output
        OT[Tier 2: Open Themes<br/>Distinctive]:::output
        NT[Tier 3: Narrative<br/>Market Perception]:::output
    end

    %% Routing
    SE --> L1
    L1 -- Mapped --> CT
    L1 -- Unmapped --> OT
    L1 -. Trigger .-> L2
    L2 -- Filtered --> OT
    DN --> L3
    L3 --> NT

    CT --> DB
    OT --> DB
    NT --> DB
```
