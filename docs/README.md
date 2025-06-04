# Trabalho GB Eng de Sofware
## Objetivo
O objetivo deste trabalho é que os alunos projetem, implementem e documentem uma API RESTful
utilizando boas práticas de Arquitetura de Software.
O projeto deve ser realizado em grupos de até 3 pessoas e contemplar aspectos como modularização,
padrões arquiteturais, testes automatizados e documentação adequada.

## Descrição do Trabalho
Os grupos deverão desenvolver uma API para um sistema de gestão de tarefas colaborativas, permitindo
que usuários criem, editem, atribuam e concluam tarefas. A API deve seguir uma arquitetura bem
definida, garantindo boas práticas de desacoplamento e modularização. A escolha por um padrão de
arquitetura fica à cargo do grupo.
Além da implementação, é necessário entregar uma documentação técnica detalhando as decisões
arquiteturais e um conjunto de testes automatizados para garantir a confiabilidade da API.

## Rodando a aplicação
Este projeto roda localmente. Siga os passos abaixo para instalar as dependências, rodar o servidor, acessar a documentação, executar testes e gerar relatórios de cobertura.

### Instale o ambiente virtual (venv)
- No terminal, na raiz do projeto:

No Windows:
```bash
python -m venv .venv
```

No Linux/macOS:
```bash
python3 -m venv .venv
```

### Ative o ambiente virtual
No Linux/macOS:
```bash
source .venv/bin/activate
```

No Windows:
```bash
.venv\Scripts\activate
```

### Instale as dependências do projeto
Com o venv ativado:
```bash
pip install -r requirements.txt
```

### Configure o acesso ao banco
O arquivo ` config_URI.py ` **NÃO está no repositório** (está no .gitignore).
Solicite a URI de conexão diretamente com os responsáveis pelo projeto e crie o arquivo config_URI.py com o seguinte conteúdo:
```bash
MONGO_URI = "sua_uri_aqui"
```

### Rode o servidor
Com o venv ativado, execute:
```bash
uvicorn controller.main:app --reload
```

O servidor estará disponível em http://127.0.0.1:8000

### Acesse a documentação (Swagger/OpenAPI)
Documentação interativa: http://127.0.0.1:8000/docs
Documentação alternativa (ReDoc): http://127.0.0.1:8000/redoc

### Como fazer chamadas à API
Você pode usar ferramentas como **Swagger UI**, **Postman** ou ` curl ` para testar os endpoints.
Exemplo usando ` curl ` para criar um usuário:
```bash
curl -X POST "http://127.0.0.1:8000/users" -H "Content-Type: application/json" -d '{"username": "usuario", "email": "email@exemplo.com", "password": "senha"}'
```

### Rodando os testes automatizados
Com o venv ativado e na raiz do projeto:
```bash
pytest
```

Ou para rodar apenas a pasta de testes:
```bash
pytest testes/
```

### Gerando relatórios de cobertura de testes
Para gerar o arquivo ` .coverage ` na pasta testes:
```bash
COVERAGE_FILE=testes/.coverage pytest --cov=controller --cov=view --cov=model
```

Para ver o relatório no terminal (com linhas faltantes):
```bash
COVERAGE_FILE=testes/.coverage pytest --cov=controller --cov=view --cov=model --cov-report=term-missing
```

Para gerar um relatório em HTML (será criado um diretório ` htmlcov `):
```bash
COVERAGE_FILE=testes/.coverage pytest --cov=controller --cov=view --cov=model --cov-report=html
```

Abra o arquivo ` htmlcov/index.html ` no navegador para visualizar.

Nota sobre o arquivo ` config_URI.py `:
Esse arquivo contém a URI de conexão com o banco de dados MongoDB e está no ` .gitignore ` por segurança.
Solicite a URI diretamente aos responsáveis pelo projeto para conseguir rodar a aplicação.


# Decisões de código
Cheque o arquivo ADR.md em Trabalho_GB_Engenharia_de_software > docs > ADR.md