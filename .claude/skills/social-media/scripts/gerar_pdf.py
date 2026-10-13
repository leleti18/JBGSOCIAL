#!/usr/bin/env python3
"""Gera o PDF de roteiro de social media a partir de um posts.json.

Uso: gerar_pdf.py posts.json saida.pdf
"""
import json
import sys
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (PageBreak, Paragraph, SimpleDocTemplate,
                                Spacer, Table, TableStyle)

ACCENT = colors.HexColor("#6C3CE1")
LIGHT = colors.HexColor("#F1EDFC")

ss = getSampleStyleSheet()
H1 = ParagraphStyle("H1", parent=ss["Title"], textColor=ACCENT, fontSize=26, leading=30)
H2 = ParagraphStyle("H2", parent=ss["Heading2"], textColor=ACCENT, spaceBefore=10)
BODY = ParagraphStyle("B", parent=ss["BodyText"], fontSize=10, leading=14)
SMALL = ParagraphStyle("S", parent=BODY, fontSize=8, textColor=colors.grey)


def p(text, style=BODY):
    return Paragraph(escape(str(text or "—")).replace("\n", "<br/>"), style)


def kv_table(rows):
    data = [[p(k, ParagraphStyle("k", parent=BODY, fontName="Helvetica-Bold")), p(v)]
            for k, v in rows]
    t = Table(data, colWidths=[3.8 * cm, 12.7 * cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), LIGHT),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.lightgrey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return t


def grid(header, rows, widths):
    data = [[p(h, ParagraphStyle("h", parent=BODY, textColor=colors.white,
                                 fontName="Helvetica-Bold")) for h in header]]
    data += [[p(c) for c in r] for r in rows]
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), ACCENT),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT]),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.lightgrey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return t


def build(data, out):
    doc = SimpleDocTemplate(out, pagesize=A4, leftMargin=2.2 * cm, rightMargin=2.2 * cm,
                            topMargin=2 * cm, bottomMargin=2 * cm,
                            title=f"Roteiro — {data.get('cliente', '')}")
    s = []
    s += [Spacer(1, 6 * cm), p("Roteiro de Conteúdo", H1),
          p(data.get("cliente"), ParagraphStyle("c", parent=BODY, fontSize=16)),
          p(data.get("periodo"), BODY), PageBreak()]

    est = data.get("estrategia", {})
    s.append(p("Estratégia", H2))
    s.append(kv_table([("Objetivo", est.get("objetivo")), ("Público", est.get("publico")),
                       ("Tom de voz", est.get("tom")),
                       ("Pilares", ", ".join(est.get("pilares", [])))]))
    s.append(Spacer(1, 0.6 * cm))

    posts = data.get("posts", [])
    s.append(p("Calendário", H2))
    s.append(grid(["Data", "Rede", "Formato", "Pilar", "Tema"],
                  [[x.get("data"), x.get("plataforma"), x.get("formato"),
                    x.get("pilar"), x.get("tema")] for x in posts],
                  [2.3 * cm, 2.5 * cm, 2.7 * cm, 3.2 * cm, 5.8 * cm]))

    for i, x in enumerate(posts, 1):
        s += [PageBreak(),
              p(f"Post {i} — {x.get('tema')}", H2),
              p(f"{x.get('data')} · {x.get('plataforma')} · {x.get('formato')}", SMALL),
              Spacer(1, 0.3 * cm),
              kv_table([("Pilar", x.get("pilar")), ("Objetivo", x.get("objetivo")),
                        ("Gancho", x.get("gancho")), ("CTA", x.get("cta")),
                        ("Direção de arte", x.get("direcao_arte")),
                        ("Áudio", x.get("audio")),
                        ("Link Canva", x.get("link_canva"))])]
        if x.get("roteiro"):
            s += [p("Roteiro", H2),
                  grid(["Cena", "Tempo", "Visual", "Fala / texto"],
                       [[c.get("cena"), c.get("tempo"), c.get("visual"),
                         c.get("fala_texto")] for c in x["roteiro"]],
                       [1.4 * cm, 2 * cm, 6.5 * cm, 6.6 * cm])]
        s += [p("Legenda", H2), p(x.get("legenda")),
              p(" ".join(x.get("hashtags", [])), SMALL)]
        if x.get("observacoes"):
            s += [p("Observações", H2), p(x["observacoes"])]

    doc.build(s)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    with open(sys.argv[1], encoding="utf-8") as f:
        build(json.load(f), sys.argv[2])
    print("PDF gerado:", sys.argv[2])
