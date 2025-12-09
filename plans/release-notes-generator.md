I would like to build a release notes generator for my application, SaaS Pegasus.

I want to use Pydantic AI. There should be a few tools it has access to.

The first is `make_diff`, which, given any two commits or branches should return a formatted string
with a summary and details of those changes. There is already a make_diff file in the repo that
does this, but we may need to adapt it to be a tool call. We will also likely need to pass in the
repository directory to the tool, which we can hard-code in the environment somewhere.

The second should be `get_release_notes`. This should be able to return a markdown-formatted release
notes reference that can be used as an example. This tool will be reading from the file system,
and probably the path will also need to be configurable (hard code in environment).

The returned output of the agent should be a draft of release notes, in the style of the current
release notes, based on the provided diff.

You can start with the weather example in `agent.py` and remove all weather-relateed functionality,
replacing it with the above.

There is an instructions file for the agent you can use in the instructions folder.
