"""
Re-autoriza o LinkedIn OAuth com escopos adicionais de leitura de perfil.

Uso:
    python src/scripts/linkedin_auth.py

Fluxo:
    1. Abre o link de autorização no terminal
    2. Você clica, aprova no LinkedIn
    3. O servidor local captura o callback
    4. Troca o code pelo token e salva no .env
"""

import http.server
import os
import sys
import urllib.parse
import urllib.request
import json
import webbrowser
from pathlib import Path
from dotenv import load_dotenv, set_key

load_dotenv()

REDIRECT_URI = "http://localhost:8888/callback"
SCOPES = "openid profile email r_liteprofile w_member_social"

ROOT = Path(__file__).resolve().parents[2]
ENV_PATH = ROOT / ".env"

# ─── Servidor de callback ─────────────────────────────────────────────────────

captured_code = None


class CallbackHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        global captured_code
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)

        if "error" in params:
            error = params["error"][0]
            desc = params.get("error_description", [""])[0]
            self.send_response(400)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(
                f"<h2>Erro: {error}</h2><p>{desc}</p>".encode("utf-8")
            )
            print(f"\n[ERRO] LinkedIn retornou: {error} — {desc}")
            return

        code = params.get("code", [None])[0]
        if code:
            captured_code = code
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(
                b"<h2>&#10003; Autorizado!</h2>"
                b"<p>Pode fechar esta aba. O token foi salvo no .env.</p>"
            )
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Parametro 'code' nao encontrado.")

    def log_message(self, format, *args):
        pass  # silencia logs do servidor


# ─── OAuth ───────────────────────────────────────────────────────────────────

def build_auth_url(client_id: str, state: str = "linkedin_reauth") -> str:
    params = urllib.parse.urlencode({
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPES,
        "state": state,
    })
    return f"https://www.linkedin.com/oauth/v2/authorization?{params}"


def exchange_code_for_token(code: str, client_id: str, client_secret: str) -> dict:
    body = urllib.parse.urlencode({
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": client_id,
        "client_secret": client_secret,
    }).encode()

    req = urllib.request.Request(
        "https://www.linkedin.com/oauth/v2/accessToken",
        data=body,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


def save_token(token_data: dict):
    access_token = token_data.get("access_token", "")
    set_key(str(ENV_PATH), "LINKEDIN_ACCESS_TOKEN", access_token)
    if "refresh_token" in token_data:
        set_key(str(ENV_PATH), "LINKEDIN_REFRESH_TOKEN", token_data["refresh_token"])
    scope = token_data.get("scope", "")
    expires_in = token_data.get("expires_in", "?")
    print(f"  Escopos concedidos : {scope}")
    print(f"  Expira em          : {expires_in}s (~{int(expires_in)//86400} dias)")


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    client_id = os.getenv("LINKEDIN_CLIENT_ID")
    client_secret = os.getenv("LINKEDIN_CLIENT_SECRET")

    if not client_id or not client_secret:
        print("[ERRO] LINKEDIN_CLIENT_ID ou LINKEDIN_CLIENT_SECRET não encontrados no .env")
        sys.exit(1)

    auth_url = build_auth_url(client_id)

    print("\n" + "=" * 60)
    print("  REAUTORIZAÇÃO LINKEDIN")
    print("=" * 60)
    print(f"\nEscopos solicitados: {SCOPES}\n")
    print("Abrindo navegador... Se não abrir automaticamente, acesse:")
    print(f"\n  {auth_url}\n")
    print("Aguardando callback em http://localhost:8888 ...")
    print("=" * 60)

    webbrowser.open(auth_url)

    server = http.server.HTTPServer(("localhost", 8888), CallbackHandler)
    server.timeout = 120  # 2 minutos para o usuário aprovar

    while captured_code is None:
        server.handle_request()
        if captured_code is None and server.timeout:
            # timeout hit — verifica uma vez mais
            break

    if not captured_code:
        print("\n[ERRO] Tempo esgotado. Nenhum code recebido.")
        sys.exit(1)

    print("\nCode recebido. Trocando pelo token...")

    try:
        token_data = exchange_code_for_token(captured_code, client_id, client_secret)
    except urllib.error.HTTPError as e:
        print(f"[ERRO] Falha ao trocar code: HTTP {e.code} — {e.read().decode()}")
        sys.exit(1)

    save_token(token_data)

    print("\n✓ Token salvo no .env com sucesso!")

    # Verifica o que conseguimos ler agora
    print("\nTestando acesso ao perfil...")
    token = token_data["access_token"]

    for name, url in [
        ("userinfo (OpenID)", "https://api.linkedin.com/v2/userinfo"),
        ("liteprofile", "https://api.linkedin.com/v2/me?projection=(id,firstName,lastName,headline,location,summary)"),
    ]:
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
        try:
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read())
                print(f"\n  ✓ {name}:")
                print(f"    {json.dumps(data, ensure_ascii=False)[:200]}")
        except urllib.error.HTTPError as e:
            print(f"  ✗ {name}: HTTP {e.code}")


if __name__ == "__main__":
    main()
