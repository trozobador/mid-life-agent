import json
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


ACCENT = colors.HexColor("#1a5276")
DARK   = colors.HexColor("#1c1c1c")
GRAY   = colors.HexColor("#555555")
LIGHT  = colors.HexColor("#888888")

PAGE_W, PAGE_H = A4
MARGIN_H = 1.5 * cm
MARGIN_V = 1.2 * cm


def _styles():
    base = {"fontName": "Helvetica", "leading": 11, "textColor": DARK}
    return {
        "name":    ParagraphStyle("name",    fontSize=18, fontName="Helvetica-Bold",
                                  textColor=ACCENT, leading=22, spaceAfter=1),
        "label":   ParagraphStyle("label",   fontSize=9,  fontName="Helvetica",
                                  textColor=GRAY,  leading=12, spaceAfter=2),
        "contact": ParagraphStyle("contact", fontSize=8,  fontName="Helvetica",
                                  textColor=GRAY,  leading=10, spaceAfter=0, alignment=TA_CENTER),
        "section": ParagraphStyle("section", fontSize=9,  fontName="Helvetica-Bold",
                                  textColor=ACCENT, leading=11, spaceBefore=5, spaceAfter=2),
        "summary": ParagraphStyle("summary", fontSize=8,  fontName="Helvetica",
                                  textColor=DARK,  leading=11, spaceAfter=3, alignment=TA_JUSTIFY),
        "job_co":  ParagraphStyle("job_co",  fontSize=8.5,fontName="Helvetica-Bold",
                                  textColor=DARK,  leading=10),
        "job_pos": ParagraphStyle("job_pos", fontSize=8,  fontName="Helvetica-Oblique",
                                  textColor=GRAY,  leading=10),
        "bullet":  ParagraphStyle("bullet",  fontSize=7.5,fontName="Helvetica",
                                  textColor=DARK,  leading=10, leftIndent=8, spaceAfter=0),
        "edu":     ParagraphStyle("edu",     fontSize=8,  fontName="Helvetica",
                                  textColor=DARK,  leading=10),
        "skill_k": ParagraphStyle("skill_k", fontSize=7.5,fontName="Helvetica-Bold",
                                  textColor=DARK,  leading=10),
        "skill_v": ParagraphStyle("skill_v", fontSize=7.5,fontName="Helvetica",
                                  textColor=DARK,  leading=10),
        "cert":    ParagraphStyle("cert",    fontSize=7.5,fontName="Helvetica",
                                  textColor=DARK,  leading=10),
        "proj":    ParagraphStyle("proj",    fontSize=7.5,fontName="Helvetica",
                                  textColor=DARK,  leading=10),
    }


def _hr():
    return HRFlowable(width="100%", thickness=0.5, color=ACCENT, spaceAfter=3)


def _fmt_date(d: str) -> str:
    if not d:
        return ""
    if d == "Present":
        return "Presente"
    parts = d.split("-")
    months = {"01":"Jan","02":"Fev","03":"Mar","04":"Abr","05":"Mai","06":"Jun",
              "07":"Jul","08":"Ago","09":"Set","10":"Out","11":"Nov","12":"Dez"}
    if len(parts) == 2:
        return f"{months.get(parts[1], parts[1])}/{parts[0]}"
    return parts[0]


