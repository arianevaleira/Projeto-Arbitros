from models import conectar_db
from datetime import date

class Partida:

    @classmethod
    def registrar_partida(cls, sol_id, con_id, arb_id):
            conn = conectar_db()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT arb_id FROM tb_arbitros WHERE arb_id = %s", (arb_id,))
            if not cursor.fetchone():
                cursor.close()
                conn.close()
                raise ValueError("Árbitro não encontrado.")

            cursor.execute("SELECT con_id FROM tb_contratantes WHERE con_id = %s", (con_id,))
            if not cursor.fetchone():
                cursor.close()
                conn.close()
                raise ValueError("Contratante não encontrado.")

            cursor.execute("SELECT sol_id FROM tb_solicitacoes WHERE sol_id = %s", (sol_id,))
            if not cursor.fetchone():
                cursor.close()
                conn.close()
                raise ValueError("Solicitação não encontrada.")

            cursor.execute('''
                INSERT INTO tb_partidas (par_sol_id, par_con_id, par_arb_id, status)
                VALUES (%s, %s, %s, 'Agendada')
            ''', (sol_id, con_id, arb_id,))
            conn.commit()
            cursor.close()
            conn.close()
            return True


    @classmethod
    def listar_partidas_contratante(cls, con_id):
        conn = conectar_db()
        cursor = conn.cursor(dictionary=True)

        cursor.execute('''
            SELECT p.par_id, p.status, s.sol_data,s.sol_descricao ,s.sol_inicio, s.sol_termino, 
                u.usu_nome AS contratante, ar.usu_nome AS arbitro, p.par_arb_id
            FROM tb_partidas AS p
            JOIN tb_solicitacoes AS s ON p.par_sol_id = s.sol_id
            JOIN tb_contratantes AS c ON s.sol_con_id = c.con_id
            JOIN tb_usuarios AS u ON c.con_usu_id = u.usu_id
            JOIN tb_arbitros AS arb ON s.sol_arb_id = arb.arb_id
            JOIN tb_usuarios AS ar ON arb.arb_usu_id = ar.usu_id
            WHERE u.usu_id = %s ORDER BY CASE status WHEN 'Agendada' THEN 1 WHEN 'Realizada' THEN 2 WHEN 'Cancelada' THEN 3 END
        ''', (con_id,))
        
        partidas = cursor.fetchall()
        
        data_atual = date.today()

        for partida in partidas:
            if partida['sol_data'] < data_atual:
                cursor.execute("""
                    UPDATE tb_partidas
                    SET status = 'Realizada'
                    WHERE par_id = %s
                """, (partida['par_id'],))
        
        conn.commit()
        cursor.close()
        conn.close()

        return partidas

    @classmethod
    def listar_partidas_arbitro(cls, arb_id):
        conn = conectar_db()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute('''  
                    SELECT p.par_id, s.sol_data, s.sol_inicio, s.sol_termino,s.sol_descricao, u_arbitro.usu_nome AS arbitro, u_contratante.usu_nome AS contratante, p.status, p.par_arb_id, p.par_con_id FROM tb_partidas AS p 
                    JOIN tb_solicitacoes AS s ON p.par_sol_id = s.sol_id 
                    JOIN tb_arbitros AS arb ON s.sol_arb_id = arb.arb_id 
                    JOIN tb_usuarios AS u_arbitro ON arb.arb_usu_id = u_arbitro.usu_id 
                    JOIN tb_contratantes AS con ON s.sol_con_id = con.con_id 
                    JOIN tb_usuarios AS u_contratante ON con.con_usu_id = u_contratante.usu_id
                    WHERE arb.arb_id IN ( 
                        SELECT arb_id FROM tb_arbitros WHERE arb_usu_id = %s
                    ) ORDER BY CASE status WHEN 'Agendada' THEN 1 WHEN 'Realizada' THEN 2 WHEN 'Cancelada' THEN 3 END;''', (arb_id,))
        
        partidas = cursor.fetchall()
        
        data_atual = date.today()
        
        for partida in partidas:
            if partida['sol_data'] < data_atual:
                cursor.execute("""
                    UPDATE tb_partidas
                    SET status = 'Realizada'
                    WHERE par_id = %s
                """, (partida['par_id'],))
        
        conn.commit()
        cursor.close()
        conn.close()

        return partidas
    

    @classmethod
    def cancelar_partida(cls,id):
        conn = conectar_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("UPDATE tb_partidas SET status = 'Cancelada' WHERE par_id = %s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return True
