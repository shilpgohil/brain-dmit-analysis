# Diagrams

> All diagrams are Mermaid and reflect the code as-is. Names match real modules/classes/endpoints.

## 1. System architecture

```mermaid
flowchart TB
    subgraph Client["Presentation - frontend/ (Next.js 16, client-only)"]
        NEW["/analysis/new<br/>10-slot upload grid"]
        RES["/analysis/[id]<br/>results + 1.8s polling"]
        SESS["/sessions · /compare · /system"]
        API_TS["src/lib/api.ts<br/>NEXT_PUBLIC_API_URL"]
        NEW --> API_TS
        RES --> API_TS
        SESS --> API_TS
    end

    subgraph API["API layer - api/ (FastAPI, port 8001)"]
        MAIN["main.py<br/>CORS · /api/health · static mounts"]
        SR["routes/sessions.py"]
        AR["routes/analysis.py"]
        SCH["schemas.py (Pydantic v2)"]
        STORE["store.py<br/>session_store dict"]
        PERS["persistence.py<br/>SQLite data/sessions.db"]
        MAIN --> SR & AR
        SR & AR --> STORE
        STORE <--> PERS
    end

    subgraph Core["Core processing (synchronous, CPU-bound)"]
        IDP["integrated_dmit_pipeline.py<br/>IntegratedDMITPipeline"]
        PREP["preprocessing_images/<br/>FingerToFingerprintPipeline"]
        OFE["optimized_feature_extractor_clean.py<br/>OptimizedFeatureExtractor"]
        PC["pattern_classifier.py<br/>PatternClassifier"]
        MAP["dmit_intelligence_mapper.py"]
        EXT["dmit_extensions/engine.py<br/>41 extensions"]
        IDP --> PREP --> OFE
        OFE --> PC
        IDP --> MAP
        IDP --> EXT
    end

    subgraph Report["Reporting"]
        PREM["premium_pdf_report/<br/>PremiumReportGenerator (API path)"]
        ADV["advanced_3d_pdf_generator/<br/>create_3d_report (CLI path)"]
    end

    subgraph FS["Filesystem"]
        UP[("uploads/{sid}/SLOT.ext")]
        OUT[("output/dmit_report_{sid}.pdf")]
    end

    API_TS -- "REST JSON + multipart" --> MAIN
    AR -- "BackgroundTasks → asyncio.to_thread" --> IDP
    AR --> PREM
    IDP -. "CLI only" .-> ADV
    SR --> UP
    PREM --> OUT
    MAIN -- "/uploads /output static" --> FS
```

## 2. Request / data flow (analysis lifecycle)

```mermaid
flowchart LR
    A["POST /api/sessions"] --> B["uploads/{sid}/ created<br/>status=pending"]
    B --> C["POST /api/sessions/{sid}/images<br/>files + finger_positions=L1..R5"]
    C --> D["POST /api/analysis/run"]
    D -->|"202-style {status: started}"| E["background thread<br/>_run_pipeline_sync"]
    E --> F["preprocessing → extracting → mapping<br/>→ extending → generating_report"]
    F --> G["session.result = AnalysisResult<br/>status=completed · persist to SQLite"]
    D -.-> H["GET /api/analysis/{sid}<br/>poll every 1.8s"]
    H -->|in flight| F
    H -->|completed| I["full AnalysisResult JSON"]
    I --> J["GET /api/analysis/{sid}/report/download<br/>PDF FileResponse"]
```

## 3. Component dependency graph

```mermaid
flowchart TD
    main["api.main"] --> sessions["api.routes.sessions"]
    main --> analysis["api.routes.analysis"]
    main --> store["api.store"]
    sessions --> helpers["api.helpers"] & schemas["api.schemas"] & store
    analysis --> helpers & schemas & store
    store --> persistence["api.persistence (sqlite3)"]

    analysis -. "lazy import in task" .-> idp["integrated_dmit_pipeline"]
    analysis -. "lazy import in task" .-> prem["premium_pdf_report.generator"]

    idp --> prep["preprocessing_images.pipeline"]
    prep --> s1["stage1_segmentation"] & s2["stage2_validation"] & s3["stage3_roi_detection"] & s4["stage4_nail_removal"] & s5["stage5_ridge_enhancement"]
    idp --> ofe["optimized_feature_extractor_clean"]
    ofe -. optional .-> pc["pattern_classifier"]
    idp --> mapper["dmit_intelligence_mapper"]
    idp --> engine["dmit_extensions.engine"]
    engine --> base["dmit_extensions.base"] & exts["41 extension modules"]
    idp -. "CLI only" .-> adv["advanced_3d_pdf_generator"]
    adv --> rdp["core.real_data_processor"] & rcg["visual.real_chart_generator"] & pb["core.pdf_builder"]

    prem --> theme["theme"] & charts["charts"] & coverbg["cover_background"]
    prem --> sects["sections/* (9 modules)"] --> shelp["sections.helpers"]
```

## 4. Sequence diagram — main workflow

