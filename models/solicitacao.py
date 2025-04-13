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
                          sol_con_id AS con_id, sol_status AS status, sol_arb_id as arb_id
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
    def alterar_status(cls, id, status):
        conn = conectar_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("UPDATE tb_solicitacoes SET sol_status = %s WHERE sol_id = %s", (status, id,))
        conn.commit()
        cursor.close()
        conn.close()
        return True
