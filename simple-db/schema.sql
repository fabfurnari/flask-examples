drop table if exists entries;
create table entries (
  id integer primary key,
  colore text not null,
  citta text not null
);

insert into 'entries' values(NULL, 'bianco', 'roma');
