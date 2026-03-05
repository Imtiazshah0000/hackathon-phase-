-- 1. Core CRM Schema: Companies, Leads, Interactions

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE companies (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL UNIQUE,
    domain VARCHAR(255) UNIQUE,
    industry VARCHAR(100),
    size_range VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE leads (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_id UUID REFERENCES companies(id),
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(255) UNIQUE NOT NULL,
    job_title VARCHAR(100),
    status VARCHAR(50) DEFAULT 'NEW', -- NEW, RESEARCHING, QUALIFIED, DISQUALIFIED
    source VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE interactions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    lead_id UUID REFERENCES leads(id),
    channel VARCHAR(50), -- SLACK, EMAIL, LINKEDIN
    direction VARCHAR(20), -- INBOUND, OUTBOUND
    content TEXT,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. Enriched Data & Agent Logs (ADR-3)

CREATE TABLE enrichments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    lead_id UUID REFERENCES leads(id),
    source VARCHAR(100), -- TAVILY, LINKEDIN, COMPANY_WEBSITE
    raw_data JSONB, -- The complete JSON response from search tools
    extracted_facts JSONB, -- Simplified facts: { "revenue": "10M+", "headcount": 50 }
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE qualification_results (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    lead_id UUID REFERENCES leads(id),
    score INTEGER CHECK (score >= 0 AND score <= 100),
    reasoning TEXT,
    criteria_met JSONB, -- e.g., { "BANT": { "Budget": "Yes", "Authority": "Director+" } }
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE agent_audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    lead_id UUID REFERENCES leads(id),
    step_name VARCHAR(100), -- INTAKE, RESEARCH, QUALIFICATION, OUTREACH
    model_used VARCHAR(100),
    prompt_tokens INTEGER,
    completion_tokens INTEGER,
    raw_response TEXT,
    details JSONB,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. Relationships & Indexes for Optimization

CREATE INDEX idx_leads_email ON leads(email);
CREATE INDEX idx_leads_company_id ON leads(company_id);
CREATE INDEX idx_interactions_lead_id ON interactions(lead_id);
CREATE INDEX idx_enrichments_lead_id ON enrichments(lead_id);
CREATE INDEX idx_audit_logs_lead_id ON agent_audit_logs(lead_id);

-- 4. Sample Testing Data

INSERT INTO companies (name, domain, industry, size_range) VALUES
('Acme Corp', 'acme.corp', 'Manufacturing', '1000-5000'),
('CyberDyne Systems', 'cyberdyne.io', 'AI & Robotics', '500-1000');

INSERT INTO leads (company_id, first_name, last_name, email, job_title, status) VALUES
((SELECT id FROM companies WHERE name = 'Acme Corp'), 'John', 'Doe', 'j.doe@acme.corp', 'VP of Sales', 'NEW'),
((SELECT id FROM companies WHERE name = 'CyberDyne Systems'), 'Sarah', 'Connor', 's.connor@cyberdyne.io', 'Head of Security', 'NEW');
