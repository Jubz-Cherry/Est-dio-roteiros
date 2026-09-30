# Estúdio H2

Site do time de marketing da H2 para gerar e guardar temas e roteiros de vídeo (Torneio, Cash Game, Home Game, A&B e CPH), com uma biblioteca compartilhada pelo time.

**Site publicado:** https://claude.ai/artifact/VLnTEtPedZZR6WA7PA4AHs

## Arquivos

- `estudio-h2.html`: o site inteiro, numa página só (HTML, CSS e JavaScript, sem bibliotecas externas). Fontes: Archivo (títulos) e Manrope (texto), via Google Fonts.
- `docs/handover.md`: o que foi pedido, o que foi entregue, pendências e ideias para as próximas versões.
- `docs/referencias/roteiros-home-game-2026-01.pdf`: a tarefa do ClickUp que serve de base para o padrão de roteiro da H2.

## Como funciona

O site roda como Artifact do Claude e usa três recursos do runtime (`window.claude.use`):

| Recurso | Para quê |
|---|---|
| `db` | Biblioteca compartilhada (coleção `biblioteca`) e informações do clube (documento `config/clube`) |
| `sample` | Geração de roteiros e temas pela IA, incluindo os quadros da propaganda de inspiração |
| `user` (escopo `profile`) | Identificar quem salvou cada item e mostrar o primeiro nome |

Aberto fora do Claude (por exemplo, direto do arquivo), o site carrega, mas a biblioteca e a geração ficam indisponíveis e ele avisa isso na tela.

### Dados

- `biblioteca/{id}`: `tipo` (roteiro/tema), `area`, `titulo`, `mensagem`, `conteudo`, `meta`, `inspiracao`, `thumb` (miniatura JPEG em data URI), `autor`, `createdAt`, `updatedAt`, `exemplo`.
- `config/clube`: `sobre`, `cardapio`, `updatedAt`, `updatedBy`.

## Padrão de roteiro da H2

Em todas as categorias (Torneio, Cash Game, Home Game, A&B e CPH), o roteiro segue o modelo da tarefa "Mkt Live SP | ADS | Roteiros | Home Game | 2026 | 01" (constante `PADRAO` no código):

- Cabeçalho `CATEGORIA H2 — "assinatura"`. Home Game usa "A nossa Home, o seu Game!"; nas outras categorias a IA propõe um trocadilho no mesmo espírito (constante `ASSINATURAS`).
- Narrativa em três atos, por exemplo preparação → revelação → experiência.
- Tabela Tempo | Cena | Fala / Som, com faixas de 1 a 3 segundos, câmera e transições descritas e pessoas identificadas por letras.
- Packshot final com a ficha H2 integrada ao lettering e o logo H2.
- Botão "Copiar tabela" no roteiro gerado e na biblioteca: copia uma tabela de verdade para colar no ClickUp, Docs ou Word.

## CPH

A categoria CPH (Campeonato Paulista de Poker) substituiu Institucional. Quando a categoria é CPH, os prompts de temas e roteiros recebem o território de marca do campeonato (constante `CPH` no código): a temporada de 9 etapas, os cinco pilares (história e legado, tradição e credibilidade, técnica, relevância e pertencimento) e a narrativa do Main Event, "O título que vira legado".

- O roteiro usa o padrão da H2, com cabeçalho `CPH — "assinatura"` e packshot com o logo do CPH.
- Os temas variam entre os pilares e tratam o CPH como temporada, não como eventos isolados.
- A IA não inventa nomes de campeões, posições no Ranking, etapas ou valores: usa marcadores entre colchetes.
- Itens antigos salvos como Institucional continuam na biblioteca e mantêm a categoria ao serem editados.

## Como publicar uma nova versão

Edite `estudio-h2.html` e republique no mesmo Artifact (mesmo link), mantendo as capacidades `db`, `sample` e `user` com escopo `profile`.

## Versões

- **v1:** biblioteca, roteiro com 8 perguntas, temas e "Sobre o clube".
- **v2:** pergunta de propaganda de inspiração, com envio de até 8 quadros do vídeo para a IA.
- **v3:** padrão de roteiro da H2 (três atos, tabela Tempo | Cena | Fala / Som e packshot) em Torneio, Cash Game, Home Game e A&B, e botão "Copiar tabela".
- **v4:** a propaganda de inspiração funciona também onde a IA não recebe imagens. O vídeo continua podendo ser anexado, a descrição da propaganda entra no lugar dos quadros e, se a IA recusar os quadros na hora de gerar, o roteiro é gerado uma vez sem eles.
- **v5:** análise automática da propaganda, feita no navegador sem IA: cortes, duração dos planos, formato, cores, movimento da câmera e volume do áudio. A análise vai para a IA em toda geração com referência, e a descrição das cenas fica opcional.
- **v6:** a categoria Institucional vira CPH, com o território de marca do Campeonato Paulista de Poker nos temas e roteiros.
