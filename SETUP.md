# Monitorador de E-mail Inteligente

## Visao Geral

```
[Gmail Trigger 1h] → [Montar Prompt] → [Claude Haiku API] → [Processar Resposta] → [Google Sheets]
```

Monitora `monitoramento.atividades@wowcubo.com.br` a cada 1 hora, classifica e-mails com IA e registra no Google Sheets.

## Links do Projeto

| Recurso | URL |
|---------|-----|
| n8n Cloud | https://wowcubo.app.n8n.cloud/ |
| Workflow | https://wowcubo.app.n8n.cloud/workflow/e76WAPogOMQOJjJa |
| Google Sheets | https://docs.google.com/spreadsheets/d/1yMNQaeHXTZ0ct5IRSY08EJEyhRehKdmL70MvlgtQ668 |
| GitHub | https://github.com/wowcubo/monitorador-email |

## Arquitetura

### Nodes do Workflow

| Node | Tipo | Funcao |
|------|------|--------|
| Gmail - Emails Novos | Gmail Trigger | Le emails novos a cada 60 min |
| Montar Prompt | Code | Monta o body JSON para a API do Claude |
| Claude API Classificar | HTTP Request | Envia email para Claude Haiku classificar |
| Processar Resposta | Code | Parseia JSON da resposta e monta dados |
| Salvar no Google Sheets | Google Sheets | Registra classificacao na planilha |

### Credenciais Configuradas no n8n

| Credencial | Tipo | ID |
|------------|------|----|
| Gmail - monitoramento.atividades@wowcubo.com.br | Gmail OAuth2 | XirkAAAoxac8gEDo |
| Anthropic API Key - Monitorador | Header Auth | GPLcpmDpmzjLfPYU |
| Google Sheets account 5 | Google Sheets OAuth2 | 7oCMUv1ewFSIrgV0 |

### Classificacao da IA

**Categorias:** Financeiro, Suporte, Vendas, Administrativo, Sistema, Spam

**Urgencia:** 1 (informativo) a 5 (critico)

**Anomalia:** detecta remetentes suspeitos, phishing, solicitacoes financeiras inesperadas, erros de sistema

### Campos da Planilha (aba "Log")

```
email_de | email_assunto | email_data | categoria | urgencia | anomalia | motivo_anomalia | resumo | acao_sugerida | departamento_destino | tags | alerta | processado_em
```

## Custos Estimados

| Item | Custo Mensal |
|------|-------------|
| n8n Cloud (plano atual) | $0 |
| Claude Haiku API (~720 emails/mes) | ~$1-3 |
| Google Sheets | $0 |
| **Total** | **~$1-3/mes** |

## Estrutura do Projeto

```
monitorador-email/
├── SETUP.md                                        ← este arquivo
├── prompt/
│   └── classificador.md                            ← prompt completo da IA
├── n8n/
│   ├── backup-workflow-e76WAPogOMQOJjJa.json       ← backup do workflow atual do n8n
│   ├── api-create-workflow.json                    ← JSON base de criacao
│   ├── fix_workflow.py                             ← script de correcao v1
│   ├── fix_workflow2.py                            ← script de correcao v2
│   ├── fix_workflow3.py                            ← script de correcao v3 (final)
│   └── workflow-monitorador-email.json             ← versao original (nao usar)
└── sheets/
    └── template-colunas.md                         ← estrutura da planilha
```

## Evolucao (Fases Futuras)

| Fase | Descricao | Status |
|------|-----------|--------|
| 1 | Classificar emails + salvar no Sheets | Concluido |
| 2 | Alertas por email (urgencia >= 4, anomalias) | Pendente |
| 3 | Respostas automaticas para categorias simples | Pendente |
| 4 | Encaminhamento automatico por departamento | Pendente |
| 5 | Integracao WhatsApp (BotConversa) | Pendente |
| 6 | Dashboard com metricas e tendencias | Pendente |

## Alertas (configurar na Fase 2)

- **Urgente** (urgencia >= 4): email para ricardo@wowcubo.com.br
- **Anomalia** (anomalia = true): email para ricardo@wowcubo.com.br
- **Normal**: apenas registra no Sheets
