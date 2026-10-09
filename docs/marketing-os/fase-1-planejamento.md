# Marketing OS — Planejamento técnico da Fase 1 (Fundação)

**Status:** proposta para revisão. Nenhum código foi escrito ainda.
**Data:** 09/10/2026
**Escopo:** monorepo, frontend e backend configurados, PostgreSQL + Prisma, autenticação e layout principal.

> Este documento está provisoriamente no repositório do Estúdio H2 só para registrar o plano.
> A recomendação é que o Marketing OS tenha um repositório próprio (ver decisão D1).

---

## 1. Análise da arquitetura proposta

O handover está bem fundamentado. Os pontos fortes são: stack consolidada e bem documentada, separação clara entre `web` e `api`, controle de acesso validado no backend e MVP enxuto. Os pontos abaixo precisam de ajuste ou de definição antes do código.

| # | Ponto | Observação | Proposta |
|---|---|---|---|
| A1 | `packages/shared` | Compartilhar schemas Zod entre front e back evita validar o mesmo formulário de dois jeitos. Mas pacotes compartilhados em TypeScript costumam dar trabalho no build. | Pacote "só fonte" (sem build próprio). O Vite já entende TypeScript; na API, o `tsx` roda em dev e o `tsup` empacota o `shared` junto no build. |
| A2 | Autenticação | "Sessão em cookie HttpOnly" é a escolha certa para um app web interno (melhor que JWT no `localStorage`, que fica exposto a XSS e não pode ser revogado). Falta definir onde a sessão vive. | Sessões guardadas no PostgreSQL, implementadas por nós (≈150 linhas). É didático, sem dependência extra e permite "derrubar" sessões. |
| A3 | CSRF | Com cookie de sessão, toda requisição que altera dados precisa de proteção CSRF. | `SameSite=Lax` + verificação do cabeçalho `Origin` em métodos que alteram dados + aceitar só `application/json`. Dispensa token CSRF quando front e API estão no mesmo site. |
| A4 | Domínios em produção | Cookies e CORS dependem de onde front e API vão morar. | Em dev, o Vite faz proxy de `/api` → mesma origem, sem CORS. Em produção, front e API no mesmo domínio (ex.: `os.empresa.com` e `api.os.empresa.com`). Definir na Fase 6, mas sem decisões que impeçam isso. |
| A5 | Papéis | Admin/Gestor/Membro/Visualizador são por workspace, e workspaces só chegam na Fase 2. | Na Fase 1, só o usuário e a sessão. O primeiro usuário é criado por um script de seed; o papel dele entra na Fase 2. |
| A6 | Modelo `User` | Falta um jeito de desativar alguém sem apagar o histórico. | Adicionar `disabledAt` (opcional). Usuário desativado não loga, e as sessões dele são invalidadas. |
| A7 | Camadas do backend | O handover pede rotas, validação, regra de negócio e acesso a dados separados. | Cada módulo com `routes` → `controller` → `service` → `repository`, e `schemas` para o Zod (detalhes na seção 4). |
| A8 | Dados mockados | O layout precisa mostrar algo antes da Fase 2 existir. | Estados vazios reais ("Nenhum espaço ainda") em vez de dados falsos. O dashboard mostra cards com "—" e a mensagem "disponível na Fase 3". |
| A9 | Versões | Prisma, Tailwind, Express e Zod tiveram versões grandes recentes (Tailwind v4 com configuração em CSS, Express 5, Zod 4, Prisma com `prisma.config.ts`). | Fixar as versões no momento da instalação e seguir a documentação oficial da versão instalada, não tutoriais antigos. |

---

## 2. Decisões pendentes

Cada item tem uma recomendação. Se você concordar, basta responder "ok" para seguirmos com ela.

