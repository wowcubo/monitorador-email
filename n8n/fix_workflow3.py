import json, subprocess

API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2MGY3M2FlOS1lMTJjLTRlOWQtODcxZS01MzM3YTQ1NmIyNmQiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwianRpIjoiZmU0OThkMGYtYjFkNy00M2MzLTk2OTYtODNhZTg2ZmY3ZGQwIiwiaWF0IjoxNzc0NTg5NTk1fQ.bapqwXas8ViVouXt7kFLK-J1ev2B5xhf3C52O8rnMsM"
WF_ID = "e76WAPogOMQOJjJa"
BASE = "https://wowcubo.app.n8n.cloud/api/v1"

result = subprocess.run(
    ["curl", "-s", "-X", "GET", f"{BASE}/workflows/{WF_ID}",
     "-H", f"X-N8N-API-KEY: {API_KEY}",
     "-H", "Content-Type: application/json"],
    capture_output=True, text=True
)
wf = json.loads(result.stdout)

# 1. Add a "Montar Prompt" Code node between Gmail and Claude API
montar_prompt = {
    "parameters": {
        "jsCode": """const email = $input.first().json;

const prompt = `Voce e um assistente especializado em classificar e-mails corporativos. Analise o e-mail abaixo e retorne APENAS um JSON valido, sem markdown, sem code blocks, sem explicacao.

Categorias: Financeiro, Suporte, Vendas, Administrativo, Sistema, Spam
Urgencia: 1 (informativo) a 5 (critico)
Anomalia: true se remetente suspeito, phishing, solicitacao financeira urgente inesperada, erro de sistema, ou padrao incomum.

De: ${email.From || 'desconhecido'}
Assunto: ${email.Subject || 'sem assunto'}
Conteudo: ${email.snippet || 'sem conteudo'}

Retorne este JSON preenchido:
{"categoria": "string", "urgencia": 1, "anomalia": false, "motivo_anomalia": "string ou null", "resumo": "resumo em 1 linha", "acao_sugerida": "o que fazer", "departamento_destino": "string ou null", "tags": ["tag1"]}`;

return [{
  json: {
    model: "claude-haiku-4-5-20251001",
    max_tokens: 1024,
    messages: [{ role: "user", content: prompt }]
  }
}];"""
    },
    "name": "Montar Prompt",
    "type": "n8n-nodes-base.code",
    "typeVersion": 2,
    "position": [390, 300]
}

# 2. Update Claude API node - use raw JSON body from previous node
for node in wf['nodes']:
    if node['name'] == 'Claude API Classificar':
        node['parameters']['sendBody'] = True
        node['parameters']['specifyBody'] = "json"
        node['parameters']['jsonBody'] = "={{ JSON.stringify($json) }}"
        node['position'] = [590, 300]
    elif node['name'] == 'Processar Resposta':
        node['position'] = [850, 300]
    elif node['name'] == 'Salvar no Google Sheets':
        node['position'] = [1110, 300]

# Add the new node
wf['nodes'].append(montar_prompt)

# Fix connections
wf['connections'] = {
    "Gmail - Emails Novos": {
        "main": [[{"node": "Montar Prompt", "type": "main", "index": 0}]]
    },
    "Montar Prompt": {
        "main": [[{"node": "Claude API Classificar", "type": "main", "index": 0}]]
    },
    "Claude API Classificar": {
        "main": [[{"node": "Processar Resposta", "type": "main", "index": 0}]]
    },
    "Processar Resposta": {
        "main": [[{"node": "Salvar no Google Sheets", "type": "main", "index": 0}]]
    }
}

update = {
    'nodes': wf['nodes'],
    'connections': wf['connections'],
    'settings': {'executionOrder': 'v1'},
    'name': wf['name']
}

with open('C:/Users/Ricardo/claude-code/monitorador-email/wf_update.json', 'w') as f:
    json.dump(update, f)

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
    for n in resp['nodes']:
        print(f"  {n['name']} pos={n['position']}")
