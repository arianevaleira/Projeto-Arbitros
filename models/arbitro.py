from models import conectar_db

class Arbitro():
    def __init__(self, **kwargs):
        self._id = None
        if 'usu_id' in kwargs.keys():
            self._usu_id = kwargs['usu_id']


    def get_id(self):
        return str(self._id)


    @classmethod
    def add_arbitro(cls, usu_id):        
        conn = conectar_db()  
        cursor = conn.cursor(dictionary=True)      
        cursor.execute("INSERT INTO tb_arbitros(arb_usu_id) VALUE(%s)", (usu_id,))
        conn.commit()
        conn.close()
        cursor.close()
        return True
    
    @classmethod
    def listar(cls):
        conn = conectar_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT arb_id as id, usu_nome as nome FROM tb_arbitros JOIN tb_usuarios ON usu_id = arb_usu_id")
        arbitros = cursor.fetchall()
        cursor.close()
        conn.close()
        return arbitros

    
