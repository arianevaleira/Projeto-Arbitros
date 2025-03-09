from models import conectar_db

class Contratante():
    def __init__(self, **kwargs):
        self._id = None
        if 'usu_id' in kwargs.keys():
            self._usu_id = kwargs['usu_id']


    def get_id(self):
        return str(self._id)


    @classmethod
    def add_contratante(cls, usu_id):        
        conn = conectar_db()  
        cursor = conn.cursor(dictionary=True)      
        cursor.execute("INSERT INTO tb_contratantes(con_usu_id) VALUE(%s)", (usu_id,))
        conn.commit()
        conn.close()
        cursor.close()
        return True
    
