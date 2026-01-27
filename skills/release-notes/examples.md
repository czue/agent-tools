# Release Notes Examples

These examples demonstrate the expected style and format for SaaS Pegasus release notes. When generating release notes, read this file to match the tone, structure, and level of detail.

## Example 1: Hotfix release

```markdown
## Version 2025.12.1

This is a hotfix release that fixes an issue where production Dockerfiles weren't building on 2025.12 when
celery was enabled because `git` was not installed. The fix is installing `git` before installing Python dependencies.

Thanks Denis and Chris for reporting!

*Dec 14, 2025*
```

## Example 2: Bugfix release

```markdown
## Version 2025.11.2

This is a bugfix release addressing a few issues:

- **Switched the default production celery pool from `gevent` to `threads`.**
  This fixes compatibility issues between `gevent` and `asyncio` that arose when using agents inside Celery.
  Thanks Matt for reporting and suggesting the fix!
  - This change also removes `gevent` from production requirements. If you were using it elsewhere you should keep it.
- Fixed a bug where the "New Agent Chat" button didn't properly set the agent name on React / non-async builds.
- Fixed a whitespace issue in the Digital Ocean `app-spec.yaml` file that was causing an invalid config.
- Bumped the Postgres version on Digital Ocean to the latest (version 18).
- Added the `/.vite/` path back to the `.gitignore` file.

*November 27, 2025*
```

## Example 3: Feature release with sections

```markdown
## Version 2025.12

This release upgrades Pegasus to Django 6, adds Google Gemini (Nano Banana Pro) as an AI image generation option,
and includes several minor fixes and updates.

### Django 6

Pegasus has been upgraded to Django 6! This includes:

- **Upgraded Django to version 6.0.**
- **Bumped the minimum Python version to 3.12** to match Django 6's requirements.
- **Removed `django-template-partials` dependency**, as template partials are now built into Django 6.
  Also simplified the template loader configuration in `settings.py` by removing the partials-related setup.
- Temporarily added a workaround to `pyproject.toml` / `requirements.in` to allow installing `django-celery-beat`
  from source, until [this issue is resolved](https://github.com/celery/django-celery-beat/issues/977).

See the upgrading section below for more details.

### Gemini / Nano Banana Image Generation

You can now generate images in the image demo with Google Gemini (Nano Banana Pro).
This model is *very* good at image generation and opens up a lot of new application use cases.
See the [image generation documentation](/ai/images) for setup details.

### Other Changes

- **Upgraded most JavaScript packages to their latest versions.**
- **Upgraded most Python packages to their latest versions.**
- **Added `django.contrib.postgres` to installed apps when using Postgres.**
  This is required to use the Wagtail integration on Django 6.
- **Pinned the Postgres Docker image to version 17 everywhere.** Thanks Eugen for reporting a configuration mismatch for version 18!
- **Improved admin defaults**
  - The ecommerce `Purchase` admin now includes search fields (user email, checkout session ID) and autocomplete for the user field.
  - The `CustomUser` admin now includes search fields for email, first name, and last name.
- **Fixed various type annotations throughout the codebase to pass stricter type checking.**
  This is part of an ongoing effort to improve the type safety of the codebase.
- Upgraded the default uv version to 0.9.17
- Updated `settings.ADMINS` to use a simpler format with just email addresses instead of name/email tuple,
  which will be removed in Django 7.
- Added translations in a few places.
- Added a project description field to `pyproject.toml` that uses your project's description.

#### Fixed

- Fixed a typo in the subscription template filename (`no_subsription_access.html` → `no_subscription_access.html`).
- Fixed a typo in a comment in the team model's manager documentation.
- Fixed timezone warnings in subscription tests by using `timezone.now()` instead of `datetime.utcnow()`.
- Fixed missing return type annotations and added better error handling in ecommerce helpers.
- Added a return statement to the `get_discounted_price` billing utility to match the return type of the function.
- Removed a redundant import in the team invitation views.
- Fixed a few compatibility issues on the experimental Django Ninja build.

### CLI changes

- Released [v0.10 of the CLI](https://github.com/saaspegasus/pegasus-cli/releases/tag/v0.10) which
  adds Django 6.0 support and fixes a few bugs (details in release notes there).

### Upgrading

A few notes on upgrading to Django 6:

- **Django 6 requires Python 3.12 or later.** This was already the default version in Pegasus, but if you are on an older
  version you will need to upgrade. Using any supported Pegasus deployment option should handle this for you.
- If your project was using `django-template-partials` (used by the Pegasus CLI),
  you should review [Django's migration guide](https://github.com/carltongibson/django-template-partials/blob/main/Migration.md).
  Most of this is handled by Pegasus, but **you must remove the `{% load partials %}` from all your existing templates that have it**.

*December 12, 2025*
```

## Example 4: Major feature release

