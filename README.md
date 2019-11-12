# Valida CEP Gothan City

### Desafio

Desenvolver um validador de CEP que permita apenas valores maiores que 100000 e menores que 999999. O CEP também não pode conter dígitos repetitivos alternados em pares.

O validador de CEP deve ser apresentado em uma página web para cadastro e consulta dos CEPs inseridos. Os CEPs devem conter uma cidade vinculada a eles.

#### Ferramentas utilizadas

O validador de CEP utiliza o *módulo regex* para aceitar números maiores que 100000 e menores que 999999 (definindo o início do campo com números entre 1 e 9 e aceitando mais 5 outros dígitos qualquer) e indices de string para invalidar dígitos iguais alternados em pares.

O desenvolvimento web foi feito utilizando o *módulo flask*. Foi utilizado *Bootstrap* nos templates.

Definida uma classe CEP com atributos **cep**,**cidade**, **step1**, **step2**. A classe possui apenas 1 método para validação do CEP de acordo com a proposta. O método altera os valores booleanos dos atributos **step1** e **step2** para permitir que o registro seja adicionado ao banco de dados.

Foi utilizado o *módulo flask-sqlalchemy* para comunicação com o banco de dados e o *módulo flask-login* para efetuar a autenticação do usuário.

#### Passos para executar o projeto

1. pip install pipenv
2. pipenv install (no diretório onde encontra-se o Pipfile)
3. pipenv shell
4. flask app.py
5. Acessar no navegador localhost:5000
6. Inserir username = admin e password = masterkey
7. Have Fun!