# Handover: Estúdio H2

**Projeto:** site compartilhável do time de marketing para gerar e guardar temas e roteiros de vídeo
**Responsável:** Julia Nascimento (julia.nascimento@h2grupo.com)
**Data:** 24/09/2026
**Link do site:** https://claude.ai/artifact/VLnTEtPedZZR6WA7PA4AHs (versão 2)
**Projeto no Claude:** "gerador de temas e roteiros"

---

## 1. O que foi pedido

1. Um site compartilhável entre o time de marketing, com uma **biblioteca** que gera e salva temas e roteiros automaticamente, conforme a necessidade.
2. Três categorias:
   - **A&B:** alimentos e bebidas, ligados ao cardápio do clube H2.
   - **Roteiros para vídeos.**
   - **Temas para vídeos:** cada tema com uma mensagem principal, respondendo "o que esse tema quer dizer?".
3. Visual no estilo da referência enviada: landing page de fintech, com degradê violeta, títulos grandes em caixa alta, menu em pílula e cards arredondados.
4. **Roteiro:** uma sequência de perguntas (tempo de duração, sobre o que o vídeo aborda etc.). O roteiro gerado fica salvo na biblioteca, com opção de copiar, editar ou apagar.
5. **Temas:** gerados por demanda, como divulgação de torneio, cash games, home game e A&B (cardápio do clube).
6. Depois veio mais um pedido: poder **anexar um vídeo de propaganda como inspiração**, para a IA montar o roteiro com base nele.

---

## 2. O que foi entregue

### 2.1 Estrutura do site

| Área | O que tem |
|---|---|
| **Topo (hero)** | Menu (Início, Roteiro, Temas, Biblioteca), o título "Ideias que viram vídeo pronto", contadores ao vivo de roteiros, temas e A&B, e os botões "Gerar roteiro" e "Gerar temas" |
| **Estúdio** | Duas abas, "Roteiro para vídeo" e "Temas para vídeo", mais o atalho "Tenho uma propaganda de inspiração" |
| **Sobre o clube** | Área retrátil com dois campos compartilhados: "Sobre a H2 e tom de voz" e "Cardápio de A&B". Tudo o que estiver lá entra automaticamente em toda geração |
| **Biblioteca** | Todos os itens salvos pelo time, com filtros (Todos / Roteiros / Temas / A&B), busca por texto e filtro por categoria |

### 2.2 Roteiro para vídeo: as 9 perguntas

São feitas uma de cada vez, com barra de progresso e um painel lateral "Suas respostas", onde dá para clicar e voltar a qualquer pergunta.

1. **Categoria:** Torneio, Cash Game, Home Game, A&B ou CPH.
2. **Propaganda de inspiração:** opcional, com upload de vídeo (ver 2.3).
3. **Duração:** 15s, 30s, 45s, 60s, 90s ou 3 min.
4. **Sobre o que o vídeo aborda:** texto livre.
5. **Plataforma:** Reels, Stories, TikTok, YouTube Shorts, YouTube ou WhatsApp.
6. **Objetivo:** divulgar evento, gerar inscrições, engajamento, apresentar o cardápio ou fortalecer a marca.
7. **Tom:** emocionante, descontraído, sofisticado, com humor ou informativo.
8. **Formato de gravação:** apresentador, narração em off, só imagens e texto, depoimento ou bastidores.
9. **Informações obrigatórias e CTA:** opcional (datas, valores, link na bio, @ do clube).

As perguntas de múltipla escolha também aceitam uma opção escrita à mão.

**Resultado:**
- O roteiro vem dividido em cenas, cada uma com tempo, visual, fala e texto na tela.
- Traz também mensagem principal, CTA, legenda, hashtags e dicas de gravação.
- O texto é editável antes de salvar.
- Os botões disponíveis são: Salvar na biblioteca, Gerar outra versão, Copiar e Recomeçar.

### 2.3 Propaganda de inspiração (versão 2)

**Como funciona:**
- A pessoa anexa um vídeo, clicando ou arrastando.
- O site separa até 8 quadros ao longo do vídeo e mostra na tela, cada um com o tempo em que aparece.
- Tem um campo opcional, "O que aproveitar dessa referência", para indicar por exemplo o gancho, os cortes rápidos ou o texto grande na tela.

**O que a IA faz:**
- Analisa gancho, ritmo de cortes, enquadramentos, movimento de câmera, texto na tela, cores e CTA.
- Monta um roteiro **original** da H2 com a mesma lógica, sem copiar marca, falas, slogans ou pessoas da referência.
- O roteiro ganha a seção "Inspiração", que explica o que foi aproveitado.

**Na biblioteca:** o item salvo aparece com a etiqueta "Com inspiração" e uma miniatura do vídeo.

**Limites:**
- **Sem áudio:** a IA vê só as imagens do vídeo. Música e fala precisam ser descritas no campo de observações.
- **Formato:** MP4 (H.264) funciona melhor. Alguns .mov de iPhone (HEVC) podem não abrir no navegador.
- **O que fica salvo:** o vídeo não é guardado, só a miniatura e o nome do arquivo.
- **Permissão:** se a conta de quem está usando não permitir enviar imagens para a IA, o site avisa e segue sem o vídeo.

### 2.4 Temas para vídeo

