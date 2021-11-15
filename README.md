# data-nerds-tool-survey-results

## Overview

In this repository, I am analyzing the results from the Data Nerds Data Tools survey I sent out.  I also decided to treat this simple analysis project as I would any production application and have included the following:

- Unit tests done in pytest [tests](./tests/)
- A [pyproject.toml](pyproject.toml) file that includes my project configurations which include my pinned packages via poetry
- Continuous Integration done via GitHub Actions [GitHub Actions](./.github/workflows/)
- A [Pull Request Template](./.github/pull_request_template.md) which is useful for pre-populating the Pull Request description.
- A [Makefile](Makefile) that streamlines common commands as well as used in the GitHub Actions.
- A [LICENSE](LICENSE) file which is good to ensure no one steals or misuses your project.
- A [.pre-commit] file which will run a series of checks prior to committing a change.  You can read more about pre-commit checks [here](https://pre-commit.com/)

## Note

Normally I would do my prototyping in a separate directory to reduce package dependencies for my data application but for the sake of highlighting my workflow and process, I decided to keep it in here.

## Results Juicebox Summary

Visualized results of the survey can be found here [Juicebox - Data Tools Survey Results](https://antonison-cg.myjuicebox.io/a/data_tools_survey_results/#4t7FF6tw5aa)