"""Gera fluxo-n8n.json a partir de formulario-h2.html.

Rode de novo sempre que mudar o formulário:  python3 gerar-fluxo-n8n.py
Depois, no n8n: menu do fluxo > Import from File > fluxo-n8n.json
"""
import json
from pathlib import Path

PASTA = Path(__file__).parent
CAMINHO_FORM = "cadastro-h2"           # GET  /webhook/cadastro-h2         -> mostra o formulário
CAMINHO_ENVIO = "cadastro-h2-enviar"   # POST /webhook/cadastro-h2-enviar  -> recebe o cadastro

fonte = (PASTA / "formulario-h2.html").read_text(encoding="utf-8")
marca = 'const WEBHOOK_URL = "";'
assert marca in fonte, "não achei a constante WEBHOOK_URL no formulário"
# Aberto pelo link de teste (/webhook-test/), envia para o teste; pelo de produção, para a produção
corpo = fonte.replace(
    marca,
    f'const WEBHOOK_URL = (location.pathname.includes("/webhook-test/") ? "/webhook-test/" : "/webhook/") + "{CAMINHO_ENVIO}";',
)
html = (
    '<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">'
    '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
    "</head><body>" + corpo + "</body></html>"
)

LIMPAR = """// Pega o cadastro enviado pelo formulário e deixa só os campos da planilha
return $input.all().map(item => {
  // O formulário manda tudo num campo "dados" (texto em JSON)
  const corpo = item.json.body || {};
  let b = corpo;
  try { if (typeof corpo.dados === 'string') b = JSON.parse(corpo.dados); else if (typeof corpo === 'string') b = JSON.parse(corpo); } catch (e) { b = {}; }
  return { json: {
    createdAt: b.createdAt || new Date().toISOString(),
    nome: String(b.nome || '').trim(),
    nascimento: b.nascimento || '',
    genero: b.genero || '',
    homegame: String(b.homegame || '').trim(),
    instagram: b.instagram || '',
    representante: String(b.representante || '').trim(),
    email: String(b.email || '').trim().toLowerCase(),
    celular: b.celular || '',
    endereco: b.endereco || '',
    cep: b.cep || '',
    cidade: b.cidade || '',
    uf: b.uf || '',
    origem: b.origem || '',
    dias: b.dias || '',
    frequencia: b.frequencia || '',
    buyin: b.buyin || '',
    arrecadacao: b.arrecadacao || '',
    jogadores: b.jogadores || '',
    motivo: b.motivo || '',
    optinEmail: b.optinEmail === true,
    aceiteTermos: b.aceiteTermos === true
    // status e emailEnviadoEm ficam de fora: num e-mail repetido, a planilha mantém o que já tinha
  }};
}).filter(i => i.json.email);"""

NOTA = """## Fun Festival no seu homegame
**1.** Abra o nó *Google Sheets*, escolha sua credencial do Google e a planilha.
**2.** Na planilha, a aba **Cadastros** precisa ter na linha 1:
createdAt | nome | nascimento | genero | homegame | instagram | representante | email | celular | endereco | cep | cidade | uf | origem | dias | frequencia | buyin | arrecadacao | jogadores | motivo | optinEmail | aceiteTermos | status | emailEnviadoEm
**3.** Ative o fluxo (Active). O link do formulário é a *Production URL* do nó **Abrir formulário**.

Próximo passo: depois do Google Sheets, ligar o envio do e-mail pelo Salesforce (ver LOGICA-AUTOMACAO.md)."""

fluxo = {
    "name": "Fun Festival homegame: formulário → planilha",
    "nodes": [
        {
            "parameters": {"content": NOTA, "height": 340, "width": 520},
            "id": "b6f7d0c2-1a11-4c2e-9a01-000000000001",
            "name": "Como usar",
            "type": "n8n-nodes-base.stickyNote",
            "typeVersion": 1,
            "position": [-80, -420],
        },
        {
            "parameters": {"path": CAMINHO_FORM, "responseMode": "responseNode", "options": {}},
            "id": "b6f7d0c2-1a11-4c2e-9a01-000000000002",
            "name": "Abrir formulário",
            "type": "n8n-nodes-base.webhook",
            "typeVersion": 2,
            "position": [0, 0],
            "webhookId": "6134dca6-3766-498b-bdbd-24dfe3c0d7aa",
        },
        {
            "parameters": {
                "respondWith": "text",
                "responseBody": html,
                "options": {
                    "responseHeaders": {
                        "entries": [{"name": "Content-Type", "value": "text/html; charset=utf-8"}]
                    }
                },
            },
            "id": "b6f7d0c2-1a11-4c2e-9a01-000000000003",
            "name": "Mostrar formulário",
            "type": "n8n-nodes-base.respondToWebhook",
            "typeVersion": 1.1,
            "position": [240, 0],
        },
        {
            "parameters": {
                "httpMethod": "POST",
                "path": CAMINHO_ENVIO,
                "responseMode": "onReceived",
                "options": {"allowedOrigins": "*"},
            },
            "id": "b6f7d0c2-1a11-4c2e-9a01-000000000004",
            "name": "Receber cadastro",
            "type": "n8n-nodes-base.webhook",
            "typeVersion": 2,
            "position": [0, 220],
            "webhookId": "0d2f3c1e-7f6a-4f0e-8a51-5f2b7d9e4c10",
        },
        {
            "parameters": {"jsCode": LIMPAR},
            "id": "b6f7d0c2-1a11-4c2e-9a01-000000000005",
            "name": "Limpar dados",
            "type": "n8n-nodes-base.code",
            "typeVersion": 2,
            "position": [240, 220],
        },
        {
            "parameters": {
                "operation": "appendOrUpdate",
                "documentId": {"__rl": True, "mode": "url", "value": ""},
                "sheetName": {"__rl": True, "mode": "name", "value": "Cadastros"},
                "columns": {
                    "mappingMode": "autoMapInputData",
                    "value": {},
                    "matchingColumns": ["email"],
                },
                "options": {},
            },
            "id": "b6f7d0c2-1a11-4c2e-9a01-000000000006",
            "name": "Google Sheets",
            "type": "n8n-nodes-base.googleSheets",
            "typeVersion": 4.5,
            "position": [480, 220],
        },
    ],
    "connections": {
        "Abrir formulário": {"main": [[{"node": "Mostrar formulário", "type": "main", "index": 0}]]},
        "Receber cadastro": {"main": [[{"node": "Limpar dados", "type": "main", "index": 0}]]},
        "Limpar dados": {"main": [[{"node": "Google Sheets", "type": "main", "index": 0}]]},
    },
    "settings": {"executionOrder": "v1"},
    "pinData": {},
}

(PASTA / "fluxo-n8n.json").write_text(json.dumps(fluxo, ensure_ascii=False, indent=2), encoding="utf-8")
print("fluxo-n8n.json gerado")
