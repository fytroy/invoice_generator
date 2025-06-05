import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from jinja2 import Environment, FileSystemLoader

def create_invoice_pdf(invoice_data, output_filename="invoice.pdf"):
    """
    Generates a PDF invoice from provided data.

    Args:
        invoice_data (dict): A dictionary containing all invoice details.
                             Expected keys:
                                 - 'invoice_number'
                                 - 'invoice_date' (datetime object or string in YYYY-MM-DD)
                                 - 'due_date' (datetime object or string in YYYY-MM-DD)
                                 - 'bill_to_name'
                                 - 'bill_to_address' (list of strings for lines)
                                 - 'items' (list of dicts, each with 'description', 'quantity', 'unit_price')
                                 - 'subtotal'
                                 - 'tax_rate' (e.g., 0.05 for 5%)
                                 - 'tax_amount'
                                 - 'total_amount'
                                 - 'company_name' (Your company)
                                 - 'company_address' (Your company address, list of strings)
                                 - 'company_phone'
                                 - 'company_email'
                                 - 'payment_terms'
        output_filename (str): The name of the output PDF file.
    """
    doc = SimpleDocTemplate(output_filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # 1. Company Header
    story.append(Paragraph(invoice_data['company_name'], styles['h1']))
    for line in invoice_data['company_address']:
        story.append(Paragraph(line, styles['Normal']))
    story.append(Paragraph(f"Phone: {invoice_data['company_phone']}", styles['Normal']))
    story.append(Paragraph(f"Email: {invoice_data['company_email']}", styles['Normal']))
    story.append(Spacer(1, 0.2 * inch))

    # 2. Invoice Title
    story.append(Paragraph("INVOICE", styles['h2']))
    story.append(Spacer(1, 0.1 * inch))

    # 3. Invoice Details (Number, Date, Due Date)
    invoice_details_data = [
        ["Invoice #:", invoice_data['invoice_number']],
        ["Invoice Date:", invoice_data['invoice_date'].strftime('%Y-%m-%d') if isinstance(invoice_data['invoice_date'], datetime) else invoice_data['invoice_date']],
        ["Due Date:", invoice_data['due_date'].strftime('%Y-%m-%d') if isinstance(invoice_data['due_date'], datetime) else invoice_data['due_date']]
    ]
    invoice_details_table = Table(invoice_details_data, colWidths=[2 * inch, 3 * inch])
    invoice_details_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(invoice_details_table)
    story.append(Spacer(1, 0.2 * inch))

    # 4. Bill To Section
    story.append(Paragraph("BILL TO:", styles['h3']))
    story.append(Paragraph(invoice_data['bill_to_name'], styles['Normal']))
    for line in invoice_data['bill_to_address']:
        story.append(Paragraph(line, styles['Normal']))
    story.append(Spacer(1, 0.2 * inch))

    # 5. Items Table
    table_data = [['Description', 'Quantity', 'Unit Price', 'Amount']]
    for item in invoice_data['items']:
        amount = item['quantity'] * item['unit_price']
        table_data.append([
            item['description'],
            str(item['quantity']),
            f"${item['unit_price']:.2f}",
            f"${amount:.2f}"
        ])

    # Calculate total for table if not already calculated (good for verification)
    # total_items_amount = sum(item['quantity'] * item['unit_price'] for item in invoice_data['items'])

    table = Table(table_data, colWidths=[3 * inch, 1 * inch, 1.5 * inch, 1.5 * inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F2F2F2')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'), # Align Qty, Unit Price, Amount to right
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
    ]))
    story.append(table)
    story.append(Spacer(1, 0.2 * inch))

    # 6. Totals
    totals_data = [
        ["Subtotal:", f"${invoice_data['subtotal']:.2f}"],
        [f"Tax ({invoice_data['tax_rate']*100:.0f}%):", f"${invoice_data['tax_amount']:.2f}"],
        ["TOTAL DUE:", f"${invoice_data['total_amount']:.2f}"]
    ]
    totals_table = Table(totals_data, colWidths=[5.5 * inch, 2 * inch]) # Adjust colWidths to push totals to the right
    totals_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, -1), (1, -1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (1, -1), (1, -1), colors.red), # Make total amount stand out
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(totals_table)
    story.append(Spacer(1, 0.2 * inch))

    # 7. Payment Terms
    story.append(Paragraph("Payment Terms:", styles['h3']))
    story.append(Paragraph(invoice_data['payment_terms'], styles['Normal']))
    story.append(Spacer(1, 0.5 * inch))

    # 8. Footer/Thank You
    story.append(Paragraph("Thank you for your business!", styles['h3']))

    doc.build(story)
    print(f"Invoice '{output_filename}' generated successfully!")

def calculate_invoice_totals(items, tax_rate):
    """Calculates subtotal, tax amount, and total amount for invoice items."""
    subtotal = sum(item['quantity'] * item['unit_price'] for item in items)
    tax_amount = subtotal * tax_rate
    total_amount = subtotal + tax_amount
    return subtotal, tax_amount, total_amount

def get_invoice_data_from_user():
    """Prompts the user for invoice details."""
    print("\n--- Enter Invoice Details ---")
    data = {}

    data['company_name'] = input("Your Company Name: ")
    data['company_address'] = [input("Your Company Address Line 1: ")]
    while True:
        line = input("Your Company Address Line (leave blank to finish): ")
        if not line:
            break
        data['company_address'].append(line)
    data['company_phone'] = input("Your Company Phone: ")
    data['company_email'] = input("Your Company Email: ")

    data['invoice_number'] = input("Invoice Number: ")
    data['invoice_date'] = input("Invoice Date (YYYY-MM-DD): ")
    data['due_date'] = input("Due Date (YYYY-MM-DD): ")

    data['bill_to_name'] = input("Bill To Name: ")
    data['bill_to_address'] = [input("Bill To Address Line 1: ")]
    while True:
        line = input("Bill To Address Line (leave blank to finish): ")
        if not line:
            break
        data['bill_to_address'].append(line)

    data['items'] = []
    print("\n--- Enter Items/Services (type 'done' when finished) ---")
    while True:
        description = input("Item Description (or 'done'): ")
        if description.lower() == 'done':
            break
        try:
            quantity = float(input("Quantity: "))
            unit_price = float(input("Unit Price: "))
            data['items'].append({
                'description': description,
                'quantity': quantity,
                'unit_price': unit_price
            })
        except ValueError:
            print("Invalid quantity or unit price. Please enter numbers.")

    while True:
        try:
            data['tax_rate'] = float(input("Tax Rate (e.g., 0.05 for 5%): "))
            break
        except ValueError:
            print("Invalid tax rate. Please enter a number.")

    subtotal, tax_amount, total_amount = calculate_invoice_totals(data['items'], data['tax_rate'])
    data['subtotal'] = subtotal
    data['tax_amount'] = tax_amount
    data['total_amount'] = total_amount

    data['payment_terms'] = input("Payment Terms (e.g., 'Net 30', 'Due on receipt'): ")

    return data

def main():
    invoice_data = get_invoice_data_from_user()
    output_filename = f"invoice_{invoice_data['invoice_number']}.pdf"
    create_invoice_pdf(invoice_data, output_filename)

if __name__ == "__main__":
    main()