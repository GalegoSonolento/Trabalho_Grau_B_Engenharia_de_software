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


# Decisões de código
Todas as decisões sobre a aplicação devem ser acompanhadas por uma documentação do porquê a escolha foi feita.

## 001 - Definição de objetivo da API
- Status: Aceita
- Contexto: A proposta do trabalho é fazer uma API de testes e mantê-la simples. Na descrição do trabalho fica bastante claro que o trabaho é um *mock* de tarefas colaborativas.
- Decisão: Vamos seguir as especificações dadas no enunciado e nos manteremos perto desse objetivos
- Consequências: Uma API de tarefas colaborativas é simples o suficiente para implementar rápido mas complexa o suficiente para gerar problemas durante a implementação; principalmente durante a fase de testes e integração com Banco de Dados externo.
- Conformidade: Somos alunos de computação que têm trabalhos de 8 horas diárias, sair do objetivo do trabalho vai ser mais difícil que do que se policiar para se manter.
- Anotações: 
    ● Autor: Henrique Haag
    ● Data de aprovação: 2025-05-21
    ● Aprovado por: Henrique Haag
    ● Substituído em: --
    ● Última modificação: 2025-05-21
    ● Modificado por: Henrique Haag

## 002 - Architetura Hexagonal
- Status: Em aprovação
- Contexto: Arquitetura hexagonal é conhecida como uma ideia interessante para usar em trabalhos com APIs pequenas e com uma certa escalabilidade.
- Decisão: Vamos usar essa idea para isolar o core da aplicação e ainda permitir as chamadas de forma simples.
- Consequências: É fácil de trocar os bancos de dados e é bastante desacoplado, apesar de precisa de uma interface para tudo.
- Conformidade: O grupo precisa ser relembrado dessa aplicação e deve sempre reler este documento antes de montar qualquer mudança dentro do código.
- Anotações: Suporta a necessidade de modularização e testes extensivos (assim como a necessidade de ser *stateless*).

    ● Autor: Henrique Haag
    ● Data de aprovação: 
    ● Aprovado por: 
    ● Substituído em: --
    ● Última modificação: 2025-05-21
    ● Modificado por: Henrique Haag

## 003 - Requisitos funcionais
A API deve expor os seguintes endpoints:
Usuários
    • POST /users Criar um novo usuário.→
    • GET /users/{id} Obter informações de um usuário específico.→
    • PUT /users/{id} Atualizar informações do usuário.→
    • DELETE /users/{id} Remover um usuário (soft delete recomendado).→
    Tarefas
    • POST /tasks Criar uma nova tarefa.→
    • GET /tasks/{id} Obter detalhes de uma tarefa.→
    • GET /tasks?assignedTo={userId} Listar todas as tarefas atribuídas a um usuário.→
    • PUT /tasks/{id} Atualizar informações da tarefa (título, descrição, status).→
    • DELETE /tasks/{id} Remover uma tarefa.→
    Autenticação
    • POST /auth/login Login de usuários, retornando um token (por exemplo: JWT) para→
    autenticação nas demais requisições.

- Anotações: anteriormente deveríamos ter um endpoint de *logout* (POST /auth/logout Logout do usuário), mas ela foi descartada depois que definimos o *stateless* como padrão.

    ● Autor: Cassia Nino
    ● Data de aprovação: 2025-05-07
    ● Aprovado por: Cassia Nino
    ● Substituído em: --
    ● Última modificação: 2025-05-07
    ● Modificado por: Cassia Nino

## 004 - Escolha da linguagem de programação
- Status: Aceita
- Contexto: A maioria dos membros do grupo conhecem melhor a linguagem Python e preferem escrever nela.
- Decisão: Vamos usar a linguagem como core da aplicação e utilizar bibliotecas específicas para cada uma das requisições - FastAPI e PyTest.
- Consequências: Por um lado é bastante simples de escrever em Python e a curva de aprendizado é menor. Todavia, é uma linguagem mais lenta e não tem as funções de API como nativas.
- Conformidade: Uma vez que o código começou a ser escrito não voltaremos mais atrás. Todas as pesquisas devem ser feitas com base nessa decisão (ou seja, outras fontes de código precisam seguir essa especificação).
- Anotações:

    ● Autor: Henrique Haag
    ● Data de aprovação: 2025-05-07
    ● Aprovado por: Arthur Wild
    ● Substituído em: 2025-05-21
    ● Última modificação: 2025-05-21
    ● Modificado por: Henrique Haag

