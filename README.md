# Projeto de Controle de Estoque

Este projeto implementa um sistema de controle de estoque usando a linguagem de programação Python, o framework Flask e o banco de dados SQLite. Ele permite gerenciar categorias de produtos, adicionar produtos ao estoque, listar produtos disponíveis e realizar autenticação de usuários.

## Funcionalidades

- Registro de usuários
- Autenticação de usuários usando tokens JWT
- Renovação do token de acesso
- Listagem de categorias
- Criação de novas categorias
- Adição de produtos ao estoque
- Listagem de produtos disponíveis

## Configuração

1. Clone o repositório do projeto:

```bash
git clone https://github.com/seu-usuario/nome-do-repositorio.git
```

2. Acesse o diretório do projeto:

```bash
cd nome-do-repositorio
```

3. Crie e ative um ambiente virtual:

```bash
python3 -m venv venv
source venv/bin/activate
```

4. Instale as dependências do projeto:

```bash
pip install -r requirements.txt
```

5. Crie o arquivo `.env` na raiz do projeto e defina as seguintes variáveis de ambiente:

```
JWT_SECRET_KEY=seu-segredo
```

6. Execute o arquivo `criar_db.py` para criar o banco de dados SQLite:

```bash
python criar_db.py
```

7. Inicie a aplicação:

```bash
python app.py
```

A aplicação estará disponível em `http://localhost:5000`.

## Uso

### Autenticação

Para realizar a autenticação, envie uma solicitação POST para `/auth` com o seguinte corpo JSON:

```json
{
  "email": "seu-email",
  "password": "sua-senha"
}
```

O endpoint irá retornar um token de acesso que deve ser incluído no cabeçalho das solicitações subsequentes para autenticação.

### Renovação do Token de Acesso

Para renovar o token de acesso, envie uma solicitação POST para `/auth/refresh` com o token de acesso atual incluído no cabeçalho da solicitação:

```
Authorization: Bearer seu-token-de-acesso
```

O endpoint irá retornar um novo token de acesso válido por mais tempo.

### Categorias

- Para listar todas as categorias disponíveis, envie uma solicitação GET para `/categories`.
- Para criar uma nova categoria, envie uma solicitação POST para `/categories` com o seguinte corpo JSON:

```json
{
  "name": "nome-da-categoria"
}
```

### Produtos

- Para adicionar um produto ao estoque, envie uma solicitação POST para `/inventory/add` com o seguinte corpo JSON:

```json
{
  "product_id": "id-do-produto",
  "quantity": "quantidade"
}
```

- Para listar todos os produtos disponíveis, envie uma solicitação GET para `/products`.

### Usuários

- Para registrar um novo usuário, envie uma solicitação POST para `/users` com o seguinte corpo JSON:

```json
{
  "email": "seu-email",
  "password": "sua-senha"
}
```

- Para listar todos os usuários registrados, envie uma solicitação GET para `/users`.

## Contribuição

As contribuições são bem-vindas! Sinta-se à vontade para

 enviar pull requests para melhorar o projeto.

## Licença

Este projeto está licenciado sob a licença [MIT](https://opensource.org/licenses/MIT).

---

Este é apenas um arquivo README de exemplo. Você pode personalizá-lo de acordo com o seu projeto, fornecendo mais informações relevantes sobre o uso, a configuração e as funcionalidades específicas do seu sistema de controle de estoque.