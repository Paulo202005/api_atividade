from models import Pessoas

# Inclui dados na tabela pessoa
def insere_pessoa():
    pessoa = Pessoas(nome='Sergio', idade=40)
    print(pessoa)
    pessoa.save()

# Altera dados na tabela pessoa
def altera_pessoa():
    pessoa = Pessoas.query.filter_by(nome='Sergio').first()
    pessoa.idade = 39
    pessoa.save()

# Exclui dados na tabela pessoa
def exclui_pessoa():
    pessoa = Pessoas.query.filter_by(nome='Sergio').first()
    pessoa.delete()

# Consulta dados na tabela pessoa
def consulta_pessoa():
    pessoa = Pessoas.query.all()
    #pessoa = Pessoas.query.filter_by(nome='Sergio').first()
    #print(pessoa.nome, pessoa.idade)
    print(pessoa)

if __name__ == '__main__':
    insere_pessoa()
    #altera_pessoa()
    #exclui_pessoa()
    consulta_pessoa()
