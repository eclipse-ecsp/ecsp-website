# Table of Contents

This section describes the step-by-step instructions for building Cloud microservices, Mobile App, SDK, and Device Client components in the Eclipse CSP environment.

1. [Overview](#overview)

2. [Build New Cloud Components using CI tool GitHub Actions](#build-new-cloud-components-using-ci-tool-github-actions)

3. [Build Existing Cloud Components manually in Local](#build-existing-cloud-components-manually-in-local)

4. [License Compliance](#license-compliance)

5. [GitHub Action Runners](#github-action-runners)

6. [Build Device Client on Local and via Github Actions](#build-device-client-on-local-and-via-github-actions)

7. [Build IOS and Android Mobile SDK and App on Local and via Github Actions](#build-ios-and-android-mobile-sdk-and-app-on-local-and-via-github-actions)

## Overview

- Custom libraries, Stream Processors, and APIs utilize the `Maven` ecosystem for build automation and lifecycle management.
- Device Client is an edge component and can be built using `CMake` and other dependant Linux distribution components.
- IOS Mobile SDK and sample App use an IOS simulator platform and is built using `xcodebuild` tool.
- Android Mobile SDK and sample App use a `Gradle` ecosystem to manage the build automation and lifecycle of the component.
- GitHub Actions are utilized to automate the build workflow.
- Libraries are published as artifacts to the GitHub Packages.
- Libraries are shipped as dependencies for the Stream Processors and API components.
- Libraries are not containerized.
- Stream Processors and API components are containerized using Docker and are published to container registry.
- Docker images are deployed to the environment using the Kubernetes manifests.
- Kubernetes stores manifests as helm charts in the [Charts](https://github.com/eclipse-ecsp/csp-charts) repository.

## Build new Cloud Components using CI Tool GitHub Actions

- GitHub workflows would need to be implemented to automate the build process.
- Workflows are defined in the `.github/workflows` directory by a YAML file checked in to the repository.
- A workflow can be triggered by creating a release, by creating a Pull Request or upon merging the Pull Request to the `main` branch.
- A workflow can also be manually triggered from the GitHub Actions tab in the repository.
- Custom libraries can be published as artifacts to the GitHub Packages.
- Deployable components are containerized using Docker and published to container registry.
- The workflow for device client, IOS Mobile SDK and Android Mobile SDK packages the artifacts as standalone release distribution.
Note: See workflows for existing components for reference  

### Create a Release

- Maintainers of the repository can release in the GitHub repository.
- The release triggers the build workflow in the GitHub Actions.
- Release notes are configured to be generated automatically and the template is defined in the `.github/release.yml` file on the repository.

## Build existing Cloud Components manually in Local

Refer the ECSP Github repositories for detailed components build processes

### Fork the repository

- Fork the repository to your GitHub account
- Clone the forked repository locally

### Build using maven tool

- To install Maven in the local machine, see the information <https://maven.apache.org/install.html>
- The build process requires access to download artifacts from the GitHub packages.
- The following configuration is added in the `pom.xml` file to download the dependent artifacts from GitHub Packages

```xml
<distributionManagement>
    <repository>
        <id>ossrh</id>
        <name>Maven central</name>
        <url>https://oss.sonatype.org/service/local/staging/deploy/maven2/</url>
    </repository>
</distributionManagement>
```

- Create a GitHub Personal Access Token (PAT) at <https://github.com/settings/tokens> and grant `read:packages` permission.
- Use Configure SSO and authorize your PAT for your GitHub organization if required.
- Add the following configuration in the './settings.xml` file

```xml  
  <settings>
    <servers>
      <server>
        <id>github</id>
        <username>GITHUB_USERNAME</username>
        <password>GITHUB_TOKEN</password>
      </server>
    </servers>
  </settings>
```

- Run `mvn clean install` to build the project
- The build artifacts will be available in the `target` directory

### Create a Pull Request

- Contributors can create a Pull Request (PR) to merge the changes to the main repository.
- The PR triggers the build workflow in the GitHub Actions.
- PR must be reviewed and approved by the maintainers and merged only if the CI build action is successful.
- The Issue number must be mentioned in the PR description.
- The PR description must align to the configured [Pull Request Template](pull-request-template/pull_request_template.md)
- The issue templates are defined in the `.github/ISSUE_TEMPLATE` directory on the repository.
- The template is defined in the `.github/pull_request_template.md` file on the repository.

### Publish the artifacts to GitHub Packages

- Custom libraries are published as artifacts to GitHub Packages under the `csp-central-repo` repository.
- The workflow is configured to set up the JDK version to Zulu distribution of Java 17 with the settings path pointed to location in the repository workspace.
- The workflow includes a step to run `mvn deploy` to publish the artifacts to GitHub Packages.

```yaml
steps:
    - uses: actions/checkout@v4
    - name: Set up JDK 17
      uses: actions/setup-java@v4
      with:
        java-version: '17'
        distribution: 'zulu'
        server-id: github # Value of the distributionManagement/repository/id field of the pom.xml
        settings-path: ${{ github.workspace }} # location for the settings.xml file

    - name: Build with Maven
      run: mvn -DskipTests=true -B package --file pom.xml -s $GITHUB_WORKSPACE/settings.xml
      env:
        GITHUB_TOKEN: ${{ secrets.REPO_TOKEN }}

    - name: Publish to GitHub Packages Apache Maven
      run: mvn -DskipTests=true deploy -s $GITHUB_WORKSPACE/settings.xml
      env:
        GITHUB_TOKEN: ${{ secrets.REPO_TOKEN }}

```

- Refer the package link mentioned in the [published_libraries](libraries.md) list to view the published version of the library.

### Containerize and Publish the Docker Images to Container Registry

Note: Below points can also be referred for newly created components

- Deployable units are structured as a single module project and multi-module project.
- The workflow is configured to set up the JDK version to Zulu distribution of Java 17 with the settings path pointed to location in the repository workspace.
- The workflow includes step to run `mvn clean install` to package the artifacts.
- The workflow includes the steps to connect to the container registry and push the Docker image.

```yaml
 steps:
    - uses: actions/checkout@v3
    - name: Set up JDK 17
      uses: actions/setup-java@v4
      with:
        java-version: '17'
        distribution: 'zulu'
        cache: maven
    - name: Build with Maven
      run: mvn -B package spring-boot:repackage --file pom.xml -s $GITHUB_WORKSPACE/mvn_settings.xml
      env:
        GITHUB_TOKEN: ${{ secrets.REPO_TOKEN }}
    - name: Log in to the Container registry
      uses: docker/login-action@65b78e6e13532edd9afa3aa52ac7964289d1a9c1
      with:
        registry: ${{ env.REGISTRY }}
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}
```

- Before pushing the Docker image to the container registry, the workflow extracts the Group id, Artifact id and Version (GAV) from the pom.xml file and includes steps to determine the hashcode of the image tags.

```yaml
 - name: Extract GAV
   id: extract
   uses: andreacomo/maven-gav-extractor@v2
 - name: Log GAV
   run: |
        echo ${{ steps.extract.outputs.group-id }}
        echo ${{ steps.extract.outputs.artifact-id }}
        echo ${{ steps.extract.outputs.version }}
        echo ${{ steps.extract.outputs.name }}
   shell: bash

 - id: lower-repo
   name: Repository to lowercase
   run: |
        echo "githubowner=${GITHUB_REPOSITORY_OWNER@L}" >> $GITHUB_OUTPUT

 - name: Determine image tags hash
   if: env.IMAGE_TAG_HASH == ''
   run: |
        echo "IMAGE_TAG_HASH=${GITHUB_SHA::7}" | tee -a $GITHUB_ENV
 - name: Extract metadata (tags, labels) for Docker
   id: meta
   uses: docker/metadata-action@9ec57ed1fcdbf14dcef7dfbe97b2010124a938b7
   with:
      images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}

 - name: Build and push Docker image
   id: push
   uses: docker/build-push-action@f2a1d5e99d037542a71f64918e516c093c6f3fc4
   with:
      context: .
      push: true
      tags: ${{ env.REGISTRY }}/${{  steps.lower-repo.outputs.githubowner }}/${{  steps.extract.outputs.artifact-id }}:${{ steps.extract.outputs.version }}-${{ env.IMAGE_TAG_HASH }}
      labels: ${{ steps.meta.outputs.labels }}
      build-args: |
            ARTIFACT_ID=${{  steps.extract.outputs.artifact-id }}
            ARTIFACT_VERSION=${{ steps.extract.outputs.version }}
```

- The workflow also includes a step to generate signed build provenance attestations for generated artifacts.

```yaml
    - name: Generate artifact attestation
      uses: actions/attest-build-provenance@v1
      with:
        subject-name: ${{ env.REGISTRY }}/${{  steps.lower-repo.outputs.githubowner }}/${{ steps.extract.outputs.artifact-id}}
        subject-digest: ${{ steps.push.outputs.digest }}
        push-to-registry: true

```

- For multi-module projects, the GAV is extracted from each child module.
- The POM file location is added for each stage.

```yaml
   - name: Extract gateway3 pom
     id: extract-api-gateway3
     uses: andreacomo/maven-gav-extractor@v2
     with:
        pom-location: ${{ github.workspace }}/api-gateway3/pom.xml
   - name: Log api-gateway3
     run: |
       echo ${{ steps.extract-api-gateway3.outputs.group-id }}
       echo ${{ steps.extract-api-gateway3.outputs.artifact-id }}
       echo ${{ steps.extract-api-gateway3.outputs.version }}
       echo ${{ steps.extract-api-gateway3.outputs.name }}
     shell: bash

   - name: Extract registry pom
     id: extract-api-registry
     uses: andreacomo/maven-gav-extractor@v2
     with:
       pom-location: ${{ github.workspace }}/api-registry/pom.xml
   - name: Log api-registry
     run: |
       echo ${{ steps.extract-api-registry.outputs.group-id }}
       echo ${{ steps.extract-api-registry.outputs.artifact-id }}
       echo ${{ steps.extract-api-registry.outputs.version }}
       echo ${{ steps.extract-api-registry.outputs.name }}
     shell: bash
```

- For each module, the Docker image is pushed to the container registry.
- The Context Path and FilePath of the dockerfile is added for each module in the build and push stage.
- Artifacts are generated for each child module and signed build provenance attestations are generated for each module.

```yaml
   - name: Build and push Docker image for API Gateway
     id: push-api-gateway
     uses: docker/build-push-action@f2a1d5e99d037542a71f64918e516c093c6f3fc4
     with:
         context: ./api-gateway3
         file: ./api-gateway3/Dockerfile
         push: true
         tags: ${{ env.REGISTRY }}/${{  steps.lower-repo.outputs.githubowner }}/${{  steps.extract-api-gateway3.outputs.artifact-id }}:${{ steps.extract-api-gateway3.outputs.version }}-${{ env.IMAGE_TAG_HASH }}
         labels: ${{ steps.meta.outputs.labels }}
         build-args: |
           PROJECT_JAR_NAME=${{  steps.extract-api-gateway3.outputs.artifact-id }}-${{ steps.extract-api-gateway3.outputs.version }}
     env:
         GITHUB_TOKEN: ${{ secrets.REPO_TOKEN }}

   - name: Build and push Docker image for API Registry
     id: push-api-registry
     uses: docker/build-push-action@f2a1d5e99d037542a71f64918e516c093c6f3fc4
     with:
       context: ./api-registry
       file: ./api-registry/Dockerfile
       push: true
       tags: ${{ env.REGISTRY }}/${{  steps.lower-repo.outputs.githubowner }}/${{  steps.extract-api-registry.outputs.artifact-id }}:${{ steps.extract-api-registry.outputs.version }}-${{ env.IMAGE_TAG_HASH }}
       labels: ${{ steps.meta.outputs.labels }}
       build-args: |
         PROJECT_JAR_NAME=${{  steps.extract-api-registry.outputs.artifact-id }}-${{ steps.extract-api-registry.outputs.version }}
     env:
       GITHUB_TOKEN: ${{ secrets.REPO_TOKEN }}

   - name: Generate artifact attestation api gateway
     uses: actions/attest-build-provenance@v1
     with:
       subject-name: ${{ env.REGISTRY }}/${{  steps.lower-repo.outputs.githubowner }}/${{ steps.extract-api-gateway3.outputs.artifact-id}}
       subject-digest: ${{ steps.push-api-gateway.outputs.digest }}
       push-to-registry: true

   - name: Generate artifact attestation api registry
     uses: actions/attest-build-provenance@v1
     with:
       subject-name: ${{ env.REGISTRY }}/${{  steps.lower-repo.outputs.githubowner }}/${{ steps.extract-api-registry.outputs.artifact-id}}
       subject-digest: ${{ steps.push-api-registry.outputs.digest }}
       push-to-registry: true
```

- The dockerfile is configured in the repositories,
- Some components utilize custom base images as Docker entry points, which are pulled from the [Docker Base Image](https://hub.docker.com/u/eclipseecsp) repository.

### Authentication

- A GitHub Personal Access Token (PAT) has been created at <https://github.com/settings/tokens> and grants the `read:packages` and `write:packages`
- SSO is configured for the token to authorize for the source organization
- The token is added as a secret in the repository settings and referenced in the workflow file.

### Consolidated List of Components and Libraries

For the list of components, libraries, the build ecosystem, and repository links, see:

- [List of Components](components.md)
- [List of Libraries](libraries.md)

## License Compliance

- Components are scanned and reviewed for OSS license compliance using [Eclipse Dash License Tool](https://github.com/eclipse-dash/dash-licenses)
- The Dash License Tool is integrated with the GitHub Actions workflow to scan the dependencies.
- The license compliance report is generated as artifacts upon execution of the workflow and reviewed by the maintainers.

## GitHub Action Runners

The GitHub-hosted runners `ubuntu-latest` and `macos-latest` are utilized for the build process.

Below are the configurations for the runners:

| Virtual Machine | Processor (CPU) | Memory (RAM) | Storage (SSD) | Workflow Label                 |
|:----------------|:----------------|:-------------|:--------------|:-------------------------------|
| `ubuntu`        | 4               | 16 GB        | 14 GB         | `ubuntu-latest` `ubuntu-20.04` |
| `macos`         | 3 (M1)          | 14 GB        | 14 GB         | `macos-latest`                 |

### Limitations on standard runners

No current limitations.

### Optimizations

The following optimizations have been implemented for the build process:

- Use of a Cache to store dependencies
- Use of parallel jobs to run multiple jobs concurrently
- Reusable workflows to avoid duplication of code and to maintain consistency - TBD

## Build Device Client on Local and via Github Actions

&nbsp;&nbsp;&nbsp;&nbsp;[Onboard Device Client Build Guidelines](./device-client-build_guidelines.md)

## Build IOS and Android Mobile SDK and App on Local and via Github Actions

&nbsp;&nbsp;&nbsp;&nbsp;[Mobile Application Build Guidelines](./mobile-app-build_guidelines.md)
