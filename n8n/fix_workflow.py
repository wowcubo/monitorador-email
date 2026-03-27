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

# Fix Claude API node - use Gmail field names
claude_body = '={\n  "model": "claude-haiku-4-5-20251001",\n  "max_tokens": 1024,\n  "messages": [\n    {\n      "role": "user",\n      "content": "Voce e um assistente especializado em classificar e-mails corporativos. Analise o e-mail abaixo e retorne APENAS um JSON valido, sem markdown, sem code blocks, sem explicacao.\\n\\nCategorias: Financeiro, Suporte, Vendas, Administrativo, Sistema, Spam\\nUrgencia: 1 (informativo) a 5 (critico)\\nAnomalia: true se remetente suspeito, phishing, solicitacao financeira urgente inesperada, erro de sistema, ou padrao incomum.\\n\\nDe: {{ $json.From }}\\nAssunto: {{ $json.Subject }}\\nConteudo: {{ $json.snippet }}\\n\\nRetorne JSON:\\n{\\n  \\"categoria\\": \\"string\\",\\n  \\"urgencia\\": 1-5,\\n  \\"anomalia\\": true/false,\\n  \\"motivo_anomalia\\": \\"string ou null\\",\\n  \\"resumo\\": \\"resumo em 1 linha\\",\\n  \\"acao_sugerida\\": \\"o que fazer\\",\\n  \\"departamento_destino\\": \\"string ou null\\",\\n  \\"tags\\": [\\"tag1\\"]\\n}"\n    }\n  ]\n}'

# Fix Processar Resposta - use $input and $() properly
process_code = """const items = $input.all();
const results = [];
for (const item of items) {
  try {
    const content = item.json.content[0].text;
    let jsonStr = content;
    jsonStr = jsonStr.replace(/```json\\n?/g, '').replace(/```\\n?/g, '');
    const jsonMatch = jsonStr.match(/\\{[\\s\\S]*\\}/);
    if (jsonMatch) jsonStr = jsonMatch[0];
    const classificacao = JSON.parse(jsonStr);

    const urgencia = classificacao.urgencia || 0;
    const anomalia = classificacao.anomalia || false;
    let alerta = 'normal';
    if (urgencia >= 4) alerta = 'urgente';
    else if (anomalia === true) alerta = 'anomalia';

    const gmailData = $('Gmail - Emails Novos').first().json;

    results.push({ json: {
      email_de: gmailData.From || '',
      email_assunto: gmailData.Subject || '',
      email_data: new Date(parseInt(gmailData.internalDate || '0')).toISOString(),
      ...classificacao,
      alerta: alerta,
      processado_em: new Date().toISOString()
    }});
  } catch (e) {
    results.push({ json: { erro: 'Falha ao processar resposta da IA', detalhes: e.message, alerta: 'erro' } });
  }
}
return results;"""

for node in wf['nodes']:
    if node['name'] == 'Claude API Classificar':
        node['parameters']['jsonBody'] = claude_body
    elif node['name'] == 'Processar Resposta':
        node['parameters']['jsCode'] = process_code

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
    print(f"OK - {resp['name']} atualizado")

    # Verify
    for n in resp['nodes']:
        if n['name'] == 'Processar Resposta':
            code = n['parameters']['jsCode']
            has_input = '$input.all()' in code
            has_gmail = "$('Gmail" in code
            print(f"  $input.all(): {'OK' if has_input else 'MISSING'}")
            print(f"  $('Gmail...'): {'OK' if has_gmail else 'MISSING'}")
