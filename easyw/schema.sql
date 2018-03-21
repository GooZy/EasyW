drop table if exists images;
create table images (
  id integer primary key autoincrement,
  path text not null
);