# Invoice Generator

A Python script to generate PDF invoices. This script prompts the user for company details, client information, itemized services/products, tax rates, and payment terms, then generates a professional-looking PDF invoice.

## Features

- Generates PDF invoices from command-line inputs.
- Calculates subtotal, tax amount, and total amount automatically.
- Customizable company and client information.
- Support for multiple line items.
- Outputs a well-formatted PDF document.

## Requirements

- Python 3.x
- reportlab (`pip install reportlab`)

## How to Use

1.  **Ensure Python and pip are installed.**
2.  **Install the `reportlab` library:**
    ```bash
    pip install reportlab
    ```
3.  **Run the script from your terminal:**
    ```bash
    python invoice_generator.py
    ```
4.  **Enter the invoice details when prompted.**
    The script will ask for:
    *   Your company's details (name, address, phone, email)
    *   Invoice metadata (invoice number, invoice date, due date)
    *   Client's billing information (name, address)
    *   Item/service details (description, quantity, unit price) - you can add multiple items.
    *   Tax rate (e.g., 0.05 for 5%)
    *   Payment terms
5.  **Find the generated PDF.**
    A PDF file named `invoice_<invoice_number>.pdf` (e.g., `invoice_123.pdf`) will be created in the same directory where you ran the script.

## Sample Invoice Data Input

When you run the script, you will be prompted for various details. Here's an example of what you might enter:

*   **Your Company Name:** My Awesome LLC
*   **Your Company Address Line 1:** 123 Main St
*   **Your Company Address Line (leave blank to finish):** Anytown, ST 12345
*   **Your Company Phone:** 555-123-4567
*   **Your Company Email:** contact@myawesomellc.com
*   **Invoice Number:** INV2023-001
*   **Invoice Date (YYYY-MM-DD):** 2023-10-26
*   **Due Date (YYYY-MM-DD):** 2023-11-25
*   **Bill To Name:** John Doe Corp
*   **Bill To Address Line 1:** 456 Client Ave
*   **Bill To Address Line (leave blank to finish):** Otherville, ST 67890
*   **Item Description (or 'done'):** Web Development Services
*   **Quantity:** 10
*   **Unit Price:** 100
*   **Item Description (or 'done'):** Design Mockups
*   **Quantity:** 5
*   **Unit Price:** 50
*   **Item Description (or 'done'):** done
*   **Tax Rate (e.g., 0.05 for 5%):** 0.07
*   **Payment Terms:** Net 30

This will generate an invoice with the specified details.

## License

This project is licensed under the MIT License. See the LICENSE file for details (if a LICENSE file is added).
If no LICENSE file is present, it is assumed to be under the MIT License by default for this project.
