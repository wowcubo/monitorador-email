# Template Google Sheets - Monitorador de E-mail

## Nome da planilha: Monitorador E-mail WowCubo

### Aba: Log

Crie uma planilha Google Sheets com as seguintes colunas na aba "Log":

| Coluna | Nome | Formato | Descrição |
|--------|------|---------|-----------|
| A | email_de | Texto | Remetente do e-mail |
| B | email_assunto | Texto | Assunto do e-mail |
| C | email_data | Data/Hora | Data de recebimento |
| D | categoria | Texto | Financeiro, Suporte, Vendas, Administrativo, Sistema, Spam |
| E | urgencia | Número | 1 a 5 |
| F | anomalia | Booleano | TRUE / FALSE |
| G | motivo_anomalia | Texto | Motivo se for anomalia |
| H | resumo | Texto | Resumo em 1 linha |
| I | acao_sugerida | Texto | Ação recomendada pela IA |
| J | departamento_destino | Texto | Para quem encaminhar |
| K | tags | Texto | Tags separadas por vírgula |
| L | processado_em | Data/Hora | Timestamp do processamento |

### Aba: Dashboard (futura)

Para fase 2, adicionar aba com:
- Contagem por categoria (gráfico pizza)
- E-mails por dia (gráfico linha)
- Anomalias no mês
- Urgência média

### Formatação condicional sugerida

- **Urgência 4-5**: linha com fundo vermelho claro
- **Anomalia = TRUE**: linha com fundo amarelo
- **Categoria = Spam**: texto cinza
