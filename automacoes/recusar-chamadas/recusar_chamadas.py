"""
Recusa automaticamente chamadas de operadoras e telemarketing num celular
Android conectado ao computador por ADB (cabo USB ou Wi-Fi).

Uso:
    python recusar_chamadas.py              # monitora e recusa
    python recusar_chamadas.py --seco       # só avisa, não recusa
    python recusar_chamadas.py --testar 0303 123 4567   # testa as regras

As regras ficam em config.py.
"""

import argparse
import csv
import re
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

import config

PASTA = Path(__file__).resolve().parent

# Estados de chamada do Android (TelephonyManager.CALL_STATE_*)
LIVRE, TOCANDO, EM_LIGACAO = 0, 1, 2


def normalizar(numero):
    """Deixa só dígitos, * e #, sem +55 e sem o zero de longa distância."""
    n = re.sub(r"[^\d*#]", "", str(numero))
    if n.startswith("55") and len(n) >= 12:
        n = n[2:]
    if n.startswith("0") and not n.startswith("0303") and not n.startswith("0304"):
        n = n[1:]
    return n


def carregar_regras():
    prefixos = [(normalizar(p), nome) for nome, lista in config.PREFIXOS.items() for p in lista]
    numeros = {normalizar(n): nome for nome, lista in config.NUMEROS.items() for n in lista}

    arquivo = PASTA / config.ARQUIVO_BLOQUEADOS
    if arquivo.exists():
        for linha in arquivo.read_text(encoding="utf-8").splitlines():
            linha = linha.split("#", 1)[0].strip()
            if linha:
                numeros[normalizar(linha)] = "Lista bloqueados.txt"

    permitidos = {normalizar(n) for n in config.PERMITIDOS}
    return prefixos, numeros, permitidos


def motivo_para_recusar(numero, regras):
    """Devolve o nome da regra que bate com o número, ou None."""
    prefixos, numeros, permitidos = regras
    n = normalizar(numero)
    if not n or n in permitidos:
        return None
    if n in numeros:
        return numeros[n]
    for prefixo, nome in prefixos:
        if n.startswith(prefixo):
            return nome
    return None


# --- Comunicação com o celular ----------------------------------------------

def adb(*args):
    resultado = subprocess.run(["adb", *args], capture_output=True, text=True, timeout=10)
    return resultado.stdout


def checar_celular():
    if not shutil.which("adb"):
        sys.exit("Não achei o adb. Instale o Android Platform Tools (veja o README).")
    aparelhos = [l for l in adb("devices").splitlines()[1:] if l.strip().endswith("device")]
    if not aparelhos:
        sys.exit("Nenhum celular conectado. Ligue a depuração USB e rode 'adb devices'.")


def estado_da_chamada():
    """Lê (estado, número) do serviço de telefonia do Android."""
    saida = adb("shell", "dumpsys", "telephony.registry")
    estado = re.search(r"mCallState=(\d)", saida)
    numero = re.search(r"mCallIncomingNumber=(\S*)", saida)
    return (int(estado.group(1)) if estado else LIVRE,
            numero.group(1) if numero else "")


def recusar():
    adb("shell", "input", "keyevent", "KEYCODE_ENDCALL")


def registrar(numero, motivo, recusada):
    arquivo = PASTA / config.ARQUIVO_LOG
    novo = not arquivo.exists()
    with arquivo.open("a", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        if novo:
            escritor.writerow(["data_hora", "numero", "motivo", "recusada"])
        escritor.writerow([datetime.now().isoformat(timespec="seconds"), numero, motivo,
                           "sim" if recusada else "não (modo seco)"])


# --- Loop principal ---------------------------------------------------------

def monitorar(seco):
    checar_celular()
    regras = carregar_regras()
    print("Monitorando chamadas. Ctrl+C para sair." + (" (modo seco)" if seco else ""))

    ultimo_estado = LIVRE
    avisou_numero_oculto = False
    while True:
        estado, numero = estado_da_chamada()

        if estado == TOCANDO and ultimo_estado != TOCANDO:
            regras = carregar_regras()  # pega edições feitas com o script rodando
            hora = datetime.now().strftime("%H:%M:%S")
            if not numero and not avisou_numero_oculto:
                print(f"[{hora}] Chamada chegando, mas o Android não informou o número "
                      "(veja 'Número não aparece' no README).")
                avisou_numero_oculto = True

            motivo = motivo_para_recusar(numero, regras)
            if motivo:
                if not seco:
                    recusar()
                print(f"[{hora}] {'Recusada' if not seco else 'Recusaria'}: {numero} ({motivo})")
                registrar(numero, motivo, not seco)
            elif numero:
                print(f"[{hora}] Deixei tocar: {numero}")

        ultimo_estado = estado
        time.sleep(config.INTERVALO)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--seco", action="store_true", help="só mostra o que faria, sem recusar")
    parser.add_argument("--testar", nargs="+", metavar="NUMERO", help="testa um número contra as regras")
    args = parser.parse_args()

    if args.testar:
        numero = " ".join(args.testar)
        motivo = motivo_para_recusar(numero, carregar_regras())
        print(f"{numero} -> {'RECUSAR (' + motivo + ')' if motivo else 'deixar tocar'}")
        return

    try:
        monitorar(args.seco)
    except KeyboardInterrupt:
        print("\nParado.")


if __name__ == "__main__":
    main()
