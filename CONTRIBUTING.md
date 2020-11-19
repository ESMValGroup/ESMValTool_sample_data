# Contributing guidelines

We welcome any kind of contribution to our software, from simple comment or question to a full fledged [pull request][1].

A contribution can be one of the following cases:

1. you have a question;
2. you think you may have found a bug (including unexpected behavior);
3. you want to make some kind of change to the code base (e.g. to fix a bug, to add a new feature, to update documentation).

The sections below outline the steps in each case.

## You have a question

1. use the search functionality [here][2] to see if someone already filed the same issue;
2. if your issue search did not yield any relevant results, make a new issue;
3. apply the "Question" label; apply other labels when relevant.

## You think you may have found a bug

1. use the search functionality [here][2] to see if someone already filed the same issue;
2. if your issue search did not yield any relevant results, make a new issue, making sure to provide enough information to the rest of the community to understand the cause and context of the problem. Depending on the issue, you may want to include:
    - the [SHA hashcode][3] of the commit that is causing your problem;
    - some identifying information (name and version number) for dependencies you're using;
    - information about the operating system;
3. apply relevant labels to the newly created issue.

## You want to make some kind of change to the code base

1. (**important**) announce your plan to the rest of the community _before you start working_. This announcement should be in the form of a (new) issue [here][2];
2. (**important**) wait until some kind of consensus is reached about your idea being a good idea;
3. if needed, create your own feature branch off of the latest master commit. While working on your feature branch, make sure to stay up to date with the master branch by pulling in changes, possibly from the 'upstream' repository (follow the instructions [here][4] and [here][5]);
<!-- 4. make sure the existing tests still work by running ``python setup.py test``; -->
<!-- 5. add your own tests (if necessary); -->
6. update or expand the documentation;
7. [push][6] your feature branch to (your fork of) the Python Template repository on GitHub;
8. create the pull request, e.g. following the instructions [here][7].

In case you feel like you've made a valuable contribution, but you don't know how to write or run tests for it, or how to generate the documentation: don't let this discourage you from making the pull request; we can help you! Just go ahead and submit the pull request, but keep in mind that you might be asked to append additional commits to your pull request.

## Code style

To increase the readability and maintainability or the ESMValTool and related source code, we aim to adhere to best practices and coding standards. Please have a look at our [code style guidelines][8].

## Licence

By contributing, you agree that your contributions will be licensed under the Apache 2.0 licence.

## Attribution

These guidelines were derived from the open-source [template for contribution guidelines from the Netherlands eScience Center][9] licenced under Apache 2.0.


[1]: https://help.github.com/articles/about-pull-requests/
[2]: https://github.com/ESMValGroup/ESMValTool_sample_data/issues
[3]: https://help.github.com/articles/autolinked-references-and-urls/#commit-shas
[4]: https://help.github.com/articles/configuring-a-remote-for-a-fork/
[5]: https://help.github.com/articles/syncing-a-fork/
[6]: https://help.github.com/articles/pushing-commits-to-a-remote-repository
[7]: https://help.github.com/articles/creating-a-pull-request/
[8]: https://docs.esmvaltool.org/projects/esmvalcore/en/latest/contributing.html#code-style
[9]: https://github.com/NLeSC/python-template/blob/master/CONTRIBUTING.md
