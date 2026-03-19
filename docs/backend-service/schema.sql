CREATE TABLE sessions (
  id INTEGER PRIMARY KEY,
  token_hash VARCHAR(128) UNIQUE NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE projects (
  id VARCHAR(64) PRIMARY KEY,
  name VARCHAR(200) NOT NULL,
  state VARCHAR(16) NOT NULL DEFAULT 'IDEA',
  api_key_encrypted TEXT,
  owner_token_hash VARCHAR(128) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_projects_owner ON projects(owner_token_hash);

CREATE TABLE commands (
  id INTEGER PRIMARY KEY,
  project_id VARCHAR(64) NOT NULL REFERENCES projects(id),
  command VARCHAR(32) NOT NULL,
  input_text TEXT NOT NULL,
  output_text TEXT NOT NULL,
  from_state VARCHAR(16) NOT NULL,
  to_state VARCHAR(16) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_commands_project_created ON commands(project_id, created_at DESC);

CREATE TABLE state (
  id INTEGER PRIMARY KEY,
  project_id VARCHAR(64) NOT NULL REFERENCES projects(id),
  command VARCHAR(32) NOT NULL,
  from_state VARCHAR(16) NOT NULL,
  to_state VARCHAR(16) NOT NULL,
  changed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_state_project_changed ON state(project_id, changed_at DESC);
