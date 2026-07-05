---
title: "Github CI/CD"
date: 2026-07-04T03:06:32-04:00
draft: false
weight: 10
toc: true
keywords: []
tags:
  - github
  - ci-cd
  - devops
---

Github's CI/CD platform is broken into 2 units: [Github Actions](https://docs.github.com/en/actions) and [reusable workflows](https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows).

Describing workflows and actions makes them sound like the same thing (or very similar), and to an extent they are. I will let Github's documentation explain this in-depth, but the short version is that a reusable workflow is a set of "jobs" to automate code actions like linting, building, releasing, etc, and they can be chained together. An action (or "reusable component") is like a CI/CD component package that a workflow can call to handle a very specific step, like [cloning a repository](https://github.com/actions/checkout) or [installing Node.js](https://github.com/actions/setup-node) (or other languages).

Official Actions are stored in the [Github Actions repository](https://github.com/actions), but anyone can create an action in their own repository. The Github Actions platform is strict about where actions and workflows must live; you cannot call an action or workflow from a path outside of `.github/`. This means that whether your reusable actions or workflows are stored in the repo that calls them, or a centralized repository with all of your pipeline components, they must exist under a specific path:

- `.github/workflows/` for reusable workflows
- `.github/actions/` for reusable components

There are some other differences between actions and workflows. Actions do not use a `jobs:` section, meaning you can't create a multi-stage actions (you would have to use a workflow for that). Additionally, actions cannot inherit or use secrets, where workflows can. This design is intentional; the idea is that a workflow is made up of a series of action calls, while each action handles 1 very specific task/process. A reddit user named `/u/queen-adreena` summed it up perfectly: ["An action is a song. A workflows is a playlist"](https://www.reddit.com/r/github/comments/17sbywi/what_is_a_github_workflow_and_how_does_it_differ/).

Github provides a [repository of reusable workflows](https://github.com/actions/reusable-workflows) that help with the development of action components.
