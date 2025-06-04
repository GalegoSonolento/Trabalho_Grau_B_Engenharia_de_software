# Decisões de código
Todas as decisões sobre a aplicação devem ser acompanhadas por uma documentação do porquê a escolha foi feita.

## 001 - Definição de objetivo da API
- Status: Aceita
- Contexto: A proposta do trabalho é fazer uma API de testes e mantê-la simples. Na descrição do trabalho fica bastante claro que o trabaho é um *mock* de tarefas colaborativas.
- Decisão: Vamos seguir as especificações dadas no enunciado e nos manteremos perto desse objetivos
- Consequências: Uma API de tarefas colaborativas é simples o suficiente para implementar rápido mas complexa o suficiente para gerar problemas durante a implementação; principalmente durante a fase de testes e integração com Banco de Dados externo.
- Conformidade: Somos alunos de computação que têm trabalhos de 8 horas diárias, sair do objetivo do trabalho vai ser mais difícil que do que se policiar para se manter.
- Anotações: 
    - Autor: Henrique Haag
    - Data de aprovação: 2025-05-21
    - Aprovado por: Henrique Haag
    - Substituído em: --
    - Última modificação: 2025-05-21
    - Modificado por: Henrique Haag

## 002 - Architetura Monolito Modular
- Status: Aprovado
- Contexto: Arquitetura monolito modular é uma abordagem útil quando se busca manter uma única base de código com divisão clara de responsabilidades internas. É especialmente indicada para sistemas em que a complexidade ainda não justifica microserviços, mas a organização e manutenção do código já se tornaram um desafio.
- Decisão: Optamos por utilizar um monolito modular para manter a simplicidade do deploy e da comunicação entre componentes, enquanto organizamos o sistema em módulos bem definidos e com baixa dependência entre si.
- Consequências: A estrutura modular facilita o entendimento do sistema e o isolamento de funcionalidades, além de permitir testes unitários mais eficazes. No entanto, ainda existe acoplamento físico, já que tudo roda dentro do mesmo processo, e é necessário cuidado para não quebrar os limites entre módulos.
- Conformidade: O grupo deve garantir que cada novo componente seja criado dentro de um módulo existente ou em um novo módulo conforme os padrões definidos. É essencial seguir as convenções de nomes, estrutura de pastas e contratos de interface entre módulos.
- Anotações: Essa arquitetura favorece a modularização e a escalabilidade futura. Pode ser um bom primeiro passo para, no futuro, migrar para uma arquitetura orientada a serviços ou microserviços, caso necessário. Além disso, mantém o sistema mais fácil de depurar e operar por rodar em um único processo.
    - Autor: Henrique Haag
    - Data de aprovação: 15/05/2025
    - Aprovado por: Guilherme Rockenbach
    - Substituído em: --
    - Última modificação: 21/05/205
    - Modificado por: Henrique Haag

## 003 - Requisitos funcionais
A API deve expor os seguintes endpoints:
Usuários
    - POST /users Criar um novo usuário.→
    - GET /users/{id} Obter informações de um usuário específico.→
    - PUT /users/{id} Atualizar informações do usuário.→
    - DELETE /users/{id} Remover um usuário (soft delete recomendado).→
    Tarefas
    - POST /tasks Criar uma nova tarefa.→
    - GET /tasks/{id} Obter detalhes de uma tarefa.→
    - GET /tasks?assignedTo={userId} Listar todas as tarefas atribuídas a um usuário.→
    - PUT /tasks/{id} Atualizar informações da tarefa (título, descrição, status).→
    - DELETE /tasks/{id} Remover uma tarefa.→
    Autenticação
    - POST /auth/login Login de usuários, retornando um token (por exemplo: JWT) para→
    autenticação nas demais requisições.

    Obs: Temos a opção de LogOut, porém ele não é utilizado dentro do nosso projeto, ele existia na concepção inicial do projeto, mas foi eliminada ao longo da execução

- Anotações: anteriormente deveríamos ter um endpoint de *logout* (POST /auth/logout Logout do usuário), mas ela foi descartada depois que definimos o *stateless* como padrão.

    - Autor: Cassia Nino
    - Data de aprovação: 2025-05-07
    - Aprovado por: Cassia Nino
    - Substituído em: --
    - Última modificação: 2025-05-07
    - Modificado por: Cassia Nino

