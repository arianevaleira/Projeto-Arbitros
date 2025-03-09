#como eu pensei em fazer 
from models import conectar_db

class Comentario:
    def __init__(self, user_id, user_tipo, comentario):
        self.user_id = user_id
        self.user_tipo = user_tipo
        self.comentario = comentario

    def salvar(self):
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tb_comentarios (user_id, user_tipo, comentario) VALUES (%s, %s, %s)",
            (self.user_id, self.user_tipo, self.comentario)
        )
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def listar():
        conn = conectar_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT c.comentario, 
                   a.arb_nome AS nome_arbitro, 
                   con.con_nome AS nome_contratante, 
                   c.user_tipo
            FROM tb_comentarios c
            LEFT JOIN tb_arbitros a ON c.user_id = a.arb_id AND c.user_tipo = 'arbitro'
            LEFT JOIN tb_contratantes con ON c.user_id = con.con_id AND c.user_tipo = 'contratante'
            ORDER BY c.com_id DESC
        """)
        comentarios = cursor.fetchall()
        cursor.close()
        conn.close()
        return comentarios
