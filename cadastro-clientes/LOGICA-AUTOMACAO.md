# Fun Festival no seu homegame: formulário → planilha → e-mail

**Responsável:** Julia Nascimento
**Prévia do formulário:** https://claude.ai/artifact/2JkVkMqUyknFigQ4UKvyy9 (só visual, não guarda nada)

## Arquivos

| Arquivo | Para quê |
|---|---|
| `formulario-h2.html` | O formulário (visual H2, 3 etapas, validação). É a fonte: mudanças são feitas aqui |
| `fluxo-n8n.json` | Fluxo pronto para importar no n8n: mostra o formulário e grava os cadastros na planilha |
| `gerar-fluxo-n8n.py` | Gera o `fluxo-n8n.json` de novo depois de mudar o formulário (`python3 gerar-fluxo-n8n.py`) |
| `apps-script.gs` | Alternativa sem n8n: liga o formulário à planilha pelo Google Apps Script |
| `LOGICA-AUTOMACAO.md` | Este documento |

## 1. Visão geral

```
Cliente abre o link do n8n  →  vê o formulário H2
        │  clica em "Concluir cadastro"
        ▼
n8n recebe o cadastro
        │
        ▼
Google Sheets (aba "Cadastros")       ← 1 linha por e-mail (repetido atualiza, não duplica)
        │
        ▼
Salesforce Marketing Cloud            ← (próximo passo) envia o e-mail pronto para aquela pessoa
        │
        ▼
n8n marca na planilha: emailEnviadoEm
```

O formulário só precisa do **e-mail** e do **consentimento** para o disparo funcionar. O resto serve para personalizar e segmentar.

## 2. Colocar o formulário no n8n

O próprio n8n mostra o formulário (não precisa de site nem de Apps Script). O fluxo tem duas partes:

| Nó | O que faz |
|---|---|
| **Abrir formulário** (Webhook GET `/webhook/cadastro-h2`) | É o link que vai para os clientes |
| **Mostrar formulário** (Respond to Webhook) | Devolve a página HTML do formulário |
| **Receber cadastro** (Webhook POST `/webhook/cadastro-h2-enviar`) | O formulário manda os dados para cá ao concluir |
| **Limpar dados** (Code) | Separa os campos e deixa o e-mail em minúsculo |
| **Google Sheets** (Append or Update, chave `email`) | Grava a linha, ou atualiza se o e-mail já existir |

Passo a passo:

1. Criar a planilha no Google Sheets com uma aba **Cadastros** e, na linha 1, as colunas: `createdAt | nome | nascimento | genero | homegame | instagram | representante | email | celular | endereco | cep | cidade | uf | origem | dias | frequencia | buyin | arrecadacao | jogadores | motivo | optinEmail | aceiteTermos | status | emailEnviadoEm`
2. No n8n: criar um fluxo novo > menu **⋯** > **Import from File** > escolher `fluxo-n8n.json`.
3. Abrir o nó **Google Sheets**: escolher (ou criar) a credencial do Google e colar o link da planilha.
4. Salvar e ligar o fluxo (**Active**).
5. Abrir o nó **Abrir formulário** e copiar a **Production URL**. Esse é o link do formulário para os clientes.
6. Testar com o seu e-mail e conferir a linha nova na planilha.

Observações:
- Use a **Production URL** (`/webhook/...`). A Test URL (`/webhook-test/...`) só funciona com o fluxo aberto em modo de teste, e o formulário envia para o endereço de produção.
- Mudou alguma coisa no formulário? Edite `formulario-h2.html`, rode `python3 gerar-fluxo-n8n.py` e importe de novo (ou cole o HTML novo no campo **Response Body** do nó **Mostrar formulário**, trocando `const WEBHOOK_URL = "";` por `const WEBHOOK_URL = "/webhook/cadastro-h2-enviar";`).
- Se a pessoa se cadastrar de novo com o mesmo e-mail, a linha é atualizada e as colunas `status` e `emailEnviadoEm` continuam como estavam.

### 2.1 Alternativa sem n8n: Google Apps Script

Se precisar colocar no ar antes de ter acesso ao n8n:

1. Na planilha: Extensões > Apps Script. Colar o conteúdo de `apps-script.gs`.
2. Arquivo > Novo > HTML, nome `formulario`, colar o conteúdo de `formulario-h2.html` e acrescentar ao código:

```js
function doGet() {
  return HtmlService.createHtmlOutputFromFile("formulario")
    .setTitle("Cadastro H2 Club")
    .addMetaTag("viewport", "width=device-width, initial-scale=1");
}
```

3. Implantar > Nova implantação > **App da Web**. Executar como **Eu**, acesso **Qualquer pessoa**.
4. Colar a URL que termina em `/exec` em `const WEBHOOK_URL = "";` no HTML `formulario` e implantar de novo (Gerenciar implantações > Editar > Nova versão).
5. A URL `/exec` é o link do formulário.

## 3. Colunas da planilha (Fun Festival no seu homegame)

