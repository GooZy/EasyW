drop table if exists images;
create table images (
  id integer primary key autoincrement,
  path text not null,
  create_time date default current_timestamp,
  modify_time date default current_timestamp
);

drop table if exists users;
create table users (
  id integer primary key autoincrement,
  username text not null,
  password text not null,
  create_time date default current_timestamp,
  modify_time date default current_timestamp,
  UNIQUE (username)
);
