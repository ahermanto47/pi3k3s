# pi3k3s

On the master host(where you will be invoking ansible commands)

1. Create SSH key pair:

```
ssh-keygen -t ed25519 -C "ansible"
```

2. Install ansible.posix collection:

```
ansible-galaxy collection install ansible.posix
```

3. Install sshpass:

```
sudo dnf install sshpass
```

4. Run the distribute-ssh-key.yml playbook:

```
ansible-playbook -k -K distribute-ssh-key.yml
```

5. Test ssh to one of the machine in inventory, it should no longer asking for password and log you straight in

```
ssh <user>@<host>  
```