```markdown
## Version 2025.11

Here's what's in the November release.

### New Team scoping features

These updates provide more consistent ways to filter your models based on the current team and help avoid
writing bugs related to forgetting to apply a team filter to your DB queries.

If you're happy with the current teams setup you can largely ignore these changes—they mainly add
new, optional functionality on top of the existing system.

If you would like to introduce more strict Team filtering and checking in your app, review
the changes below and updated sections of the documentation.

Details:

- Added a new [context variable](/teams/#team-context-variable) to keep track of the current team.
- Updated the `TeamsMiddleware` to automatically set/unset the variable for the user's current team.
- Added a new `TeamScopedManager` class to automatically filter a queryset based on the current team (from the context variable).
- Updated `BaseTeamModel` to add `for_team = TeamScopedManager()`, which can be used to automatically filter a team
  moodel based on the current team.
- `TeamsMiddleware` will no longer set `request.team` to the user's default team if it is not in the URL.
  Previously it would return the most recently visited team or the first team that the user is a member of.
  If you need that behavior, you can now use `request.default_team`.
- Added several tests for the above functionality.

See [the updated teams documentation](/teams) for more information about working with these tools,
including how to use them to [always enforce that a team is set](/teams/#strict-team-access).


### Other changes

**Added**

- **Added [AGENTS.md](https://agents.md/) as an additional output format for AI rules files.**
- **You can now clone/copy projects in SaaS Pegasus**—starting a new project with an existing project's configuration
  instead of the defaults each time.  (Thanks Patrick for the suggestion!)

**Changed**

- **Upgraded all Python packages.**
- **Upgraded all JavaScript packages.**
- Updated `.vite` declaration in the `.gitignore` to make it more obvious how to check in vite's built static files if you want to do that. Thanks Lile for suggesting!
- Updated AI API key environment variables to be the defaults used by Pydantic AI so they can be set in a single place.
  You should now set `OPENAI_API_KEY` instead of `AI_CHAT_OPENAI_API_KEY`
  and `ANTHROPIC_API_KEY` instead of `AI_CHAT_ANTHROPIC_API_KEY`.
- Updated links to the Django docs to always point to the latest stable release.
- Updated Kit (formerly ConvertKit) mailing list integration to V4 of the API. Thanks Ben H for suggesting!
  - Changed `CONVERTKIT_API_KEY` setting / environment variable name to `KIT_API_KEY`.
  - Also updated [the docs](/configuration/#kit-formerly-convertkit).
- Updated `django_browser_reload` to only setup the app/middleware if `DEBUG=True`.
  This removes a warning in production. (Thanks Zac for the suggestion!)
- Made minor updates to AI rules files.

**Fixed**

- The employee agent demo now uses a proper `Enum` for departments, preventing invalid options from being used.
- Fixed an issue with using `TransactionTestCase` in certain build configurations due to an issue with `django-waffle`.
  This was done by updating a migration to remove the unexpected tables, as outlined in
  [this comment](https://github.com/django-waffle/django-waffle/issues/317#issuecomment-488398832). Thanks Ben N for reporting!
  - The migration was also renamed - see upgrade section for details.
- Fixed some places where types were set incorrectly or didn't pass type-checking.
- Fixed a bug where `django_browser_reload` was always enabled, even if you had turned it off.


### Upgrading

- If you had any code dependent on `request.team` being set even if there was no team in the URL, you should
update that code to use `request.default_team`.
- If you were using the (Convert)Kit integration, you should update based on the [latest documentation](/configuration/#kit-formerly-convertkit).
- The migration `/apps/web/migrations/0002_patch_djstripe_column.py` was renamed to `/apps/web/migrations/0002_patch_third_party_tables.py`.
  - In most cases, this should apply correctly, but if you have any issues with it,
    you can re-create the migration by running `./manage.py makemigrations web --empty`
    and then copying the contents of the file across (except for the generated `("web", "000x_xxxx"),` dependency line).
    Alternatively, if you don't use `TransactionTestCase`, you can just reject the migration file changes.

*Nov 10, 2025*
```

## Style Notes

1. **Opening sentence**: Always start with a 1-2 sentence summary of what this version adds or fixes
2. **Sections**: Use sections (`###`) for major features; use a flat list for smaller/bugfix releases
3. **Sub-sections**: Use `**Added**`, `**Changed**`, `**Fixed**` groupings when there are many changes
4. **Bold for emphasis**: Use `**bold**` for the first part of important items
5. **Action verbs**: Start items with "Added", "Fixed", "Improved", "Updated", "Removed", "Upgraded", etc.
6. **Specificity**: Be specific about what changed, not vague ("Fixed sidebar bug" → "Fixed sidebar navigation not highlighting the active page")
7. **User impact**: Focus on what users will experience, not implementation details
8. **Thanks**: Credit contributors with "Thanks [Name] for reporting!" or "Thanks [Name] for the suggestion!"
9. **Library updates**: Mention "Upgraded all Python/JavaScript packages" rather than listing each one, unless specific libraries are significant
10. **Links**: Include links to relevant documentation, issues, or external resources where helpful
11. **Upgrading section**: Include an "Upgrading" section for releases that require manual migration steps
12. **Date**: End each release with the date in `*Month Day, Year*` format
