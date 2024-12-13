from flask import Flask, render_template, redirect, url_for, request, session, flash
from sqlalchemy import select
from sqlalchemy.testing.pickleable import User

from models import Pessoa, db_session, Atividade

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

@app.route('/')
def index():
    return redirect('/pessoas')


@app.route('/pessoas')
def pessoas():
    sql_pessoas = select(Pessoa)
    resultado_pessoas = db_session.execute(sql_pessoas).scalars().all()
    lista_pessoas = []
    for n in resultado_pessoas:
        lista_pessoas.append(n.serialize_pessoa())
        print(lista_pessoas[-1])
    return render_template("lista_pessoas.html",
                           lista_de_pessoas=lista_pessoas)


@app.route('/nova_pessoa', methods=['POST', 'GET'])
def nova_pessoa():
    # quando clicar no botão de salvar
    if request.method == 'POST':

        # se o campo nome não estiver preenchido
        if not request.form['form_nome'] or not request.form['form_sobrenome'] or not request.form['form_CPF']:
            flash("Preencha todos os campos", "error")
        else:
            # coletar os dados digitalizados pelo usuario
            nome = request.form['form_nome']
            sobrenome = request.form['form_sobrenome']
            cpf = request.form['form_CPF']

            # Procurar no banco se ja existe o cpf digitado
            pessoa_cpf = select(Pessoa).where(Pessoa.cpf == cpf)
            pessoa_cpf = db_session.execute(pessoa_cpf).scalars().first()
            print(f"user_cpf: {pessoa_cpf}")

            # verificar se ja existe o cpf
            if not pessoa_cpf:
                # popular a classe usuario com os dados coletados
                pessoa = Pessoa(nome=nome, sobrenome=sobrenome, cpf=cpf)
                print(pessoa)

                # Salvar no banco
                pessoa.save()
                db_session.close()
                flash("Pessoa cadastrada com sucesso!", "success")
                return redirect(url_for('pessoas'))
            else:
                flash(" O cpf ja existe")
    return render_template('nova_pessoa.html')




@app.route('/lista_atividades')
def lista_atividades():
    sql_lista_atividades = select(Atividade)
    resultado_atividades = db_session.execute(sql_lista_atividades).scalars().all()
    lista_atividades = []
    for n in resultado_atividades:
        lista_atividades.append(n.serialize_atividades())
        print(lista_atividades[-1])
    return render_template("lista_atividades.html",
                           lista_de_atividades=lista_atividades)



@app.route('/nova_atividade', methods=['POST', 'GET'] )
def nova_atividade():
    # quando clicar no botão de salvar
    if request.method == 'POST':

        # se o campo nome não estiver preenchido
        if not request.form['form_nome'] or not request.form['form_id_pessoa']:
            flash("Preencha todos os campos", "error")
        else:
            # coletar os dados digitalizados pelo usuario
            nome = request.form['form_nome']
            pessoa_id = request.form['form_id_pessoa']

            # popular a classe usuario com os dados coletados
            atividade = Atividade(nome=nome, pessoa_id=int(pessoa_id))

            # Salvar no banco
            atividade.save()
            db_session.close()
            flash(" Nova atividade cadastrada com sucesso!", "success")
            return redirect(url_for('lista_atividades'))
    return render_template('nova_atividade.html')


app.run(debug=True)