| # | Decisão | Opções | Recomendação |
|---|---|---|---|
| **D1** | Onde fica o código | (a) repositório novo `marketing-os`; (b) pasta dentro deste repositório | **(a)**: são projetos diferentes, com CI, issues e permissões diferentes. |
| **D2** | Gerenciador do monorepo | npm workspaces; pnpm; pnpm + Turborepo | **npm workspaces**: já vem com o Node, funciona bem no Windows e é suficiente para dois apps. Turborepo pode entrar depois, se o build ficar lento. |
| **D3** | PostgreSQL local no Windows | Docker Desktop (WSL2); instalador nativo do PostgreSQL | **Docker Desktop**: um `docker compose up -d` sobe o banco igual para todo mundo, e um banco de testes separado vem junto. O instalador nativo fica documentado como alternativa. |
| **D4** | Sessões | Próprias, no Postgres; `express-session` + `connect-pg-simple`; biblioteca de auth | **Próprias, no Postgres**: código pequeno, que você vai entender linha por linha, e sem dependência de biblioteca descontinuada. |
| **D5** | Cadastro público | Ligado; desligado com convites | **Desligado por padrão** (`ALLOW_PUBLIC_SIGNUP=false`). Admin inicial via `npm run db:seed`; convites entram na Fase 2. A rota `/auth/register` existe, mas responde 403 quando desligada. |
| **D6** | Idioma | Código e interface | **Código em inglês** (nomes de tabelas, funções, rotas) e **interface em português**. Mensagens de erro da API com `code` em inglês e `message` em português. |
| **D7** | Testes | Vitest; Jest | **Vitest** no front e no back (rápido e compatível com Vite) + **Supertest** para testar a API de verdade contra um banco de teste. |
| **D8** | Versão do Node | 22 LTS; 24 LTS | **24 LTS**, fixada em `.nvmrc` e em `engines`. |
| **D9** | Hospedagem | — | **Adiar** para a Fase 6, mantendo a decisão A4 em mente. Nenhum serviço pago entra sem levantamento de custos. |

---

## 3. Estrutura inicial do projeto (Fase 1)

Só o que a Fase 1 usa. Pastas de módulos futuros (`workspaces`, `tasks` etc.) **não** são criadas vazias; elas nascem na fase delas.

```text
marketing-os/
├── .github/workflows/ci.yml        # lint, typecheck, testes e build
├── apps/
│   ├── api/
│   │   ├── prisma/
│   │   │   ├── schema.prisma
│   │   │   ├── migrations/         # gerado pelo Prisma, versionado no Git
│   │   │   └── seed.ts             # cria o admin inicial
│   │   ├── src/
│   │   │   ├── config/
│   │   │   │   └── env.ts          # lê e valida variáveis de ambiente com Zod
│   │   │   ├── lib/
│   │   │   │   ├── prisma.ts       # instância única do Prisma Client
│   │   │   │   ├── logger.ts       # pino, com campos sensíveis ocultos
│   │   │   │   └── errors.ts       # AppError e códigos de erro padronizados
│   │   │   ├── middlewares/
│   │   │   │   ├── require-auth.ts
│   │   │   │   ├── verify-origin.ts    # proteção CSRF
│   │   │   │   ├── validate.ts         # aplica um schema Zod a body/params/query
│   │   │   │   └── error-handler.ts
│   │   │   ├── modules/
│   │   │   │   ├── auth/
│   │   │   │   │   ├── auth.routes.ts
│   │   │   │   │   ├── auth.controller.ts
│   │   │   │   │   ├── auth.service.ts
│   │   │   │   │   ├── session.service.ts
│   │   │   │   │   ├── session.repository.ts
│   │   │   │   │   ├── auth.rate-limit.ts
│   │   │   │   │   └── auth.test.ts
│   │   │   │   └── users/
│   │   │   │       ├── user.repository.ts
│   │   │   │       └── user.mapper.ts      # nunca expõe passwordHash
│   │   │   ├── app.ts              # monta o Express (testável sem abrir porta)
│   │   │   └── server.ts           # só chama app.listen
│   │   ├── tsconfig.json
│   │   ├── vitest.config.ts
│   │   └── package.json
│   └── web/
│       ├── public/
│       ├── src/
│       │   ├── components/
│       │   │   ├── ui/             # componentes shadcn (gerados pela CLI)
│       │   │   ├── sidebar/        # Sidebar, SidebarItem, SidebarSection
│       │   │   ├── topbar/         # Topbar, Breadcrumbs, GlobalSearch, UserMenu
│       │   │   ├── theme-toggle.tsx
│       │   │   └── empty-state.tsx
│       │   ├── contexts/
│       │   │   ├── auth-context.tsx
│       │   │   └── theme-context.tsx
│       │   ├── hooks/
│       │   │   ├── use-auth.ts
│       │   │   └── use-sidebar.ts
│       │   ├── layouts/
│       │   │   ├── app-layout.tsx  # sidebar + topbar + <Outlet/>
│       │   │   └── auth-layout.tsx # tela centralizada do login
│       │   ├── pages/
│       │   │   ├── login-page.tsx
│       │   │   ├── home-page.tsx
│       │   │   ├── my-tasks-page.tsx
│       │   │   ├── settings-page.tsx
│       │   │   └── not-found-page.tsx
│       │   ├── routes/
│       │   │   ├── router.tsx
│       │   │   └── protected-route.tsx
│       │   ├── services/
│       │   │   ├── api-client.ts   # fetch com credentials e tratamento de erro
│       │   │   └── auth-service.ts
│       │   ├── styles/globals.css  # Tailwind + tokens de cor (light/dark)
│       │   ├── types/
│       │   └── main.tsx
│       ├── index.html
│       ├── vite.config.ts          # proxy /api → localhost:3333
│       └── package.json
├── packages/
│   └── shared/
│       ├── src/
│       │   ├── schemas/auth.ts     # loginSchema, registerSchema
│       │   ├── types/api.ts        # formato padrão de resposta e erro
│       │   └── index.ts
│       └── package.json
├── docs/
│   ├── arquitetura.md
│   ├── instalacao-windows.md
│   └── decisoes/                   # registros curtos de decisões (ADR)
├── docker-compose.yml              # postgres (dev) + postgres (teste)
├── .env.example
├── .editorconfig
├── .gitattributes                  # evita problemas de fim de linha no Windows
├── .nvmrc
├── eslint.config.js
├── .prettierrc
├── package.json                    # workspaces + scripts da raiz
└── README.md
```