## 004 - Escolha da linguagem de programação
- Status: Aceita
- Contexto: A maioria dos membros do grupo conhecem melhor a linguagem Python e preferem escrever nela.
- Decisão: Vamos usar a linguagem como core da aplicação e utilizar bibliotecas específicas para cada uma das requisições - FastAPI e PyTest.
- Consequências: Por um lado é bastante simples de escrever em Python e a curva de aprendizado é menor. Todavia, é uma linguagem mais lenta e não tem as funções de API como nativas.
- Conformidade: Uma vez que o código começou a ser escrito não voltaremos mais atrás. Todas as pesquisas devem ser feitas com base nessa decisão (ou seja, outras fontes de código precisam seguir essa especificação).
- Anotações:

    - Autor: Henrique Haag
    - Data de aprovação: 2025-05-07
    - Aprovado por: Arthur Wild
    - Substituído em: 2025-05-21
    - Última modificação: 2025-05-21
    - Modificado por: Henrique Haag

## 005: Escolha do Banco de Dados - MongoDB
- Status: Aceito
- Contexto: Desenvolvimento de uma API RESTful para um sistema de gestão de tarefas colaborativas, utilizando FastAPI e Arquitetura Monolitica Modular, conforme especificado no projeto da disciplina.
- Decisão: Optamos por utilizar o MongoDB, um banco de dados NoSQL orientado a documentos, como a solução de armazenamento para a API.
- Consequências: Alinhamento com API RESTful e Formato JSON, benefício: Simplifica a integração com modelos Pydantic do FastAPI, reduzindo o overhead de desenvolvimento; Flexibilidade de Esquema para Desenvolvimento Rápido, Suporte a Relacionamentos Simples, Compatibilidade com Arquitetura Hexagonal, Escalabilidade e Estado Stateless, Integração com FastAPI e Motor, Facilidade de Configuração e Implantação, Suporte a Documentação e Testes, Alternativas Consideradas
- Conformidade: Apesar de ser simples de implementar outro banco, uma vez o Mongo DB implementado ele não vai mais ser alterado (até porque apenas uma pessoa do grupo vai ser responsável por isso).
- Anotações: Escolhido no dia da definição do trabalho mesmo, serviu como ponto de partida.

    - Autor: Henrique Haag
    - Data de aprovação: 2025-05-07
    - Aprovado por: Arthur Wild
    - Substituído em: --
    - Última modificação: 2025-05-21
    - Modificado por: Henrique Haag

## 006: Implementação de testes automatizados com PyTest
- Status: Aceito
- Contexto: Uma vez que o Python será a linguagem utilizada, utilizar a ferramenta de testes mais comun da linguagem é o melhor caminho.
- Decisão: Vamos usar testes unitários com PyTest.
- Consequências: Não é tão potente quanto outras bibliotecas de testes unitários (JUnit, por exemplo), mas é a mais simples de implementar e tem uma usabilidade boa.
- Conformidade: Novamente, será feito por uma pessoa com base das estruturas prontas já no código. Idealmente teremos um teste para cada função e quem escrevê-la precisa montar um teste pra ela.
- Anotações: Os testes precisam cobrir 60% da aplicação.

    - Autor: Henrique Haag
    - Data de aprovação: 2025-05-07
    - Aprovado por: Arthur Wild
    - Substituído em: --
    - Última modificação: 2025-05-21
    - Modificado por: Henrique Haag

