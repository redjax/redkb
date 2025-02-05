---
tags:
  
  - ansible
  - automation
  - ssh
---

# SSH Setup

Ansible uses SSH to connect to remote machines and run tasks. It is advisable to create an SSH key just for executing Ansible playbooks, and an Ansible service account on the remote, i.e. `ansible_svc`. This user account is not meant to be logged into on the remote, but can be granted permissions so Ansible can run and do things like install software, update packages, etc.

Creating a service account for Ansible to use is easily automated. I always create an `onboard` inventory, which is where I declare machines temporarily to run any base/common setup steps, including creating my Ansible service user.

After running my onboarding playbook, I remote the host from the inventory file and add it to whatever other "permanent" inventories it will exist in. This step allows me to quickly set up a new host by passing an SSH password for when I have not already copied my Ansible SSH keys.

## Create SSH key

Create an SSH key just for Ansible execution. You will copy the public key to your remote manually, then Ansible will use this key to authenticate.

```shell title="Create Ansible SSH key"
ssh-keygen -t rsa -b 4096 -f ~/.ssh/ansible_id_rsa -N ""
```

This will create 2 keys, `~/.ssh/ansible_id_rsa` (the private key, do not copy this to the remote), and `~/.ssh/ansible_id_rsa.pub` (this is the key you copy to the remote).

In your `~/.ssh/config`, add your hosts by the same name you use in your Ansible inventory file. 

## Playbook: Create ansible_svc user

```yaml title="plays/create_ansible_svc_user.yml" linenums="1"
---
- name: "Setup service account for Ansible"
  hosts: all

  vars:
    service_account_name: "{{ ansible_svc_account_name | default('ansible_svc') }}"
    service_account_shell: "{{ ansible_svc_account_shell | default('/bin/bash') }}"
    local_

  tasks:
    - name: "Gather facts"
      ansible.builtin.package_facts:
        manager: auto

    
```
