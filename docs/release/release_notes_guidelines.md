# Release Notes Guidelines

## Instructions for Maintainers

- A maintainer or release manager can create a new release tag
- Change log for all the PRs merged since the last release should be included in the release notes
- When merging PRs ensure that the related issue is tagged in the PR
- Issue Templates are configured in the repositories under `.github/ISSUE_TEMPLATE` directory
- Automatically generated release notes `.github/release.yml` is configured for the repo and must be used while creating a new release tag
- The automatically generated release notes include a list of merged pull requests, a list of contributors to the release, and a link to a full changelog
- Sample templates are available below for reference:

  - **Release Templates**  
  &nbsp;&nbsp;&nbsp;&nbsp;[release.yml](release-template/release.yml)

  - **Issue Templates**  
    &nbsp;&nbsp;&nbsp;&nbsp;[bug.yml](../build/issue-templates/bug.yml)  
    &nbsp;&nbsp;&nbsp;&nbsp;[documentation.yml](../build/issue-templates/documentation.yml)  
    &nbsp;&nbsp;&nbsp;&nbsp;[feature.yml](../build/issue-templates/feature.yml)  
    &nbsp;&nbsp;&nbsp;&nbsp;[maintenance.yml](../build/issue-templates/maintenance.yml)  
