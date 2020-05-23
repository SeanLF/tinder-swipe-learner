DROP TABLE IF EXISTS users;

CREATE TABLE users (
  id VARCHAR(30) PRIMARY KEY,
  photos BLOB, -- JSON
  age TINYINT,
  bio TEXT,
  class VARCHAR(10),
  match_id VARCHAR(50)
);
