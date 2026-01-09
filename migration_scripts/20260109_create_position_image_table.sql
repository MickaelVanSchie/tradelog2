create table position_image(
    id UUID primary key,
    position_id UUID references position(id),
    type text not null default 'open',
    extension text not null default 'png'
);