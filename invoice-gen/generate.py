#!/usr/bin/env python3
"""Invoice generator CLI. Pulls hours from Toggl and generates a PDF invoice."""

import click
from datetime import datetime, timedelta
from pathlib import Path

from config import load_client, load_sender, get_next_invoice_number, get_last_end_date, save_last_end_date
from toggl import get_project_id, get_total_hours, get_workspace_id
from pdf import render_invoice_html, generate_pdf


def format_date_range(start: str, end: str) -> str:
    """Format date range like 'Feb 4 - 20, 2026'."""
    s = datetime.strptime(start, "%Y-%m-%d")
    e = datetime.strptime(end, "%Y-%m-%d")
    if s.month == e.month and s.year == e.year:
        return f"{s.strftime('%b')} {s.day} - {e.day}, {e.year}"
    return f"{s.strftime('%b')} {s.day}, {s.year} - {e.strftime('%b')} {e.day}, {e.year}"


@click.command()
@click.option("--start", default=None, help="Start date (YYYY-MM-DD). Defaults to day after last invoice end date.")
@click.option("--end", required=True, help="End date (YYYY-MM-DD)")
@click.option("--client", required=True, help="Client config name (matches filename in clients/)")
@click.option("--description", default="Ongoing bolt assistant work.", help="Work description")
@click.option("--output-dir", default="/home/czue/Dropbox/Personal/Elodin/invoices", help="Output directory for PDFs")
@click.option("--dry-run", is_flag=True, help="Show hours and preview without generating PDF")
def main(start: str | None, end: str, client: str, description: str, output_dir: str, dry_run: bool):
    """Generate an invoice PDF from Toggl time entries."""
    # Resolve start date
    if start is None:
        last_end = get_last_end_date(client)
        if last_end is None:
            raise click.ClickException("No previous invoice found for this client. Please provide --start.")
        start = (datetime.strptime(last_end, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")
        click.echo(f"Using start date: {start} (day after last invoice)")

    # Load configs
    client_config = load_client(client)
    sender = load_sender()

    # Fetch hours from Toggl
    click.echo(f"Fetching hours from Toggl for {client_config.toggl_project_name} ({start} to {end})...")
    workspace_id = get_workspace_id()
    project_id = get_project_id(workspace_id, client_config.toggl_project_name)
    hours = get_total_hours(workspace_id, project_id, start, end)
    amount = hours * client_config.rate

    click.echo(f"  Hours: {hours}")
    click.echo(f"  Rate: {client_config.currency} {client_config.rate:.2f}/hr")
    click.echo(f"  Amount: {client_config.currency} {amount:,.2f}")

    if dry_run:
        click.echo("\n[Dry run] No PDF generated.")
        return

    # Generate invoice
    invoice_num = get_next_invoice_number()
    invoice_number = f"INV-{invoice_num}"
    end_date = datetime.strptime(end, "%Y-%m-%d")
    invoice_date = end_date.strftime("%b %d %Y")
    due_date = (end_date + timedelta(days=14)).strftime("%b %d %Y")

    context = {
        "sender": sender,
        "client": client_config,
        "invoice_number": invoice_number,
        "invoice_date": invoice_date,
        "due_date": due_date,
        "date_range": format_date_range(start, end),
        "description": description,
        "hours": hours,
        "rate": client_config.rate,
        "amount": amount,
        "currency": client_config.currency,
    }

    html = render_invoice_html(context)

    # Save PDF
    month_abbrev = end_date.strftime("%b").lower()
    filename = f"{invoice_number}-czue-{client}-{month_abbrev}-{end_date.day:02d}.pdf"
    output_path = Path(output_dir) / filename
    generate_pdf(html, output_path)

    # Save last end date for next invoice
    save_last_end_date(client, end)

    click.echo(f"\nInvoice saved to: {output_path}")


if __name__ == "__main__":
    main()