### Por que cada camada existe no backend

Pense numa requisição `POST /api/v1/auth/login` atravessando as camadas:

1. **`auth.routes.ts`**: diz "esta URL, com este método, passa por estes middlewares e cai neste controller". Não tem lógica.
2. **`validate(loginSchema)`**: o Zod confere o formato do corpo. Se o e-mail for inválido, responde 400 e nada abaixo é executado.
3. **`auth.controller.ts`**: traduz HTTP para chamada de função. Lê `req.body`, chama o service, grava o cookie e escolhe o status. Não conhece o banco.
4. **`auth.service.ts`**: a regra de negócio ("usuário desativado não loga", "senha confere?", "cria sessão nova"). Não conhece `req`/`res`, então dá para testar isoladamente.
5. **`*.repository.ts`**: o único lugar que chama `prisma.*`. Se uma consulta mudar, só muda aqui.

Regra prática: **controller fala HTTP, service fala regra de negócio, repository fala banco.**

---

## 4. Proposta de autenticação

### 4.1 Modelo de dados da Fase 1

```prisma
model User {
  id           String    @id @default(uuid()) @db.Uuid
  name         String
  email        String    @unique          // salvo sempre em minúsculas
  passwordHash String
  avatarUrl    String?
  disabledAt   DateTime?                  // proposta A6
  createdAt    DateTime  @default(now())
  updatedAt    DateTime  @updatedAt
  sessions     Session[]
}

model Session {
  id         String   @id @default(uuid()) @db.Uuid
  tokenHash  String   @unique             // SHA-256 do token; o token em si só existe no cookie
  userId     String   @db.Uuid
  user       User     @relation(fields: [userId], references: [id], onDelete: Cascade)
  expiresAt  DateTime
  lastUsedAt DateTime @default(now())
  createdAt  DateTime @default(now())
  userAgent  String?

  @@index([userId])
  @@index([expiresAt])
}
```

**Por que guardar o hash do token, e não o token?** Se um backup do banco vazar, quem o tiver não consegue se passar por ninguém: o banco só tem `sha256(token)`, e o cookie tem o token. É o mesmo raciocínio de não guardar a senha.

**Por que UUID?** IDs sequenciais (1, 2, 3…) permitem adivinhar recursos de outros workspaces. UUID não resolve autorização (isso é papel do backend), mas tira a facilidade.

### 4.2 Fluxos

