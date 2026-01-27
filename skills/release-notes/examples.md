# Release Notes Examples

These examples demonstrate the expected style and format for SaaS Pegasus release notes.

## Example 1: Feature-focused release

```markdown
Version 2024.12.1 adds comprehensive API documentation and improves the developer onboarding experience.

### API Documentation

- Added OpenAPI/Swagger documentation for all REST endpoints
- Interactive API explorer available at `/api/docs/`
- Auto-generated client libraries for Python and TypeScript

### Other Changes

- Upgraded Django to 5.1.2 with security patches
- Fixed issue where password reset emails weren't sent in production
- Improved form validation error messages across all forms
- Added loading spinners to async form submissions
- Removed deprecated `LEGACY_AUTH_BACKEND` setting
```

## Example 2: Maintenance release

```markdown
Version 2024.11.3 is a maintenance release with bug fixes and dependency updates.

- Fixed sidebar navigation not highlighting the active page on mobile
- Resolved race condition in WebSocket reconnection logic
- Updated htmx to 2.0.3
- Updated Tailwind CSS to 3.4.15
- Fixed incorrect timezone handling in scheduled task notifications
- Improved database query performance for team member listings
```

## Example 3: Major feature release

```markdown
Version 2024.10 introduces multi-tenancy support and a redesigned dashboard.

### Multi-Tenancy

Organizations can now create isolated workspaces with separate data, billing, and user management. Each workspace operates independently while sharing the same codebase.

- Workspace creation and management UI
- Per-workspace billing and subscription handling
- Workspace-scoped API keys
- Admin tools for cross-workspace management

### Dashboard Redesign

The main dashboard has been completely redesigned with a focus on actionable insights.

- New activity feed showing recent team actions
- Quick-action buttons for common tasks
- Customizable widget layout
- Dark mode support

### Other Changes

- Added bulk user import via CSV
- Improved email deliverability with DKIM signing
- Fixed issue where deleted users could still receive notifications
- Upgraded to Python 3.12
```

## Style Notes

1. **Opening sentence**: Always start with a 1-2 sentence summary of what this version adds or fixes
2. **Sections**: Use sections for major features; use a flat list for smaller releases
3. **Action verbs**: Start items with "Added", "Fixed", "Improved", "Updated", "Removed", etc.
4. **Specificity**: Be specific about what changed, not vague ("Fixed sidebar bug" → "Fixed sidebar navigation not highlighting the active page")
5. **User impact**: Focus on what users will experience, not implementation details
6. **Library updates**: Only mention specific libraries if they're significant or user-facing
