DROP TABLE results;
CREATE TABLE results (
  id SERIAL,
  driver_id INTEGER,
  race_id INTEGER,
  team_id INTEGER,
  year INTEGER,
  round INTEGER,
  position INTEGER,
  points INTEGER,
  PRIMARY KEY(id),
  FOREIGN KEY(driver_id) REFERENCES drivers (id),
  FOREIGN KEY(race_id) REFERENCES races (id),
  FOREIGN KEY(team_id) REFERENCES teams (id)
)
