create table Orders (
  id			integer primary key autoincrement not null,
  datetime	timestamp,
  contract_text    text,
  file_address    text,
  format 	text not null references Format(name),
  contract_type    not null references ContractType(name),
  party    text,
  user_email    text,
  check_type    not null references CheckType(name),
  lawyer_id    not null references Lawyer(id),
  done    boolean,
  cost    real,
  time_amount    real,
  deadline    timestamp
);

create table Format (
  name    text primary key,
  needs_recognition    boolean,
  needs_format    boolean
);

create table ContractType (
	name 		text primary key
);

create table CheckType (
	name 		text primary key
);

create table Lawyer (
	id			integer primary key autoincrement not null,
	name 		text,
	email    text
);
