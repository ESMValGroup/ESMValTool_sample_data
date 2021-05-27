# Contributing guidelines

We welcome any kind of contribution to our software, from simple comment or question to a full fledged [pull request][1].

A contribution can be one of the following cases:

1. you have a question;
2. you think you may have found a bug (including unexpected behavior);
3. you want to make a change to the code (e.g. to fix a bug, to add a new feature, to update documentation).

The sections below outline the steps in each case.

## You have a question

1. use the search functionality [here][2] to see if someone already filed the same issue;
2. if your issue search did not yield any relevant results, make a new issue;
3. apply the "question" label; apply other labels when relevant if you can.

## You think you may have found a bug

1. use the search functionality [here][2] to see if someone already filed the same issue;
2. if your issue search did not yield any relevant results, make a new issue, making sure to provide enough information to the rest of the community to understand the cause and context of the problem. Depending on the issue, you may want to include:
    - some identifying information (name and version number) for dependencies you're using;
    - information about the operating system;
3. apply relevant labels to the newly created issue if you can.

## You want to make a change to the code

1. (**important**) announce your plan to the rest of the community _before you start working_. This announcement should be in the form of a (new) issue [here][2];
2. (**important**) wait until some kind of consensus is reached about your idea being a good idea;
3. if needed, create your own feature branch off of the latest main branch. While working on your feature branch, make sure to stay up to date with the main branch by pulling in changes, possibly from the 'upstream' repository (follow the instructions [here][4] and [here][5]);
<!-- 4. make sure the existing tests still work by running ``python setup.py test``; -->
<!-- 5. add your own tests (if necessary); -->
6. update or expand the documentation;
7. [push][6] your feature branch to (your fork of) the ESMValTool_sample_data repository on GitHub;
8. create the pull request, e.g. following the instructions [here][7].

In case you feel like you've made a valuable contribution, but you don't know how to write or run tests for it, or how to generate the documentation: don't let this discourage you from making the pull request; we can help you! Just go ahead and submit the pull request, but keep in mind that you might be asked to append additional commits to your pull request.

## General guidelines

`ESMValTool_sample_data` is a subproject of ESMValTool. For general documentation about contributing to ESMValTool projects, see the [ESMValTool contributing guidelines][8].

## License

By contributing, you agree that your contributions will be licensed under the Apache 2.0 license.

## Attribution

These guidelines were derived from the open-source [template for contribution guidelines from the Netherlands eScience Center][9] licensed under Apache 2.0.

[1]: https://help.github.com/articles/about-pull-requests/
[2]: https://github.com/ESMValGroup/ESMValTool_sample_data/issues
[3]: https://help.github.com/articles/autolinked-references-and-urls/#commit-shas
[4]: https://help.github.com/articles/configuring-a-remote-for-a-fork/
[5]: https://help.github.com/articles/syncing-a-fork/
[6]: https://help.github.com/articles/pushing-commits-to-a-remote-repository
[7]: https://help.github.com/articles/creating-a-pull-request/
[8]: https://docs.esmvaltool.org/en/latest/community/index.html
[9]: https://github.com/NLeSC/python-template/blob/master/CONTRIBUTING.md


# Updating the test data

Create and activate conda environment with the required dependencies
```bash
conda env create -f environment.yml -n esmvaltool_test_data
conda activate esmvaltool_test_data
```

Copy [`config.yml.template`](config.yml.template) to `config.yml` and customize, at least add your
ESGF username and password.
Create an account on [https://esgf-data.dkrz.de/user/add/](https://esgf-data.dkrz.de/user/add/) if you do not have one.

Run
```bash
python download_sample_data.py
```
to download a sample of the test data.

[`datasets.yml`](datasets.yml) defines the datasets that will be downloaded. Any datasets that are problematic can be added under `ignore`.
