create table pair
(
    id             UUID primary key,
    base_currency  text not null,
    quote_currency text not null,
    constraint unique_base_quote_currency unique (base_currency, quote_currency)
);

create index idx_pair_id
    on pair (base_currency);

create table position
(
    id             UUID primary key,
    pair_id        UUID references pair (id),
    type           text      not null,
    entry          float     not null,
    stop_loss      float     not null,
    take_profit    float     not null,
    exit_price     float     not null,
    position_size  float     not null,
    opening_reason text      not null,
    created        timestamp not null default now(),
    updated        timestamp
);

create index idx_position_id on position (id);

create table position_comment
(
    id       UUID primary key,
    trade_id UUID references position (id),
    created  timestamp not null default now(),
    content  text      not null
);

create index idx_position_comment_id on position_comment (id);