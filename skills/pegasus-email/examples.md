July 2026: Free Announcement

Hi <<First Name>>,

Cory from SaaS Pegasus here. I’m very excited for this announcement today, and I'll just cut to the chase: You can now use Pegasus for free!

What you get out-of-the-box is the core of Pegasus: a ready-to-use Django project foundation built for the modern era. It's the exact same code that has powered thousands of production apps built on the proprietary version of Pegasus—with sensible, modern default tooling (uv, vite, ruff, mypy, agent skills, etc.), and the essential batteries included (auth, Tailwind, DRF, Celery, etc.).

You can use Pegasus for free by logging into your existing account and creating a project today. You'll be able to directly download the code or use Pegasus's built in sync-to-Github feature. You can make as many projects as you want, and even manage your projects in your favorite coding agents. On the free tier, all code is MIT-licensed and yours forever.

Alternatively, if you don't want to customize, you can immediately fork the example repo on Github here.

Note that some features—including billing, multitenancy, and integrated AI agents—are still on the paid version of Pegasus.

My goal is to make Pegasus the best way to start a Django project, and I believe that's already true today. Please check it out and let me know if you have any feedback! I'll read and respond to every reply.

Hope you're having a good start to July! I'm currently enjoying the melting heat in Canada. 🫠

Cory

p.s. To celebrate the launch, I'm offering 50% off Pegasus Unlimited. If you try the free version and like what you see, the discount will be automatically applied on checkout.


---
May 2026: comicify/scriv/misc

Hello!

Cory from SaaS Pegasus (the Django boilerplate) here with the monthly-ish update.

In the last couple months I've been busy dogfooding Pegasus on some real apps. First, I built a new app called comicify.me. It lets you use the latest AI models to make comic books featuring your family. Like this:

I've been using it with my kids regularly and it's been super fun. Their favorite part is finding all the mistakes that the AI inevitably makes! If you want to try it, it's free to use till I hit my API key spending limit. 😅

Comicify went from idea to live product in a few weekends. I need to write or make a video on my process, because it is so different than it was just a few months ago. I used Pegasus as a foundation, Claude design for all the UI, and Claude code to build everything. Not to mention that the product itself is like 95% prompts and agents. Software is changing so fast. It's fun and exciting and weird and scary at the same time.

The other thing I did recently is completely rewrite Scriv's AI stack. If you're not familiar, Scriv is a "chat with your knowledge base" app I launched a few years ago. It powers the chatbot on the Pegasus docs site and the bot in the Slack community.

Back when I made Scriv (in the ancient past of 2023), it was built on a pattern called Retrieval Augmented Generation (RAG). RAG used to be state-of-the-art, but these days, thanks to smarter models and longer contexts, it is all but obsolete. So I thought I'd see if I could convert the whole thing to agents using Pegasus's new Pydantic AI stack. The end result has been great—the bots are smarter and the app is much more extensible. The Scriv codebase with these changes is available on the Pegasus marketplace.

Of course, these projects have motivated a number of updates to Pegasus. Here are some of the highlights:
- Pegasus now runs on Python 3.14.
- New projects use native Tailwind/DaisyUI classes instead of the old Pegasus custom classes. I find this helps coding agents, which seem to do a better job the more "standard" your stack is.
- Pegasus's built-in agent chat now streams thinking and tool calls in real time, giving users better visibility into what's happening.
- I conducted a big security audit. Added protections against supply chain attacks, ran multiple AI-scanning tools and patched a number of small attack vectors.
- Agents can now manage your Pegasus projects. Say "spin up a new pegasus project", "let's enable billing" or "upgrade to the latest release" and they'll handle the rest.
- A bunch of other small changes, too many to list here, that you can find in the release notes.

That's it from me for the month. As always, if you have any feedback or suggestions, just hit reply.

Hope you're handling the rapid change we're all going through ok!

Cory

---
March 2026: Front end

Cory from Pegasus here with the monthly SaaS Pegasus update.

# Upgrade your Pegasus projects from the command line

