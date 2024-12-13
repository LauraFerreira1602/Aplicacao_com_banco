from models import Pessoa, db_session
from sqlalchemy import select


# inserir dados na tabela
def inserir_pessoa():
    pessoa = Pessoa(nome=str(input('Nome: ')),
                    sobrenome=str(input('Sobrenome: ')),
                    cpf=str(input('CPF: ')),
                    )

    print(pessoa)
    pessoa.save()


def consultar_pessoa():
    var_pessoa = select(Pessoa)
    var_pessoa = db_session.execute(var_pessoa).all()
    print(var_pessoa)


def atualizar_pessoa():
    var_pessoa = select(Pessoa).where(Pessoa.nome == str(input('Nome: ')), )
    var_pessoa = db_session.execute(var_pessoa).scalar()
    print(var_pessoa)
    var_pessoa.nome = str(input('Nome: '))
    var_pessoa.save()


# remover pessoa
def deletar_pessoa():
    pessoa = Pessoa.query.filter_by(nome=str(input('Nome: '))).first()
    print(pessoa)
    pessoa.delete()


if __name__ == '__main__':
    while True:
        print('Menu')
        print('1 - inserir pessoa')
        print('2 - consultar pessoa')
        print('3 - atualizar pessoa')
        print('4 - deletar pessoa')
        print('5 - sair')

        escolha = input('Escolha: ')

        if escolha == '1':
            inserir_pessoa()

        elif escolha == '2':
            consultar_pessoa()

        elif escolha == '3':
            atualizar_pessoa()

        elif escolha == '4':
            deletar_pessoa()

        elif escolha == '5':
            break
