# Mesa Certa

O Mesa Certa é um sistema web simples para gerenciamento de comandas de restaurante.  
A aplicação permite cadastrar pedidos, visualizar as comandas registradas em uma tabela e calcular automaticamente o valor total de cada item.

## Funcionalidades

- Cadastro de comandas
- Listagem das comandas em tabela
- Cálculo automático do valor total
- Edição de comandas cadastradas
- Exclusão de comandas
- Validação de campos obrigatórios
- Exibição de mensagens de sucesso e erro

## Tecnologias utilizadas

- Python
- Flask
- HTML
- CSS
- JavaScript
- Selenium
- unittest

## Estrutura do projeto

```text
MesaCerta/
├── app.py
├── test_sistema.py
├── README.md
├── static/
│   ├── css/
│   │   └── style.css
│   ├── img/
│   │   └── logo.png
│   └── js/
│       └── script.js
└── templates/
    ├── layout.html
    ├── index.html
    └── comandas.html
```

## Como instalar as dependências

Na pasta do projeto, execute:

```bash
python -m pip install flask selenium
```

## Como executar o projeto

Na pasta do projeto, execute:

```bash
python app.py
```

Depois, acesse no navegador:

```text
http://127.0.0.1:5000
```

Para encerrar o servidor, pressione `CTRL + C` no terminal.

## Como executar os testes

Com o servidor Flask rodando, abra outro terminal na pasta do projeto e execute:

```bash
python -m unittest test_sistema.py
```

Se todos os testes passarem, será exibido um resultado semelhante a:

```text
......
----------------------------------------------------------------------
Ran 6 tests in X.XXXs

OK
```

## Testes automatizados

O projeto possui testes automatizados com Selenium e unittest, cobrindo os seguintes cenários:

- Cadastro de comanda com sucesso
- Validação de quantidade inválida
- Navegação entre páginas
- Tentativa de cadastro com campo obrigatório vazio
- Verificação da mensagem de sucesso
- Verificação da quantidade e ordem dos itens na tabela

## Observações

Para executar os testes, é necessário ter o Google Chrome instalado. O Selenium será responsável por abrir o navegador durante a execução dos testes.