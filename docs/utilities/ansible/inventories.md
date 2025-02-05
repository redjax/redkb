---
tags:
  - ansible
  - automation
---

# Inventories

Inventories instruct Ansible on how to interact with your infrastructure, describing things like the path to a Python interpreter on the remote host, the SSH user Ansible should connect as and which SSH key to use, variables for your playbooks and roles, as well as custom/arbitrary variable declaration for things like software versions (if a play/role installs a specific version of a piece of software), secrets/tokens, & more.

Variables are declared in a directory alongside the inventory file, `group_vars/all.yml`. You can add other `.yml` files for variables, and Ansible will "join" them all when running plays.

!!! note

    There are [multiple ways to create your inventory](https://docs.ansible.com/ansible/latest/inventory_guide/intro_inventory.html). Ansible supports inventory files described in [`ini`](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/ini_inventory.html) and [`yaml`](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/yaml_inventory.html).

    I have used both, but more recently prefer `yaml` for describing my inventory. This guide assumes you will also use `yaml` inventories, but if you choose to use `ini` instead, you can translate the configurations by referencing the Ansible documentation.

## Example inventories

### Example: simple inventory

```yaml title="Simple Ansible inventory" linenums="1"
---
## A group for all machines in this inventory.
#  You can call these hosts in groups within this inventory after declaring here
all:
  ## Describe your hosts
  host1:
    ## Set the host IP/FQDN Ansible will use to connect
    ansible_host: "192.168.1.xxx"
  host2:
    ansible_host: "192.168.1.xxx"
    ## Override the remote machine's user Ansible will run as
    ansible_user: "username"
  host3:
    ansible_host: "192.168.1.xxx"
    ## Override the example_var_int value for just this host
    example_var_int: 42

  ## Vars that apply to all hosts.
  #  Can be overridden at the host definition or group level
  vars:
    ## Set variables Ansible will pass to plays/roles when this inventory is used
    #  Call in a playbook/role with {{ example_var }} or {{ example_var_int }}
    example_var: "I'm an example string"
    example_var_int: 100
  
## Group hosts declared in 'all' for controlling execution
#  with ansible-playbook -i inventory.yml --limit <group-name>
debian:
  ## You can just use the hostname from 'all'. Any vars declared at this level
  #  will override values set in 'all' definition
  host1:
  host3:
    example_var: "My value is now this string, and example_var_int will be 42 because it was overridden in the 'all' group"

## If you use a service like DigitalOcean, you can create a group for those hosts
digitalOcean:
  host2:
    ## You can add variables you haven't declared yet
    example_bool: true

```