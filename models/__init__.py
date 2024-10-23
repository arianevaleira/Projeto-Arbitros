from flask_login import UserMixin
from werkzeug.security import generate_password_hash
import mysql.connector


def conectar_db():
    return mysql.connector.connect(host='localhost', user='root', password='mysqlK.O2806', database='db_projeto')

class User(UserMixin):
    _hash : str
    def __init__(self, **kwargs):
        self._id = None
        if 'nome' in kwargs.keys():
            self._nome = kwargs['nome']
        if 'email' in kwargs.keys():
            self._email = kwargs['email']
        if 'cpf' in kwargs.keys():
            self._cpf = kwargs['cpf']
        if 'telefone' in kwargs.keys():
            self._telefone = kwargs['telefone']
        if 'senha' in kwargs.keys():
            self._senha = kwargs['senha']
        if 'hash' in kwargs.keys():
            self._hash = kwargs['hash']
        if 'tipo' in kwargs.keys():
            self._tipo = kwargs['tipo']


    def get_id(self):
        return str(self._id)

    
    @property
    def _senha(self):
        return self._hash
    
    @_senha.setter
    def _senha(self, senha):
        self._hash = generate_password_hash(senha)

    def add_usuario(self):        
        conn = conectar_db()  
        cursor = conn.cursor(dictionary=True)      
        cursor.execute("INSERT INTO tb_usuarios(usu_nome, usu_email, usu_cpf, usu_telefone, usu_senha, usu_tipo) VALUES(%s,%s,%s,%s,%s,%s)", (self._nome, self._email, self._cpf, self._telefone, self._hash, self._tipo,))
        self._id = cursor.lastrowid
        conn.commit()
        conn.close()
        cursor.close()
        return True
    
    @classmethod
    def get(cls,user_id):
        conn = conectar_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tb_usuarios WHERE usu_id = %s", (user_id,))
        user = cursor.fetchone()
        conn.commit()
        conn.close()
        if user:
            loaduser = User(email=user['usu_email'] , hash=user['usu_senha'])
            loaduser._id = user['usu_id']
            return loaduser
        else:
            return None
    
    @classmethod
    def exists(cls, email):
        conn = conectar_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tb_usuarios WHERE usu_email = %s", (email,))
        user = cursor.fetchall()
        conn.commit()
        conn.close()
        if user:
            return True
        else:
            return False
    
    
    
    @classmethod
    def get_by_email(cls,email):
        conn = conectar_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT usu_id, usu_email, usu_senha FROM tb_usuarios WHERE usu_email = %s", (email,))
        user = cursor.fetchone() 
        conn.commit()
        conn.close()
    
        return user