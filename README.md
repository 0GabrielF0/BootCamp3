##Integrantes:
**Adler Murga Ferreira** **RA:22511624**

**Alexandre Henrique Paiva Rocha** **RA:22451424**

**Arthur Gabriel da Silva Barbosa** **RA:22500598**

**Gabriel Francisco Pires de Assis** **RA:22408417**

**Jean de Almeida Brito** **RA:22612228**

**José Rafael de Lucena Martini** **RA:22610479**


# Validador de Placas Brasileiras

## 1. Visão Geral do Projeto

O **Validador de Placas Brasileiras** é um sistema desenvolvido para verificar se uma placa de veículo é válida de acordo com os padrões de identificação veicular utilizados no Brasil.

O projeto contempla os dois principais formatos:

* **Padrão antigo:** `ABC-1234`
* **Padrão Mercosul:** `ABC1D23`

O objetivo é receber uma placa como entrada, realizar sua validação e informar se ela é válida, identificando o padrão correspondente quando aplicável.

O projeto será desenvolvido utilizando **Spec-Driven Development (SDD)**, mantendo as especificações como referência para a implementação e os testes.

---

## 2. Guia de Instalação e Execução

### Pré-requisitos

* Python 3.12 ou superior
* Git
* Docker

### Clonar o repositório

### Criar ambiente virtual

### Ativar o ambiente virtual

### Instalar as dependências

```bash
pip install -r requirements.txt
```

### Executar o projeto

A forma definitiva de execução será definida durante a implementação da aplicação.

---

## 3. ADRs — Registro de Decisões Arquiteturais

### ADR-001 — Python

**Decisão:** Utilizar Python como linguagem principal.

**Motivo:** Possui sintaxe simples, ampla utilização no desenvolvimento de aplicações e facilita a implementação e os testes do modelo de validação.

### ADR-002 — FastAPI

**Decisão:** Utilizar FastAPI para disponibilizar a validação através de uma API.

**Motivo:** Framework leve e adequado para criação de APIs em Python, permitindo organizar a comunicação entre entrada e resultado da validação.

### ADR-003 — pytest

**Decisão:** Utilizar pytest para os testes automatizados.

**Motivo:** Permite criar testes de forma simples e verificar se a implementação segue as regras definidas nas especificações.

### ADR-004 — Docker

**Decisão:** Utilizar Docker para padronização do ambiente.

**Motivo:** Permite que os integrantes da equipe executem o projeto em ambientes semelhantes, reduzindo problemas relacionados às diferenças de configuração.

### ADR-005 — Spec-Driven Development

**Decisão:** Utilizar SDD como abordagem de desenvolvimento.

**Motivo:** As especificações serão definidas antes da implementação, servindo como referência para o desenvolvimento, utilização do agente de IA e criação dos testes.

---

## 4. Tecnologias

* Python
* FastAPI
* pytest
* Docker
* Git
* GitHub

---

## 5. Status do Projeto
 **Em desenvolvimento**

As próximas etapas incluem a criação das especificações, implementação do modelo de validação, integração com a API e desenvolvimento do conjunto de testes automatizados.
