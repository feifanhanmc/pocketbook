drop table if exists users
go
drop table if exists assets
go
drop table if exists transactions
go
drop table if exists transtypes
go
create table if not exists users (
    id              integer         primary key     auto_increment,
    acc_user        varchar(8)      not null,
    pwd_user_md5    varchar(32)     not null,
    nam_user        varchar(50)     default '',
    vlu_email       varchar(25)     default '',
    vlu_phone       varchar(11)     default '',
    vlu_openid      varchar(30)     default '',
    nam_nick        varchar(50)     default '',
    cod_gender      varchar(1)      default '',
    vlu_lang        varchar(20)     default '',
    vlu_city        varchar(20)     default '',
    vlu_prov        varchar(20)     default '',
    vlu_country     varchar(20)     default '',
    url_avatar      varchar(200)    default ''
)
go

create table if not exists assets (
    id              integer         primary key     auto_increment,
    acc_user        varchar(8)      not null,
    acc_asset       varchar(8)      not null,
    nam_asset       varchar(50)     default '',
    rmk_asset       varchar(50)     default '',
    tye_asset       varchar(20)     default '',
    amt_asset       decimal(18,2)   default 0,
    ico_asset       varchar(20)     default 'other',
    boo_active      integer         default 1
)
go

create table if not exists transactions (
    id                  integer         primary key     auto_increment,
    acc_user            varchar(8)      not null,
    acc_asset           varchar(8)      not null,
    nam_asset           varchar(50)     default '',
    amt_trans           decimal(18,2)   default 0,
    tye_flow            varchar(10)     default '',
    dte_trans           varchar(8)      default '',
    tme_trans           varchar(6)      default '',
	acc_asset_related   varchar(8)      default '',
	nam_asset_related   varchar(50)     default '',
	cod_trans_type      varchar(15)     default '',
    txt_trans_type      varchar(30)     default '',
    txt_trans_type_sub  varchar(30)     default '',
	txt_remark          varchar(50)     default '',
	ico_trans           varchar(20)     default 'other'
)
go

create table if not exists transtypes (
    id                   integer         primary key     auto_increment,
    acc_user             varchar(8)      default '',
    cod_trans_type       varchar(15)     not null,
    txt_trans_type       varchar(30)     default '',
    txt_trans_type_sub   varchar(30)     default '',
    tye_flow             varchar(10)     default '',
    boo_active           integer         default 1

)

