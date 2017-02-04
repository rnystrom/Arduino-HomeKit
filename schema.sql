DROP TABLE IF EXISTS channels;
CREATE TABLE channels (
  pk INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  created TEXT NOT NULL
);

DROP TABLE IF EXISTS devices;
CREATE TABLE devices (
  pk INTEGER PRIMARY KEY AUTOINCREMENT,
  channel_pk INTEGER,
  username TEXT NOT NULL,
  pinCode TEXT NOT NULL,
  name TEXT NOT NULL,
  pin INTEGER,
  serial_number TEXT NOT NULL,
  model TEXT,
  manufacturer TEXT,
  state INTEGER,
  sequence TEXT NOT NULL,
  created TEXT NOT NULL,
  FOREIGN KEY(channel_pk) REFERENCES channels(pk)
);
