# Monitorador de E-mail Inteligente - Setup

## Visão Geral

```
[IMAP Trigger 1h] → [Claude Haiku API] → [Google Sheets] → [Switch] → [Alertas]
```

Monitora `monitoramento.atividades@wowcubo.com.br` a cada 1 hora, classifica e-mails com IA e alerta sobre urgências e anomalias.

---

## Passo a Passo

### 1. Criar a API Key da Anthropic

1. Acesse: https://console.anthropic.com/
2. Crie uma conta (se ainda não tem)
3. Vá em **API Keys** → **Create Key**
4. Copie a chave (começa com `sk-ant-...`)
5. Adicione créditos: **$5 é suficiente para meses de uso**

### 2. Criar a Google Sheets

1. Crie uma planilha nova no Google Sheets
2. Renomeie a primeira aba para **Log**
3. Adicione os cabeçalhos na linha 1 (ver `sheets/template-colunas.md`):
   ```
   email_de | email_assunto | email_data | categoria | urgencia | anomalia | motivo_anomalia | resumo | acao_sugerida | departamento_destino | tags | processado_em
   ```
4. Copie a URL da planilha (vai precisar no n8n)

### 3. Importar o Workflow no n8n

1. Acesse: https://wowcubo.app.n8n.cloud/
2. Vá em **Workflows** → **Add Workflow** → **Import from File**
3. Selecione: `n8n/workflow-monitorador-email.json`

### 4. Configurar Credenciais no n8n

#### 4.1 IMAP (Leitura de E-mail)

1. No n8n: **Credentials** → **Add Credential** → **IMAP**
2. Configure:
   - **Host**: servidor IMAP do wowcubo.com.br (pegar com provedor)
   - **Port**: 993
   - **User**: `monitoramento.atividades@wowcubo.com.br`
   - **Password**: senha do e-mail
   - **SSL**: ativado
3. No node "Ler E-mails Novos", selecione essa credencial

#### 4.2 Anthropic API Key

1. No n8n: **Credentials** → **Add Credential** → **Header Auth**
2. Configure:
   - **Name**: `x-api-key`
   - **Value**: `sk-ant-...` (sua chave)
3. No node "Claude API - Classificar", selecione essa credencial

#### 4.3 Google Sheets

1. No n8n: **Credentials** → **Add Credential** → **Google Sheets OAuth2**
2. Siga o fluxo de autenticação do Google
3. No node "Salvar no Google Sheets":
   - Cole a URL da planilha
   - Selecione a aba "Log"

#### 4.4 SMTP (Envio de Alertas)

1. No n8n: **Credentials** → **Add Credential** → **SMTP**
2. Configure com os dados SMTP do wowcubo.com.br
3. Nos nodes de alerta, configure o campo "Para" com seu e-mail pessoal

### 5. Testar

1. Envie um e-mail de teste para `monitoramento.atividades@wowcubo.com.br`
2. No n8n, clique em **Test Workflow** (execução manual)
3. Verifique:
   - [ ] E-mail foi lido
   - [ ] Claude classificou corretamente
   - [ ] Registro apareceu no Google Sheets
   - [ ] Alerta foi enviado (se urgência >= 4 ou anomalia)

### 6. Ativar

1. No n8n, ative o workflow (toggle no canto superior direito)
2. Ele vai rodar automaticamente a cada 1 hora

---

## Estrutura do Projeto

```
monitorador-email/
├── SETUP.md                              ← este arquivo
├── prompt/
│   └── classificador.md                  ← prompt completo da IA
├── n8n/
│   └── workflow-monitorador-email.json   ← workflow para importar
└── sheets/
    └── template-colunas.md               ← estrutura da planilha
```

## Custos Estimados

| Item | Custo Mensal |
|------|-------------|
| n8n Cloud (plano atual) | $0 |
| Claude Haiku API (~720 emails/mês) | ~$1-3 |
| Google Sheets | $0 |
| **Total** | **~$1-3/mês** |

## Evolução (Fases Futuras)

- **Fase 2**: Respostas automáticas para categorias simples
- **Fase 3**: Encaminhamento automático por departamento
- **Fase 4**: Integração WhatsApp (BotConversa)
- **Fase 5**: Dashboard com métricas e tendências
