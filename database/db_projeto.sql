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
    usu_cep varchar(45),
    usu_cidade varchar(45),
    usu_estado varchar(45),
    usu_latitude DECIMAL(10, 8),
	usu_longitude DECIMAL(11, 8),
    usu_tipo enum('arbitro', 'contratante')
);

create table if not exists tb_arbitros (
    arb_id int auto_increment primary key not null,
    arb_usu_id int not null,
    arb_certificado varchar(255),
    foreign key (arb_usu_id) references tb_usuarios(usu_id)
);

create table if not exists tb_contratantes (
    con_id int auto_increment primary key not null,
    con_usu_id int not null,
    foreign key (con_usu_id) references tb_usuarios(usu_id)
);


create table tb_solicitacoes (
    sol_id int auto_increment primary key not null,
    sol_data date not null,
    sol_inicio time not null,
    sol_termino time not null,
    sol_descricao text,
    sol_status enum ('Pendente', 'Aceita', 'Recusada') default 'Pendente',
    sol_con_id int not null,
    sol_arb_id int not null,
    foreign key (sol_con_id) references tb_contratantes(con_id),
    foreign key (sol_arb_id) references tb_arbitros(arb_id)
);

create table if not exists tb_comentarios (
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


CREATE TABLE tb_partidas (
    par_id INT AUTO_INCREMENT PRIMARY KEY,
    par_sol_id INT,
    par_con_id INT,
    par_arb_id INT,
    status VARCHAR(50),
    FOREIGN KEY (par_sol_id) REFERENCES tb_solicitacoes(sol_id),
    FOREIGN KEY (par_con_id) REFERENCES tb_contratantes(con_id),
    FOREIGN KEY (par_arb_id) REFERENCES tb_arbitros(arb_id)
);



select * from tb_arbitros;
select * from tb_usuarios;
select * from tb_comentarios;
select * from tb_contratantes;
select * from tb_solicitacoes;
select * from tb_notificacoes;
select * from tb_partidas;
SHOW TABLES;
