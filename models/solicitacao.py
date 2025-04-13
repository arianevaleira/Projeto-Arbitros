from models import conectar_db

class Solicitacao:
    
    @classmethod
    def criar_solicitacao(cls, data, inicio, fim, desc, contr, arb):
        conn = conectar_db()  
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT con_id FROM tb_contratantes WHERE con_usu_id = %s", (contr,))
        con_id = cursor.fetchone()
        cursor.execute("INSERT INTO tb_solicitacoes(sol_data, sol_inicio, sol_termino, sol_descricao, sol_con_id, sol_arb_id) VALUES(%s,%s,%s,%s,%s,%s)", (data, inicio, fim, desc, con_id['con_id'], arb,))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    
    @classmethod
    def listar(cls, id):
        conn = conectar_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''SELECT sol_id, sol_data AS data, sol_inicio AS inicio, sol_termino AS fim, sol_descricao AS descricao, 
                          (SELECT usu_nome FROM tb_usuarios JOIN tb_contratantes ON con_usu_id = usu_id WHERE con_id = sol_con_id) AS contratante, 
                          sol_con_id AS con_id, sol_status AS status 
                          FROM tb_solicitacoes 
                          JOIN tb_arbitros ON arb_id = sol_arb_id 
                          JOIN tb_usuarios ON usu_id = arb_usu_id 
                          WHERE usu_id = %s and sol_status in ('Pendente', 'Recusada')
                          ORDER BY CASE sol_status WHEN 'Pendente' THEN 1 WHEN 'Recusada' THEN 2 END''', (id,))
        solicitacoes = cursor.fetchall()
        cursor.close()
        conn.close()
        return solicitacoes

    @classmethod
    def listar_partidas_contratante(cls, con_id):
        conn = conectar_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT p.par_id, p.status, s.sol_data, s.sol_inicio, s.sol_termino, 
                u.usu_nome AS contratante, ar.usu_nome AS arbitro
            FROM tb_partidas AS p
            JOIN tb_solicitacoes AS s ON p.par_sol_id = s.sol_id
            JOIN tb_contratantes AS c ON s.sol_con_id = c.con_id
            JOIN tb_usuarios AS u ON c.con_usu_id = u.usu_id
            JOIN tb_arbitros AS arb ON s.sol_arb_id = arb.arb_id
            JOIN tb_usuarios AS ar ON arb.arb_usu_id = ar.usu_id
            WHERE u.usu_id = %s
        ''', (con_id,))
        partidas = cursor.fetchall()
        cursor.close()
        conn.close()
        return partidas


    @classmethod
    def listar_partidas_arbitro(cls, arb_id):
        conn = conectar_db()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute('''  
                    SELECT p.par_id, s.sol_data, s.sol_inicio, s.sol_termino, u_arbitro.usu_nome AS arbitro, u_contratante.usu_nome AS contratante FROM tb_partidas AS p 
                    JOIN tb_solicitacoes AS s ON p.par_sol_id = s.sol_id 
                    JOIN tb_arbitros AS arb ON s.sol_arb_id = arb.arb_id 
                    JOIN tb_usuarios AS u_arbitro ON arb.arb_usu_id = u_arbitro.usu_id 
                    JOIN tb_contratantes AS con ON s.sol_con_id = con.con_id 
                    JOIN tb_usuarios AS u_contratante ON con.con_usu_id = u_contratante.usu_id
                    WHERE arb.arb_id IN ( 
                        SELECT arb_id FROM tb_arbitros WHERE arb_usu_id = %s
                    );''', (arb_id,))
        
        partidas = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return partidas

    @classmethod
    def alterar_status(cls, id, status):
        conn = conectar_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("UPDATE tb_solicitacoes SET sol_status = %s WHERE sol_id = %s", (status, id,))
        conn.commit()
        cursor.close()
        conn.close()
        return True

    @classmethod
    def registrar_partida(cls, sol_id, con_id, arb_id):
            conn = conectar_db()
            cursor = conn.cursor(dictionary=True)

            # Verificar se o arbitro ta no banco 
            cursor.execute("SELECT arb_id FROM tb_arbitros WHERE arb_usu_id = %s", (arb_id,))
            if not cursor.fetchone():
                cursor.close()
                conn.close()
                raise ValueError("Árbitro não encontrado.")
            else:
                id_arb = cursor.fetchone()

           #Ver se o contrantante ta tambem
            cursor.execute("SELECT con_id FROM tb_contratantes WHERE con_id = %s", (con_id,))
            if not cursor.fetchone():
                cursor.close()
                conn.close()
                raise ValueError("Contratante não encontrado.")

            # Verificar se a solicitação existe
            cursor.execute("SELECT sol_id FROM tb_solicitacoes WHERE sol_id = %s", (sol_id,))
            if not cursor.fetchone():
                cursor.close()
                conn.close()
                raise ValueError("Solicitação não encontrada.")

            # Tenta inserir a partida 
            cursor.execute('''
                INSERT INTO tb_partidas (par_sol_id, par_con_id, par_arb_id, status)
                VALUES (%s, %s, %s, 'Aceita')
            ''', (sol_id, con_id, id_arb))
            conn.commit()
            cursor.close()
            conn.close()
            return True
