# Invoice Generator Design

## Overview

CLI tool that pulls hours from Toggl and generates a PDF invoice matching the existing Invoicely format. Lives in `invoice-gen/` as a standalone Python project with its own `pyproject.toml`.

## Architecture

```
invoice-gen/
├── pyproject.toml          # uv-managed: httpx, click, jinja2, playwright
├── generate.py             # CLI entry point (click)
├── toggl.py                # Toggl API client - fetch time entries, sum hours
├── pdf.py                  # Render Jinja2 HTML template → PDF via Playwright
├── config.py               # Load client configs, invoice counter, shared settings
├── templates/
│   └── invoice.html        # Jinja2 HTML/CSS template matching sample invoice
├── clients/
│   └── peregrine.toml      # Per-client config
└── .env                    # Toggl API token, sender details
```

## CLI Interface

```bash
uv run generate.py --start 2026-02-04 --end 2026-02-20 --client peregrine
```

Options:
- `--start` (required): Start date (YYYY-MM-DD)
- `--end` (required): End date (YYYY-MM-DD)
- `--client` (required): Client config name (matches filename in `clients/`)
- `--description`: Work description bullets (default: "Ongoing bolt assistant work.")
- `--output-dir`: Where to save PDFs (default: `./output/`)
- `--dry-run`: Show hours and invoice preview without generating PDF

## Components

### Toggl API Client (`toggl.py`)

Uses the [Toggl Reports API v3](https://engineering.toggl.com/docs/reports_v3/) to fetch time entries:
- Authenticates with API token (from `.env`)
- Filters by client name and date range
- Returns total hours (rounded to nearest quarter hour to match existing invoices)

### PDF Generation (`pdf.py`)

- Jinja2 HTML template styled with inline CSS to match the sample invoice layout
- Playwright renders HTML to PDF (full CSS support, easy to iterate on design)
- Template includes: header, from/to addresses, invoice metadata, line items table, totals, payment details footer

### Client Config (`clients/peregrine.toml`)

```toml
name = "Acme Corp"
country = "United States"
rate = 100.00
currency = "USD"
toggl_project_name = "acme"
line_item_description = "Software development and coordination"
```

### Shared Config (`.env`)

```
TOGGL_API_TOKEN=xxx
TOGGL_WORKSPACE_ID=xxx

# Sender details
SENDER_NAME="Your Name"
SENDER_COMPANY="Your Company"
SENDER_ADDRESS="123 Main St\nCity, State, 12345\nCountry"
SENDER_TAX_ID="000-00-0000"
SENDER_EMAIL="you@example.com"

# Payment details stored as-is for template rendering
PAYMENT_DETAILS_USD="Paypal: you@example.com\nBank Name\nAccount Number: 000000000\nRouting Number: 000000000"
PAYMENT_DETAILS_ZAR="Bank Name\nAccount Number: 000000000\nBranch Code: 000000"

DEFAULT_RATE=100.00
```

### Invoice Numbering

Simple `counter.json` in the project directory:
```json
{"last_invoice_number": 24}
```

Auto-increments on each generation. The invoice number format is `INV-{number}`.

## Output

PDF saved as: `{output_dir}/INV-{number}-czue-{client}-{month_abbrev}-{end_day}.pdf`
Example: `output/INV-25-czue-peregrine-mar-04.pdf`

## Dependencies

- **httpx**: HTTP client for Toggl API
- **click**: CLI framework
- **jinja2**: HTML templating
- **playwright**: Headless browser PDF rendering
- **python-dotenv**: Environment config
- **tomli**: TOML parsing (stdlib in 3.11+, but explicit for clarity)
