# Validador de Placas Brasileiras

## Integrantes

- **Adler Murga Ferreira** — RA: 22511624
- **Alexandre Henrique Paiva Rocha** — RA: 22451424
- **Arthur Gabriel da Silva Barbosa** — RA: 22500598
- **Gabriel Francisco Pires de Assis** — RA: 22408417
- **Jean de Almeida Brito** — RA: 22612228
- **José Rafael de Lucena Martini** — RA: 22610479

---

## Visão Geral

O **Validador de Placas Brasileiras** é um projeto para verificar se uma placa de veículo está de acordo com os padrões de identificação veicular utilizados no Brasil.

O sistema terá como objetivo validar os dois principais formatos:

- **Padrão antigo:** `ABC-1234`
- **Padrão Mercosul:** `ABC1D23`

A aplicação deverá receber uma placa como entrada, realizar sua normalização e verificar se ela corresponde a um dos padrões definidos.

Quando a placa for válida, o sistema deverá informar o padrão identificado. Caso contrário, deverá informar que a placa é inválida.

---

## Objetivo

Desenvolver uma solução capaz de validar placas brasileiras de forma automática, seguindo regras previamente definidas e documentadas.

O projeto utiliza **Spec-Driven Development (SDD)**, de forma que as especificações sirvam como referência para a implementação e posteriormente para os testes.

---

## Escopo Atual

### Dentro do escopo

- Recebimento de uma placa.
- Normalização da entrada.
- Validação do padrão antigo.
- Validação do padrão Mercosul.
- Identificação do padrão da placa.
- Retorno estruturado do resultado.
- Testes automatizados.
- Execução padronizada utilizando Docker.

### Fora do escopo

- Consulta de proprietário.
- Consulta de RENAVAM.
- Integração com DETRAN.
- Consulta de bancos de dados de veículos.
- Reconhecimento de placas por imagem ou câmera.

---

## Tecnologias

- **Python** 
- **FastAPI** — API da aplicação.
- **pytest** — testes automatizados.
- **Docker** — padronização do ambiente.
- **Git/GitHub** — controle de versão e colaboração.

---

## Organização do Desenvolvimento

O projeto segue uma estrutura baseada em **Spec-Driven Development (SDD)**:

```text
Problema
   ↓
Especificação
   ↓
Arquitetura
   ↓
Implementação
   ↓
Testes
   ↓
Validação e refinamento
```

---

## Controle de Versão

O desenvolvimento utiliza o seguinte fluxo de branches:

```text
main
 ↑
develop
 ↑
feature/*
```

### Branches

- `main` — versão principal e estável do projeto.
- `develop` — branch de integração do desenvolvimento.
- `feature/*` — desenvolvimento de funcionalidades específicas.

---

## Estrutura de Documentação

As especificações do projeto estão sendo organizadas para servir como referência durante o desenvolvimento.

Documentos previstos:

- Problema e objetivo.
- Requisitos funcionais e não funcionais.
- Regras de validação.
- Arquitetura.
- Contratos da API.
- Instruções para o agente de IA.

---

## Status do Projeto

**Em desenvolvimento — etapa de especificação e organização do ambiente.**

Atualmente, a equipe está estruturando:

- Repositório GitHub.
- Branches de desenvolvimento.
- Issues e organização das tarefas.
- Especificações do sistema.
- Arquitetura inicial.
- Documentação do projeto.

**A implementação do código e os testes automatizados serão realizados nas próximas etapas.**

---

## Próximas Etapas

1. Finalizar as especificações.
2. Organizar as tarefas no GitHub Projects.
3. Configurar as regras de proteção das branches.
4. Criar a estrutura do projeto.
5. Configurar o ambiente Docker.
6. Configurar o agente de geração de código.
7. Implementar o validador.
8. Criar o Test Harness.
9. Executar os testes em Docker.
10. Realizar Pull Requests e revisões.