**Login: `POST /api/v1/auth/login`**
1. Rate limit: no máximo 10 tentativas a cada 15 min por IP + e-mail (`express-rate-limit`, em memória, o que basta para uma instância só).
2. Valida `{ email, password }` com Zod e normaliza o e-mail (`trim().toLowerCase()`).
3. Busca o usuário. **Se não existir, verifica a senha contra um hash falso mesmo assim**, para que a resposta demore o mesmo tempo e não revele quais e-mails existem.
4. `argon2.verify(passwordHash, password)`. Se falhar ou se o usuário estiver desativado, responde **401 com a mesma mensagem genérica**: "E-mail ou senha inválidos".
5. Gera o token: `crypto.randomBytes(32)` em base64url (256 bits aleatórios).
6. Cria a `Session` com `tokenHash` e `expiresAt` = agora + 7 dias.
7. Envia o cookie `mos_session`: `HttpOnly`, `SameSite=Lax`, `Path=/`, `Secure` em produção e `Max-Age` de 7 dias.
8. Responde `{ data: { user } }`, sem `passwordHash`.

Cada login cria **uma sessão nova**, o que impede *session fixation*.

**`GET /api/v1/auth/me`**: o middleware `requireAuth` lê o cookie, calcula o hash, busca a sessão, confere a validade e se o usuário está ativo, e coloca `req.user`. Se a sessão tiver passado da metade da validade, ela é renovada por mais 7 dias (expiração deslizante). Sem sessão válida, responde 401.

**`POST /api/v1/auth/logout`**: apaga a sessão no banco e limpa o cookie. Responde 204.

**`POST /api/v1/auth/register`**: responde 403 `SIGNUP_DISABLED` quando `ALLOW_PUBLIC_SIGNUP=false`. Quando ligado, valida, gera o hash com Argon2id e cria o usuário.

**Senhas:** Argon2id com os parâmetros recomendados pela OWASP (19 MiB de memória, 2 iterações, paralelismo 1). Mínimo de 12 e máximo de 128 caracteres, sem exigir "maiúscula + símbolo" (recomendação do NIST 800-63B: comprimento vale mais que complexidade).

### 4.3 Camadas de segurança da Fase 1

| Proteção | Como |
|---|---|
| Cabeçalhos HTTP | `helmet` |
| CORS | Em dev, desnecessário (proxy do Vite). Allowlist via `CORS_ORIGINS`, com `credentials: true`, nunca `*`. |
| CSRF | `SameSite=Lax` + middleware `verify-origin` (métodos POST/PATCH/PUT/DELETE exigem `Origin` na allowlist) + somente `Content-Type: application/json` |
| Tamanho do corpo | `express.json({ limit: '100kb' })` |
| XSS | O React já escapa o conteúdo; `dangerouslySetInnerHTML` fica proibido por regra de lint. O cookie `HttpOnly` não pode ser lido por JavaScript. |
| Logs | `pino` com `redact` em `password`, `cookie`, `authorization` e `passwordHash` |
| Segredos | Só em `.env` (fora do Git). O `env.ts` valida tudo ao iniciar e derruba a API se faltar algo. |
| Limpeza | Sessões expiradas são removidas ao iniciar a API e a cada 6 horas |

### 4.4 Padrão de resposta da API (valerá para todas as fases)

```jsonc
// sucesso
{ "data": { ... } }
// sucesso paginado (a partir da Fase 3)
{ "data": [ ... ], "meta": { "nextCursor": "..." } }
// erro
{ "error": { "code": "VALIDATION_ERROR", "message": "Dados inválidos", "details": [ ... ] } }
```

Códigos iniciais: `VALIDATION_ERROR` (400), `INVALID_CREDENTIALS` (401), `UNAUTHENTICATED` (401), `FORBIDDEN` (403), `SIGNUP_DISABLED` (403), `NOT_FOUND` (404), `RATE_LIMITED` (429), `INTERNAL_ERROR` (500). Erros 500 nunca expõem stack trace ao cliente.

### 4.5 Frontend da autenticação