My favorite update from this month is that you can now upgrade your Pegasus project from the command line. Combined with the Pegasus Claude skills you can literally open Claude and type "hey can you update my project to the latest Pegasus release" and it will do that end-to-end until you have a mergeable PR ready to go. What used to be a once-every-three-month chore is now something I can do on all my projects in a few minutes.

I recorded a video of this process and how it works if you want to learn more.

# Standalone front end improvements

I'm continuing to build out the standalone React front end and am hoping to get it to full parity with the other architecture options. This month I've updated nearly everything related to users, auth, and team management. The big ones still remaining are biling and AI workflows.

# Upgrades and cleanups

This past period I focused a lot on technical debt and cleanup. Speed is great, but only if you have a solid foundation. Here are the highlights:
The front end now uses Vite 8 everywhere. This should dramatically speed up production build times.
Stripe and dj-stripe have been finally updated to their latest versions. Billing code updates should be much smoother moving forwards.
All AI calls go through Pydantic AI now and I ditched LiteLLM (which turned out to be great timing given the recent supply chain attack on the package). I've been using Pydantic AI a ton and am really loving it for building agents.
That's it for this month! Can't believe it's almost April already.

Hope you're doing well,
Cory

---
Jan 2026: Agents

Hello,

So, like many other developers, I've been using agents in my work a lot more lately. In the last couple months I've gone from mostly working in my IDE and editing code to mostly working in Claude Code and reviewing code.

I have very mixed feelings about this change and what it means for me, coders, and the future of software development. But regardless of how I feel, the change is coming and I'm hoping to bring myself and SaaS Pegasus along for the ride.

So, this past month, I spent most of my time building applications with Claude Code and other agent tools and then incorporating workflows and changes that I found useful back into Pegasus. My goal is to make Pegasus the best foundation to build on—with or without AI (but probably with it more and more).

Here's what that process led to this month.

Skills for Claude Code

I've started shipping agent skills with Pegasus—reusable prompts that handle common tasks like resolving merge conflicts during upgrades, fixing type errors, and setting up git worktrees. These are skills that I am using regularly on my own projects, and iterating on as I go. There are only a handful now, but I'm hoping to expand these substantially over time.

And they're also open source! I'll be putting generic Django skills here, and Pegasus-specific ones here. If you have skills you've found especially useful, I'd love contributions.

Standalone frontend ported to shadcn/ui

The standalone React frontend has been rebuilt on shadcn/ui. Beyond being a better component library, LLMs are remarkably good at working with shadcn—it's become the de facto standard and there is great tooling in the ecosystem for agents. This makes AI-assisted frontend work much smoother.

Type checking with mypy

This is an indirect one. When building with agents, it's important to give them as many verification tools as possible. Tests, linters, etc. And one of the more useful tools—especially in larger/more mature projects—is type checking. Having a strongly typed system helps agents catch errors and verify their work before code review.

To this end, I've added optional type checking to Pegasus, built on mypy (I'll probably add ty support once it's out of beta). The release also includes a number of small improvements caught by the type-checker.

Git worktree support

This one is still pretty experimental, but for those running multiple agents in parallel (or just working on multiple branches), Pegasus now includes utilities for managing git worktrees with isolated ports for all services. Each worktree gets its own database and dev server ports so they don't conflict. I'm still having a hard time wrapping my head around doing more than one or two things at once, but if you are a big multi-tasker, this should help!

As always, you can view the complete release notes online.

Finally I thought I'd leave you with this comment from a Pegasus community member about how he's building on top of Pegasus:

"In my view SaaS Pegasus is a perfect match for AI assisted coding - up to vibe coding. It's is the solid foundation and it provides valuable best practices for the model to look at. With SaaS Pegasus, vibe coding feels like dancing on solid ground with guardrails around. Last year, I played around a lot and also built apps on FastAPI, FastHTML, the new Air by Audrey and Danny Greenfield, Litestar, also client/mobile apps with Flet. When it comes to needing a solid SaaS and app foundation SaaS Pegasus and Django win hands down."

That's it from me! Hope you're having a great start to the year.

Cory

p.s. Got a question or suggestion for me or Pegasus? Just hit reply.