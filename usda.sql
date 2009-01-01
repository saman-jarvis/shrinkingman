CREATE TABLE food_group (
  id            INTEGER NOT NULL PRIMARY KEY,
  name          VARCHAR(200)
);

CREATE TABLE food (
  id            INTEGER NOT NULL PRIMARY KEY,
  group_id      INTEGER NOT NULL,
  l_descr       VARCHAR(200),
  s_descr       VARCHAR(60),
  common_name   VARCHAR(100),
  manufacturer  VARCHAR(50),
  survey        INTEGER,
  note          VARCHAR(60),
  refuse        INTEGER,
  sci_name      VARCHAR(60),
  nit_to_prot   FLOAT,
  prot_to_cal   FLOAT,
  fat_to_cal    FLOAT,
  carb_to_cal   FLOAT
);
