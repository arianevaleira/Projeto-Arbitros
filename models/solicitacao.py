from models import conectar_db

class Solicitacao:
        
    @classmethod
    def criar_solicitacao(cls, data, inicio, fim, desc, contr, arb):
        conn = conectar_db()  
        cursor = conn.cursor(dictionary=True)
        cursor.execute("select con_id from tb_contratantes where con_usu_id = %s", (contr,))
        con_id = cursor.fetchone()
        cursor.execute("INSERT INTO tb_solicitacoes(sol_data, sol_inicio, sol_termino, sol_descricao, sol_con_id, sol_arb_id) VALUES(%s,%s,%s,%s,%s,%s)", (data, inicio, fim, desc, con_id['con_id'], arb,))
        conn.commit()
        conn.close()
        cursor.close()
        return True
    
    @classmethod
    def listar(cls, id):
        conn = conectar_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT sol_data as data, sol_inicio as inicio, sol_termino as fim, sol_descricao as descricao, (select usu_nome from tb_usuarios join tb_contratantes on con_usu_id = usu_id where con_id = sol_con_id)  as contratante, sol_con_id as con_id from tb_solicitacoes join tb_arbitros on arb_id = sol_arb_id join tb_usuarios on usu_id = arb_usu_id where usu_id = %s", (id,))
        solicitacoes = cursor.fetchall()
        cursor.close()
        conn.close()
        return solicitacoes