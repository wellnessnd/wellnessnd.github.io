import os
import pypdf
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm

def build_pdf():
    pdf_filename = 'docs/sources/translation_temp.pdf'
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=A4,
        leftMargin=1.6*cm,
        rightMargin=1.6*cm,
        topMargin=1.5*cm,
        bottomMargin=1.5*cm
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
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

    header_badge = ParagraphStyle(
        'Badge',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        alignment=1,
        textColor=colors.HexColor('#0F766E')
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#1E293B')
    )

    center_style = ParagraphStyle(
        'BodyCenter',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        alignment=1,
        textColor=colors.HexColor('#1E293B')
    )

    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor('#0F172A')
    )

    table_body = ParagraphStyle(
        'TableBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor('#1E293B')
    )

    table_center = ParagraphStyle(
        'TableCenter',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10,
        alignment=1,
        textColor=colors.HexColor('#1E293B')
    )

    elements = []

    # PAGE 1: DIPLOMA TRANSLATION
    elements.append(Paragraph('OFFICIAL CERTIFIED TRANSLATION FROM RUSSIAN', header_badge))
    elements.append(Spacer(1, 4))
    elements.append(Paragraph('RUSSIAN FEDERATION', subtitle_style))
    elements.append(Paragraph('Federal State Budgetary Educational Institution of Higher Education<br/><b>MOSCOW PEDAGOGICAL STATE UNIVERSITY (MPGU)</b>', subtitle_style))
    elements.append(Spacer(1, 4))
    elements.append(Paragraph('DIPLOMA OF PROFESSIONAL RETRAINING', title_style))
    elements.append(Paragraph('<b>Series / Number:</b> 772422586900 &nbsp;|&nbsp; <b>Document of Qualification</b><br/><b>Registration No.:</b> 1913 &nbsp;|&nbsp; <b>City:</b> Moscow &nbsp;|&nbsp; <b>Date of Issue:</b> February 27, 2026', center_style))
    elements.append(Spacer(1, 4))
    elements.append(HRFlowable(width='100%', thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=8))

    elements.append(Paragraph('<i>Statutory note on diploma blank:</i> <b>&ldquo;Valid upon presentation of a diploma of higher education&rdquo;</b><br/><i>[Underlying Higher Education Qualification: Master of Management degree, National Research University Higher School of Economics (HSE), Diploma Series 107704 No. 0006734, issued March 16, 2017 &bull; Doctoral Degree Dr. phil. (magna cum laude), Europa-Universit&auml;t Flensburg, 2026]</i>', ParagraphStyle('Notice', parent=body_style, fontSize=7.5, leading=10.5, textColor=colors.HexColor('#475569'))))
    elements.append(Spacer(1, 8))

    main_text = (
        'This diploma certifies that<br/><br/>'
        '<font size="12"><b>NATALIIA EDUARDOVNA DOLGOVA</b></font><br/><br/>'
        'has successfully completed professional retraining at the<br/>'
        '<b>Institute of Pedagogy and Psychology</b><br/>'
        'during the period from <b>February 25, 2025 to February 19, 2026</b><br/>'
        'under the professional retraining program:<br/>'
        '<font size="11"><b>&laquo;PRACTICAL PSYCHOLOGY&raquo;</b></font><br/><br/>'
        'By the decision of the State Attestation Commission dated <b>February 19, 2026 (Protocol No. 2)</b>,<br/>'
        'this diploma confirms the award of the qualification:<br/><br/>'
        '<font size="12" color="#0F766E"><b>&laquo;PRACTICAL PSYCHOLOGIST&raquo;</b></font><br/><br/>'
        'and confers the legal right to engage in professional activity in the field of:<br/>'
        '<b>PSYCHOLOGICAL COUNSELING</b>'
    )
    elements.append(Paragraph(main_text, center_style))
    elements.append(Spacer(1, 14))

    sig_data = [
        [Paragraph('<b>Chair of the Examination Commission:</b>', body_style), Paragraph('L. V. Bayborodova <i>[Signature]</i>', body_style)],
        [Paragraph('<b>Head of Division / Program Director:</b>', body_style), Paragraph('D. A. Kudryavtseva <i>[Signature]</i>', body_style)],
        [Paragraph('<b>Secretary:</b>', body_style), Paragraph('O. N. Zotova <i>[Signature]</i>', body_style)],
        [Paragraph('<b>Official State Seal:</b>', body_style), Paragraph('<i>[Round Blue Official State Seal of the Ministry of Education of the Russian Federation, Moscow Pedagogical State University (MPGU), OGRN 1027739452123, INN 7704077771]</i>', body_style)],
    ]
    sig_table = Table(sig_data, colWidths=[6.8*cm, 10.8*cm])
    sig_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('TOPPADDING', (0,0), (-1,-1), 3),
    ]))
    elements.append(sig_table)

    elements.append(Spacer(1, 10))
    elements.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#CBD5E1'), spaceAfter=5))
    elements.append(Paragraph('<b>Translator Statement:</b> I certify that this is a complete, true and accurate English translation of the official Russian Diploma of Professional Retraining No. 772422586900 issued to Nataliia Eduardovna Dolgova on February 27, 2026 by Moscow Pedagogical State University.', ParagraphStyle('TransCert', parent=body_style, fontSize=7.2, leading=9.5, textColor=colors.HexColor('#64748B'))))

    elements.append(PageBreak())

    # PAGE 2: SUPPLEMENT / TRANSCRIPT TRANSLATION
    elements.append(Paragraph('OFFICIAL CERTIFIED TRANSLATION FROM RUSSIAN &mdash; DIPLOMA SUPPLEMENT / TRANSCRIPT', header_badge))
    elements.append(Spacer(1, 4))
    elements.append(Paragraph('MOSCOW PEDAGOGICAL STATE UNIVERSITY (MPGU)<br/><b>SUPPLEMENT TO DIPLOMA OF PROFESSIONAL RETRAINING No. 772422586900</b>', subtitle_style))
    elements.append(Paragraph('<b>Holder:</b> Nataliia Eduardovna Dolgova &nbsp;|&nbsp; <b>Supplement Blank No.:</b> 772425289373<br/><b>Prior Higher Education:</b> Higher Education Diploma Series 107704 No. 0006734, issued March 16, 2017 (Master Degree, HSE)<br/><b>Qualification Awarded:</b> Practical Psychologist &nbsp;|&nbsp; <b>Total Academic Workload: 1,080 Hours</b>', ParagraphStyle('TransMeta', parent=center_style, fontSize=7.5, leading=10.5)))
    elements.append(Spacer(1, 4))
    elements.append(HRFlowable(width='100%', thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=5))

    courses = [
        ('1', 'Introduction to Professional Psychological Practice', '36', 'Passed (Credit)'),
        ('2', 'General Psychology', '54', 'Excellent (Grade A / 5)'),
        ('3', 'Fundamentals of Personality Theory', '36', 'Passed (Credit)'),
        ('4', 'Methodology and Methods of Psychological Research', '36', 'Passed (Credit)'),
        ('5', 'Psychophysiology with Fundamentals of Neuropsychology', '36', 'Passed (Credit)'),
        ('6', 'Educational Psychology', '54', 'Excellent (Grade A / 5)'),
        ('7', 'Special Needs Psychology (Inclusion)', '36', 'Passed (Credit)'),
        ('8', 'Pathopsychology (Abnormal Psychology)', '36', 'Passed (Credit)'),
        ('9', 'Social Psychology', '54', 'Excellent (Grade A / 5)'),
        ('10', 'Conflictology &amp; Conflict Resolution', '54', 'Excellent (Grade A / 5)'),
        ('11', 'Psychodiagnostics &amp; Psychological Assessment', '36', 'Passed (Credit)'),
        ('12', 'Psychology of Deviant Behavior', '36', 'Passed (Credit)'),
        ('13', 'Organizational and Management Psychology', '36', 'Passed (Credit)'),
        ('14', 'Gerontopsychology', '36', 'Passed (Credit)'),
        ('15', 'Developmental and Age-Related Psychology', '54', 'Excellent (Grade A / 5)'),
        ('16', 'Career Counseling: Methods and Tools', '36', 'Passed (Credit)'),
        ('17', 'Fundamentals of Psychological Counseling', '54', 'Excellent (Grade A / 5)'),
        ('18', 'Family Psychology', '36', 'Passed (Credit)'),
        ('19', 'Family Counseling Practicum', '36', 'Passed (Credit)'),
        ('20', 'Art Therapy Practicum', '36', 'Passed (Credit)'),
        ('21', 'Psychology of Training and Facilitation', '36', 'Passed (Credit)'),
        ('22', 'Methods of Active Socio-Psychological Learning', '36', 'Passed (Credit)'),
        ('23', 'General Psychological Practicum', '36', 'Passed (Credit)'),
        ('24', 'Personal and Professional Counseling Practicum', '36', 'Passed (Credit)'),
        ('25', 'Child and Adolescent Counseling Practicum', '36', 'Passed (Credit)'),
        ('&mdash;', '<b>PRACTICE &amp; SUPERVISION: Supervised Clinical / Counseling Practice</b>', '36', '<b>Passed (Credit)</b>'),
        ('&mdash;', '<b>FINAL ATTESTATION: Final State Qualifying Examination</b>', '36', '<b>Excellent (Grade A / 5)</b>'),
    ]

    table_rows = [
        [Paragraph('<b>#</b>', table_header), Paragraph('<b>Course / Discipline Title</b>', table_header), Paragraph('<b>Academic Hours</b>', table_header), Paragraph('<b>Grade / Assessment</b>', table_header)]
    ]

    for num, title, hrs, grade in courses:
        table_rows.append([
            Paragraph(num, table_center),
            Paragraph(title, table_body),
            Paragraph(hrs, table_center),
            Paragraph(grade, table_body),
        ])

    table_rows.append([
        Paragraph('', table_header),
        Paragraph('<b>TOTAL PROGRAM WORKLOAD (ACADEMIC HOURS):</b>', table_header),
        Paragraph('<b>1,080</b>', table_header),
        Paragraph('<b>Qualification Conferred</b>', table_header),
    ])

    course_table = Table(table_rows, colWidths=[0.8*cm, 9.8*cm, 2.8*cm, 4.2*cm])
    course_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 1.2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.2),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#F8FAFC')),
    ]))
    elements.append(course_table)
    elements.append(Spacer(1, 4))

    elements.append(Paragraph('<b>Institutional Verification:</b> Moscow Pedagogical State University (MPGU), Institute of Pedagogy and Psychology. Head: D. A. Kudryavtseva, Secretary: O. N. Zotova. Official State Seal affixed.', ParagraphStyle('FooterNote', parent=body_style, fontSize=7, leading=9, textColor=colors.HexColor('#64748B'))))

    doc.build(elements)
    print('Generated translation PDF:', pdf_filename)

    # NOW MERGE TRANSLATION (2 pages) + ORIGINAL DIPLOMA SCAN (1 page) + ORIGINAL ANNEX SCANS (2 pages)
    writer = pypdf.PdfWriter()
    writer.append(pdf_filename)
    writer.append('docs/sources/Nataliia_Dolgova_Psychology_Diploma.pdf')
    writer.append('docs/sources/Nataliia_Dolgova_Psychology_Diploma_Annex.pdf')

    final_output = 'docs/sources/Nataliia_Dolgova_Psychology_Diploma_and_English_Translation.pdf'
    with open(final_output, 'wb') as f:
        writer.write(f)
    writer.close()
    print('Successfully created complete document with English translation:', final_output)
    
    # Cleanup temp translation
    if os.path.exists(pdf_filename):
        os.remove(pdf_filename)

if __name__ == '__main__':
    build_pdf()
