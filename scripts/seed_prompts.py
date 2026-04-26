"""
Seed script: populates database with 100 prompts, 5 categories, 5 collections.
Run: python -m scripts.seed_prompts
"""
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.models.prompt import Prompt
from app.models.collection import Collection, CollectionPrompt
from app.models.user import User
from app.core.security import hash_password

# ──────────────────────────────────────────
# SEED DATA
# ──────────────────────────────────────────

CATEGORIES = ["coding", "writing", "analysis", "marketing", "data"]

PROMPTS_DATA = [
    # CODING (20 prompts)
    {
        "title": "Debug Python Code",
        "content": "You are an expert Python developer. Analyze the following code, identify all bugs, explain each issue clearly, and provide the corrected version with comments.",
        "category": "coding",
        "tags": ["python", "debug", "code-review"],
    },
    {
        "title": "REST API Design",
        "content": "You are a senior backend architect. Design a complete REST API for the given system, including endpoints, HTTP methods, request/response schemas, authentication, and error handling.",
        "category": "coding",
        "tags": ["api", "rest", "backend", "design"],
    },
    {
        "title": "SQL Query Optimizer",
        "content": "You are a database performance expert. Analyze the given SQL query, identify performance bottlenecks, and rewrite it with optimizations. Explain each optimization made.",
        "category": "coding",
        "tags": ["sql", "database", "optimization"],
    },
    {
        "title": "Code Review Assistant",
        "content": "You are a senior software engineer conducting a code review. Evaluate the code for correctness, performance, security, readability, and maintainability. Provide specific, actionable feedback.",
        "category": "coding",
        "tags": ["code-review", "best-practices"],
    },
    {
        "title": "Algorithm Design",
        "content": "You are a competitive programmer and algorithms expert. Design an efficient algorithm for the given problem. Explain your approach, time/space complexity, and provide clean implementation.",
        "category": "coding",
        "tags": ["algorithms", "data-structures", "complexity"],
    },
    {
        "title": "Docker Setup",
        "content": "You are a DevOps engineer. Create a production-ready Docker setup for the given application including Dockerfile, docker-compose.yml, with best practices for security and performance.",
        "category": "coding",
        "tags": ["docker", "devops", "containers"],
    },
    {
        "title": "React Component Builder",
        "content": "You are a senior React developer. Build a reusable, well-structured React component for the given requirements. Include proper TypeScript types, props, state management, and unit tests.",
        "category": "coding",
        "tags": ["react", "typescript", "frontend"],
    },
    {
        "title": "FastAPI Endpoint Creator",
        "content": "You are a FastAPI expert. Create production-ready API endpoints for the given requirements including Pydantic schemas, database models, business logic, error handling, and documentation.",
        "category": "coding",
        "tags": ["fastapi", "python", "api"],
    },
    {
        "title": "System Design Interview",
        "content": "You are a principal engineer conducting a system design interview. Design a scalable system for the given problem. Cover architecture, databases, caching, load balancing, and trade-offs.",
        "category": "coding",
        "tags": ["system-design", "architecture", "scalability"],
    },
    {
        "title": "Git Workflow Advisor",
        "content": "You are a Git expert and team lead. Design an optimal Git branching strategy and workflow for the given team size and project type. Include naming conventions and best practices.",
        "category": "coding",
        "tags": ["git", "workflow", "version-control"],
    },
    {
        "title": "Security Audit",
        "content": "You are a cybersecurity expert. Perform a comprehensive security audit of the given code or system. Identify vulnerabilities (OWASP Top 10), explain risks, and provide remediation steps.",
        "category": "coding",
        "tags": ["security", "owasp", "audit"],
    },
    {
        "title": "Unit Test Generator",
        "content": "You are a TDD expert. Generate comprehensive unit tests for the given code. Cover happy paths, edge cases, error scenarios. Use proper mocking and follow testing best practices.",
        "category": "coding",
        "tags": ["testing", "unit-tests", "tdd"],
    },
    {
        "title": "Microservices Architecture",
        "content": "You are a cloud architect. Design a microservices architecture for the given monolith. Define service boundaries, communication patterns, data management, and deployment strategy.",
        "category": "coding",
        "tags": ["microservices", "architecture", "cloud"],
    },
    {
        "title": "Machine Learning Pipeline",
        "content": "You are an ML engineer. Design a complete machine learning pipeline for the given problem. Include data preprocessing, feature engineering, model selection, training, evaluation, and deployment.",
        "category": "coding",
        "tags": ["machine-learning", "python", "pipeline"],
    },
    {
        "title": "Database Schema Designer",
        "content": "You are a database architect. Design an optimized database schema for the given requirements. Include tables, relationships, indexes, constraints, and explain design decisions.",
        "category": "coding",
        "tags": ["database", "schema", "postgresql"],
    },
    {
        "title": "CLI Tool Builder",
        "content": "You are a Python developer specializing in CLI tools. Build a complete command-line tool for the given task using Click or Typer. Include help text, error handling, and user-friendly output.",
        "category": "coding",
        "tags": ["python", "cli", "automation"],
    },
    {
        "title": "Async Python Expert",
        "content": "You are an async Python specialist. Rewrite the given synchronous code using async/await, asyncio, and proper concurrency patterns. Explain the performance improvements.",
        "category": "coding",
        "tags": ["python", "async", "concurrency"],
    },
    {
        "title": "API Rate Limiter Design",
        "content": "You are a backend engineer. Design and implement an API rate limiting system. Cover algorithms (token bucket, sliding window), implementation, Redis integration, and bypass prevention.",
        "category": "coding",
        "tags": ["api", "rate-limiting", "redis"],
    },
    {
        "title": "CI/CD Pipeline Designer",
        "content": "You are a DevOps engineer. Design a complete CI/CD pipeline for the given project. Include build, test, security scanning, staging, and production deployment stages with rollback strategy.",
        "category": "coding",
        "tags": ["cicd", "devops", "automation"],
    },
    {
        "title": "Performance Profiler",
        "content": "You are a performance engineering expert. Analyze the given code or system for performance issues. Use profiling techniques, identify bottlenecks, and provide optimized solutions with benchmarks.",
        "category": "coding",
        "tags": ["performance", "optimization", "profiling"],
    },

    # WRITING (20 prompts)
    {
        "title": "Technical Blog Writer",
        "content": "You are a senior technical writer. Write an engaging, SEO-optimized technical blog post about the given topic. Include a compelling intro, clear explanations, code examples, and strong conclusion.",
        "category": "writing",
        "tags": ["blog", "technical-writing", "seo"],
    },
    {
        "title": "LinkedIn Post Creator",
        "content": "You are a LinkedIn content strategist. Create a high-engagement LinkedIn post about the given topic. Use a hook, storytelling, key insights, and a call-to-action. Optimize for the algorithm.",
        "category": "writing",
        "tags": ["linkedin", "social-media", "professional"],
    },
    {
        "title": "Email Campaign Writer",
        "content": "You are an email marketing expert. Write a compelling email campaign for the given product/service. Include subject line, preview text, personalized body, clear CTA, and A/B test variations.",
        "category": "writing",
        "tags": ["email", "marketing", "copywriting"],
    },
    {
        "title": "Product Description Writer",
        "content": "You are a conversion copywriter. Write compelling product descriptions that sell. Focus on benefits over features, use sensory language, address objections, and include urgency elements.",
        "category": "writing",
        "tags": ["ecommerce", "copywriting", "product"],
    },
    {
        "title": "Case Study Builder",
        "content": "You are a B2B content writer. Write a detailed case study for the given scenario. Structure: challenge, solution, implementation, results, testimonials. Use data and specifics.",
        "category": "writing",
        "tags": ["case-study", "b2b", "content"],
    },
    {
        "title": "Cover Letter Generator",
        "content": "You are a career coach and professional writer. Write a compelling, personalized cover letter for the given job position and candidate background. Make it stand out while remaining authentic.",
        "category": "writing",
        "tags": ["career", "cover-letter", "job-application"],
    },
    {
        "title": "Press Release Writer",
        "content": "You are a PR professional. Write a compelling press release for the given announcement. Follow AP style, include strong headline, compelling lead, supporting quotes, and boilerplate.",
        "category": "writing",
        "tags": ["pr", "press-release", "communications"],
    },
    {
        "title": "YouTube Script Writer",
        "content": "You are a YouTube content creator and scriptwriter. Write a compelling video script for the given topic. Include hook, intro, main content with transitions, and strong outro with CTA.",
        "category": "writing",
        "tags": ["youtube", "script", "video-content"],
    },
    {
        "title": "Whitepaper Author",
        "content": "You are an industry expert and technical writer. Write a comprehensive whitepaper on the given topic. Include executive summary, problem statement, solution, evidence, and recommendations.",
        "category": "writing",
        "tags": ["whitepaper", "thought-leadership", "research"],
    },
    {
        "title": "Newsletter Creator",
        "content": "You are a newsletter writer with high open rates. Create an engaging newsletter for the given audience and topic. Include curated insights, original analysis, actionable tips, and community updates.",
        "category": "writing",
        "tags": ["newsletter", "content-marketing", "audience"],
    },
    {
        "title": "Resume Optimizer",
        "content": "You are a professional resume writer and ATS expert. Rewrite and optimize the given resume for the target role. Quantify achievements, use strong action verbs, and ensure ATS compatibility.",
        "category": "writing",
        "tags": ["resume", "career", "ats"],
    },
    {
        "title": "Documentation Writer",
        "content": "You are a technical documentation expert. Write comprehensive, user-friendly documentation for the given software/API. Include getting started guide, API reference, examples, and troubleshooting.",
        "category": "writing",
        "tags": ["documentation", "technical-writing", "api-docs"],
    },
    {
        "title": "Social Media Calendar",
        "content": "You are a social media strategist. Create a 30-day content calendar for the given brand. Include post ideas, captions, hashtags, best posting times, and engagement strategies for each platform.",
        "category": "writing",
        "tags": ["social-media", "content-calendar", "strategy"],
    },
    {
        "title": "Persuasive Essay Writer",
        "content": "You are an expert debater and essayist. Write a highly persuasive essay on the given topic. Use rhetorical devices, strong evidence, anticipate counterarguments, and build to a compelling conclusion.",
        "category": "writing",
        "tags": ["essay", "persuasion", "academic"],
    },
    {
        "title": "Story Outline Creator",
        "content": "You are a published fiction author. Create a detailed story outline for the given concept. Include character arcs, plot structure (three-act), key scenes, themes, and narrative hooks.",
        "category": "writing",
        "tags": ["fiction", "storytelling", "creative-writing"],
    },
    {
        "title": "Grant Proposal Writer",
        "content": "You are a successful grant writer. Write a compelling grant proposal for the given project and funding opportunity. Cover need statement, objectives, methodology, evaluation, and budget justification.",
        "category": "writing",
        "tags": ["grant", "nonprofit", "proposal"],
    },
    {
        "title": "Speech Writer",
        "content": "You are a presidential speechwriter. Write a powerful speech for the given occasion and speaker. Include memorable opening, three key messages, storytelling elements, emotional peaks, and unforgettable closing.",
        "category": "writing",
        "tags": ["speech", "public-speaking", "communication"],
    },
    {
        "title": "SEO Article Writer",
        "content": "You are an SEO content expert. Write a comprehensive, search-optimized article on the given keyword/topic. Include proper heading structure, semantic keywords, internal linking suggestions, and meta description.",
        "category": "writing",
        "tags": ["seo", "content", "blogging"],
    },
    {
        "title": "Podcast Script Creator",
        "content": "You are a podcast producer and scriptwriter. Create a complete podcast episode script for the given topic. Include intro, interview questions or talking points, transitions, sponsor segments, and outro.",
        "category": "writing",
        "tags": ["podcast", "audio", "script"],
    },
    {
        "title": "Customer Story Writer",
        "content": "You are a customer success storyteller. Write an engaging customer success story for the given scenario. Structure: customer background, challenge, solution journey, measurable results, and future outlook.",
        "category": "writing",
        "tags": ["customer-story", "testimonial", "marketing"],
    },

    # ANALYSIS (20 prompts)
    {
        "title": "SWOT Analysis Expert",
        "content": "You are a strategic consultant. Conduct a comprehensive SWOT analysis for the given company/product. Provide specific, data-driven insights for each quadrant and strategic recommendations.",
        "category": "analysis",
        "tags": ["swot", "strategy", "business"],
    },
    {
        "title": "Competitor Analysis",
        "content": "You are a market intelligence analyst. Perform a detailed competitor analysis for the given company. Compare products, pricing, market positioning, strengths, weaknesses, and strategic opportunities.",
        "category": "analysis",
        "tags": ["competitor", "market-research", "strategy"],
    },
    {
        "title": "Financial Statement Analyzer",
        "content": "You are a CFA-level financial analyst. Analyze the given financial statements. Calculate key ratios, identify trends, assess financial health, and provide investment/business recommendations.",
        "category": "analysis",
        "tags": ["finance", "financial-analysis", "investment"],
    },
    {
        "title": "User Research Synthesizer",
        "content": "You are a UX researcher. Synthesize the given user research data. Identify patterns, key insights, user pain points, opportunities, and translate findings into actionable product recommendations.",
        "category": "analysis",
        "tags": ["ux", "user-research", "product"],
    },
    {
        "title": "Market Sizing Expert",
        "content": "You are a strategy consultant. Estimate the market size for the given product/service using TAM/SAM/SOM framework. Use both top-down and bottom-up approaches with clear assumptions.",
        "category": "analysis",
        "tags": ["market-sizing", "tam-sam-som", "strategy"],
    },
    {
        "title": "Risk Assessment Analyst",
        "content": "You are a risk management expert. Conduct a comprehensive risk assessment for the given project or business. Identify risks, assess probability and impact, and create a risk mitigation plan.",
        "category": "analysis",
        "tags": ["risk", "management", "assessment"],
    },
    {
        "title": "A/B Test Interpreter",
        "content": "You are a data scientist specializing in experimentation. Analyze the given A/B test results. Assess statistical significance, practical significance, segment effects, and provide clear recommendations.",
        "category": "analysis",
        "tags": ["ab-testing", "statistics", "data-science"],
    },
    {
        "title": "Business Model Analyzer",
        "content": "You are a business model expert. Analyze the given business model using the Business Model Canvas framework. Identify strengths, weaknesses, revenue opportunities, and disruption risks.",
        "category": "analysis",
        "tags": ["business-model", "canvas", "strategy"],
    },
    {
        "title": "Product Metrics Analyst",
        "content": "You are a product analytics expert. Analyze the given product metrics and KPIs. Identify concerning trends, leading/lagging indicators, root causes, and recommend actions with expected impact.",
        "category": "analysis",
        "tags": ["metrics", "kpi", "product-analytics"],
    },
    {
        "title": "Tech Stack Evaluator",
        "content": "You are a CTO-level technology advisor. Evaluate the given technology stack choices. Analyze scalability, maintainability, cost, talent availability, and provide recommendations with trade-off analysis.",
        "category": "analysis",
        "tags": ["tech-stack", "architecture", "evaluation"],
    },
    {
        "title": "Customer Churn Analyzer",
        "content": "You are a customer success analyst. Analyze the given customer churn data. Identify churn patterns, at-risk segments, root causes, and create a comprehensive retention strategy.",
        "category": "analysis",
        "tags": ["churn", "retention", "customer-success"],
    },
    {
        "title": "Content Performance Analyzer",
        "content": "You are a content analytics expert. Analyze the given content performance data. Identify top performers, underperformers, audience engagement patterns, and provide content strategy recommendations.",
        "category": "analysis",
        "tags": ["content-analytics", "performance", "seo"],
    },
    {
        "title": "Pricing Strategy Analyst",
        "content": "You are a pricing strategy expert. Analyze the given market and product to recommend optimal pricing strategy. Consider value-based, competitive, and cost-plus approaches with psychological pricing tactics.",
        "category": "analysis",
        "tags": ["pricing", "strategy", "revenue"],
    },
    {
        "title": "Survey Data Interpreter",
        "content": "You are a market research analyst. Analyze the given survey data. Identify key themes, statistical patterns, demographic segments, actionable insights, and present findings with visual recommendations.",
        "category": "analysis",
        "tags": ["survey", "market-research", "data"],
    },
    {
        "title": "Sales Funnel Analyzer",
        "content": "You are a revenue operations analyst. Analyze the given sales funnel data. Identify conversion rate issues, drop-off points, bottlenecks, and provide specific optimizations for each funnel stage.",
        "category": "analysis",
        "tags": ["sales-funnel", "conversion", "revenue"],
    },
    {
        "title": "SEO Audit Analyzer",
        "content": "You are an SEO expert. Conduct a comprehensive SEO audit of the given website/data. Cover technical SEO, on-page optimization, backlink profile, content quality, and prioritized action plan.",
        "category": "analysis",
        "tags": ["seo", "audit", "digital-marketing"],
    },
    {
        "title": "Brand Perception Analyzer",
        "content": "You are a brand strategist. Analyze the given brand perception data, social mentions, and customer feedback. Assess brand health, identify perception gaps, and recommend brand strengthening strategies.",
        "category": "analysis",
        "tags": ["brand", "perception", "strategy"],
    },
    {
        "title": "Cohort Analysis Expert",
        "content": "You are a growth analyst. Conduct a detailed cohort analysis of the given user data. Identify retention patterns, revenue trends by cohort, and actionable insights to improve user lifecycle value.",
        "category": "analysis",
        "tags": ["cohort", "retention", "growth"],
    },
    {
        "title": "Operations Efficiency Analyzer",
        "content": "You are an operations consultant. Analyze the given business processes for efficiency. Identify bottlenecks, waste (lean methodology), automation opportunities, and calculate ROI of improvements.",
        "category": "analysis",
        "tags": ["operations", "efficiency", "lean"],
    },
    {
        "title": "Trend Forecaster",
        "content": "You are a strategic foresight analyst. Analyze current trends in the given industry. Identify emerging signals, potential disruptions, 1-year and 3-year forecasts, and strategic implications.",
        "category": "analysis",
        "tags": ["trends", "forecasting", "strategy"],
    },

    # MARKETING (20 prompts)
    {
        "title": "Brand Positioning Statement",
        "content": "You are a brand strategist at a top agency. Create a compelling brand positioning statement for the given company. Include target audience, category, differentiation, and reason to believe.",
        "category": "marketing",
        "tags": ["brand", "positioning", "strategy"],
    },
    {
        "title": "Google Ads Copy Writer",
        "content": "You are a PPC specialist with high CTR track record. Write compelling Google Search Ads for the given product/service. Create 5 headlines (30 chars), 2 descriptions (90 chars), and extensions.",
        "category": "marketing",
        "tags": ["google-ads", "ppc", "copywriting"],
    },
    {
        "title": "Product Launch Strategy",
        "content": "You are a product marketing manager. Create a comprehensive go-to-market strategy for the given product launch. Cover positioning, messaging, channels, launch timeline, and success metrics.",
        "category": "marketing",
        "tags": ["product-launch", "gtm", "strategy"],
    },
    {
        "title": "Customer Persona Builder",
        "content": "You are a customer research expert. Build detailed buyer personas for the given product/service. Include demographics, psychographics, goals, pain points, buying triggers, and preferred channels.",
        "category": "marketing",
        "tags": ["personas", "customer-research", "marketing"],
    },
    {
        "title": "Growth Hacking Strategist",
        "content": "You are a growth hacker with proven track record. Develop 10 creative, low-cost growth experiments for the given startup. Include hypothesis, execution plan, metrics, and expected impact.",
        "category": "marketing",
        "tags": ["growth-hacking", "startup", "acquisition"],
    },
    {
        "title": "Influencer Outreach Script",
        "content": "You are an influencer marketing specialist. Write personalized outreach messages for the given campaign. Create DM template, email template, and follow-up sequence for micro and macro influencers.",
        "category": "marketing",
        "tags": ["influencer", "outreach", "partnership"],
    },
    {
        "title": "Landing Page Optimizer",
        "content": "You are a CRO (Conversion Rate Optimization) expert. Rewrite and optimize the given landing page copy. Focus on headline, value proposition, social proof, objection handling, and CTA optimization.",
        "category": "marketing",
        "tags": ["landing-page", "cro", "conversion"],
    },
    {
        "title": "Customer Retention Strategist",
        "content": "You are a customer lifecycle marketing expert. Design a comprehensive customer retention program for the given business. Include onboarding, engagement, win-back campaigns, and loyalty mechanics.",
        "category": "marketing",
        "tags": ["retention", "lifecycle", "loyalty"],
    },
    {
        "title": "Content Marketing Strategy",
        "content": "You are a content marketing director. Build a complete content marketing strategy for the given brand. Cover content pillars, formats, distribution channels, editorial calendar, and measurement framework.",
        "category": "marketing",
        "tags": ["content-strategy", "editorial", "inbound"],
    },
    {
        "title": "Viral Campaign Creator",
        "content": "You are a viral marketing expert. Design a creative viral marketing campaign for the given brand/product. Include core mechanic, content format, seeding strategy, and amplification plan.",
        "category": "marketing",
        "tags": ["viral", "campaign", "creative"],
    },
    {
        "title": "Facebook Ad Copy Creator",
        "content": "You are a Facebook Ads specialist. Write high-converting Facebook ad copy for the given product. Create primary text, headline, description for awareness, consideration, and conversion objectives.",
        "category": "marketing",
        "tags": ["facebook-ads", "social-ads", "copywriting"],
    },
    {
        "title": "Email Subject Line Generator",
        "content": "You are an email marketing expert with 40%+ open rates. Generate 20 compelling email subject lines for the given campaign. Cover curiosity, urgency, personalization, benefit, and question formats.",
        "category": "marketing",
        "tags": ["email", "subject-lines", "open-rate"],
    },
    {
        "title": "Referral Program Designer",
        "content": "You are a growth product manager. Design a high-converting referral program for the given business. Cover incentive structure, mechanics, messaging, referral flow, and anti-fraud measures.",
        "category": "marketing",
        "tags": ["referral", "growth", "virality"],
    },
    {
        "title": "SEO Keyword Strategy",
        "content": "You are an SEO strategist. Develop a comprehensive keyword strategy for the given website/niche. Cover seed keywords, long-tail opportunities, competitor gap analysis, and content cluster planning.",
        "category": "marketing",
        "tags": ["seo", "keywords", "content-strategy"],
    },
    {
        "title": "Partnership Proposal Writer",
        "content": "You are a business development expert. Write a compelling partnership proposal for the given opportunity. Cover mutual value, integration depth, co-marketing opportunities, and success metrics.",
        "category": "marketing",
        "tags": ["partnerships", "business-development", "b2b"],
    },
    {
        "title": "Pricing Page Copywriter",
        "content": "You are a SaaS pricing page specialist. Write compelling pricing page copy for the given product. Cover plan names, feature descriptions, value anchoring, FAQ section, and trust elements.",
        "category": "marketing",
        "tags": ["pricing", "saas", "conversion"],
    },
    {
        "title": "Brand Voice Guide Creator",
        "content": "You are a brand identity expert. Create a comprehensive brand voice and tone guide for the given company. Include personality traits, dos/don'ts, examples across channels, and writing guidelines.",
        "category": "marketing",
        "tags": ["brand-voice", "style-guide", "content"],
    },
    {
        "title": "Webinar Promotion Copy",
        "content": "You are a webinar marketing specialist. Write complete promotional copy for the given webinar. Include registration page copy, email sequence (3 emails), social posts, and follow-up messages.",
        "category": "marketing",
        "tags": ["webinar", "events", "promotion"],
    },
    {
        "title": "Community Building Strategy",
        "content": "You are a community growth expert. Design a community building strategy for the given brand. Cover platform selection, content programming, engagement mechanics, moderation, and growth tactics.",
        "category": "marketing",
        "tags": ["community", "engagement", "growth"],
    },
    {
        "title": "Pitch Deck Narrative",
        "content": "You are a startup pitch expert and investor. Write a compelling pitch deck narrative for the given startup. Cover problem, solution, market size, traction, team, ask, and investor-specific talking points.",
        "category": "marketing",
        "tags": ["pitch-deck", "startup", "fundraising"],
    },

    # DATA (20 prompts)
    {
        "title": "Data Pipeline Designer",
        "content": "You are a senior data engineer. Design a robust ETL/ELT data pipeline for the given requirements. Cover ingestion, transformation, validation, error handling, monitoring, and orchestration strategy.",
        "category": "data",
        "tags": ["data-pipeline", "etl", "data-engineering"],
    },
    {
        "title": "Dashboard KPI Designer",
        "content": "You are a data visualization expert. Design a comprehensive KPI dashboard for the given business function. Specify metrics, visualizations, data sources, refresh frequency, and stakeholder requirements.",
        "category": "data",
        "tags": ["dashboard", "kpi", "visualization"],
    },
    {
        "title": "Pandas Data Wrangler",
        "content": "You are a Python data scientist. Write clean, efficient Pandas code to wrangle the given dataset. Cover data cleaning, type conversion, missing values, outliers, and feature engineering.",
        "category": "data",
        "tags": ["pandas", "python", "data-cleaning"],
    },
    {
        "title": "SQL Analytics Query Builder",
        "content": "You are a senior data analyst. Write advanced SQL queries for the given analytics requirements. Use CTEs, window functions, aggregations. Optimize for performance and readability.",
        "category": "data",
        "tags": ["sql", "analytics", "queries"],
    },
    {
        "title": "Data Quality Framework",
        "content": "You are a data quality engineer. Design a comprehensive data quality framework for the given data assets. Cover completeness, accuracy, consistency, timeliness checks, and automated alerting.",
        "category": "data",
        "tags": ["data-quality", "validation", "monitoring"],
    },
    {
        "title": "Predictive Model Builder",
        "content": "You are a machine learning scientist. Build a predictive model for the given business problem. Cover feature selection, model choice rationale, training pipeline, evaluation metrics, and deployment plan.",
        "category": "data",
        "tags": ["machine-learning", "prediction", "modeling"],
    },
    {
        "title": "Statistical Analysis Guide",
        "content": "You are a statistician. Perform the appropriate statistical analysis for the given dataset and hypothesis. Choose the right test, check assumptions, interpret results, and communicate findings clearly.",
        "category": "data",
        "tags": ["statistics", "hypothesis-testing", "analysis"],
    },
    {
        "title": "Data Warehouse Designer",
        "content": "You are a data warehouse architect. Design a data warehouse schema for the given business. Choose between star/snowflake schema, define fact and dimension tables, and plan for scalability.",
        "category": "data",
        "tags": ["data-warehouse", "schema", "architecture"],
    },
    {
        "title": "NLP Text Classifier",
        "content": "You are an NLP engineer. Build a text classification system for the given dataset. Cover text preprocessing, feature extraction, model selection, training, evaluation, and production deployment.",
        "category": "data",
        "tags": ["nlp", "classification", "machine-learning"],
    },
    {
        "title": "Data Story Teller",
        "content": "You are a data storytelling expert. Transform the given data and insights into a compelling narrative. Structure the story arc, choose the right visualizations, and make insights actionable for non-technical audiences.",
        "category": "data",
        "tags": ["data-storytelling", "visualization", "communication"],
    },
    {
        "title": "Anomaly Detection System",
        "content": "You are a data science engineer. Design an anomaly detection system for the given use case. Cover algorithm selection, threshold setting, real-time vs batch detection, and alerting mechanism.",
        "category": "data",
        "tags": ["anomaly-detection", "monitoring", "machine-learning"],
    },
    {
        "title": "Recommendation Engine Designer",
        "content": "You are an ML engineer specializing in recommendations. Design a recommendation system for the given platform. Compare collaborative filtering, content-based, and hybrid approaches with implementation plan.",
        "category": "data",
        "tags": ["recommendations", "collaborative-filtering", "ml"],
    },
    {
        "title": "Time Series Forecaster",
        "content": "You are a forecasting specialist. Build a time series forecasting model for the given data. Cover seasonality, trend analysis, model selection (ARIMA, Prophet, LSTM), and uncertainty quantification.",
        "category": "data",
        "tags": ["time-series", "forecasting", "prediction"],
    },
    {
        "title": "Feature Engineering Expert",
        "content": "You are a feature engineering specialist. Create powerful features for the given machine learning problem. Cover domain-specific features, interactions, transformations, and feature selection methodology.",
        "category": "data",
        "tags": ["feature-engineering", "ml", "data-science"],
    },
    {
        "title": "Spark Big Data Processor",
        "content": "You are a big data engineer. Write optimized Apache Spark code to process the given large-scale dataset. Cover partitioning, caching, broadcast variables, and performance optimization techniques.",
        "category": "data",
        "tags": ["spark", "big-data", "pyspark"],
    },
    {
        "title": "Data Governance Framework",
        "content": "You are a data governance expert. Design a data governance framework for the given organization. Cover data catalog, lineage, access controls, privacy compliance (GDPR/CCPA), and data ownership.",
        "category": "data",
        "tags": ["data-governance", "privacy", "compliance"],
    },
    {
        "title": "Causal Inference Analyst",
        "content": "You are a causal inference expert. Design a study to estimate the causal effect of the given intervention. Choose between RCT, diff-in-diff, instrumental variables, or regression discontinuity with justification.",
        "category": "data",
        "tags": ["causal-inference", "statistics", "experimentation"],
    },
    {
        "title": "Real-time Streaming Designer",
        "content": "You are a streaming data engineer. Design a real-time data streaming architecture for the given use case. Compare Kafka, Kinesis, Flink approaches. Cover throughput, latency, and fault tolerance.",
        "category": "data",
        "tags": ["streaming", "kafka", "real-time"],
    },
    {
        "title": "Data Monetization Strategist",
        "content": "You are a data strategy consultant. Identify data monetization opportunities for the given company's data assets. Cover internal efficiency gains, new product opportunities, and external data partnerships.",
        "category": "data",
        "tags": ["data-monetization", "strategy", "business-value"],
    },
    {
        "title": "MLOps Platform Designer",
        "content": "You are an MLOps architect. Design an end-to-end MLOps platform for the given organization. Cover model registry, CI/CD for ML, monitoring, feature store, A/B testing, and retraining triggers.",
        "category": "data",
        "tags": ["mlops", "platform", "ml-engineering"],
    },
]

