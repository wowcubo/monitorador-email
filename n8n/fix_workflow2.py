import json, subprocess

API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2MGY3M2FlOS1lMTJjLTRlOWQtODcxZS01MzM3YTQ1NmIyNmQiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwianRpIjoiZmU0OThkMGYtYjFkNy00M2MzLTk2OTYtODNhZTg2ZmY3ZGQwIiwiaWF0IjoxNzc0NTg5NTk1fQ.bapqwXas8ViVouXt7kFLK-J1ev2B5xhf3C52O8rnMsM"
WF_ID = "e76WAPogOMQOJjJa"
BASE = "https://wowcubo.app.n8n.cloud/api/v1"

# Get current workflow
result = subprocess.run(
    ["curl", "-s", "-X", "GET", f"{BASE}/workflows/{WF_ID}",
     "-H", f"X-N8N-API-KEY: {API_KEY}",
     "-H", "Content-Type: application/json"],
    capture_output=True, text=True
)
wf = json.loads(result.stdout)

# Build the JSON body as a proper n8n expression
# Use ={{ }} expressions for dynamic parts
prompt = (
    "Voce e um assistente especializado em classificar e-mails corporativos. "
    "Analise o e-mail abaixo e retorne APENAS um JSON valido, sem markdown, sem code blocks, sem explicacao. "
    "Categorias: Financeiro, Suporte, Vendas, Administrativo, Sistema, Spam. "
    "Urgencia: 1 (informativo) a 5 (critico). "
    "Anomalia: true se remetente suspeito, phishing, solicitacao financeira urgente inesperada, erro de sistema, ou padrao incomum. "
    "De: {{ $json.From }} "
    "Assunto: {{ $json.Subject }} "
    "Conteudo: {{ $json.snippet }} "
    "Retorne este JSON preenchido: "
    '{"categoria": "string", "urgencia": 1, "anomalia": false, "motivo_anomalia": "string ou null", '
    '"resumo": "resumo em 1 linha", "acao_sugerida": "o que fazer", "departamento_destino": "string ou null", '
    '"tags": ["tag1"]}'
)

# Build as a valid JSON that n8n will parse
json_body_obj = {
    "model": "claude-haiku-4-5-20251001",
    "max_tokens": 1024,
    "messages": [
        {
            "role": "user",
            "content": prompt
        }
    ]
}

# n8n expects the jsonBody as a string starting with = for expressions
json_body_str = "=" + json.dumps(json_body_obj, ensure_ascii=False)

for node in wf['nodes']:
    if node['name'] == 'Claude API Classificar':
        node['parameters']['jsonBody'] = json_body_str
        print(f"Updated jsonBody ({len(json_body_str)} chars)")

update = {
    'nodes': wf['nodes'],
    'connections': wf['connections'],
    'settings': {'executionOrder': 'v1'},
    'name': wf['name']
}

with open('C:/Users/Ricardo/claude-code/monitorador-email/wf_update.json', 'w') as f:
    json.dump(update, f)

# Push update
result = subprocess.run(
    ["curl", "-s", "-X", "PUT", f"{BASE}/workflows/{WF_ID}",
     "-H", f"X-N8N-API-KEY: {API_KEY}",
     "-H", "Content-Type: application/json",
     "-d", f"@C:/Users/Ricardo/claude-code/monitorador-email/wf_update.json"],
    capture_output=True, text=True
)
resp = json.loads(result.stdout)
if 'message' in resp:
    print(f"ERROR: {resp['message']}")
else:
    print(f"OK - workflow atualizado")