## 005: Escolha do Banco de Dados - MongoDB
- Status: Aceito
- Contexto: Desenvolvimento de uma API RESTful para um sistema de gestão de tarefas colaborativas, utilizando FastAPI e Arquitetura Hexagonal, conforme especificado no projeto da disciplina.
- Decisão: Optamos por utilizar o MongoDB, um banco de dados NoSQL orientado a documentos, como a solução de armazenamento para a API.
- Consequências: Alinhamento com API RESTful e Formato JSON, benefício: Simplifica a integração com modelos Pydantic do FastAPI, reduzindo o overhead de desenvolvimento; Flexibilidade de Esquema para Desenvolvimento Rápido, Suporte a Relacionamentos Simples, Compatibilidade com Arquitetura Hexagonal, Escalabilidade e Estado Stateless, Integração com FastAPI e Motor, Facilidade de Configuração e Implantação, Suporte a Documentação e Testes, Alternativas Consideradas
- Conformidade: Apesar de ser simples de implementar outro banco, uma vez o Mongo DB implementado ele não vai mais ser alterado (até porque apenas uma pessoa do grupo vai ser responsável por isso).
- Anotações: Escolhido no dia da definição do trabalho mesmo, serviu como ponto de partida.

● Autor: Henrique Haag
● Data de aprovação: 2025-05-07
● Aprovado por: Arthur Wild
● Substituído em: --
● Última modificação: 2025-05-21
● Modificado por: Henrique Haag

## 006: Implementação de testes automatizados com PyTest
- Status: Aceito
- Contexto: Uma vez que o Python será a linguagem utilizada, utilizar a ferramenta de testes mais comun da linguagem é o melhor caminho.
- Decisão: Vamos usar testes unitários com PyTest.
- Consequências: Não é tão potente quanto outras bibliotecas de testes unitários (JUnit, por exemplo), mas é a mais simples de implementar e tem uma usabilidade boa.
- Conformidade: Novamente, será feito por uma pessoa com base das estruturas prontas já no código. Idealmente teremos um teste para cada função e quem escrevê-la precisa montar um teste pra ela.
- Anotações: Os testes precisam cobrir 60% da aplicação.

    ● Autor: Henrique Haag
    ● Data de aprovação: 2025-05-07
    ● Aprovado por: Arthur Wild
    ● Substituído em: --
    ● Última modificação: 2025-05-21
    ● Modificado por: Henrique Haag

## 007: Documentação de chamadas da aplicação
- Status: Aceito
- Contexto: Precisamos montar uma maneira de demonstrar a documentação das chamadas de API para o usuário a fim de que ele saiba quais chamadas de API fazer e como se conectar na nossa aplicação.
- Decisão: Vamos usar Swagger (https://swagger.io/) para documentação de *end user* uma vez que existe familiaridade com a forma de apresentação e escrita.
- Consequências: Não sabemos usar a ferramenta e a curva de aprendizado ainda precisa ser percorrida. Mas não parece tão complexo.
- Conformidade: Isso será a última parte a ser elaborada no projeto e também será montado por apenas uma pessoa. Provavelmente de uma vez só. A documentação estará a cargo dela sobre tutoriais e como montar tudo.
- Anotações: Isso pode mudar no futuro.

    ● Autor: Henrique Haag
    ● Data de aprovação: --
    ● Aprovado por: --
    ● Substituído em: --
    ● Última modificação: 2025-05-21
    ● Modificado por: Henrique Haag



Título
Status
Contexto
Decisão
Consequências
Conformidade
Anotações

● Autor
● Data de aprovação
● Aprovado por
● Substituído em
● Última modificação
● Modificado por