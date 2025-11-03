-- Create table ShortLink
CREATE TABLE IF NOT EXISTS ShortLink (
    id SERIAL PRIMARY KEY,
    original_url TEXT NOT NULL,
    short_code VARCHAR(12) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Index on original_url for faster lookups
CREATE INDEX IF NOT EXISTS idx_shortlink_original_url ON ShortLink (original_url);

-- Create table ClickEvent
CREATE TABLE IF NOT EXISTS ClickEvent (
    id SERIAL PRIMARY KEY,
    link_id INTEGER NOT NULL REFERENCES ShortLink(id) ON DELETE CASCADE,
    timestamp TIMESTAMP DEFAULT NOW(),
    user_agent TEXT,
    ip_address INET
);

-- Index for faster time-based queries
CREATE INDEX IF NOT EXISTS idx_clickevent_timestamp ON ClickEvent (timestamp);
