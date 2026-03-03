---
name: open-as-html
description: Convert markdown or conversation output to a clean HTML file and open it in the browser. Use when the user wants to copy content into Google Docs, share formatted output, preview content as a web page, or says things like "open that as HTML," "make that pasteable," "put that in a doc," or "open that in the browser."
allowed-tools: Write, Bash(xdg-open:*), Bash(open:*)
---

# Open as HTML

Convert content from the conversation into a styled HTML file and open it in the default browser for easy copy-paste into Google Docs or other rich text editors.

## Arguments

- `$0`: (optional) description of what content to convert. If not provided, convert the most recent substantive output from the conversation.

## Workflow

1. Identify the content to convert — either specified by the user or the most recent substantive output.
2. Convert it to clean, semantic HTML with this structure:
   - Use `<h1>`, `<h2>`, `<h3>` for headings
   - Use `<ol>`/`<ul>` for lists
   - Use `<em>` and `<strong>` for emphasis
   - Use `<table>` for any tabular data
   - Use `<pre><code>` for code blocks
3. Wrap in a minimal HTML document with basic styling:
   ```html
   <!DOCTYPE html>
   <html>
   <head>
   <style>
     body { font-family: Arial, sans-serif; max-width: 700px; margin: 40px auto; padding: 0 20px; }
     li { margin-bottom: 8px; }
     table { border-collapse: collapse; margin: 16px 0; }
     th, td { border: 1px solid #ccc; padding: 8px 12px; text-align: left; }
     pre { background: #f5f5f5; padding: 12px; border-radius: 4px; overflow-x: auto; }
   </style>
   </head>
   <body>
   <!-- content here -->
   </body>
   </html>
   ```
4. Write to `/tmp/claude-output.html`.
5. Open with: `xdg-open /tmp/claude-output.html 2>/dev/null || open /tmp/claude-output.html 2>/dev/null`
