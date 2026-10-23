# Cadastro de clientes H2: formulário → planilha → e-mail

**Responsável:** Julia Nascimento
**Prévia do formulário:** https://claude.ai/artifact/2JkVkMqUyknFigQ4UKvyy9 (só visual, não guarda nada)

## Arquivos

| Arquivo | Para quê |
|---|---|
| `formulario-h2.html` | O formulário (visual H2, 3 etapas, validação) |
| `apps-script.gs` | Código que liga o formulário à planilha do Google Sheets |
| `LOGICA-AUTOMACAO.md` | Este documento |

## 1. Visão geral

```
Cliente preenche o formulário
        │
        ▼
Google Sheets (aba "Cadastros")       ← guarda os dados, 1 linha por e-mail
        │  linha nova
        ▼
n8n                                   ← (depois) percebe a linha nova
        │
        ▼
Salesforce Marketing Cloud            ← envia o e-mail pronto para aquela pessoa
        │
        ▼
n8n marca na planilha: "email_enviado"
```

O formulário só precisa do **e-mail** e do **consentimento** para o disparo funcionar. O resto serve para personalizar e segmentar.

## 2. Ligar o formulário à planilha (dá para fazer já, sem n8n)

1. Criar uma planilha no Google Sheets.
2. Extensões > Apps Script. Apagar o que tiver e colar o conteúdo de `apps-script.gs`.
3. Implantar > Nova implantação > tipo **App da Web**. Executar como **Eu**, acesso **Qualquer pessoa**. Autorizar.
4. Copiar a URL que termina em `/exec`.
5. No `formulario-h2.html`, colar essa URL em `const WEBHOOK_URL = "";`.
6. Colocar o formulário num endereço público. A forma mais simples é o próprio Apps Script servir a página (ver item 2.1). Também pode ir para uma CloudPage ou para o site da H2.

O que o script faz:
- Cria a aba "Cadastros" com o cabeçalho, se não existir.
- Grava uma linha por cadastro.
- Se o e-mail já existe, **atualiza** a linha em vez de duplicar, e mantém o `status`. Assim ninguém recebe o e-mail de boas-vindas duas vezes.

### 2.1 Publicar o formulário pelo próprio Apps Script (opcional)

No mesmo projeto do Apps Script: Arquivo > Novo > HTML, nome `formulario`, colar o conteúdo de `formulario-h2.html` e acrescentar ao código:

```js
function doGet() {
  return HtmlService.createHtmlOutputFromFile("formulario")
    .setTitle("Cadastro H2 Club")
    .addMetaTag("viewport", "width=device-width, initial-scale=1");
}
```

Depois de uma nova implantação, a mesma URL `/exec` abre o formulário e também recebe os envios. Esse é o link que vai para os clientes.

## 3. Colunas da planilha

| Coluna | Exemplo | Obrigatório |
|---|---|---|
| `createdAt` | 2026-10-23T18:40:00.000Z | automático |
| `nome` | Julia Nascimento | sim |
| `nascimento` | 1998-04-12 | sim (bloqueia menores de 18) |
| `genero` | Feminino | não |
| `email` | julia@email.com | sim, **chave do contato** |
| `celular` | +5511912345678 | sim |
| `cep` | 05422000 | não |
| `cidade` / `uf` | São Paulo / SP | sim |
| `origem` | Instagram | não |
| `interesses` | Torneios; Cash Game | sim |
| `nivel` | Jogo por diversão | não |
| `optinEmail` | TRUE | sim (LGPD) |
| `aceiteTermos` | TRUE | sim |
| `status` | `novo` → `email_enviado` (ou `erro`) | automático |
| `emailEnviadoEm` | data do envio | preenchido pelo n8n |

## 4. O fluxo no n8n (quando houver acesso)

**Ideia principal:** não existe uma lista que o n8n percorre e filtra. Cada linha nova na planilha é uma pessoa, e o n8n roda uma vez para cada uma. O "e-mail por e-mail" acontece sozinho.

O modelo de e-mail fica no Salesforce. O n8n só diz "manda o e-mail de boas-vindas para fulana@email.com, o nome dela é Fulana", e o Salesforce encaixa os dados no modelo.

| # | Nó do n8n | O que faz |
|---|---|---|
| 1 | **Google Sheets Trigger** (Row Added) | Olha a aba "Cadastros" de tempos em tempos e pega as linhas novas. |
| 2 | **IF** | Segue só se `optinEmail = TRUE` e `status = novo`. |
| 3 | **HTTP Request: token** | `POST https://<subdominio>.auth.marketingcloudapis.com/v2/token` com `grant_type=client_credentials`, `client_id`, `client_secret`. Devolve o `access_token`. |
| 4 | **HTTP Request: enviar** | Manda o e-mail pronto para a pessoa (opções abaixo). |
| 5 | **Google Sheets: Update Row** | Procura a linha pelo `email` e grava `status = email_enviado` e `emailEnviadoEm`. Se o passo 4 falhar, grava `status = erro`. |

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

## 5. Enquanto não há n8n

Com a planilha já recebendo os cadastros:

1. Filtrar a planilha por `optinEmail = TRUE` e `status = novo`.
2. Exportar como CSV e importar numa Data Extension do Marketing Cloud (`email` como Subscriber Key).
3. Enviar o e-mail pronto para essa Data Extension pelo Email Studio.
4. Marcar na planilha `status = email_enviado` nessas linhas.

## 6. Sobre o e-mail de boas-vindas

- Personalizar com o primeiro nome: o n8n pode mandar um atributo `primeiroNome` já separado (`{{ $json.nome.split(" ")[0] }}`), e no e-mail usar `%%primeiroNome%%`.
- Conteúdo por interesse (blocos dinâmicos): quem marcou Torneios vê a agenda, quem marcou Gastronomia vê o cardápio.
- Link de descadastro obrigatório (`%%unsub_center_url%%`).

## 7. Pendências

1. Criar a planilha e instalar o `apps-script.gs`.
2. Link da Política de Privacidade (hoje mostra um aviso no lugar).
3. Montar o e-mail de boas-vindas e a Send Definition ou Journey no Marketing Cloud.
4. Installed Package do Salesforce para o n8n.
5. Logo oficial da H2 em SVG (hoje o topo usa "H2 Club" em texto).
