from models import conectar_db

class Notificacao:
        

    # Falta testar, acho que vai dar erro
    # Por enquanto só presta a de listar    
    # @classmethod
    # def nova_notificacao(cls, usu_id, arb_id, acao):
    #     conn = conectar_db()  
    #     cursor = conn.cursor(dictionary=True)
    #     cursor.execute("select usu_nome from tb_usuarios join tb_arbitros on arb_usu_id = usu_id where arb_id = %s", (arb_id,))
    #     nome_arb = cursor.fetchone()
    #     conteudo = f"O árbitro {nome_arb} {acao} sua solicitação"
    #     cursor.execute("INSERT INTO tb_notificacoes(not_usu_id, not_conteudo) VALUES(%s,%s)", (usu_id, conteudo,))
    #     conn.commit()
    #     conn.close()
    #     cursor.close()
    #     return True
    
    @classmethod
    def listar(cls, usu_id):
        conn = conectar_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT not_id as id, not_conteudo as conteudo, not_data as data FROM tb_notificacoes where not_usu_id = %s ", (usu_id,))
        notificacoes = cursor.fetchall()
        cursor.close()
        conn.close()
        return notificacoes
    
    @classmethod
    def delete(cls,id):
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tb_notificacoes WHERE not_id = %s', (id,))
        conn.commit()
        cursor.close()
        conn.close()