- **`api-client.ts`**: `fetch` com `credentials: 'include'`. Converte `{ error }` em uma `ApiError` tipada.
- **`AuthProvider`**: usa `useQuery(['me'])` para saber quem está logado. O login chama `useMutation` e depois invalida `['me']`.
- **`ProtectedRoute`**: enquanto `me` carrega, mostra um skeleton; se der 401, redireciona para `/login?redirect=/rota-original`.
- **Login**: React Hook Form + `zodResolver(loginSchema)`, **o mesmo schema do backend** (vindo do `shared`). Mostra erros por campo, botão com spinner e alerta genérico em caso de 401 ou 429.
- **Nada de token em `localStorage`.** O navegador cuida do cookie sozinho.

---

## 5. Proposta do layout principal

```text
┌──────────────┬────────────────────────────────────────────────────────┐
│ ◆ Marketing OS│  Início / Visão geral        [🔍 Buscar…  Ctrl K] [+ Tarefa] ☾ (JN) │
│ Workspace ▾  ├────────────────────────────────────────────────────────┤
│              │                                                        │
│ ⌂ Início     │  Título da página                                      │
│ ✓ Minhas tar.│  [filtros]                         [Lista|Kanban|Cal.] │
│ ✉ Caixa (em breve)                                                    │
│              │                                                        │
│ ESPAÇOS    + │                conteúdo (<Outlet/>)                    │
│  Nenhum espaço                                                        │
│  ainda       │                                                        │
│              │                                                        │
│ ⚙ Configurações                                                       │
│ (JN) Julia ▾ │                                                        │
│ [«] recolher │                                                        │
└──────────────┴────────────────────────────────────────────────────────┘
```

**Sidebar**
- Expandida: 256 px. Recolhida: 64 px, só ícones, com tooltip. O estado fica no `localStorage`.
- Atalho `Ctrl+B` para recolher e expandir.
- Abaixo de 1024 px, vira gaveta (shadcn `Sheet`), aberta pelo botão ☰ da topbar.
- A seção "Espaços" já existe com estado vazio; a árvore de pastas e listas vem na Fase 2.
- "Caixa de entrada" aparece desabilitada, com o selo "em breve".

**Topbar**
- Breadcrumb gerado a partir do `handle` das rotas do React Router.
- Busca global: campo com atalho `Ctrl+K`, que abre um `CommandDialog` com navegação entre páginas. A busca em tarefas entra na Fase 3.
- "+ Tarefa": visível, mas desabilitado até a Fase 3, com tooltip explicando.
- Alternância de tema: claro, escuro ou sistema.
- Avatar com menu: Perfil, Configurações e Sair.

**Tema**
- Tokens CSS (`--background`, `--surface`, `--surface-elevated`, `--primary`…) definidos para `:root` (claro) e `.dark` (escuro), seguindo o formato de variáveis que o shadcn usa. O dark usa exatamente a paleta do handover; o claro será proposto com o mesmo violeta `#8B5CF6`.
- Fonte Inter (via `@fontsource-variable/inter`, servida pelo próprio app, sem depender do Google Fonts).
- A preferência fica no `localStorage`. Um script inline no `index.html` aplica o tema antes de o React carregar, para evitar o "piscar" de tela clara.
- Animações respeitam `prefers-reduced-motion`.

**Rotas da Fase 1**

| Rota | Página | Conteúdo na Fase 1 |
|---|---|---|
| `/login` | Login | Completo |
| `/` | Início | Saudação e 4 cards de indicadores em estado vazio |
| `/minhas-tarefas` | Minhas tarefas | Estado vazio |
| `/configuracoes` | Configurações | Abas Perfil (dados reais do `/me`) e Preferências (tema) |
| `*` | 404 | Completo |

---

## 6. Entregas pequenas e verificáveis

Cada entrega termina com um commit e um "como verificar". Só passamos para a próxima depois de você testar.

