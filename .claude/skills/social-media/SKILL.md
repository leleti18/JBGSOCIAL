---
name: social-media
description: Gestão de social media de ponta a ponta — analisa o perfil do cliente, define estratégia e pilares, monta calendário editorial, cria posts (legenda, roteiro, arte no Canva) e gera o PDF de roteiro com especificações. Use quando pedirem análise de perfil/Instagram/TikTok, calendário de conteúdo, criação de posts, carrosséis, reels, roteiros ou PDF de planejamento de redes sociais.
---

# Social Media

Fluxo integrado: **Briefing → Análise do perfil → Estratégia → Calendário → Posts → Arte (Canva) → PDF de roteiro**.

Dados de cada cliente ficam em `clientes/<slug>/` (copie `clientes/_modelo/`). Nunca grave senhas/tokens em arquivos do repositório; acessos ficam só na sessão ou em variáveis de ambiente.

## Etapas

### 1. Briefing
Leia `clientes/<slug>/briefing.md`. Se faltar algo, use o checklist em `references/briefing-checklist.md` e pergunte antes de seguir.

### 2. Análise do perfil
Colete (via link público, dados enviados ou ferramentas disponíveis): bio, destaques, grade, frequência, formatos, engajamento, melhores/piores posts, tom de voz, concorrentes (3–5).
Entregue no formato de `references/analise-perfil.md`: diagnóstico, oportunidades, riscos e 3 prioridades.

### 3. Estratégia
Defina objetivo (SMART), público/persona, 3–5 pilares de conteúdo com % de mix, tom de voz, formatos e frequência. Salve em `clientes/<slug>/estrategia.md`.

### 4. Calendário editorial
Gere `clientes/<slug>/calendario.csv` com colunas:
`data, dia_semana, plataforma, formato, pilar, tema, gancho, objetivo, cta, status`
Considere datas comemorativas, lançamentos e horários de pico do perfil. Mês padrão = 12–20 posts, salvo pedido diferente.

### 5. Posts
Para cada item do calendário, preencha o modelo de `references/roteiro-modelo.md`:
gancho (0–3s), roteiro cena a cena (reels/vídeo) ou slide a slide (carrossel), legenda final, hashtags, CTA, direção de arte, trilha/áudio, referências.

### 6. Arte no Canva
Use as ferramentas Canva (`list-brand-kits` → aplicar kit da marca; `generate-design` / `create-design-from-brand-template` / `autofill-design`; `export-design` para PNG/PDF). Registre o link de cada design no calendário (coluna `link_canva`). Sem brand kit, pergunte cores/fontes/logo antes de criar.

### 7. PDF de roteiro
Monte `clientes/<slug>/posts.json` (estrutura em `references/roteiro-modelo.md`) e rode:
```
python3 .claude/skills/social-media/scripts/gerar_pdf.py clientes/<slug>/posts.json clientes/<slug>/roteiro.pdf
```
O PDF tem capa, resumo da estratégia, calendário e uma página por post com todas as especificações.

## Regras
- Português do Brasil, no tom de voz definido no briefing.
- Todo post tem gancho, CTA e objetivo mensurável.
- Respeitar limites das plataformas (legenda IG 2.200 caracteres, até 30 hashtags — usar 5–10 relevantes).
- Não inventar métricas: se não tiver acesso ao dado, marque "a confirmar".
- Aprovação do cliente antes de qualquer publicação ou envio externo.
