from models import conectar_db

class Arbitro:
    def __init__(self, **kwargs):
        self._id = None
        if 'usu_id' in kwargs:
            self._usu_id = kwargs['usu_id']

    def get_id(self):
        return str(self._id)

    @classmethod
    def add_arbitro(cls, usu_id):
        conn = conectar_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("INSERT INTO tb_arbitros (arb_usu_id) VALUES (%s)", (usu_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    
    @classmethod
    def listar(cls):
        conn = conectar_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT arb_id AS id, usu_nome AS nome 
            FROM tb_arbitros 
            JOIN tb_usuarios ON usu_id = arb_usu_id
        """)
        arbitros = cursor.fetchall()
        cursor.close()
        conn.close()
        return arbitros

    @classmethod
    def atualizar_usuario(cls, arb_usu_id, cep, estado, cidade):
        conn = conectar_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            UPDATE tb_usuarios 
            SET usu_cep = %s, usu_estado = %s, usu_cidade = %s
            WHERE usu_id = %s
        """, (cep, estado, cidade, arb_usu_id))
        conn.commit()
        cursor.close()
        conn.close()

    @classmethod
    def atualizar_certificado(cls, arb_usu_id, caminho_certificado):
        conn = conectar_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            UPDATE tb_arbitros 
            SET arb_certificado = %s
            WHERE arb_usu_id = %s
        """, (caminho_certificado, arb_usu_id))
        conn.commit()
        cursor.close()
        conn.close()
