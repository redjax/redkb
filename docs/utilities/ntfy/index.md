---
tags:
  - http
  - utilities
  - bash
  - powershell
  - python
---
# Ntfy <!-- omit in toc -->

[Ntfy](https://ntfy.sh) is a PUB/SUB for sending/receiving push notifications. It uses simple HTTP requests, making it highly flexible and portable, and [can be self-hosted easily with Docker](https://docs.ntfy.sh/install/#docker).

## TODO

- [ ] Break this file up into smaller sections
- [ ] Add example Bash scripts for controlling Dockerized ntfy instance

## Table of Contents <!-- omit in toc -->

- [TODO](#todo)
- [Quick How-To](#quick-how-to)
- [Basic notification](#basic-notification)
- [Title, priority, and tags](#title-priority-and-tags)
- [Style messages with emoji \& tags](#style-messages-with-emoji--tags)
- [Style messages with Markdown](#style-messages-with-markdown)
- [Attachments](#attachments)
- [Action buttons](#action-buttons)
- [Priorities](#priorities)
- [Scheduled Messages](#scheduled-messages)
- [Send as GET requests with webhooks](#send-as-get-requests-with-webhooks)
- [Publish as JSON](#publish-as-json)
- [Links](#links)

## Quick How-To

Ntfy works off of HTTP requests. This makes it highly flexible, allowing you to [choose which HTTP client](https://docs.ntfy.sh/publish/) you use. Throughout this page, code examples have a header with tabs indicating a language to show the example in, i.e. `Command line (curl)`, `ntfy CLI`, `HTTP`, etc.

This section assumes you are using Bash + cURL. It should be easy to translate the examples if you're using another tool or library. In cURL, `-d` is the "data" to send (i.e. the message), `-H` is a header, and `-u` is for [API token auth](https://docs.ntfy.sh/publish/#access-tokens).

An Ntfy request needs, at minimum, the data/message to send and a URL to your topic, i.e. `ntfy.sh/topicName`. If you are [self-hosting ntfy](https://docs.ntfy.sh/install/), replace any `ntfy.sh` domain in this section with your domain, i.e. `ntfy.example.com`.

This page as [a full list of supported parameters you can pass in a request](https://docs.ntfy.sh/publish/#list-of-all-parameters).

## Basic notification

This is a very simply request that sends a message "Hello, world!" to the `greetings` topic on Ntfy's official PUBSUB instance.

```bash
curl -d "Hello, world!" ntfy.sh/greetings
```

## Title, priority, and tags

To set the title, priority, and tags properties, pass them as headers to cURL with `-H "<key>: <value>"`. You can optionally pass them as `X-<Key>`.

[Priorities](https://docs.ntfy.sh/publish/#message-priority) range from 1 to 5, with 1 being the lowest and 5 being the highest priority.

```bash
curl \
  -H "X-Title: This is a notification title" \
  -H "X-Priority: urgent" \
  -H "X-Tags: warning,skull" \
  -d "This is an urgent alert!" \
  ntfy.sh/urgent-alerts
```

You can do multi-line messages, too.

```bash
curl \
  -H "X-Title: Multiple lines?" \
  -d "This message will have multiple lines.

Just add newlines without closing the quote,

splitting the content over multiple lines."
  ntfy.sh/multiple-lines
```

## Style messages with emoji & tags

*See the [ntfy tags & emojis docs](https://docs.ntfy.sh/publish/#tags-emojis)*

You can pass an `X-Tags` parameter to add tags to a notification.

```bash
curl -H "X-Tags: warning,somehostname,job-name" \
  -d "Job name failed on host: somehostname" \
  ntfy.sh/backups
```

You can also pass them with `-H ta:tagname` (no quotes).

## Style messages with Markdown

*[ntfy docs: Markdown formatting](https://docs.ntfy.sh/publish/#markdown-formatting)*

````bash
curl \
  -H "X-Markdown: yes" \
  -d "This message is *styled*! **Big and bold**.

> Let he who is without blame throw the first stone.

![meaning image tag name](url-to-file)

```python
print(f"This is a code block in a message!")
```

[This is a link to Ntfy](https://ntfy.sh)

Things to do:

- Make some requests of your own!
  - Learn Ntfy syntax
  - Pick a tool
    - cURL
    - Powershell Invoke-WebRequest
    - Python httpx/requests
  - Create some notifications!

---

That's all, folks."

  ntfy.sh/markdown-message
````

## Attachments

*[Ntfy attachments documentation](https://docs.ntfy.sh/publish/#attachments)*

## Action buttons

*[Ntfy action buttons documentation](https://docs.ntfy.sh/publish/#action-buttons)*

## Priorities

| Priority | ID  | Name           | Description                                                                                            |
| -------- | --- | -------------- | ------------------------------------------------------------------------------------------------------ |
| Max      | 5   | `max`/`urgent` | Really long vibration bursts, default notification sound with a pop-over notification.                 |
| High     | 4   | `high`         | Long vibration burst, default notification sound with a pop-over notification.                         |
| Default  | 3   | `default`      | Short default vibration and sound. Default notification behavior.                                      |
| Low      | 2   | `low`          | No vibration or sound. Notification will not visibly show up until notification drawer is pulled down. |
| Min      | 1   | `min`          | No vibration or sound. The notification will be under the fold in "Other notifications".               |

Examples:

```bash
curl -H "X-Priority: 5" -d "An urgent message" ntfy.sh/alerts
curl -H "Priority: low" -d "Low priority message" ntfy.sh/alerts
curl -H p:4 -d "A high priority message" ntfy.sh/alerts
```

## Scheduled Messages

*[Ntfy scheduled message docs](https://docs.ntfy.sh/publish/#scheduled-delivery)*

If [message caching](https://docs.ntfy.sh/publish/#message-caching) is enabled on the server, you can pass a header with syntax describing when the message should be sent. Header options are `X-Delay`, `X-At`, `X-In`.

Examples:

```bash
curl -H "At: tomorrow, 10am" -d "Good morning" ntfy.sh/hello
curl -H "In: 30min" -d "It's 30 minutes later now" ntfy.sh/reminder
curl -H "Delay: 1639194738" -d "Unix timestamps are awesome" ntfy.sh/itsaunixsystem
```

## Send as GET requests with webhooks

*[Ntfy webhooks docs](https://docs.ntfy.sh/publish/#webhooks-publish-via-get)*

## Publish as JSON

*[Ntfy JSON publishing docs](https://docs.ntfy.sh/publish/#publish-as-json)*

In some instances, you may not have control over the headers of a request, such as with [Jellyfin](https://jellyfin.org/). You can also pass your full notification as JSON. The example below uses most of thee available parameters. The only required parameter is `topic`.

```bash
curl ntfy.sh \
  -d '{
    "topic": "alerts",
    "message": "Disk space is low at 5.1 GB",
    "title": "Low disk space alert",
    "tags": ["warning","cd"],
    "priority": 4,
    "attach": "https://filesrv.lan/space.jpg",
    "filename": "diskspace.jpg",
    "click": "https://homecamera.lan/xasds1h2xsSsa/",
    "actions": [{ "action": "view", "label": "Admin panel", "url": "https://filesrv.lan/admin" }]
  }'
```

## Links

- [ntfy home](https://ntfy.sh)
- [ntfy Github](https://github.com/binwiederhier/ntfy)
- [ntfy docs](https://docs.ntfy.sh)
  - [ntfy docs: publishing (sending messages)](https://docs.ntfy.sh/publish/)
  - [ntfy docs: emoji shortcodes](https://docs.ntfy.sh/emojis/)
  - [ntfy docs: list of all parameters](https://docs.ntfy.sh/publish/#list-of-all-parameters)