def generate_pdf(json_path: str, pdf_path: str):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        leftMargin=MARGIN_H,
        rightMargin=MARGIN_H,
        topMargin=MARGIN_V,
        bottomMargin=MARGIN_V,
    )

    S = _styles()
    story = []
    basics = data.get("basics", {})
    usable_w = PAGE_W - 2 * MARGIN_H

    # ── Header ──────────────────────────────────────────────────────────
    story.append(Paragraph(basics.get("name", ""), S["name"]))
    story.append(Paragraph(basics.get("label", ""), S["label"]))

    loc = basics.get("location", {})
    city = loc.get("city", "")
    region = loc.get("region", "")
    location_str = f"{city}, {region}" if city and region else city or region

    profiles = basics.get("profiles", [])
    linkedin = next((p["url"] for p in profiles if p.get("network","").lower() == "linkedin"), "")
    contact_parts = [
        basics.get("email", ""),
        basics.get("phone", ""),
        location_str,
        linkedin,
    ]
    story.append(Paragraph("  |  ".join(p for p in contact_parts if p), S["contact"]))
    story.append(Spacer(1, 4))

    # ── Summary ─────────────────────────────────────────────────────────
    summary = basics.get("summary", "")
    if summary:
        story.append(Paragraph("RESUMO PROFISSIONAL", S["section"]))
        story.append(_hr())
        story.append(Paragraph(summary, S["summary"]))

    # ── Skills ──────────────────────────────────────────────────────────
    skills = data.get("skills", [])
    if skills:
        story.append(Paragraph("COMPETÊNCIAS", S["section"]))
        story.append(_hr())
        col_w = usable_w / 2
        pairs = []
        for skill in skills:
            name = skill.get("name", "")
            kws  = ", ".join(skill.get("keywords", []))
            pairs.append([
                Paragraph(f"<b>{name}:</b>", S["skill_k"]),
                Paragraph(kws, S["skill_v"]),
            ])
        # split into 2-column layout
        rows = []
        for i in range(0, len(pairs), 2):
            left  = pairs[i]
            right = pairs[i+1] if i+1 < len(pairs) else [Paragraph("", S["skill_v"]), Paragraph("", S["skill_v"])]
            rows.append([left[0], left[1], right[0], right[1]])

        t = Table(rows, colWidths=[col_w*0.25, col_w*0.75, col_w*0.25, col_w*0.75])
        t.setStyle(TableStyle([
            ("VALIGN", (0,0), (-1,-1), "TOP"),
            ("LEFTPADDING",  (0,0), (-1,-1), 0),
            ("RIGHTPADDING", (0,0), (-1,-1), 4),
            ("TOPPADDING",   (0,0), (-1,-1), 1),
            ("BOTTOMPADDING",(0,0), (-1,-1), 1),
        ]))
        story.append(t)
        story.append(Spacer(1, 2))

    # ── Work Experience ──────────────────────────────────────────────────
    work = data.get("work", [])
    if work:
        story.append(Paragraph("EXPERIÊNCIA PROFISSIONAL", S["section"]))
        story.append(_hr())
        for job in work:
            start = _fmt_date(job.get("startDate", ""))
            end   = _fmt_date(job.get("endDate",   ""))
            period = f"{start} – {end}" if start else end

            header = Table(
                [[Paragraph(job.get("name",""), S["job_co"]),
                  Paragraph(period, ParagraphStyle("per", fontSize=8,
                      fontName="Helvetica", textColor=LIGHT, leading=10, alignment=TA_RIGHT))]],
                colWidths=[usable_w * 0.65, usable_w * 0.35],
            )
            header.setStyle(TableStyle([
                ("LEFTPADDING",  (0,0),(-1,-1),0),
                ("RIGHTPADDING", (0,0),(-1,-1),0),
                ("TOPPADDING",   (0,0),(-1,-1),0),
                ("BOTTOMPADDING",(0,0),(-1,-1),0),
                ("VALIGN",       (0,0),(-1,-1),"BOTTOM"),
            ]))
            story.append(header)
            story.append(Paragraph(job.get("position",""), S["job_pos"]))
            for h in job.get("highlights", []):
                story.append(Paragraph(f"• {h}", S["bullet"]))
            story.append(Spacer(1, 3))

    # ── Education ────────────────────────────────────────────────────────
    education = data.get("education", [])
    if education:
        story.append(Paragraph("FORMAÇÃO ACADÊMICA", S["section"]))
        story.append(_hr())
        for edu in education:
            end = _fmt_date(edu.get("endDate", ""))
            label = f"{edu.get('studyType','')} em {edu.get('area','')}"
            row_text = f"<b>{edu.get('institution','')}</b> — {label}"
            if end:
                row_text += f"  <font color='#888888'>{end}</font>"
            story.append(Paragraph(row_text, S["edu"]))
        story.append(Spacer(1, 2))

    # ── Projects ─────────────────────────────────────────────────────────
    projects = data.get("projects", [])
    if projects:
        story.append(Paragraph("PROJETOS", S["section"]))
        story.append(_hr())
        for proj in projects:
            story.append(Paragraph(
                f"<b>{proj.get('name','')}</b> — {proj.get('description','')}",
                S["proj"]
            ))
        story.append(Spacer(1, 2))

    # ── Certifications ───────────────────────────────────────────────────
    certs = data.get("certificates", [])
    if certs:
        story.append(Paragraph("CERTIFICAÇÕES", S["section"]))
        story.append(_hr())
        for cert in certs:
            date_str = cert.get("date", "")
            story.append(Paragraph(
                f"• <b>{cert.get('name','')}</b>"
                + (f"  <font color='#888888'>({date_str})</font>" if date_str else ""),
                S["cert"]
            ))

    doc.build(story)
    print(f"PDF gerado: {pdf_path}")
    return pdf_path


if __name__ == "__main__":
    import sys
    json_p = sys.argv[1] if len(sys.argv) > 1 else "outputs/job_desc/json/resume.json"
    pdf_p  = sys.argv[2] if len(sys.argv) > 2 else "outputs/job_desc/pdf/output_resume.pdf"
    generate_pdf(json_p, pdf_p)
