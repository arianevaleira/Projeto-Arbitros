DROP DATABASE IF EXISTS db_projeto;

create database db_projeto;
use db_projeto;

create table if not exists tb_usuarios (
usu_id int auto_increment primary key not null,
usu_nome varchar(45) not null,
usu_email varchar(155) not null,
usu_cpf varchar(45) not null,
usu_telefone varchar(45) not null, 
usu_senha text not null,
usu_tipo enum ('arbitro', 'contratante')
);


create table if not exists tb_arbitros (
arb_id int auto_increment primary key not null,
arb_usu_id int not null,
foreign key (arb_usu_id) references tb_usuarios (usu_id)
);

create table if not exists tb_contratantes (
con_id int auto_increment primary key not null,
con_usu_id int not null,
foreign key (con_usu_id) references tb_usuarios (usu_id)
);


create table tb_solicitacoes (
sol_id int auto_increment primary key not null,
sol_data date not null,
sol_inicio time not null,
sol_termino time not null,
sol_local varchar(255),
sol_modalidade varchar(45) not null,
sol_descricao text,
sol_con_id int not null,
foreign key (sol_con_id) references tb_contratantes(con_id),
sol_arb_id int not null,
foreign key (sol_arb_id) references tb_arbitros(arb_id)
);

create table tb_comentarios (
com_id int auto_increment primary key not null,
com_conteudo text not null,
com_usu_id int not null,
foreign key (com_usu_id) references tb_usuarios(usu_id)
);

create table tb_notificacoes (
not_id int auto_increment primary key not null,
not_usu_id int not null,
not_conteudo text not null,
not_data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
foreign key (not_usu_id) references tb_usuarios(usu_id)
);
