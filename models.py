# from bibliotecas
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base, relationship

# Configurar banco de dados
# Criando conexão
engine = create_engine('sqlite:///nome.sqlite3')
db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


# Projeto pessoas que tem atividades
class Pessoa(Base):
    __tablename__ = 'pessoa'
    id = Column(Integer, primary_key=True)  #chave primaria (unico) integer = tipo de dado
    nome = Column(String(40), nullable=False, index=True)  #nullable tem que obrigatoriamente preencher o espaço
    sobrenome = Column(String(40), nullable=False, index=True)  # index pesquisa
    cpf = Column(String(11), nullable=False, index=True, unique=True)  # string o tamanho dele

    #colum = coluna

    # representação classe
    def __repr__(self):
        return '<Pessoa: {} {}>'.format(self.nome, self.sobrenome)  #self ele chama ele mesmo

    #função para salvar no banco
    def save(self):
        db_session.add(self)  #sessão de acesso
        db_session.commit()  #salvar a informação

    # função para deletar
    def delete(self):
        db_session.delete(self)  #delete
        db_session.commit()  #salvar

    # é usado para separa as informações
    def serialize_pessoa(self):
        dados_user = {
            "id_user": self.id,
            "nome": self.nome,
            "sobrenome": self.sobrenome,
            "cpf": self.cpf
        }

        return dados_user


class Atividade(Base):
    __tablename__ = 'atividade'
    id = Column(Integer, primary_key=True)
    nome = Column(String(80), nullable=False)
    pessoa_id = Column(Integer, ForeignKey('pessoa.id'), nullable=False)
    pessoa = relationship('Pessoa')

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize_atividades(self):
        dados_atividades = {
            "id_atividades": self.id,
            "nome": self.nome,
            "pessoa_id": self.pessoa_id

        }

        return dados_atividades


# metodo para criar banco
def init_db():
    Base.metadata.create_all(bind=engine)


# metodo de segurança
if __name__ == '__main__':
    init_db()
