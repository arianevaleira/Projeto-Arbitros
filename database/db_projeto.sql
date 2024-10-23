create database db_projeto;
use db_projeto;

create table if not exists tb_usuarios (
usu_id int auto_increment primary key not null,
usu_nome varchar(45) not null,
usu_email varchar(155) not null,
usu_cpf varchar(45) not null,
usu_telefone varchar(45) not null,
usu_senha text not null,
usu_tipo enum("profissional", "comum")
);


create table tb_solicitacoes (
sol_id int auto_increment primary key not null,
sol_data date not null,
sol_inicio time not null,
sol_termino time not null,
sol_local varchar(255),
sol_modalidade varchar(45) not null,
sol_descricao text,
sol_usu_id int not null,
foreign key (sol_usu_id) references tb_usuarios(usu_id)
);

create table tb_comentarios (
com_id int auto_increment primary key not null,
com_conteudo text not null,
com_usu_id int not null,
foreign key (com_usu_id) references tb_usuarios(usu_id)
);
