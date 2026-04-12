# api-quick-schedule

Projeto back-end desenvolvido em **Django REST Framework** para otimizar o agendamento entre clientes e prestadores de serviço. A API permite o gerenciamento completo de usuários, serviços, disponibilidade de prestadores e agendamentos.

---

## Sumário

- [Instalação](#instalação)
- [Autenticação](#autenticação)
- [Tipos de Usuário](#tipos-de-usuário)
- [Endpoints](#endpoints)
  - [Auth](#auth)
  - [User](#user)
  - [Service](#service)
  - [Provider Availability](#provider-availability)
  - [Appointments](#appointments)
- [Variáveis de Ambiente (Postman)](#variáveis-de-ambiente-postman)

---

## Instalação

> **Pré-requisito:** Crie o banco de dados antes de rodar as migrações.

```bash
# 1. Criar e ativar o ambiente virtual
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/macOS

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Rodar migrações
python manage.py migrate

# 4. Iniciar o servidor
python manage.py runserver
```

O servidor estará disponível em: `http://127.0.0.1:8000`

---

## Autenticação

A API utiliza autenticação por **Token**. Após o login, inclua o token em todas as requisições autenticadas pelo header:

```
Authorization: Token <seu_token_aqui>
```

As rotas de **registro** e **login** são públicas (não exigem token).

---

## Tipos de Usuário

| Código | Tipo        |
|--------|-------------|
| `C`    | Cliente     |
| `P`    | Prestador   |

---

## Endpoints

### Auth

Base path: `/api/auth/`

---

#### Registrar Usuário

```
POST /api/auth/register/
```

Cria uma nova conta de usuário. Rota pública.

**Body (form-data):**

| Campo       | Tipo   | Obrigatório | Exemplo            |
|-------------|--------|-------------|---------------------|
| first_name  | string | ✅          | `Carlos`            |
| last_name   | string | ✅          | `Ferreira`          |
| email       | string | ✅          | `teste@teste.com`   |
| password    | string | ✅          | `Teste!123`         |
| user_type   | string | ✅          | `C` ou `P`          |

---

#### Login

```
POST /api/auth/login/
```

Autentica o usuário e retorna o token de acesso. Rota pública.

**Body (form-data):**

| Campo    | Tipo   | Obrigatório |
|----------|--------|-------------|
| email    | string | ✅          |
| password | string | ✅          |

---

#### Logout

```
POST /api/auth/logout/
```

Encerra a sessão do usuário autenticado. Requer token.

---

### User

Base path: `/api/user/`

Todas as rotas requerem autenticação via token.

---

#### Listar Usuários

```
GET /api/user/
```

Retorna a lista de todos os usuários.

---

#### Exibir Usuário

```
GET /api/user/{id}/
```

Retorna os dados de um usuário específico.

---

#### Criar Usuário

```
POST /api/user/
```

**Body (form-data):**

| Campo      | Tipo   | Obrigatório | Exemplo           |
|------------|--------|-------------|-------------------|
| first_name | string | ✅          | `Carlos`          |
| last_name  | string | ✅          | `Oliveira`        |
| email      | string | ✅          | `teste1@email.com`|
| password   | string | ✅          | `Teste!123`       |
| user_type  | string | ✅          | `C` ou `P`        |

---

#### Atualizar Usuário

```
PATCH /api/user/{id}/
```

Atualiza parcialmente os dados de um usuário.

**Body (form-data):** Envie apenas os campos que deseja alterar.

| Campo      | Tipo   | Exemplo     |
|------------|--------|-------------|
| first_name | string | `Cadu Teste`|

---

#### Deletar Usuário

```
DELETE /api/user/{id}/
```

Remove o usuário do sistema.

---

### Service

Base path: `/api/service/`

Todas as rotas requerem autenticação via token.

---

#### Listar Serviços

```
GET /api/service/
```

Retorna todos os serviços disponíveis.

---

#### Exibir Serviço

```
GET /api/service/{id}/
```

Retorna os detalhes de um serviço específico.

---

#### Criar Serviço

```
POST /api/service/
```

**Body (form-data):**

| Campo       | Tipo   | Obrigatório | Exemplo                    |
|-------------|--------|-------------|----------------------------|
| name        | string | ✅          | `Veterinário - Check Up`   |
| description | string | ✅          | `Check Up básico de seu pet.` |
| price       | number | ✅          | `70`                       |
| duration    | number | ✅          | `30` (em minutos)          |

---

#### Atualizar Serviço

```
PATCH /api/service/{id}/
```

Atualiza parcialmente um serviço.

**Body (form-data):** Envie apenas os campos que deseja alterar.

| Campo    | Tipo   | Exemplo |
|----------|--------|---------|
| duration | number | `45`    |

---

#### Deletar Serviço

```
DELETE /api/service/{id}/
```

Remove um serviço do sistema.

---

### Provider Availability

Base path: `/api/user/{provider_id}/availability/`

Gerencia os horários de disponibilidade de um prestador de serviço. Requer autenticação via token.

---

#### Exibir Disponibilidade

```
GET /api/user/{provider_id}/availability/
```

Retorna os horários disponíveis cadastrados para o prestador.

---

#### Criar Disponibilidade

```
POST /api/user/{provider_id}/availability/
```

**Body (form-data):**

| Campo          | Tipo   | Obrigatório | Exemplo  | Descrição                              |
|----------------|--------|-------------|----------|----------------------------------------|
| week_day       | number | ✅          | `1`      | Dia da semana (0=Domingo, 1=Segunda…) |
| hour_beginning | string | ✅          | `08:00`  | Horário de início (HH:MM)             |
| hour_ending    | string | ✅          | `18:00`  | Horário de término (HH:MM)            |

---

#### Atualizar Disponibilidade

```
PATCH /api/user/{provider_id}/availability/{id}
```

**Body (form-data):**

| Campo          | Tipo   | Exemplo |
|----------------|--------|---------|
| hour_beginning | string | `07:30` |
| hour_ending    | string | `18:30` |

---

### Appointments

Base path: `/api/appointments/`

Gerencia os agendamentos entre clientes e prestadores. Requer autenticação via token.

---

#### Listar Agendamentos

```
GET /api/appointments
```

Retorna todos os agendamentos do usuário autenticado.

---

#### Exibir Agendamento

```
GET /api/appointments/{id}/
```

Retorna os detalhes de um agendamento específico.

---

#### Criar Agendamento

```
POST /api/appointments/
```

**Body (form-data):**

| Campo          | Tipo     | Obrigatório | Exemplo                  |
|----------------|----------|-------------|--------------------------|
| service        | number   | ✅          | `1`                      |
| hour_beginning | datetime | ✅          | `2026-04-13T17:00:00`    |

---

#### Atualizar Agendamento

```
PATCH /api/appointments/{id}/
```

**Body (form-data):**

| Campo          | Tipo     | Exemplo               |
|----------------|----------|-----------------------|
| hour_beginning | datetime | `2026-04-13T17:00:00` |

---

#### Confirmar Agendamento

```
PATCH /api/appointments/{id}/confirm/
```

Confirma um agendamento pendente. Geralmente usado pelo prestador de serviço.

Sem body obrigatório.

---

#### Cancelar Agendamento

```
DELETE /api/appointments/{id}/
```

Cancela/remove um agendamento.

---

## Variáveis de Ambiente (Postman)

Configure a variável `base_url` na sua collection do Postman:

| Variável   | Valor (exemplo)          |
|------------|--------------------------|
| `base_url` | `http://127.0.0.1:8000`  |

A autenticação é feita via **API Key** no header:

```
Authorization: Token <seu_token>
```
