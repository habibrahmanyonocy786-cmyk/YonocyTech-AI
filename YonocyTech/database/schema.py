from database import get_connection

SCHEMA_VERSION = 1


def migrate():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS schema_version (
            version INTEGER PRIMARY KEY
        )
    """)

    current = cursor.execute("SELECT MAX(version) FROM schema_version").fetchone()[0]
    if current and current >= SCHEMA_VERSION:
        conn.close()
        return

    _create_tables(cursor)
    _seed_defaults(cursor)

    cursor.execute("INSERT INTO schema_version (version) VALUES (?)", (SCHEMA_VERSION,))
    conn.commit()
    conn.close()


def _create_tables(cursor):
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT    NOT NULL,
            email       TEXT    UNIQUE NOT NULL,
            password    TEXT    NOT NULL,
            role        TEXT    DEFAULT 'user',
            plan        TEXT    DEFAULT 'free',
            created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login  TIMESTAMP,
            is_active   INTEGER DEFAULT 1
        );

        CREATE TABLE IF NOT EXISTS sessions (
            id          TEXT    PRIMARY KEY,
            user_id     INTEGER REFERENCES users(id),
            title       TEXT    DEFAULT 'New Session',
            focus       TEXT,
            created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            message_count INTEGER DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS messages (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id  TEXT    REFERENCES sessions(id),
            role        TEXT    NOT NULL,
            content     TEXT    NOT NULL,
            focus       TEXT,
            tokens_used INTEGER DEFAULT 0,
            timestamp   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS providers (
            id            TEXT    PRIMARY KEY,
            name          TEXT    NOT NULL,
            status        TEXT    DEFAULT 'active',
            rate_limit    INTEGER DEFAULT 30,
            priority      INTEGER DEFAULT 1,
            api_key_set   INTEGER DEFAULT 0,
            updated_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS agents (
            id                TEXT    PRIMARY KEY,
            name              TEXT    NOT NULL,
            icon              TEXT    DEFAULT '🤖',
            status            TEXT    DEFAULT 'active',
            default_provider  TEXT    REFERENCES providers(id),
            priority          INTEGER DEFAULT 1,
            updated_at        TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS contact_messages (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT    NOT NULL,
            email       TEXT    NOT NULL,
            subject     TEXT,
            message     TEXT    NOT NULL,
            is_read     INTEGER DEFAULT 0,
            created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS usage_logs (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER REFERENCES users(id),
            provider_id TEXT    REFERENCES providers(id),
            agent_id    TEXT    REFERENCES agents(id),
            tokens_used INTEGER DEFAULT 0,
            latency_ms  REAL    DEFAULT 0,
            success     INTEGER DEFAULT 1,
            timestamp   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS settings (
            key         TEXT    PRIMARY KEY,
            value       TEXT    NOT NULL,
            updated_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE INDEX IF NOT EXISTS idx_sessions_user ON sessions(user_id);
        CREATE INDEX IF NOT EXISTS idx_messages_session ON messages(session_id);
        CREATE INDEX IF NOT EXISTS idx_usage_user ON usage_logs(user_id);
        CREATE INDEX IF NOT EXISTS idx_usage_timestamp ON usage_logs(timestamp);
    """)


def _seed_defaults(cursor):
    cursor.executemany("""
        INSERT OR IGNORE INTO providers (id, name, status, rate_limit, priority, api_key_set)
        VALUES (?, ?, ?, ?, ?, ?)
    """, [
        ("openrouter",    "OpenRouter (Primary)",     "active", 30, 1, 0),
        ("huggingface",   "HuggingFace Inference",    "active", 20, 2, 0),
        ("github-models", "GitHub Models (Azure AI)", "active", 25, 3, 0),
        ("deepai",        "DeepAI Image Generation",  "active", 10, 4, 0),
    ])

    cursor.executemany("""
        INSERT OR IGNORE INTO agents (id, name, icon, status, default_provider, priority)
        VALUES (?, ?, ?, ?, ?, ?)
    """, [
        ("coding",    "Coding Agent",   "💻", "active", "openrouter",    1),
        ("writing",   "Writing Agent",  "✍️", "active", "openrouter",    2),
        ("data",      "Data Agent",     "📊", "active", "huggingface",   3),
        ("design",    "Design Agent",   "🎨", "active", "openrouter",    4),
        ("marketing", "Marketing Agent","📈", "active", "openrouter",    5),
        ("research",  "Research Agent", "🔍", "active", "huggingface",   6),
    ])

    cursor.executemany("""
        INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)
    """, [
        ("site_name", "YonocyTech"),
        ("site_version", "2.0"),
        ("default_rate_limit", "30"),
        ("max_session_messages", "50"),
        ("allow_registration", "1"),
        ("maintenance_mode", "0"),
    ])
