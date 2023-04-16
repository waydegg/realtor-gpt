-- @@

create extension if not exists moddatetime;


-- @@

create table listings (
    id uuid primary key default gen_random_uuid(),
    platform varchar not null,
    platform_url varchar not null,
    latitude float not null,
    longitude float not null,
    price float not null,
    area float,
    beds float,
    baths float,
    description varchar,
    address_line_1 varchar not null,
    postal_code varchar not null,
    city varchar not null,
    state varchar not null,
    listing_images varchar[] not null,
    address_images varchar[] not null
);



