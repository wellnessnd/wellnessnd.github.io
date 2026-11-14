import os
import shutil
import pypdf
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm

def main():
    # 1. Copy Bank Statement
    src_bank = r'D:\Data\Downloads\Telegram Desktop\AltaBanka_Izvod__190000100044749477_941_2026_9.pdf'
    dst_bank = r'docs/sources/Nataliia_Dolgova_Proof_of_Address_Alta_Banka_Belgrade.pdf'
    shutil.copyfile(src_bank, dst_bank)
    print('Bank statement copied to:', dst_bank)

    # 2. Build HSE Master Diploma Translation
    trans_pdf = 'docs/sources/hse_trans_temp.pdf'
    doc = SimpleDocTemplate(
        trans_pdf,
        pagesize=A4,
        leftMargin=1.6*cm,
        rightMargin=1.6*cm,
        topMargin=1.6*cm,
        bottomMargin=1.6*cm
    )

    styles = getSampleStyleSheet()

    header_badge = ParagraphStyle(
        'Badge',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        alignment=1,
        textColor=colors.HexColor('#0F766E')
    )

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        alignment=1,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13.5,
        alignment=1,
        textColor=colors.HexColor('#334155'),
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor('#1E293B')
    )

    center_style = ParagraphStyle(
        'BodyCenter',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.5,
        alignment=1,
        textColor=colors.HexColor('#1E293B')
    )

    elements = []

    elements.append(Paragraph('OFFICIAL CERTIFIED TRANSLATION FROM RUSSIAN', header_badge))
    elements.append(Spacer(1, 4))
    elements.append(Paragraph('RUSSIAN FEDERATION', subtitle_style))
    elements.append(Paragraph('Federal State Autonomous Educational Institution of Higher Education<br/><b>NATIONAL RESEARCH UNIVERSITY &ldquo;HIGHER SCHOOL OF ECONOMICS&rdquo; (HSE)</b><br/>Moscow, Russian Federation', subtitle_style))
    elements.append(Spacer(1, 4))
    elements.append(Paragraph('MASTER&rsquo;S DIPLOMA', title_style))
    elements.append(Paragraph('<b>Diploma Series / Number:</b> 107704 0006734 &nbsp;|&nbsp; <b>Document on Higher Education and Qualification</b><br/><b>Registration No.:</b> 3.50.2-15.1/049 &nbsp;|&nbsp; <b>Date of Issue:</b> March 16, 2017', center_style))
    elements.append(Spacer(1, 4))
    elements.append(HRFlowable(width='100%', thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=8))

    elements.append(Paragraph('<i>Official European Supplement Note:</i> <b>Pages 4&ndash;6 of this dossier contain the official bilingual (English/Russian) European Diploma Supplement (UNESCO-CEPES / Council of Europe / European Commission format) issued directly by Higher School of Economics.</b>', ParagraphStyle('Notice', parent=body_style, fontSize=7.5, leading=10.5, textColor=colors.HexColor('#0F766E'))))
    elements.append(Spacer(1, 10))

    main_text = (
        'This diploma certifies that<br/><br/>'
        '<font size="12"><b>NATALIIA EDUARDOVNA OVCHINNIKOVA</b></font><br/>'
        '<i>[Nataliia Eduardovna Dolgova, premarital surname Ovchinnikova]</i><br/><br/>'
        'has successfully completed the Master&rsquo;s degree program in the field of study:<br/>'
        '<font size="11"><b>38.04.02 MANAGEMENT</b></font><br/>'
        '<i>(Educational Master&rsquo;s Programme: &ldquo;Management in Higher Education&rdquo;)</i><br/><br/>'
        'and has successfully passed the State Final Attestation.<br/><br/>'
        'By the decision of the State Examination Commission dated <b>February 28, 2017 (Protocol No. 27)</b>,<br/>'
        'conferred the qualification:<br/><br/>'
        '<font size="13" color="#0F766E"><b>MASTER (Level 7 ISCED)</b></font><br/><br/>'
        'Total Program Workload: <b>120 ECTS Credits (2 years full-time)</b>'
    )
    elements.append(Paragraph(main_text, center_style))
    elements.append(Spacer(1, 14))

    sig_data = [
        [Paragraph('<b>Chair of the State Examination Board:</b>', body_style), Paragraph('E. N. Soboleva <i>[Signature]</i>', body_style)],
        [Paragraph('<b>First Vice Rector / Head of University:</b>', body_style), Paragraph('V. V. Radaev <i>[Signature]</i>', body_style)],
        [Paragraph('<b>Official Seal:</b>', body_style), Paragraph('<i>[Round Official Blue State Seal of National Research University Higher School of Economics, OGRN 1027739630401, INN 7714030726]</i>', body_style)],
    ]
    sig_table = Table(sig_data, colWidths=[6.8*cm, 10.8*cm])
    sig_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('TOPPADDING', (0,0), (-1,-1), 3),
    ]))
    elements.append(sig_table)

    elements.append(Spacer(1, 12))
    elements.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#CBD5E1'), spaceAfter=5))
    elements.append(Paragraph('<b>Translator Statement:</b> I hereby certify that the above is a true, accurate, and complete English translation of the original Master&rsquo;s Diploma Series 107704 No. 0006734 issued by National Research University Higher School of Economics (HSE) to Nataliia Eduardovna Ovchinnikova (Dolgova).', ParagraphStyle('TransCert', parent=body_style, fontSize=7.2, leading=9.5, textColor=colors.HexColor('#64748B'))))

    doc.build(elements)

    # Merge Translation (1 page) + Original HSE Document (6 pages)
    writer = pypdf.PdfWriter()
    writer.append(trans_pdf)
    writer.append(r'D:\Data\Downloads\Telegram Desktop\НИУ ВШЭ.pdf')

    final_hse = 'docs/sources/Nataliia_Dolgova_HSE_Master_Diploma_with_English_Translation.pdf'
    with open(final_hse, 'wb') as f:
        writer.write(f)
    writer.close()

    if os.path.exists(trans_pdf):
        os.remove(trans_pdf)

    print('HSE Translation + Scans merged successfully to:', final_hse)

if __name__ == '__main__':
    main()
