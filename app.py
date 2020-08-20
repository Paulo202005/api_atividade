from flask import Flask, request
from flask_restful import Resource, Api
from models import Pessoas, Atividades

app = Flask(__name__)
api = Api(app)

class Pessoa(Resource):
    def get(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()
        try:
            response = {
                'id': pessoa.id,
                'nome': pessoa.nome,
                'idade': pessoa.idade
            }
        except AttributeError:
            response = {
                'status': 'error',
                'mensagem': 'Pessoa nao encontrada'
            }
        return response

    def put(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()
        dados = request.json
        if 'nome' in dados:
            pessoa.nome = dados['nome']
        if 'idade' in dados:
            pessoa.idade = dados['idade']
        pessoa.save()
        response = {
            'id': pessoa.id,
            'nome': pessoa.nome,
            'idade': pessoa.idade
        }
        return response

    def delete(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()
        pessoa.delete()
        mensagem = 'Pessoa {} excluida com sucesso'.format(pessoa.nome)
        return {'status': 'sucesso', 'mensagem': mensagem}

class ListaPessoas(Resource):
    def get(self):
        pessoas = Pessoas.query.all()
        response = [{'id': i.id,
                     'nome': i.nome,
                     'idade': i.idade} for i in pessoas]
        return response

    def post(self):
        dados = request.json
        pessoa = Pessoas(nome=dados['nome'], idade=dados['idade'])
        pessoa.save()
        response = {
            'id': pessoa.id,
            'nome': pessoa.nome,
            'idade': pessoa.idade
        }
        return response

class Atividade(Resource):
    def get(self, id):
        atividade = Atividades.query.filter_by(id=id).first()
        try:
            pessoa = Pessoas.query.filter_by(id=atividade.pessoa_id).first()
            response = {
                'id': atividade.id,
                'pessoa': pessoa.nome,
                'nome': atividade.nome
            }
        except AttributeError:
            response = {
                'status': 'error',
                'mensagem': 'Atividade nao encontrada'
            }
        return response

    def put(self, id):
        atividade = Atividades.query.filter_by(id=id).first()
        dados = request.json
        pessoa = Pessoas.query.filter_by(id=dados['pessoa_id']).first()
        if pessoa != None:
            if 'pessoa_id' in dados:
                atividade.pessoa_id = dados['pessoa_id']
            if 'nome' in dados:
                atividade.nome = dados['nome']
            pessoa.save()
            response = {
                'id': atividade.id,
                'pessoa': pessoa.nome,
                'nome': atividade.nome
            }
        else:
            response = {
                'status': 'error',
                'mensagem': 'Pessoa_id ({}) nao encontrada'.format(dados['pessoa_id'])
            }
        return response

    def delete(self, id):
        atividade = Atividades.query.filter_by(id=id).first()
        atividade.delete()
        mensagem = 'Atividade ({}) excluida com sucesso'.format(atividade.nome)
        return {'status': 'sucesso', 'mensagem': mensagem}

class ListaAtividades(Resource):
    def get(self):
        atividades = Atividades.query.all()
        response = [{'id': i.id,
                     'nome': i.nome,
                     'pessoa': i.pessoa.nome} for i in atividades]
        return response

    def post(self):
        dados = request.json
        pessoa = Pessoas.query.filter_by(nome=dados['pessoa']).first()
        if pessoa != None:
            atividade = Atividades(nome=dados['nome'], pessoa=pessoa)
            atividade.save()
            response = {
                'id': atividade.id,
                'pessoa': atividade.pessoa.nome,
                'nome': atividade.nome
            }
        else:
            response = {
                'status': 'error',
                'mensagem': 'Pessoa ({}) nao encontrada'.format(dados['pessoa'])
            }
        return response

api.add_resource(Pessoa, '/pessoa/<string:nome>/')
api.add_resource(ListaPessoas, '/pessoa/')
api.add_resource(Atividade, '/atividades/<int:id>/')
api.add_resource(ListaAtividades, '/atividades/')

if __name__ == '__main__':
    app.run(debug=True)