## 007: Documentação de chamadas da aplicação
- Status: Aceito
- Contexto: Precisamos montar uma maneira de demonstrar a documentação das chamadas de API para o usuário a fim de que ele saiba quais chamadas de API fazer e como se conectar na nossa aplicação.
- Decisão: Vamos usar Swagger (https://swagger.io/) para documentação de *end user* uma vez que existe familiaridade com a forma de apresentação e escrita.
- Consequências: Não sabemos usar a ferramenta e a curva de aprendizado ainda precisa ser percorrida. Mas não parece tão complexo.
- Conformidade: Isso será a última parte a ser elaborada no projeto e também será montado por apenas uma pessoa. Provavelmente de uma vez só. A documentação estará a cargo dela sobre tutoriais e como montar tudo.
- Anotações: Isso pode mudar no futuro.
    - Autor: Henrique Haag
    - Data de aprovação: --
    - Aprovado por: --
    - Substituído em: --
    - Última modificação: 2025-05-21
    - Modificado por: Henrique Haag

## 008: Implementação do Log
- Status: Aceito
- Contexto: Durante o desenvolvimento do sistema, identificou-se a necessidade de rastrear ações importantes realizadas pelos usuários e pelos próprios serviços internos da aplicação. Isso é fundamental tanto para auditoria quanto para suporte e entendimento do comportamento do sistema.
- Decisão: Foi decidido implementar um sistema de logging que registre as ações relevantes dos usuários (ex: login, alterações de dados, tentativas de acesso negado) e eventos do sistema (ex: erros, chamadas externas, tempo de resposta). Os logs devem ser persistidos em um repositório adequado (arquivo, banco ou ferramenta de observabilidade).
- Consequências: Com os logs implementados, será possível auditar ações, detectar problemas mais rapidamente e melhorar a segurança e rastreabilidade. Por outro lado, é necessário garantir que os logs não exponham dados sensíveis e que o volume gerado seja controlado para evitar impacto no desempenho e nos custos de armazenamento.
    - Autor: Henrique Haag
    - Data de aprovação: 01/06/2025
    - Aprovado por: Guilherme Rockenbach
    - Substituído em: --
    - Última modificação: 01/06/2025
    - Modificado por: Henrique Haag

## 009: Fast API
- Status: Aprovado
- Contexto: Para o desenvolvimento da camada de API do sistema, buscava-se uma tecnologia moderna, leve e com bom suporte para validação automática, documentação integrada e alta performance. A FastAPI se mostrou uma escolha adequada por sua simplicidade e foco em produtividade.
- Decisão: Optou-se por utilizar a FastAPI como framework principal para a construção das rotas HTTP da aplicação. A decisão foi baseada em sua compatibilidade com o padrão async do Python, uso de tipagem estática, suporte ao OpenAPI (Swagger), e facilidade de integração com ORMs e ferramentas externas.
- Consequências: A utilização da FastAPI facilita o desenvolvimento rápido e organizado de endpoints, além de permitir geração automática de documentação e validação de entrada/saída. Contudo, exige atenção especial com operações assíncronas mal implementadas e, por ser relativamente recente, possui menor base de exemplos comparada a frameworks mais antigos como Django ou Flask.
- Conformidade: Todos os endpoints devem ser definidos com tipagem explícita e utilizar os modelos do Pydantic para entrada e saída de dados. As rotas devem seguir a convenção REST sempre que possível. Documentação automática gerada pela FastAPI deve ser validada antes de subir para ambientes de homologação ou produção.
- Anotações: FastAPI combina bem com uma arquitetura modular e separação clara entre camadas (rotas, serviços, repositórios). A utilização de middlewares para autenticação, logging e tratamento de erros é recomendada para manter o código limpo e padronizado.
    - Autor: Henrique Haag
    - Data de aprovação: 10/05/2025
    - Aprovado por: Diogo Fernandes
    - Substituído em: --
    - Última modificação: 01/06/2025
    - Modificado por: Henrique Haag

## 010: Projeto MVC
- Contexto: Durante o desenvolvimento da aplicação, surgiu a necessidade de organizar melhor a estrutura do código para separar responsabilidades e facilitar a manutenção, testes e evolução do sistema. O padrão MVC foi escolhido por ser amplamente conhecido, intuitivo e adequado a sistemas com interface (web, API ou frontend).
- Decisão: Adotamos o padrão Model-View-Controller (MVC) para estruturar o projeto em três camadas bem definidas:
- Model: responsável pela lógica de dados, regras de negócio e comunicação com a base de dados;
- View: responsável pela apresentação das informações (pode ser HTML, JSON, etc.);
- Controller: atua como intermediário, recebendo entradas, processando com a lógica necessária e retornando as respostas apropriadas.
- Consequências: Essa separação de responsabilidades torna o código mais limpo, organizado e testável. Facilita o trabalho em equipe, pois cada desenvolvedor pode atuar em uma parte isolada. Porém, pode aumentar a quantidade de arquivos e exigir atenção para manter os papéis bem definidos (evitando que Controllers fiquem sobrecarregados ou que Models assumam lógicas de apresentação).
- Conformidade: Cada nova funcionalidade deve seguir a separação proposta: lógica de dados no Model, manipulação e roteamento no Controller, e resposta estruturada na View (ou retorno em JSON para APIs). É importante evitar lógica de negócios dentro das Views ou acoplamento direto entre View e Model.
- Anotações: Apesar de tradicional, o padrão MVC continua relevante, especialmente em aplicações que ainda mantêm renderização server-side ou APIs que exigem organização modular. Em APIs modernas, a camada View pode ser representada pela serialização dos dados (ex: Pydantic, DTOs). MVC também pode ser combinado com outras arquiteturas (como DDD ou camadas de serviço) para maior escalabilidade.
    - Autor: Henrique Haag
    - Data de aprovação: 20/05/2025
    - Aprovado por: Guilherme Rockenbach
    - Substituído em: --
    - Última modificação: 01/06/2025
    - Modificado por: Henrique Haag