| Coluna | Exemplo | Obrigatório |
|---|---|---|
| `createdAt` | 2026-10-26T18:31:03.591Z | automático |
| `nome` | Julia Nascimento | sim (quem preencheu) |
| `nascimento` | 1995-03-10 | sim (bloqueia menores de 18) |
| `genero` | Feminino | não |
| `homegame` | Poker de Quinta | sim |
| `instagram` | @pokerdequinta | não |
| `representante` | Rafa Lima | sim (quem joga o Main Event) |
| `email` | rafa@email.com | sim, e-mail do representante e **chave do contato** |
| `celular` | +5511912345678 | sim |
| `endereco` | Rua dos Pinheiros, 100 - Pinheiros | sim |
| `cep` | 05422000 | sim |
| `cidade` / `uf` | São Paulo / SP | sim |
| `origem` | Instagram | não |
| `dias` | Quinta; Sábado | sim |
| `frequencia` | 1x por semana | sim |
| `buyin` | 100 (em reais) | sim |
| `arrecadacao` | 1500 (em reais, por noite) | sim |
| `jogadores` | 9 | sim |
| `motivo` | Por que o homegame merece o buy-in | sim |
| `optinEmail` | TRUE | sim (LGPD) |
| `aceiteTermos` | TRUE | sim |
| `status` | `novo` → `email_enviado` (ou `erro`) | preenchido pelo fluxo |
| `emailEnviadoEm` | data do envio | preenchido pelo n8n |

## 4. Próximo passo no n8n: enviar o e-mail pelo Salesforce

**Ideia principal:** não existe uma lista que o n8n percorre e filtra. Cada cadastro enviado faz o fluxo rodar uma vez, só com aquela pessoa. O "e-mail por e-mail" acontece sozinho.

O modelo de e-mail fica no Salesforce. O n8n só diz "manda o e-mail de boas-vindas para fulana@email.com, o nome dela é Fulana", e o Salesforce encaixa os dados no modelo.

| # | Nó do n8n | O que faz |
|---|---|---|
| 1 | **Google Sheets** (o que já existe) | Grava ou atualiza a linha da pessoa. Ligar os nós abaixo logo depois dele. |
| 2 | **Google Sheets: Get Row(s)** + **IF** | Busca a linha pelo `email` (para ver o `emailEnviadoEm` que já estava lá) e segue só se `optinEmail` é verdadeiro e `emailEnviadoEm` está vazio. Quem já recebeu não recebe de novo. |
| 3 | **HTTP Request: token** | `POST https://<subdominio>.auth.marketingcloudapis.com/v2/token` com `grant_type=client_credentials`, `client_id`, `client_secret`. Devolve o `access_token`. |
| 4 | **HTTP Request: enviar** | Manda o e-mail pronto para a pessoa (opções abaixo). |
| 5 | **Google Sheets: Update Row** | Procura a linha pelo `email` e grava `status = email_enviado` e a data em `emailEnviadoEm`. Se o passo 4 falhar, grava `status = erro`. |

### Passo 4, opção 1: e-mail transacional (um e-mail só, na hora)

1. No Marketing Cloud (uma vez só): criar uma **Transactional Send Definition** apontando para o e-mail pronto, com a chave `h2-boas-vindas`.
2. No n8n: `POST https://<subdominio>.rest.marketingcloudapis.com/messaging/v1/email/messages/{{ $json.email }}-{{ $now.toMillis() }}`

```json
{
  "definitionKey": "h2-boas-vindas",
  "recipient": {
    "contactKey": "{{ $json.email }}",
    "to": "{{ $json.email }}",
    "attributes": { "nome": "{{ $json.nome }}", "interesses": "{{ $json.interesses }}" }
  }
}
```

### Passo 4, opção 2: Journey (régua com vários e-mails)

Journey com entrada "API Event" e o e-mail pronto como primeira atividade. No n8n:

`POST https://<subdominio>.rest.marketingcloudapis.com/interaction/v1/events`

```json
{
  "ContactKey": "{{ $json.email }}",
  "EventDefinitionKey": "APIEvent-xxxx",
  "Data": { "email": "{{ $json.email }}", "nome": "{{ $json.nome }}", "interesses": "{{ $json.interesses }}" }
}
```

Dá para colocar um segundo e-mail dias depois dentro da Journey, sem mexer no n8n.

### O que pedir para quem administra o Salesforce

- Um **Installed Package** com componente "API Integration" (Server-to-Server), com permissão de envio de e-mail (Email: Send) e, para a opção 2, de Journeys. Ele gera o `client_id`, o `client_secret` e o subdomínio.
- Essas credenciais ficam só no n8n, nunca no formulário nem na planilha.

## 5. Enquanto o envio pelo Salesforce não está no n8n

Com a planilha já recebendo os cadastros:

1. Filtrar a planilha por `optinEmail = TRUE` e `emailEnviadoEm` vazio.
2. Exportar como CSV e importar numa Data Extension do Marketing Cloud (`email` como Subscriber Key).
3. Enviar o e-mail pronto para essa Data Extension pelo Email Studio.
4. Preencher `emailEnviadoEm` com a data nessas linhas.

## 6. Sobre o e-mail de boas-vindas

- Personalizar com o primeiro nome: o n8n pode mandar um atributo `primeiroNome` já separado (`{{ $json.nome.split(" ")[0] }}`), e no e-mail usar `%%primeiroNome%%`.
- Conteúdo por interesse (blocos dinâmicos): quem marcou Torneios vê a agenda, quem marcou Gastronomia vê o cardápio.
- Link de descadastro obrigatório (`%%unsub_center_url%%`).

## 7. Pendências

1. Criar a planilha e importar o `fluxo-n8n.json` no n8n.
2. Link da Política de Privacidade (hoje mostra um aviso no lugar).
3. Montar o e-mail de boas-vindas e a Send Definition ou Journey no Marketing Cloud.
4. Installed Package do Salesforce para o n8n.
5. Logo oficial da H2 em SVG (hoje o topo usa "H2 Club" em texto).
