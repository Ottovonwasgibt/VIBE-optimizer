PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS sources (
    source_id TEXT PRIMARY KEY,
    uri TEXT NOT NULL,
    title TEXT NOT NULL,
    publisher TEXT,
    version TEXT,
    license TEXT NOT NULL,
    sha256 TEXT NOT NULL,
    retrieved_at TEXT NOT NULL,
    status TEXT NOT NULL CHECK(status IN ('staged', 'approved', 'revoked'))
);

CREATE VIRTUAL TABLE IF NOT EXISTS chunks USING fts5(
    source_id UNINDEXED,
    locator UNINDEXED,
    body,
    tokenize='unicode61'
);

CREATE TABLE IF NOT EXISTS memories (
    memory_id TEXT PRIMARY KEY,
    status TEXT NOT NULL CHECK(status IN ('proposed', 'verified', 'rejected', 'expired')),
    repository TEXT,
    git_commit TEXT,
    problem_signature TEXT NOT NULL,
    lesson TEXT NOT NULL,
    evidence_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);
