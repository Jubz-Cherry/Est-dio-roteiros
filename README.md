# Estúdio H2

Site do time de marketing da H2 para gerar e guardar temas e roteiros de vídeo (Torneio, Cash Game, Home Game, A&B e Institucional), com uma biblioteca compartilhada pelo time.

**Site publicado:** https://claude.ai/artifact/VLnTEtPedZZR6WA7PA4AHs

## Arquivos

- `estudio-h2.html`: o site inteiro, numa página só (HTML, CSS e JavaScript, sem bibliotecas externas). Fontes: Archivo (títulos) e Manrope (texto), via Google Fonts.
- `docs/handover.md`: o que foi pedido, o que foi entregue, pendências e ideias para as próximas versões.

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

## Como publicar uma nova versão

Edite `estudio-h2.html` e republique no mesmo Artifact (mesmo link), mantendo as capacidades `db`, `sample` e `user` com escopo `profile`.

## Versões

- **v1:** biblioteca, roteiro com 8 perguntas, temas e "Sobre o clube".
- **v2:** pergunta de propaganda de inspiração, com envio de até 8 quadros do vídeo para a IA.
