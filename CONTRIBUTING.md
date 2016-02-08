CONTRIBUTING.md
===============



Branches
--------

Branches are named like so:

    assignee_first_initial/name#issue_number
	
For multiple assignees the initals can be hyphenated.

For example:
	
	c/atom_support#43
	c_r/atom_support#43



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