| Entrega | O que é construído | Como verificar |
|---|---|---|
| **1.1 Esqueleto do monorepo** | `package.json` com workspaces, TypeScript, ESLint, Prettier, `.editorconfig`, `.gitattributes`, `.nvmrc`, README inicial | `npm install` e `npm run lint` sem erros |
| **1.2 API base** | Express 5, `env.ts`, logger, `helmet`, error handler, `GET /api/v1/health` | `npm run dev -w apps/api` e abrir `http://localhost:3333/api/v1/health` → `{ "data": { "status": "ok" } }` |
| **1.3 Banco** | `docker-compose.yml`, Prisma, modelos `User` e `Session`, primeira migração, seed do admin | `docker compose up -d`, `npm run db:migrate`, `npm run db:seed` e ver o usuário no `npx prisma studio` |
| **1.4 Autenticação na API** | Login, logout, me e register (com flag), sessões, rate limit, CSRF, testes | `npm test -w apps/api`: testes de senha errada, usuário desativado, sessão expirada, cookie ausente, Origin inválido e 11ª tentativa bloqueada |
| **1.5 Frontend base** | Vite, React, TypeScript, Tailwind, shadcn/ui, tokens de tema, Inter, React Router, TanStack Query, `api-client` | `npm run dev -w apps/web`: página em branco estilizada, com alternância de tema funcionando |
| **1.6 Tela de login** | `AuthProvider`, `ProtectedRoute`, página de login com validação | Logar com o admin do seed, recarregar (continua logado), sair e tentar acessar `/` (volta ao login) |
| **1.7 Layout principal** | Sidebar recolhível, topbar, breadcrumb, `Ctrl+K`, páginas placeholder com estados vazios, versão mobile | Navegar pelas páginas, recolher a sidebar, recarregar (estado mantido) e testar em 375 px de largura |
| **1.8 CI e documentação** | GitHub Actions (lint, typecheck, testes com serviço Postgres, build), `docs/instalacao-windows.md`, `docs/arquitetura.md`, primeiros ADRs | PR com o check verde; seguir a instalação do zero numa máquina Windows |

A ordem coloca o backend antes do frontend de propósito: assim você constrói e testa a autenticação com `curl`/Insomnia, entendendo o que acontece no servidor, antes de a interface esconder os detalhes.

### Como você pode participar

Sugestão de divisão para aprender backend fazendo:

- **1.2 e 1.3:** eu explico e escrevo; você roda e explora no Prisma Studio.
- **1.4:** eu escrevo `session.service.ts` e os testes; **você escreve `auth.controller.ts` e `auth.routes.ts`**, com os testes já prontos indicando quando está certo.
- **1.7:** você escreve uma das páginas placeholder seguindo o padrão da primeira.

---

## 7. Variáveis de ambiente (prévia do `.env.example`)

```dotenv
# API
NODE_ENV=development
API_PORT=3333
DATABASE_URL=postgresql://mos:mos_dev_password@localhost:5432/marketing_os
DATABASE_URL_TEST=postgresql://mos:mos_dev_password@localhost:5433/marketing_os_test
WEB_ORIGIN=http://localhost:5173
CORS_ORIGINS=http://localhost:5173
SESSION_TTL_DAYS=7
ALLOW_PUBLIC_SIGNUP=false
LOG_LEVEL=info

# Seed do admin inicial (use uma senha forte; nunca faça commit do .env)
SEED_ADMIN_NAME=
SEED_ADMIN_EMAIL=
SEED_ADMIN_PASSWORD=
```

A senha do Postgres acima vale só para o contêiner local de desenvolvimento.

---

## 8. Pré-requisitos no Windows (prévia de `docs/instalacao-windows.md`)

1. **Node.js 24 LTS:** instalador do site oficial ou `nvm-windows`.
2. **Git for Windows:** na instalação, escolher "Checkout as-is, commit Unix-style line endings". O `.gitattributes` do projeto garante o resto.
3. **Docker Desktop**, com backend WSL2 (o instalador oferece ativar).
4. **VS Code**, com as extensões ESLint, Prettier, Prisma e Tailwind CSS IntelliSense.
5. Terminal: PowerShell ou o terminal integrado do VS Code. Todos os scripts do projeto serão multiplataforma, sem `rm -rf` ou `export` nos `package.json`.

---

## 9. Fora do escopo da Fase 1

Workspaces, papéis, espaços, pastas, listas, tarefas, convites, recuperação de senha, upload de avatar, notificações, importação do ClickUp e deploy. Cada um tem sua fase no handover.

---

## 10. Próximo passo

1. Revisar as decisões **D1 a D9** (responder "ok" ou indicar a alteração).
2. Se for D1(a), criar o repositório `marketing-os` no GitHub e adicioná-lo à sessão.
3. Começar a **entrega 1.1**: esqueleto do monorepo, com cada arquivo explicado.
