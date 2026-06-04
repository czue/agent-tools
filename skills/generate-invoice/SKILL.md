---
name: generate-invoice
description: Generate a PDF invoice from Toggl time data. Use when the user wants to create an invoice, generate a bill, or mentions invoicing a client.
allowed-tools: Bash(cd *invoice-gen*), Bash(uv run*), Read, AskUserQuestion
---

# Generate Invoice

Generate a PDF invoice by pulling hours from Toggl and rendering to PDF. The tool lives at `/home/czue/src/personal/agent-tools/invoice-gen/`.

## Arguments

- `$0`: (optional) end date (YYYY-MM-DD)
- `$1`: (optional) client config name (default: "peregrine")
- `$2`: (optional) start date (YYYY-MM-DD, defaults to day after last invoice)

## Workflow

1. **Resolve the end date**:
   - If `$0` is provided, use it.
   - Otherwise, use `AskUserQuestion` to ask: "What end date for the invoice?" with options for today's date and end of last month.

2. **Resolve the client**:
   - If `$1` is provided, use it.
   - Otherwise, default to `peregrine`.

3. **Dry run first** to confirm hours and amount:
   ```bash
   cd /home/czue/src/personal/agent-tools/invoice-gen && uv run python generate.py --end <end_date> --client <client> --dry-run
   ```
   If `$2` (start date) is provided, add `--start <start_date>`.
   Show the user the hours, amount, working days, and average hours per working day, and ask for confirmation before generating.

4. **Generate the invoice**:
   ```bash
   cd /home/czue/src/personal/agent-tools/invoice-gen && uv run python generate.py --end <end_date> --client <client>
   ```
   Add `--start` and `--description` if provided by the user.

5. **Report results**: Show the output path and the invoice summary (hours, rate, amount, working days, avg hours/working day).

## CLI Options

- `--start`: Start date. Defaults to day after last invoice end date for that client.
- `--end`: End date (required).
- `--client`: Client config name matching a file in `invoice-gen/clients/`.
- `--description`: Work description (default: "Ongoing bolt assistant work.").
- `--output-dir`: Output directory (default: `/home/czue/Dropbox/Personal/Elodin/invoices`).
- `--dry-run`: Preview without generating.

## Client Configs

Client TOML files live in `invoice-gen/clients/`. Each has: name, country, rate, currency, toggl_project_name, line_item_description. To add a new client, copy `example.toml`.

## Notes

- Invoice numbers auto-increment via `invoice-gen/counter.json`.
- Last end date per client is tracked, so `--start` is usually not needed.
- Suppress `uv` warnings in output (they're noisy but harmless).
