/**
 * Recebe os cadastros do formulário H2 e grava na planilha.
 *
 * Como instalar:
 * 1. Crie uma planilha no Google Sheets e uma aba chamada "Cadastros".
 * 2. Na planilha: Extensões > Apps Script. Apague o que estiver lá e cole este arquivo.
 * 3. Implantar > Nova implantação > tipo "App da Web".
 *    Executar como: "Eu". Quem pode acessar: "Qualquer pessoa".
 * 4. Copie a URL que termina em /exec e cole na constante WEBHOOK_URL do formulário.
 * Sempre que mudar este código, faça Implantar > Gerenciar implantações > Editar > Nova versão.
 */

const ABA = "Cadastros";
const COLUNAS = [
  "createdAt", "nome", "nascimento", "genero", "homegame", "instagram", "representante", "email", "celular", "endereco", "cep", "cidade", "uf", "origem",
  "dias", "frequencia", "buyin", "arrecadacao", "jogadores", "motivo", "optinEmail", "aceiteTermos", "status", "emailEnviadoEm"
];

function doPost(e) {
  const lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    const dados = JSON.parse(e.parameter.dados || e.postData.contents);
    const email = String(dados.email || "").trim().toLowerCase();
    if (!email) return resposta({ ok: false, erro: "sem e-mail" });

    const aba = pegarAba();
    const linhaExistente = acharEmail(aba, email);
    const valores = COLUNAS.map(c => c === "emailEnviadoEm" ? "" : (dados[c] ?? ""));

    if (linhaExistente) {
      // Mesmo e-mail: atualiza os dados, mas mantém status e data de envio para não reenviar.
      const atuais = aba.getRange(linhaExistente, 1, 1, COLUNAS.length).getValues()[0];
      valores[COLUNAS.indexOf("status")] = atuais[COLUNAS.indexOf("status")];
      valores[COLUNAS.indexOf("emailEnviadoEm")] = atuais[COLUNAS.indexOf("emailEnviadoEm")];
      aba.getRange(linhaExistente, 1, 1, COLUNAS.length).setValues([valores]);
    } else {
      aba.appendRow(valores);
    }
    return resposta({ ok: true });
  } catch (err) {
    return resposta({ ok: false, erro: String(err) });
  } finally {
    lock.releaseLock();
  }
}

function pegarAba() {
  const planilha = SpreadsheetApp.getActiveSpreadsheet();
  const aba = planilha.getSheetByName(ABA) || planilha.insertSheet(ABA);
  if (aba.getLastRow() === 0) aba.appendRow(COLUNAS);
  return aba;
}

function acharEmail(aba, email) {
  const ultima = aba.getLastRow();
  if (ultima < 2) return 0;
  const col = COLUNAS.indexOf("email") + 1;
  const emails = aba.getRange(2, col, ultima - 1, 1).getValues();
  const i = emails.findIndex(([v]) => String(v).trim().toLowerCase() === email);
  return i === -1 ? 0 : i + 2;
}

function resposta(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}
