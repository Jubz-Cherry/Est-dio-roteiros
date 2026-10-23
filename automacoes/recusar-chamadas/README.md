# Recusar chamadas de operadoras

Script em Python que fica de olho no seu celular **Android** e derruba na hora as chamadas de telemarketing e das operadoras (Vivo, Claro, TIM, Oi…). Ele roda no computador e fala com o celular pelo **ADB**, a ferramenta oficial do Android para desenvolvedores. Não precisa de root.

> **iPhone:** a Apple não deixa nenhum programa externo recusar chamadas, então não dá para fazer isso com Python no iPhone. Veja as alternativas no fim.

## Arquivos

| Arquivo | O que é |
|---|---|
| `recusar_chamadas.py` | O programa |
| `config.py` | As regras: prefixos, números das operadoras, permitidos, intervalo |
| `bloqueados.txt` | Lista extra de números, um por linha, para ir colando sem mexer no código |
| `recusadas.csv` | Criado sozinho, com cada chamada recusada (data, número, motivo) |

## Como usar

1. **Instale o Python 3** (python.org) e o **Android Platform Tools** (developer.android.com/tools/releases/platform-tools). Coloque a pasta do Platform Tools no PATH para o comando `adb` funcionar no terminal.
2. **No celular**, ative as Opções do desenvolvedor (Configurações → Sobre o telefone → toque 7 vezes em "Número da versão") e ligue a **Depuração USB**.
3. Conecte o cabo, aceite o aviso no celular e confira:
   ```
   adb devices
   ```
   O celular tem que aparecer como `device`.
4. Teste as regras sem precisar do celular:
   ```
   python recusar_chamadas.py --testar 0303 123 4567
   ```
5. Rode primeiro no modo seco (só avisa, não recusa) e depois pra valer:
   ```
   python recusar_chamadas.py --seco
   python recusar_chamadas.py
   ```

Para não depender do cabo, dá para usar ADB por Wi-Fi (Android 11+: Opções do desenvolvedor → Depuração por Wi-Fi → `adb pair` e `adb connect`). O computador precisa estar ligado e na mesma rede.

## Mudando as regras

Tudo fica em `config.py`:

- `PREFIXOS`: recusa todo número que começar com o prefixo. Já vem com **0303** e **0304**, os prefixos que a Anatel obriga o telemarketing a usar. Só isso já pega a maior parte das ofertas de operadora.
- `NUMEROS`: números exatos, separados por operadora. Para incluir outra, é só acrescentar uma linha, por exemplo `"Nextel": ["1050"],`.
- `PERMITIDOS`: números que nunca são recusados (o seu banco, por exemplo).
- `INTERVALO`: de quanto em quanto tempo o celular é consultado.

Pode escrever os números como aparecem no celular: espaços, traços, `+55` e o zero da frente são ignorados. O script relê as regras a cada chamada, então dá para editar com ele rodando.

## Como funciona

A cada `INTERVALO` segundos o script roda `adb shell dumpsys telephony.registry`, que informa se o celular está tocando e qual número está ligando. Se o número cair numa regra, ele manda `adb shell input keyevent KEYCODE_ENDCALL`, que é o mesmo que apertar "recusar".

Quer mudar o jeito de recusar ou de identificar o número? As funções `estado_da_chamada()` e `recusar()` são as únicas que falam com o celular.

## Problemas comuns

- **Número não aparece:** em alguns Android recentes ou de certas marcas, o sistema esconde o número no `dumpsys`. O script avisa no terminal quando isso acontece; nesse caso ele não consegue saber quem está ligando. Confira com `adb shell dumpsys telephony.registry | grep mCallIncomingNumber` enquanto alguém liga para você.
- **A chamada não cai:** algumas marcas ignoram o `KEYCODE_ENDCALL`. Teste com `adb shell input keyevent KEYCODE_ENDCALL` durante uma chamada.
- **Operadora liga de número comum:** coloque o número em `bloqueados.txt`.

## Alternativas sem computador

- **Não Me Perturbe** (naomeperturbe.com.br): cadastro oficial e gratuito que proíbe as operadoras de ligar oferecendo produtos. Vale fazer de qualquer jeito.
- **Android:** o app Telefone do Google tem "Filtrar chamadas de spam" e bloqueio de números.
- **iPhone:** Ajustes → Telefone → "Silenciar Desconhecidos", ou apps de bloqueio como o Truecaller, que bloqueiam por lista.
