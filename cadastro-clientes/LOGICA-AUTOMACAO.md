# Cadastro de clientes H2: formulário → dados → e-mail

**Responsável:** Julia Nascimento
**Protótipo publicado:** https://claude.ai/artifact/2JkVkMqUyknFigQ4UKvyy9
**Arquivo:** `cadastro-clientes/formulario-h2.html`

## 1. Onde estamos

| Parte | Situação |
|---|---|
| Formulário (visual H2, 3 etapas, validação) | Pronto |
| Guardar os cadastros | Funciona no protótipo, só para quem é da organização H2 no Claude |
| E-mail de boas-vindas no Salesforce | A fazer pela Julia |
| Automação (n8n ou Salesforce) | Depois, quando houver acesso |

**Limite do protótipo:** a página no Claude só grava cadastros de quem está logado na organização H2. Cliente de fora consegue abrir a página, mas não consegue enviar. Ela serve para o time testar campos, texto e fluxo. Para o link que vai para o cliente, o formulário precisa morar num lugar público (opções abaixo).

## 2. Campos que o formulário envia

O nome de cada campo já está pronto para virar coluna na Data Extension do Salesforce Marketing Cloud.

| Campo | Tipo | Obrigatório | Observação |
|---|---|---|---|
| `email` | texto (e-mail, minúsculo) | sim | **Chave do contato** (Subscriber Key / Contact Key) |
| `nome` | texto | sim | Nome e sobrenome |
| `apelido` | texto | não | "Como quer ser chamado na mesa", bom para personalizar o e-mail |
| `cpf` | texto, 11 dígitos | sim | Validado pelos dígitos verificadores |
| `nascimento` | data AAAA-MM-DD | sim | Bloqueia menores de 18 |
| `genero` | texto | não | |
| `celular` | texto, +55DDDNÚMERO | sim | Formato pronto para WhatsApp/SMS |
| `cep`, `cidade`, `uf` | texto | cidade e UF sim | |
| `origem` | texto | não | Como conheceu a H2 |
| `interesses` | lista | sim | Torneios, Cash Game, Home Game, Gastronomia (A&B) |
| `nivel` | texto | não | Relação com o poker |
| `optinEmail` | booleano | sim | Consentimento para receber e-mails (LGPD) |
| `aceiteTermos` | booleano | sim | Política de Privacidade e 18+ |
| `createdAt` | data/hora ISO | automático | |
| `status` | texto | automático | `novo` → `enviado_sfmc` → `email_enviado` |
| `emailBoasVindas` | booleano | automático | Marca se o e-mail já saiu |

## 3. Caminhos para disparar o e-mail

### Caminho A: tudo dentro do Salesforce Marketing Cloud (recomendado)

Não depende do n8n e é o mais simples de manter.

1. Criar a Data Extension `H2_Cadastro_Clientes` com as colunas da tabela acima. `email` como chave primária, marcada como "Sendable", relacionada ao Subscriber Key.
2. Criar uma **CloudPage** e colar o formulário nela. No envio, um bloco AMPscript faz `UpsertData` na DE (o mesmo e-mail atualiza em vez de duplicar).
3. Criar uma **Journey** no Journey Builder com a DE como entrada ("Data Extension Entry", avaliando novos registros) e o e-mail de boas-vindas como primeira atividade.
4. Filtro de entrada: `optinEmail = true`.
5. O link da CloudPage é o link que vai para os clientes.

Resultado: a pessoa preenche, cai na DE e a Journey manda o e-mail sozinha.

### Caminho B: com o n8n no meio

Útil se o cadastro também precisar ir para outro lugar (planilha, CRM do clube, WhatsApp).

```
Formulário (LP/CloudPage)
   │  POST JSON
   ▼
n8n ─ Webhook (recebe o cadastro)
   ├─ Validar / limpar (e-mail minúsculo, sem duplicado)
   ├─ Gravar cópia (Google Sheets ou banco)
   ├─ Salesforce: pedir token  →  POST https://<subdominio>.auth.marketingcloudapis.com/v2/token
   ├─ Salesforce: gravar na DE →  POST /data/v1/async/dataextensions/key:H2_Cadastro_Clientes/rows
   └─ Salesforce: entrar na Journey → POST /interaction/v1/events
                                      { ContactKey: email, EventDefinitionKey: "...", Data: {...} }
```

- No formulário, basta preencher a constante `WEBHOOK_URL` com o endereço do webhook do n8n.
- O e-mail continua sendo montado e enviado pelo Salesforce. O n8n só leva os dados até lá.
- Credenciais do Salesforce (Client ID e Secret de um "Installed Package" com permissão em Data Extensions e Journeys) ficam só no n8n, nunca no formulário.

### Enquanto não há automação (hoje)

1. O time preenche cadastros de teste no protótipo.
2. No painel "Cadastros recebidos" (só aparece para quem edita a página), clicar em **Baixar CSV** ou **Copiar CSV**.
3. Importar o CSV na Data Extension pelo Contact Builder ou Email Studio, mapeando `email` para Subscriber Key.
4. Enviar o e-mail para a DE pelo Email Studio (envio único) ou pela Journey.

## 4. Sobre o e-mail de boas-vindas

- Usar `%%apelido%%` quando tiver, senão o primeiro nome: `IIF(Empty(apelido), nome, apelido)`.
- Conteúdo pode variar pelos `interesses` (blocos dinâmicos no Content Builder): quem marcou Torneios vê a agenda, quem marcou A&B vê o cardápio.
- Link de descadastro obrigatório (`%%unsub_center_url%%`).
- Remetente e domínio autenticados (SPF/DKIM) para não cair em spam.

## 5. LGPD: pontos para validar com o jurídico

- O texto do consentimento está no formulário; confirmar redação.
- Falta o **link da Política de Privacidade** (hoje mostra um aviso no lugar).
- CPF está como obrigatório. Se o e-mail for só de relacionamento, pode virar opcional (menos dado sensível guardado e menos desistência).
- Definir por quanto tempo os dados ficam guardados e quem tem acesso.

## 6. Pendências

1. Escolher o caminho A ou B.
2. Criar a Data Extension e a Journey no Marketing Cloud.
3. Montar o e-mail de boas-vindas.
4. Link da Política de Privacidade.
5. Confirmar se CPF fica obrigatório.
6. Logo oficial da H2 em SVG (hoje o topo usa "H2 Club" em texto).