**Como pedir:**
- **Demanda:** Torneio, Cash Game, Home Game, A&B ou CPH.
- **Quantidade:** 3, 5 ou 8 temas.
- **Tom:** emocionante, descontraído, sofisticado ou com humor.
- **Contexto:** opcional, por exemplo "série de outubro, final dia 26".

**O que cada tema traz:** título, **"O que esse tema quer dizer"** (a mensagem principal), gancho, formato sugerido e por que funciona.

**Ações:** Salvar, Salvar todos, Gerar outros e **Virar roteiro**. Esse último leva o tema direto para o fluxo de roteiro, já preenchido.

### 2.5 Biblioteca

**O que aparece em cada card:** tipo (Roteiro ou Tema), categoria, título, mensagem principal, data e o primeiro nome de quem criou.

**Ações:**
- Abrir para ler o conteúdo completo.
- Copiar com um clique.
- Editar título, tipo, categoria, mensagem e conteúdo.
- Apagar, com confirmação na própria tela.
- Nos temas, também tem o botão "Virar roteiro".

**Compartilhamento:** a biblioteca é única para o time. O que uma pessoa salva, todas as outras veem na hora.

### 2.6 Regras que a IA segue em toda geração

- Escreve em português do Brasil, com linguagem de redes sociais.
- Nunca promete ganhos nem trata o poker como fonte de renda.
- Considera o público +18 e reforça o jogo responsável quando fizer sentido.
- **Não inventa** datas, valores, prêmios, pratos ou preços. Usa marcadores como [data], [valor do buy-in] e [nome do prato] para o time preencher.
- Em A&B, usa só os itens do cardápio cadastrado em "Sobre o clube".

---

## 3. Links da H2 enviados

| Área | Link | Situação |
|---|---|---|
| Torneios | https://sp.h2club.com.br/agenda-poker | Bloqueou a leitura automática (erro 403) |
| Cash Game | https://sp.h2club.com.br/cash-game-sp | Bloqueou a leitura automática (erro 403) |
| Home Game | https://cloud.h2grupo.com.br/home-game | **Lido** e usado em "Sobre o clube" |
| Gastronomia | https://sp.h2club.com.br/gastronomia | Bloqueou a leitura automática (erro 403) |
| Cardápio (PDF) | https://sp.h2club.com.br/cardapio/H2_SP.pdf?new=1710 | Bloqueou a leitura automática (erro 403) |

**O que entrou em "Sobre o clube"** (a partir do Home Game e dos títulos das páginas):

- **Slogan:** "O jogo não para".
- **Home Game:** "Jogue poker com seus amigos! Sem se preocupar em dar as cartas." Tem a tríade Amigos, Competição, Diversão e o slogan "Sinta a emoção de um pro!". A reserva é feita por formulário. Clientes citados: Coca-Cola, G4 Educação e Copag.
- **Torneios, Cash Game e Gastronomia:** ficaram com marcadores [completar].

O gerador dentro do site não consegue abrir outras páginas da internet. Por isso as informações precisam estar escritas em "Sobre o clube".

---

## 4. Conteúdo de exemplo já na biblioteca

Estes quatro itens estão com a etiqueta "Exemplo" e podem ser apagados quando quiser:

1. Roteiro de Torneio: "A mesa final começa agora" (30s, Reels, emocionante).
2. Tema de Home Game: "O happy hour que virou torneio".
3. Tema de Cash Game: "Uma noite de terça no cash".
4. Tema de A&B: "O intervalo mais disputado".

---

## 5. Pendências

- [ ] **Compartilhar o site com o time:** hoje ele está privado. Use o menu Compartilhar da página. Só é possível compartilhar com pessoas da organização.
- [ ] **Colar o cardápio de A&B** no campo "Cardápio de A&B" da área "Sobre o clube".
- [ ] **Completar "Sobre o clube"** com torneios (séries, horários, buy-ins, garantidos), cash game (modalidades, stakes, horários), gastronomia (estilo e destaques), @ das redes e o que a marca evita dizer.
- [ ] **Testar a geração** com um pedido real de roteiro, de temas e de propaganda de inspiração.
- [ ] Apagar os exemplos, se não forem úteis.

---

## 6. Bom saber

- **Permissão da IA:** a geração usa a conta Claude de quem está gerando. Na primeira vez, cada pessoa precisa clicar em "Permitir".
- **Quem pode alterar:** todo mundo com acesso ao site pode salvar, editar e apagar itens. Não há níveis de permissão diferentes por enquanto.
- **Capacidade:** até cerca de 5.000 itens salvos no total.
- **O que foi testado:**
  - A separação dos quadros de vídeo foi testada com um vídeo de teste e funcionou.
  - A biblioteca foi conferida no acesso de um membro comum do time.
  - A geração em si deve ser testada pelo time no site publicado.

---

## 7. Ideias para próximas versões (não implementadas)

- **Aprovação:** status por item (rascunho, aprovado, publicado) e um filtro por status.
- **Calendário:** um campo de data de publicação, com visão em calendário.
- **Pastas ou campanhas:** agrupar itens por campanha, como "Série de Outubro".
- **Salvar o vídeo de referência** junto do roteiro, em vez de só a miniatura.
- **Permissões:** só algumas pessoas podem apagar itens ou editar "Sobre o clube".
- **Exportar** um roteiro em PDF ou Word para mandar para o videomaker.
- **Legendas prontas** para cada rede a partir de um roteiro salvo.

---

## 8. Notas técnicas

Ver o [README](../README.md).
