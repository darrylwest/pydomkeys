# Welcome to PyDomKeys contributing guide <!-- omit in toc -->

Thank you for investing your time in contributing to our project! Any contribution you make will be reflected in [pydomkeys](https://github.com/darrylwest/pydomkeys/) :sparkles:.

Please read our [Code of Conduct](./CODE_OF_CONDUCT.md) to keep our community approachable and respectable.

In this guide you will get an overview of the contribution workflow from opening an issue, creating a PR, testing, linting, etc, and merging the PR.

_Use the table of contents icon on the top left corner of this document to get to a specific section of this guide quickly._

## New contributor guide

To get an overview of the project, read the [README](README.md). Here are some resources to help you get started with open source contributions:

- [Set up Git](https://docs.github.com/en/get-started/quickstart/set-up-git)
- [Collaborating with pull requests](https://docs.github.com/en/github/collaborating-with-pull-requests)


## Getting started


### Development Tools

* poetry for package manager (could change to pdm soon)
* pytest, pytest-cov
* coverage
* pylint, and ruff linters
* mypy
* refurb

We also currently use [just](https://github.com/casey/just) as a command line runner, but it's not a requirement.  And, if we switch to pdm, we would use thier script support to eliminate just.  In any case, the command targets in the justfile can easily be executed on the command line.

### Code Coverage

We expect a minimum of 100% code coverage for this project.

### Issues

#### Create a new issue

If you spot a problem with the docs or a bug in the code, first search the issues to see if this has been reported.  If a relevant issue is not in the list then feel free to create one.

#### Solve an issue

Scan through our to find one that interests you. You can narrow down the search using `labels` as filters. See [Labels](/contributing/how-to-use-labels.md) for more information.

### Make Changes

_TBD_

#### Make changes locally

1. Fork the repository.
- Using GitHub Desktop:
  - [Getting started with GitHub Desktop](https://docs.github.com/en/desktop/installing-and-configuring-github-desktop/getting-started-with-github-desktop) will guide you through setting up Desktop.
  - Once Desktop is set up, you can use it to [fork the repo](https://docs.github.com/en/desktop/contributing-and-collaborating-using-github-desktop/cloning-and-forking-repositories-from-github-desktop)!

- Using the command line:
  - [Fork the repo](https://docs.github.com/en/github/getting-started-with-github/fork-a-repo#fork-an-example-repository) so that you can make your changes without affecting the original project until you're ready to merge them.

2. Install the package manager if necessary and install all the dependencies (poetry install)

3. Create a working branch and start with your changes!  The branch should have a short name and the issue number you are working on.

### Commit your update

Commit the changes once you are happy with them. Don't forget to [self-review](/contributing/self-review.md) to speed up the review process:zap:. (see precommit target)

### Pull Request

When you're finished with the changes, create a pull request, also known as a PR.
- Fill the "Ready for review" template so that we can review your PR. This template helps reviewers understand your changes as well as the purpose of your pull request.
- Don't forget to [link PR to issue](https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue) if you are solving one.
- Enable the checkbox to [allow maintainer edits](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/allowing-changes-to-a-pull-request-branch-created-from-a-fork) so the branch can be updated for a merge.
Once you submit your PR, a Docs team member will review your proposal. We may ask questions or request additional information.
- We may ask for changes to be made before a PR can be merged, either using [suggested changes](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/incorporating-feedback-in-your-pull-request) or pull request comments. You can apply suggested changes directly through the UI. You can make any other changes in your fork, then commit them to your branch.
- As you update your PR and apply changes, mark each conversation as [resolved](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/commenting-on-a-pull-request#resolving-conversations).
- If you run into any merge issues, checkout this [git tutorial](https://github.com/skills/resolve-merge-conflicts) to help you resolve merge conflicts and other issues.

### Your PR is merged!

Congratulations :tada::tada: The PyDomKeys team thanks you :sparkles:.

Once your PR is merged, your contributions will be publicly visible on the PyDomKeys repo.

Thanks, happy coding!
