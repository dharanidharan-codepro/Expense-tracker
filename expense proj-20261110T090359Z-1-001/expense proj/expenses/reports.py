"""
Report generation utilities for the Smart Expense Tracker.
Handles CSV and PDF export of expense records.
"""

import csv
import io
from datetime import date
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT


def generate_csv_report(expenses, username):
    """
    Generate a CSV file containing the user's expense records.

    Args:
        expenses: QuerySet of Expense objects for the user.
        username: The authenticated user's username.

    Returns:
        HttpResponse with CSV attachment.
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="expenses_{username}.csv"'

    writer = csv.writer(response)

    # Write header row
    writer.writerow(['Date', 'Description', 'Category', 'Amount (₹)', 'Notes'])

    # Write data rows
    total = 0
    for expense in expenses:
        writer.writerow([
            expense.date,
            expense.description,
            expense.category,
            expense.amount,
            expense.notes or ''
        ])
        total += expense.amount

    # Write total row
    writer.writerow([])
    writer.writerow(['', '', 'TOTAL', total, ''])

    return response


def generate_pdf_report(expenses, username):
    """
    Generate a PDF file containing the user's expense records.
    Uses ReportLab to build a professional-looking report.

    Args:
        expenses: QuerySet of Expense objects for the user.
        username: The authenticated user's username.

    Returns:
        HttpResponse with PDF attachment.
    """
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="expense_report_{username}.pdf"'

    # Create PDF document
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm
    )

    styles = getSampleStyleSheet()
    story = []

    # Title style
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor('#1a1a2e'),
        spaceAfter=8,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    subtitle_style = ParagraphStyle(
        'SubTitle',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#6c757d'),
        spaceAfter=4,
        alignment=TA_CENTER,
    )

    # Title
    story.append(Paragraph("💰 Smart Expense Tracker", title_style))
    story.append(Paragraph("Expense Report", title_style))
    story.append(Spacer(1, 0.3 * cm))

    # User info
    story.append(Paragraph(f"User: {username}", subtitle_style))
    story.append(Paragraph(f"Generated on: {date.today().strftime('%d %B %Y')}", subtitle_style))
    story.append(Spacer(1, 0.8 * cm))

    # Table header
    table_data = [['Date', 'Description', 'Category', 'Amount (₹)', 'Notes']]

    total = 0
    for expense in expenses:
        table_data.append([
            str(expense.date),
            expense.description[:40],  # Truncate long descriptions
            expense.category,
            f"₹{expense.amount:,.2f}",
            (expense.notes[:30] if expense.notes else '')
        ])
        total += expense.amount

    # Total row
    table_data.append(['', '', '', f'TOTAL: ₹{total:,.2f}', ''])

    # Table styling
    col_widths = [2.5 * cm, 6 * cm, 3 * cm, 3.5 * cm, 3.5 * cm]

    table = Table(table_data, colWidths=col_widths, repeatRows=1)
    table.setStyle(TableStyle([
        # Header row
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a1a2e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('TOPPADDING', (0, 0), (-1, 0), 10),

        # Data rows
        ('FONTNAME', (0, 1), (-1, -2), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -2), 9),
        ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
        ('ALIGN', (3, 1), (3, -1), 'RIGHT'),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),

        # Alternating row colors
        ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.HexColor('#f8f9fa')]),

        # Total row
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#e8f5e9')),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, -1), (-1, -1), 10),
        ('TEXTCOLOR', (3, -1), (3, -1), colors.HexColor('#2e7d32')),

        # Grid
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
        ('LINEBELOW', (0, 0), (-1, 0), 1.5, colors.HexColor('#1a1a2e')),
    ]))

    story.append(table)
    story.append(Spacer(1, 1 * cm))

    # Footer note
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.HexColor('#adb5bd'),
        alignment=TA_CENTER
    )
    story.append(Paragraph("Generated by Smart Expense Tracker — Keep track of every rupee!", footer_style))

    doc.build(story)

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response
