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


select * from tb_arbitros;
select * from tb_usuarios;
select * from tb_comentarios;
select * from tb_contratantes;
select * from tb_solicitacoes;
select * from tb_notificacoes;


DESCRIBE tb_arbitros;  -- ou o nome da tabela que você está usando para árbitros
-- Notificação quando o árbitro aceita a solicitação
INSERT INTO tb_notificacoes (not_usu_id, not_conteudo, not_data)
VALUES (1, 'O árbitro João Silva aceitou sua solicitação.', NOW());

-- Notificação quando o árbitro recusa a solicitação
INSERT INTO tb_notificacoes (not_usu_id, not_conteudo, not_data)
VALUES (2, 'O árbitro João Silva recusou sua solicitação.', NOW());

-- Notificação para árbitro de nova solicitação
INSERT INTO tb_notificacoes (not_usu_id, not_conteudo, not_data)
VALUES (3, 'Você tem uma nova solicitação de Ana Costa.', NOW());

-- Notificação para árbitro quando o status da solicitação muda
INSERT INTO tb_notificacoes (not_usu_id, not_conteudo, not_data)
VALUES (3, 'A solicitação foi atualizada para o status: Aceita.', NOW());

-- Notificação de comentário sobre o usuário
INSERT INTO tb_notificacoes (not_usu_id, not_conteudo, not_data)
VALUES (1, 'Carlos Pereira deixou um comentário sobre você.', NOW());
-- Notificação de solicitação expirada (para contratante)
INSERT INTO tb_notificacoes (not_usu_id, not_conteudo, not_data)
VALUES (1, 'A solicitação que você fez para o árbitro João Silva expirou sem resposta.', NOW());

-- Notificação de atualização de perfil (para o usuário)
INSERT INTO tb_notificacoes (not_usu_id, not_conteudo, not_data)
VALUES (2, 'Seu perfil foi atualizado com sucesso.', NOW());

-- Notificação de novo comentário (para o usuário)
INSERT INTO tb_notificacoes (not_usu_id, not_conteudo, not_data)
VALUES (1, 'Carlos Pereira comentou sobre você: "Ótimo desempenho em campo!"', NOW());

-- Notificação de novo documento (para o árbitro)
INSERT INTO tb_notificacoes (not_usu_id, not_conteudo, not_data)
VALUES (3, 'Você tem um novo certificado ou documento enviado para aprovação.', NOW());

-- Notificação de alteração de status da solicitação (para contratante)
INSERT INTO tb_notificacoes (not_usu_id, not_conteudo, not_data)
VALUES (1, 'O status da sua solicitação foi alterado para Aceita.', NOW());

-- Notificação de recomendação de árbitro (para contratante)
INSERT INTO tb_notificacoes (not_usu_id, not_conteudo, not_data)
VALUES (2, 'João Silva foi recomendado por outro contratante.', NOW());

-- Notificação de confirmação de partida (para árbitro e contratante)
INSERT INTO tb_notificacoes (not_usu_id, not_conteudo, not_data)
VALUES (3, 'Sua partida com Ana Costa foi confirmada para o dia 20/03/2025.', NOW());

-- Notificação de alteração de detalhes da partida (para árbitro e contratante)
INSERT INTO tb_notificacoes (not_usu_id, not_conteudo, not_data)
VALUES (3, 'Os detalhes da sua partida foram alterados. Verifique os novos horários e informações.', NOW());

-- Notificação de novo feedback (para árbitro ou contratante)
INSERT INTO tb_notificacoes (not_usu_id, not_conteudo, not_data)
VALUES (1, 'Carlos Pereira deixou um novo feedback sobre sua partida.', NOW());

-- Notificação de solicitação de remarcação (para árbitro e contratante)
INSERT INTO tb_notificacoes (not_usu_id, not_conteudo, not_data)
VALUES (2, 'Ana Costa solicitou a remarcação da partida para outra data.', NOW());

-- Notificação de novo convite para evento (para árbitro e contratante)
INSERT INTO tb_notificacoes (not_usu_id, not_conteudo, not_data)
VALUES (1, 'Você foi convidado para um novo evento por Carlos Pereira.', NOW());


