---
title: "Tips & Tricks"
date: 2026-11-11T15:41:06-05:00
draft: false
weight: 10
toc: true
keywords: []
tags:
  - ci-cd
  - devops
---

## Retrieve Variable Marked Secret

> [!WARNING]
> This method of printing variables works around security features in Azure Pipelines, and should only be used in an emergency. When adding variables to a [Library variable group](https://learn.microsoft.com/en-us/azure/devops/pipelines/library/variable-groups) in Azure DevOps, if you mark a value as secret, it will hide the value so no user can read it, and decrypt it only when used in a pipeline. At no point after marking a variable as secret are you able to see the value again.
>
> If you need to retrieve that secret for some reason, you can use one of the pipelines below to print the secret character-by-character in the pipeline. When each character of a secret is printed to the pipeline this way, Azure Pipelines does not detect it as a secret and will show the full value. You can copy/paste the lines into a text editor and delete each newline to "re-join" the secret into its original value.
>
> You should always [delete the pipeline run](https://learn.microsoft.com/en-us/azure/devops/pipelines/policies/retention?view=azure-devops&tabs=yaml#delete-a-run) as soon as possible after retrieving the secret; leaving the pipeline run in history exposes the secret value to anyone who can access the pipeline. It is usually advisable to delete the entire pipeline so other users can't run it.

You can use a pipeline like the one below to print values marked as secret in an Azure DevOps variable group:

```yaml
---
trigger: none
pr: none

parameters:
  - name: variableGroups
    displayName: Variable groups to read
    type: stringList
    default:
      - varGroupName1
      - varGroupName2
    values:
      - varGroupName1
      - varGroupName2
  - name: secretVariableName
    displayName: Name of the secret variable to dump
    type: string
    default: ''

jobs:
  - ${{ each group in parameters.variableGroups }}:
      - job: Dump_${{ replace(replace(replace(replace(replace(group, '-', '_'), ' ', '_'), '.', '_'), '(', ''), ')', '') }}
        displayName: Dump ${{ parameters.secretVariableName }} from ${{ group }}
        variables:
          - group: ${{ group }}
        steps:
          - bash: |
              set -euo pipefail

              secret='$(${{ parameters.secretVariableName }})'

              echo "Variable group: ${{ group }}"

              if [[ -z "$secret" ]]; then
                echo "$({{ parameters.secretVariableName }}) is empty or not set"
                exit 1
              fi

              for ((i = 0; i < ${#secret}; i++)); do
                printf "%s " "${secret:i:1}"
              done

              printf "\n"
            displayName: Output ${{ parameters.secretVariableName }} char-by-char

```

To print multiple values at a time across groups, use this pipeline:

```yaml
---
trigger: none
pr: none

parameters:
  - name: variableGroups
    displayName: Variable groups to read
    type: stringList
    default:
      - varGroupName1
      - varGroupName2
    values:
      - varGroupName1
      - varGroupName2
  - name: variablesToPrint
    displayName: Variable names to print (comma or semicolon separated, e.g. azureClientSecret,apiKey,connectionString)
    type: string
    default: 'azureClientSecret'

jobs:
  - ${{ each group in parameters.variableGroups }}:
      - ${{ each varName in split(replace(parameters.variablesToPrint, ';', ','), ',') }}:
          - job: Dump_${{ replace(replace(replace(group, '-', '_'), ' ', '_'), '.', '_') }}_${{ replace(replace(trim(varName), ' ', '_'), '.', '_') }}
            displayName: Dump ${{ trim(varName) }} from ${{ group }}
            variables:
              - group: ${{ group }}
            steps:
              - bash: |
                  set -euo pipefail

                  var_name='${{ trim(varName) }}'
                  secret="${TARGET_SECRET-}"

                  echo "Variable group: ${{ group }}"
                  echo "Variable name: ${var_name}"

                  unresolved_ref="\$(${var_name})"
                  if [[ "$secret" == "$unresolved_ref" ]]; then
                    echo "${var_name} is not defined in variable group '${{ group }}' (or this pipeline cannot access it)"
                    exit 1
                  fi

                  if [[ -z "$secret" ]]; then
                    echo "${var_name} is empty"
                    exit 1
                  fi

                  for ((i = 0; i < ${#secret}; i++)); do
                    printf "%s " "${secret:i:1}"
                  done

                  printf "\n"
                displayName: Output ${{ trim(varName) }} from ${{ group }}
                env:
                  TARGET_SECRET: $(${{ trim(varName) }})
```
