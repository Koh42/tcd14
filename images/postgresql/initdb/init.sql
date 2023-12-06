create table if not exists users (
    id serial primary key,
    name varchar(255) not null,
    email varchar(255) not null unique,
    password varchar(255) not null,
    created_at timestamp not null default now(),
    updated_at timestamp not null default now()
);

create table if not exists sessions (
    id serial primary key,
    user_id integer not null references users(id),
    token varchar(255) not null unique,
    created_at timestamp not null default now(),
    updated_at timestamp not null default now()
);
