---
title: "Survey Long"
date: 2026-09-27T13:29:55-04:00
draft: false
weight: 10
toc: true
keywords: []
tags:
  - programming
  - software-development
  - coding
  - git
  - version-control
---

This guide is a checklist of commands you can run to get an understanding of a Git repository. It is useful when you are new to contributing, or when you are inheriting maintenance of an existing repository.

The guide assumes you are using Linux or macOS. If you are on Windows, you should use WSL or Git Bash to run the commands.

## Requirements

> [!NOTE]
> Install only the tools relevant to the analyses you plan to run.

- Required base tools:
  - `bash`
  - `coreutils`
  - `findutils`
  - `grep`
  - `sed`
  - `awk`
  - `sort`
  - `tree`
  - `jq`
  - `git`
- Any repository:
  - [`tokei`](https://github.com/XAMPPRocky/tokei) or [`scc`](https://github.com/boyter/scc)
  - [`git-fame`](https://pypi.org/project/git-fame/)
  - [`git-sizer`](https://github.com/github/git-sizer)
  - [`git-filter-repo`](https://github.com/newren/git-filter-repo)
  - [`gitleaks`](https://github.com/gitleaks/gitleaks) or [`trufflehog`](https://github.com/trufflesecurity/trufflehog)
  - [`trivy`](https://github.com/aquasecurity/trivy)
  - [`osv-scanner`](https://github.com/google/osv-scanner)
  - [`semgrep`](https://github.com/semgrep/semgrep)
  - [`jscpd`](https://github.com/kucherenko/jscpd)
  - `ncdu`
  - [`syft`](https://github.com/anchore/syft)
  - [`grype`](https://github.com/anchore/grype)
  - [`hadolint`](https://github.com/hadolint/hadolint)
  - [`checkov`](https://github.com/bridgecrewio/checkov)
- Bash repositories:
  - [`shellcheck`](https://github.com/koalaman/shellcheck)
  - [`shfmt`](https://github.com/patrickvane/shfmt)
- Python repositories:
  - [`vulture`](https://github.com/jendrikseipp/vulture)
  - [`radon`](https://github.com/rubik/radon)
  - [`xenon`](https://github.com/rubik/xenon)
  - [`bandit`](https://github.com/PyCQA/bandit)
  - [`deptry`](https://github.com/osprey-oss/deptry)
- Go repositories:
  - [`go`](https://go.dev/)
  - [`golangci-lint`](https://golangci-lint.run/)
  - [`govulncheck`](https://github.com/golang/vuln)
  - [`gocyclo`](https://github.com/fzipp/gocyclo)
  - [`staticcheck`](https://staticcheck.dev/)
- Java repositories:
  - `java`
  - [`maven`](https://maven.apache.org/) and/or [`gradle`](https://gradle.org/)
  - [`spotbugs`](https://spotbugs.github.io/)
  - [`pmd`](https://pmd.github.io/)
  - [`checkstyle`](https://checkstyle.org/)
  - [`OWASP dependency-check`](https://github.com/dependency-check/DependencyCheck)
- JavaScript/TypeScript repositories:
  - `node`
  - `npm`, `pnpm`, and/or `yarn`
  - `eslint`
  - `typescript`
  - [`knip`](https://github.com/webpro-nl/knip)
  - [`dependency-cruiser`](https://github.com/sverweij/dependency-cruiser)

## Objectives

Use this runbook to establish:

- What is this repository?
  - Languages
  - code volume
  - file makeup
  - maintainers
  - commit history
  - package/deployment configuration
  - repository structure
  - large assets
- What is the health of this repository?
  - Worktree size
  - Git-history size
  - oversized blobs
  - tracked generated artifacts
  - dead code
  - duplicate code
  - complexity
  - maintainability
  - dependency hygiene
- What is risky?
  - Secrets
  - dependency vulnerabilities
  - insecure configuration
  - dangerous code patterns
  - supply-chain exposure

> [!NOTE]
> The common survey does not build, test, deploy, or rewrite the surveyed repository. Some language-specific commands may download dependencies or create build output in the target checkout. Run those commands against a disposable copy if the target repository must remain untouched.
>
> Some language-specific commands leave artifacts in the target repository, and are therefore not "read-only."

## Setup

- Create a staging directory, separate from any Git repositories, where you will run analysis and output result files to.
  - For example, `mkdir -p "$HOME/git_surveys"`.
  - You can call it whatever you want, i.e. `$HOME/git/surveys/`, `$HOME/code_analysis`, `$HOME/repository_reviews`, etc.
  - This guide will reference the path you create as `$SURVEY_ROOT`.

  ```shell
  SURVEY_ROOT="$HOME/git_surveys"
  mkdir -p "$SURVEY_ROOT"
  ```

- Each time you survey a repository, do the following:

  ```shell
  REPO="/absolute/path/to/target/repository"
  REPO_NAME="$(basename "$REPO")"
  STAMP="$(date +%Y%m%d-%H%M%S)"
  OUT="$SURVEY_ROOT/${REPO_NAME}-${STAMP}"

  ## Create survey output dirs
  mkdir -p "${OUT}"/{metadata,git,security,maintainability,language-specific,notes}
  ```

- Ensure the target is a git repository:

  ```shell
  test -d "$REPO" || {
    printf 'Repository path does not exist: %s\n' "$REPO" >&2
    exit 1
  }

  git -C "$REPO" rev-parse --is-inside-work-tree

  {
    printf 'Repository path: %s\n' "$REPO"
    printf 'Survey path: %s\n' "$OUT"
    printf 'Survey time: %s\n' "$(date -Is)"
    printf '\nGit HEAD:\n'
    git -C "$REPO" rev-parse HEAD
    printf '\nCurrent branch:\n'
    git -C "$REPO" branch --show-current
    printf '\nShallow clone:\n'
    git -C "$REPO" rev-parse --is-shallow-repository
    printf '\nGit remotes:\n'
    git -C "$REPO" remote -v
    printf '\nGit status:\n'
    git -C "$REPO" status --short --branch
  } > "$OUT/metadata/survey-context.txt"
  ```

Run all subsequent commands from the staging directory: `cd "$OUT"`

## All Repositories

These checks can be run against any repository, regardless of language(s) used in that repository.

### Get Repository Structure

  ```shell
  tree -L 3 -a \
    -I '.git|node_modules|.pnpm-store|.yarn|.next|.nuxt|dist|build|coverage|.venv|venv|__pycache__|.pytest_cache' \
    "$REPO" \
    > metadata/tree-depth-3.txt
  ```

### Find Project, Package, Container, Infrastructure, CI/CD, and Scanner Config Files

```shell
{
  find "$REPO" \
    -path "$REPO/.git" -prune -o \
    -path "$REPO/node_modules" -prune -o \
    -type f \
    \( \
      -iname 'readme*' -o \
      -name 'package.json' -o \
      -name 'pnpm-lock.yaml' -o \
      -name 'package-lock.json' -o \
      -name 'yarn.lock' -o \
      -name 'pyproject.toml' -o \
      -name 'requirements*.txt' -o \
      -name 'Pipfile' -o \
      -name 'Pipfile.lock' -o \
      -name 'poetry.lock' -o \
      -name 'go.mod' -o \
      -name 'go.sum' -o \
      -name 'Cargo.toml' -o \
      -name 'pom.xml' -o \
      -name 'build.gradle' -o \
      -name 'build.gradle.kts' -o \
      -name 'settings.gradle' -o \
      -name 'settings.gradle.kts' -o \
      -name 'Dockerfile' -o \
      -name 'Dockerfile.*' -o \
      -name 'docker-compose*.yml' -o \
      -name 'docker-compose*.yaml' -o \
      -name 'azure-pipelines*.yml' -o \
      -name 'azure-pipelines*.yaml' -o \
      -name 'renovate.json' -o \
      -name '*.tf' -o \
      -name '*.tfvars' -o \
      -name 'Chart.yaml' -o \
      -name 'values.yaml' \
    \) \
    -print

  find "$REPO" \
    -path "$REPO/.git" -prune -o \
    -path "$REPO/node_modules" -prune -o \
    -type d \
    \( \
      -name '.github' -o \
      -name '.gitlab' -o \
      -name '.devcontainer' \
    \) \
    -print
} | sort -u > metadata/important-files.txt
```

### Inventory Files by Extension

  ```shell
  find "$REPO" \
    -path "$REPO/.git" -prune -o \
    -path "$REPO/node_modules" -prune -o \
    -type f \
    -printf '%f\n' \
    | sed -n 's/.*\.\([[:alnum:]]\+\)$/.\1/p' \
    | tr '[:upper:]' '[:lower:]' \
    | sort \
    | uniq -c \
    | sort -nr \
    > metadata/file-extension-counts.txt
  ```

### Analyze Language(s) Used and Code Volume

- With `tokei`:

  ```shell
  tokei \
    --exclude "$REPO/.git" \
    --exclude "$REPO/node_modules" \
    --exclude "$REPO/.pnpm-store" \
    --exclude "$REPO/.yarn" \
    --exclude "$REPO/.next" \
    --exclude "$REPO/.nuxt" \
    --exclude "$REPO/dist" \
    --exclude "$REPO/build" \
    --exclude "$REPO/.venv" \
    --exclude "$REPO/venv" \
    "$REPO" \
    > metadata/tokei.txt
  ```

  ```shell
  tokei \
    --exclude "$REPO/.git" \
    --exclude "$REPO/node_modules" \
    --exclude "$REPO/.pnpm-store" \
    --exclude "$REPO/.yarn" \
    --exclude "$REPO/.next" \
    --exclude "$REPO/.nuxt" \
    --exclude "$REPO/dist" \
    --exclude "$REPO/build" \
    --exclude "$REPO/.venv" \
    --exclude "$REPO/venv" \
    --output json \
    "$REPO" \
    > metadata/tokei.json
  ```

- With `scc`:

  ```shell
  scc \
  --exclude-dir .git \
  --exclude-dir node_modules \
  --exclude-dir .pnpm-store \
  --exclude-dir .yarn \
  --exclude-dir .next \
  --exclude-dir .nuxt \
  --exclude-dir dist \
  --exclude-dir build \
  --exclude-dir coverage \
  --exclude-dir .venv \
  --exclude-dir venv \
  "$REPO" \
  > metadata/scc.txt
  ```

  ```shell
  scc \
    --exclude-dir .git \
    --exclude-dir node_modules \
    --exclude-dir .pnpm-store \
    --exclude-dir .yarn \
    --exclude-dir .next \
    --exclude-dir .nuxt \
    --exclude-dir dist \
    --exclude-dir build \
    --exclude-dir coverage \
    --exclude-dir .venv \
    --exclude-dir venv \
    --format json \
    "$REPO" \
    > metadata/scc.json
  ```

### Analyze Repository Size and File Makeup

```shell
du -x -h --max-depth=2 "$REPO" 2>/dev/null \
  | sort -h \
  > metadata/directory-sizes.txt
```

```shell
find "$REPO" \
  -path "$REPO/.git" -prune -o \
  -type f \
  -printf '%s\t%p\n' \
  | sort -nr \
  | head -200 \
  > metadata/largest-current-files.txt
```

- Or use `ncdu` for interactive inspection:

  ```shell
  ncdu -o metadata/ncdu-export.json "$REPO"
  ```

### Git History & Maintainer Analysis

```shell
git -C "$REPO" log --all --decorate --oneline -200 \
  > git/recent-history.txt
```

```shell
git -C "$REPO" log --all --format='%aI' \
  | cut -dT -f1 \
  | sort \
  | uniq -c \
  > git/commit-activity-by-day.txt
```

```shell
git -C "$REPO" shortlog --summary --numbered --all \
  > git/contributors-by-commits.txt
```

```shell
git -C "$REPO" log --all \
  --format='%aN <%aE>' \
  | sort \
  | uniq -c \
  | sort -nr \
  > git/contributor-identities.txt
```

> [!WARNING]
> These commands use the Python `git-fame` package by casperdcl. Other tools named `git-fame` may use different command-line options.

```shell
git fame \
  --sort commits \
  "$REPO" \
  > git/git-fame-by-commits.txt 2>&1 || true
```

```shell
git fame \
  --sort loc \
  "$REPO" \
  > git/git-fame-by-current-lines.txt 2>&1 || true
```

```shell
git fame \
  --bytype \
  "$REPO" \
  > git/git-fame-by-file-type.txt 2>&1 || true
```

### Git Object Database & Historical Bloat

```shell
git -C "$REPO" count-objects -vH \
  > git/object-database.txt
```

```shell
git -C "$REPO" rev-list --objects --all \
  | git -C "$REPO" cat-file \
      --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' \
  | awk '$1 == "blob" { print $3 "\t" $2 "\t" $4 }' \
  | sort -nr \
  | head -200 \
  > git/largest-history-blobs.txt
```

```shell
(
  cd "$REPO"
  git-sizer --verbose
) > "$OUT/git/git-sizer.txt" 2>&1 || true
```

```shell
mkdir -p git/filter-repo-analysis

git -C "$REPO" filter-repo \
  --analyze \
  --report-dir "$OUT/git/filter-repo-analysis" \
  > git/filter-repo.txt 2>&1 || true
```

### Candidate Tracked Artifacts Analysis

```shell
git -C "$REPO" ls-files \
  'node_modules/**' \
  '.next/**' \
  '.nuxt/**' \
  'dist/**' \
  'build/**' \
  'coverage/**' \
  '.venv/**' \
  'venv/**' \
  '__pycache__/**' \
  '*.sqlite' \
  '*.db' \
  '*.zip' \
  '*.tar.gz' \
  '*.gz' \
  '*.pdf' \
  '*.csv' \
  '*.xlsx' \
  '*.mp4' \
  '*.mov' \
  '*.onnx' \
  '*.pt' \
  '*.pkl' \
  > git/tracked-artifact-candidates.txt
```

### Duplicate Code

Use `jscpd` to identify duplicated code across the repository. Review generated files and vendored code before treating duplication counts as meaningful.

```shell
mkdir -p maintainability/jscpd

jscpd "$REPO" \
  --reporters console,json,html \
  --output "$OUT/maintainability/jscpd" \
  --ignore '**/.git/**,**/node_modules/**,**/.pnpm-store/**,**/.yarn/**,**/.next/**,**/.nuxt/**,**/dist/**,**/build/**,**/.venv/**,**/venv/**,**/coverage/**' \
  > maintainability/jscpd.txt 2>&1 || true
```

### Gitleaks Secret Detection

```shell
gitleaks git \
--source "$REPO" \
--report-format json \
--report-path "$OUT/security/gitleaks-history.json" \
--redact 80 \
--exit-code 0 \
--no-banner \
> security/gitleaks-history.txt 2>&1 || true
```

### Trufflehog Secret Detection

```shell
trufflehog git "file://$REPO" \
  --json \
  --no-update \
  --results=verified \
  > security/trufflehog-verified.json 2>&1 || true
```

### Trivy

```shell
trivy fs \
--scanners vuln,secret,misconfig,license \
--severity UNKNOWN,LOW,MEDIUM,HIGH,CRITICAL \
--no-progress \
--exit-code 0 \
"$REPO" \
> security/trivy.txt 2>&1 || true
```

```shell
trivy fs \
--scanners vuln,secret,misconfig,license \
--severity UNKNOWN,LOW,MEDIUM,HIGH,CRITICAL \
--no-progress \
--exit-code 0 \
--format json \
--output "$OUT/security/trivy.json" \
"$REPO" \
> security/trivy-json-generation.txt 2>&1 || true
```

### OSV-Scanner

```shell
osv-scanner scan source \
  --recursive \
  --format json \
  --output "$OUT/security/osv-scanner.json" \
  "$REPO" \
  > security/osv-scanner.txt 2>&1 || true
```

### Syft

Generate a software bill of materials (SBOM) from the repository's current filesystem. This inventories what Syft can identify in the checkout; it is not necessarily identical to the contents of a built application or container image.

```shell
syft "dir:$REPO" \
  -o "cyclonedx-json=$OUT/security/syft-sbom.cdx.json" \
  > security/syft.txt 2>&1 || true
```

If you also want to scan that SBOM with Grype, generate Syft's native JSON format:

```shell
syft "dir:$REPO" \
  -o "syft-json=$OUT/security/syft-sbom.syft.json" \
  > security/syft-native.txt 2>&1 || true
```

### Grype

Scan the [Syft SBOM](#syft) for known vulnerabilities:

```shell
grype "sbom:$OUT/security/syft-sbom.syft.json" \
  -o json \
  > security/grype.json 2> security/grype.log || true
```

> [!NOTE]
> Run this after generating `security/syft-sbom.syft.json`. Its findings may overlap with Trivy and OSV-Scanner; compare results rather than treating each scanner's count as a separate problem.

### Semgrep

```shell
semgrep scan \
  --config p/default \
  --json \
  --json-output "$OUT/security/semgrep.json" \
  "$REPO" \
  > security/semgrep.txt 2>&1 || true
```

```shell
semgrep scan \
  --config p/default \
  --sarif \
  --output "$OUT/security/semgrep.sarif" \
  "$REPO" \
  > security/semgrep-sarif-generation.txt 2>&1 || true
```

### Hadolint

Run when the repository contains Dockerfiles. This checks Dockerfile instructions without building images or changing the repository. Hadolint accepts multiple Dockerfile paths and supports JSON output.

```shell
find "$REPO" \
  -path "$REPO/.git" -prune -o \
  -path "$REPO/node_modules" -prune -o \
  -type f \
  \( -name 'Dockerfile' -o -name 'Dockerfile.*' -o -name '*.Dockerfile' \) \
  -print0 \
  | xargs -0 -r hadolint --format json \
  > security/hadolint.json 2> security/hadolint.log || true
```

### Checkov

Run when the repository contains infrastructure or deployment definitions. Checkov can analyze supported IaC and configuration files without running a deployment.

```shell
checkov \
  --directory "$REPO" \
  --output json \
  > security/checkov.json 2> security/checkov.log || true
```

> [!NOTE]
> Checkov's results may overlap with Trivy misconfiguration findings.

## Language-Specific Repositories

### Bash Repositories

Use this section when the repository contains .sh files, Bash scripts, deployment scripts, CI shell steps, or executable shell tooling.

#### Locate Shell Files

```shell
find "$REPO" \
  -path "$REPO/.git" -prune -o \
  -type f \
  \( -name '*.sh' -o -name '*.bash' \) \
  -print \
  | sort \
  > language-specific/bash-files.txt
```

```shell
find "$REPO" \
  -path "$REPO/.git" -prune -o \
  -type f \
  -perm -u+x \
  -exec sh -c '
    for file do
      if head -n 1 "$file" | grep -Eq "^#!.*\b(bash|sh)\b"; then
        printf "%s\n" "$file"
      fi
    done
  ' sh {} + \
  | sort \
  > language-specific/bash-executables.txt
```

#### Bash Script Quality

##### ShellCheck

```shell
{
  cat language-specific/bash-files.txt
  cat language-specific/bash-executables.txt
} | sort -u | while IFS= read -r file; do
  shellcheck "$file"
done > language-specific/shellcheck.txt 2>&1 || true
```

##### ShellFormat

```shell
find "$REPO" \
  -path "$REPO/.git" -prune -o \
  -type f \
  \( -name '*.sh' -o -name '*.bash' \) \
  -print0 \
  | xargs -0 -r shfmt --diff \
  > language-specific/shfmt.txt 2>&1 || true
```

### Python Repositories

Use this section when the repository contains Python source, `pyproject.toml`, `requirements*.txt`, Poetry/Pipenv metadata, or Python packages.

#### Locate Python Sources and Dependency Metadata

```shell
find "$REPO" \
  -path "$REPO/.git" -prune -o \
  -path "$REPO/.venv" -prune -o \
  -path "$REPO/venv" -prune -o \
  -type f -name '*.py' \
  | sort \
  > language-specific/python-files.txt
```

```shell
find "$REPO" \
  -path "$REPO/.git" -prune -o \
  -type f \
  \( \
    -name 'pyproject.toml' -o \
    -name 'requirements*.txt' -o \
    -name 'Pipfile' -o \
    -name 'Pipfile.lock' -o \
    -name 'poetry.lock' -o \
    -name 'pdm.lock' -o \
    -name 'uv.lock' \
  \) \
  -print \
  | sort \
  > language-specific/python-dependency-files.txt
```

#### Find Dead Python Code Candidates

```shell
vulture "$REPO" \
  --exclude "$REPO/.git,$REPO/node_modules,$REPO/.venv,$REPO/venv" \
  --min-confidence 80 \
  > language-specific/vulture.txt 2>&1 || true
```

#### Python Project Complexity and Maintainability

```shell
radon cc "$REPO" \
  --exclude "$REPO/.git,$REPO/node_modules,$REPO/.venv,$REPO/venv" \
  --show-complexity \
  --average \
  > language-specific/radon-cyclomatic-complexity.txt 2>&1 || true
```

```shell
radon mi "$REPO" \
  --exclude "$REPO/.git,$REPO/node_modules,$REPO/.venv,$REPO/venv" \
  --show \
  --multi \
  > language-specific/radon-maintainability-index.txt 2>&1 || true
```

```shell
xenon \
  --max-absolute B \
  --max-modules B \
  --max-average A \
  "$REPO" \
  > language-specific/xenon.txt 2>&1 || true
```

#### Python Static Analysis

```shell
bandit \
  --recursive "$REPO" \
  --exclude "$REPO/.git,$REPO/node_modules,$REPO/.venv,$REPO/venv" \
  --format txt \
  > language-specific/bandit.txt 2>&1 || true
```

```shell
bandit \
  --recursive "$REPO" \
  --exclude "$REPO/.git,$REPO/node_modules,$REPO/.venv,$REPO/venv" \
  --format json \
  --output "$OUT/language-specific/bandit.json" \
  > language-specific/bandit-json-generation.txt 2>&1 || true
```

#### Python Dependency Hygiene

> [!NOTE]
> Run these commands from the target repository's root, or wherever a `requirements.txt` file is found.

```shell
PYTHON_ROOT="/absolute/path/to/python-project"

(
  cd "$PYTHON_ROOT"
  deptry . --requirements-files requirements.txt
) > "$OUT/language-specific/deptry-$(basename "$PYTHON_ROOT").txt" 2>&1 || true
```

### Go Repositories

Use this section when the repository contains `go.mod`.

#### Locate Go Modules

```shell
find "$REPO" \
  -path "$REPO/.git" -prune -o \
  -type f -name 'go.mod' \
  -printf '%h\n' \
  | sort -u \
  > language-specific/go-module-roots.txt
```

#### Go Static Analysis

```shell
GO_ROOT="/absolute/path/to/go-module"

(
  cd "$GO_ROOT"
  go vet ./...
) > "$OUT/language-specific/go-vet-$(basename "$GO_ROOT").txt" 2>&1 || true
```

```shell
GO_ROOT="/absolute/path/to/go-module"

(
  cd "$GO_ROOT"
  staticcheck ./...
) > "$OUT/language-specific/staticcheck-$(basename "$GO_ROOT").txt" 2>&1 || true
```

```shell
GO_ROOT="/absolute/path/to/go-module"

(
  cd "$GO_ROOT"
  golangci-lint run ./...
) > "$OUT/language-specific/golangci-lint-$(basename "$GO_ROOT").txt" 2>&1 || true
```

#### Go Vulnerabilities Check

```shell
GO_ROOT="/absolute/path/to/go-module"

(
  cd "$GO_ROOT"
  govulncheck ./...
) > "$OUT/language-specific/govulncheck-$(basename "$GO_ROOT").txt" 2>&1 || true
```

#### Go Code Complexity & Maintainability

```shell
find "$GO_ROOT" \
  -path "$GO_ROOT/vendor" -prune -o \
  -type f -name '*.go' \
  -print0 \
  | xargs -0 -r gocyclo -over 15 \
  > "$OUT/language-specific/gocyclo-$(basename "$GO_ROOT").txt" 2>&1 || true
```

### Java Repositories

Use this section when the repository contains Maven or Gradle metadata.

#### Locate Java Projects

```shell
find "$REPO" \
  -path "$REPO/.git" -prune -o \
  -type f \
  \( -name 'pom.xml' -o -name 'build.gradle' -o -name 'build.gradle.kts' \) \
  -printf '%h\n' \
  | sort -u \
  > language-specific/java-project-roots.txt
```

#### Java Checkstyle

Use a Checkstyle all-in-one JAR installed outside the target repository. Set `CHECKSTYLE_JAR` to its absolute path, then point the scan at the Java source directory you want to review.

```shell
CHECKSTYLE_JAR="/absolute/path/to/checkstyle-all.jar"
JAVA_SOURCE="/absolute/path/to/java-project/src/main/java"

java -jar "$CHECKSTYLE_JAR" \
  -c /google_checks.xml \
  -f xml \
  -o "$OUT/language-specific/checkstyle.xml" \
  "$JAVA_SOURCE" \
  > language-specific/checkstyle.txt 2>&1 || true
```

If the project already has a Checkstyle configuration, use its XML file instead of `/google_checks.xml`. Run separately for additional source roots when needed.

#### Maven Analysis

```shell
JAVA_ROOT="/absolute/path/to/maven-project"

(
  cd "$JAVA_ROOT"
  mvn -B dependency:tree
) > "$OUT/language-specific/maven-dependency-tree-$(basename "$JAVA_ROOT").txt" 2>&1 || true
```

```shell
JAVA_ROOT="/absolute/path/to/maven-project"

(
  cd "$JAVA_ROOT"
  mvn -B spotbugs:spotbugs
) > "$OUT/language-specific/spotbugs-$(basename "$JAVA_ROOT").txt" 2>&1 || true
```

```shell
JAVA_ROOT="/absolute/path/to/maven-project"

(
  cd "$JAVA_ROOT"
  mvn -B pmd:check
) > "$OUT/language-specific/pmd-$(basename "$JAVA_ROOT").txt" 2>&1 || true
```

#### Gradle Analysis

```shell
JAVA_ROOT="/absolute/path/to/gradle-project"

(
  cd "$JAVA_ROOT"
  ./gradlew dependencies
) > "$OUT/language-specific/gradle-dependencies-$(basename "$JAVA_ROOT").txt" 2>&1 || true
```

```shell
JAVA_ROOT="/absolute/path/to/gradle-project"

(
  cd "$JAVA_ROOT"
  ./gradlew spotbugsMain
) > "$OUT/language-specific/spotbugs-$(basename "$JAVA_ROOT").txt" 2>&1 || true
```

```shell
JAVA_ROOT="/absolute/path/to/gradle-project"

(
  cd "$JAVA_ROOT"
  ./gradlew pmdMain
) > "$OUT/language-specific/pmd-$(basename "$JAVA_ROOT").txt" 2>&1 || true
```

#### Java OWASP DependencyCheck

- [ ] TODO: `OWASP DependencyCheck` scan.

### JavaScript and TypeScript Repositories

Use this section when the repository contains `package.json`, `pnpm-lock.yaml`, `package-lock.json`, `yarn.lock`, `.js`, `.jsx`, `.ts`, or `.tsx` files.

#### Locate Node Projects

```shell
find "$REPO" \
  -path "$REPO/.git" -prune -o \
  -path "$REPO/node_modules" -prune -o \
  -type f -name 'package.json' \
  -printf '%h\n' \
  | sort -u \
  > language-specific/node-project-roots.txt
```

#### Unused Node Dependencies, Exports, and Files

> [!NOTE]
> Run subsequent commands from each directory with a `package.json` file.

```shell
NODE_ROOT="/absolute/path/to/node-project"

(
  cd "$NODE_ROOT"
  knip
) > "$OUT/language-specific/knip-$(basename "$NODE_ROOT").txt" 2>&1 || true
```

#### Lint Node Code

```shell
NODE_ROOT="/absolute/path/to/node-project"

(
  cd "$NODE_ROOT"
  eslint .
) > "$OUT/language-specific/eslint-$(basename "$NODE_ROOT").txt" 2>&1 || true
```

#### TypeScript Type Checking

```shell
TYPESCRIPT_ROOT="/absolute/path/to/typescript-project"

(
  cd "$TYPESCRIPT_ROOT"
  tsc --noEmit
) > "$OUT/language-specific/typescript-$(basename "$TYPESCRIPT_ROOT").txt" 2>&1 || true
```

#### Check Dependencies for Advisories

```shell
NODE_ROOT="/absolute/path/to/node-project"

(
  cd "$NODE_ROOT"
  npm audit --json
) > "$OUT/language-specific/npm-audit-$(basename "$NODE_ROOT").json" 2>&1 || true
```

```shell
NODE_ROOT="/absolute/path/to/node-project"

(
  cd "$NODE_ROOT"
  pnpm audit --json
) > "$OUT/language-specific/pnpm-audit-$(basename "$NODE_ROOT").json" 2>&1 || true
```

```shell
NODE_ROOT="/absolute/path/to/node-project"

(
  cd "$NODE_ROOT"
  yarn audit --json
) > "$OUT/language-specific/yarn-audit-$(basename "$NODE_ROOT").json" 2>&1 || true
```

#### Check Project's Import Graph

```shell
NODE_ROOT="/absolute/path/to/node-project"

(
  cd "$NODE_ROOT"
  dependency-cruiser src --output-type err
) > "$OUT/language-specific/dependency-cruiser-$(basename "$NODE_ROOT").txt" 2>&1 || true
```
