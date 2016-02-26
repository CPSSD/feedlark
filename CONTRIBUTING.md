CONTRIBUTING.md
===============

Branches
--------

Branches are named like so:

    assignee_first_initial/name#issue_number

For multiple assignees the initals can be hyphenated.

For example:

	c/atom_support#43
	c-r/atom_support#43

Pull Requests
-------------

Changes to the repository are made on other branches and merged onto the
`master` branch.

### CI

Jekyll support is live. Please see [the ci page](http://ci.dvxl.me) to check
build status.

Access has been given to all team members, but if anybody else wants access to
the CI, just send me an email. Find it at my github!

To test your code, please make the last build have the `[ci build]` in the
git commit message. For example:

    0e25143 [ci build] Merge branch 'feature/delete-repo'


### Formatting Pull Requests

Your pull request body you should have this text:

    This pull request connects to #issue_number

With the previous example this would be:

    This pull request connects to #1

This prevents waffle from opening a separate issue for pull requests.

### Code Reviews

The code **must** be reviewed before it is merged by at least one team
member. It also **must** past the build.

Preferably a few team members should okay the pull request before it gets
merged.

Updating Documentation
----------------------

### Formatting & File Structure

All documentation should be in Markdown (.md) format. Where applicable, use the filename `README.md` and place the file in its appropriate folder. This means that GitHub will display the information below the file list.

### New Documentation

Where applicable, documentation updates related to new code/commits should be added to their own commit in your current branch, following this example format:

	ea283476	#123	Add gearman worker for word vectorisation
	fd723145	#124	Add documentation for #123

### Updated Documentation

For updating the documentation in the general case, the following procedure should be followed:

	- Create/switch to branch `doc-update`
	- Make your changes & commit
	- Make a PR to master, with a title in the following format: `Documentation update for X in path/FILE.md`
	- When merged, delete the branch `doc-update`