COLLECTIONS_DATA = [
    {
        "name": "Python Developer Toolkit",
        "description": "Essential prompts for Python developers covering debugging, testing, and optimization",
        "categories": ["coding"],
    },
    {
        "name": "Startup Launch Pack",
        "description": "Complete collection for startup founders covering marketing, analysis, and strategy",
        "categories": ["marketing", "analysis"],
    },
    {
        "name": "Data Science Essentials",
        "description": "Core data science prompts from analysis to ML model deployment",
        "categories": ["data", "analysis"],
    },
    {
        "name": "Content Creator Bundle",
        "description": "Everything a content creator needs: blogs, social media, scripts, and newsletters",
        "categories": ["writing", "marketing"],
    },
    {
        "name": "Business Strategy Suite",
        "description": "Strategic business prompts for analysis, planning, and decision making",
        "categories": ["analysis", "marketing"],
    },
]


def seed_database():
    """Main seeding function."""
    print("Starting database seeding...")

    # Create tables
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # ──────────────────────────────────────────
        # Create Admin User
        # ──────────────────────────────────────────
        admin = db.query(User).filter(User.email == "admin@prompthub.com").first()
        if not admin:
            admin = User(
                email="admin@prompthub.com",
                password_hash=hash_password("admin123"),
                is_admin=True,
            )
            db.add(admin)
            db.commit()
            print(" Admin user created: admin@prompthub.com / admin123")

        # ──────────────────────────────────────────
        # Seed Prompts
        # ──────────────────────────────────────────
        existing_count = db.query(Prompt).count()
        if existing_count == 0:
            prompts = []
            for i, data in enumerate(PROMPTS_DATA):
                prompt = Prompt(
                    title=data["title"],
                    content=data["content"],
                    category=data["category"],
                    tags=data["tags"],
                    rating=round(3.5 + (i % 3) * 0.5, 1),  # 3.5, 4.0, 4.5 rotation
                    usage_count=(i + 1) * 7,               # varied usage counts
                )
                prompts.append(prompt)

            db.add_all(prompts)
            db.commit()
            print(f" {len(prompts)} prompts seeded across {len(CATEGORIES)} categories")
        else:
            print(f"  Prompts already exist ({existing_count} found), skipping...")

        # ──────────────────────────────────────────
        # Seed Collections
        # ──────────────────────────────────────────
        existing_collections = db.query(Collection).count()
        if existing_collections == 0:
            all_prompts = db.query(Prompt).all()

            for col_data in COLLECTIONS_DATA:
                collection = Collection(
                    name=col_data["name"],
                    description=col_data["description"],
                )
                db.add(collection)
                db.flush()

                # Link relevant prompts by category
                linked_count = 0
                for prompt in all_prompts:
                    if prompt.category in col_data["categories"] and linked_count < 10:
                        link = CollectionPrompt(
                            collection_id=collection.id,
                            prompt_id=prompt.id,
                        )
                        db.add(link)
                        linked_count += 1

            db.commit()
            print(f"{len(COLLECTIONS_DATA)} collections seeded")
        else:
            print(f" Collections already exist ({existing_collections} found), skipping...")

        print("\n Database seeding completed successfully!")
        print("\n Summary:")
        print(f"   Users:       {db.query(User).count()}")
        print(f"   Prompts:     {db.query(Prompt).count()}")
        print(f"   Collections: {db.query(Collection).count()}")

    except Exception as e:
        db.rollback()
        print(f"Seeding failed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