```mermaid
sequenceDiagram
    autonumber
    participant UI as frontend /analysis/new
    participant API as FastAPI api/
    participant BG as Worker thread (_run_pipeline_sync)
    participant IDP as IntegratedDMITPipeline
    participant FE as OptimizedFeatureExtractor
    participant MAP as dmit_intelligence_mapper
    participant ENG as DMITExtensionsEngine
    participant PDF as PremiumReportGenerator
    participant DB as SQLite + uploads/ output/

    UI->>API: POST /api/sessions {subject…}
    API->>DB: mkdir uploads/{sid}; upsert session
    API-->>UI: AnalysisSession (pending)
    UI->>API: POST /api/analysis/{sid}/upload (files, finger_positions)
    API->>DB: save L1.bmp…R5.bmp; update image_paths
    UI->>API: POST /api/analysis/run
    API->>BG: BackgroundTasks → to_thread
    API-->>UI: {status: "started"}

    loop per image (≤10)
        BG->>IDP: analyze_single_finger(path)
        IDP->>IDP: FingerToFingerprintPipeline.process (optional)
        IDP->>FE: extract_optimized_features(image)
        FE->>FE: PatternClassifier.classify (cores/deltas, family, TFRC)
        FE-->>IDP: consolidated_features (~85)
        IDP->>MAP: map_features_to_dmit_profile(features, finger_type)
        MAP-->>IDP: MI / lobes / VAK / Big Five
        IDP->>ENG: run_all_extensions(features ∪ MI)
        ENG-->>IDP: {ExtensionClassName: scores}
    end
    BG->>IDP: _aggregate_results_scientifically (Table 1.1)
    IDP->>ENG: run_all_extensions(holistic MI)
    IDP-->>BG: full_result

    BG->>BG: normalize → AnalysisResult
    BG->>PDF: create_report(full_result, output_path, session_meta)
    PDF->>DB: output/dmit_report_{sid}.pdf
    BG->>DB: persist session (result, report_path, completed)

    loop poll every 1.8 s
        UI->>API: GET /api/analysis/{sid}
        API-->>UI: status + pipeline_stages (then full result)
    end
    UI->>API: GET /api/analysis/{sid}/report/download
    API-->>UI: PDF
```

## 5. Storage / schema diagram

```mermaid
erDiagram
    SESSIONS {
        TEXT id PK "session UUID"
        TEXT data "JSON snapshot of session dict"
        TEXT updated_at "ISO timestamp"
    }
    SESSION_JSON {
        string subject_name
        string status "AnalysisStatus value"
        list image_paths "uploads/{sid}/SLOT.ext"
        dict finger_slots "L1..R5 to path"
        list pipeline_stages
        json result "serialized AnalysisResult"
        string report_path "output/dmit_report_{sid}.pdf"
        string error "only on failure"
    }
    UPLOADS_DIR {
        path file "uploads/{session_id}/{SLOT}.{ext}"
    }
    OUTPUT_DIR {
        path pdf "output/dmit_report_{session_id}.pdf"
    }
    SESSIONS ||--|| SESSION_JSON : "data column contains"
    SESSION_JSON ||--o{ UPLOADS_DIR : "image_paths reference"
    SESSION_JSON ||--o| OUTPUT_DIR : "report_path references"
```

## 6. Table 1.1 scientific mapping (finger → lobe → traits)

```mermaid
flowchart LR
    subgraph Fingers
        T["Thumb L1/R1"]
        I["Index L2/R2"]
        M["Middle L3/R3"]
        R["Ring L4/R4"]
        L["Little L5/R5"]
    end
    subgraph Lobes
        PF["Prefrontal"]
        POF["Posterior Frontal"]
        PAR["Parietal"]
        TEM["Temporal"]
        OCC["Occipital"]
    end
    subgraph Traits
        PERS["Big Five · Inter/Intrapersonal · Existential"]
        LOG["Logical-Mathematical"]
        KIN["Bodily-Kinesthetic · Kinesthetic VAK"]
        AUD["Linguistic · Musical · Auditory VAK"]
        VIS["Spatial · Visual VAK"]
    end
    T --> PF --> PERS
    I --> POF --> LOG
    M --> PAR --> KIN
    R --> TEM --> AUD
    L --> OCC --> VIS
    I -.co-driver.-> VIS
    R -.co-driver.-> NAT["Naturalistic"]
    L -.co-driver.-> NAT
```

## 7. Pipeline stage state machine (per session)

```mermaid
stateDiagram-v2
    [*] --> pending: POST /api/sessions
    pending --> preprocessing: POST /api/analysis/run
    preprocessing --> extracting
    extracting --> mapping
    mapping --> extending
    extending --> generating_report: generate_pdf=true
    extending --> completed: generate_pdf=false
    generating_report --> completed: (PDF failure → completed + warning)
    preprocessing --> failed: uncaught exception
    extracting --> failed
    mapping --> failed
    extending --> failed
    completed --> preprocessing: re-run allowed
    failed --> preprocessing: re-run allowed
```
