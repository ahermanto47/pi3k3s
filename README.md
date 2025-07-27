# pi3k3s

On the master host(where you will be invoking ansible commands, in this case its an instance of Centos Stream 10)

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

6. Run k3s prerequisite playbook

```
ansible-playbook -K k3s-prerequisites.yml
```

7. Run k3s install playbook

```
ansible-playbook -K k3s-install.yml
```

8. Install kubectl

```
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
```

```
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl.sha256"
```

```
echo "$(cat kubectl.sha256)  kubectl" | sha256sum --check
```

```
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
```

9. Replace ~/.kube/config with contents from the master k3s yaml (/etc/rancher/k3s/k3s.yaml)

10. Test your new k3s cluster with
    a. kubectl cluster-info
    b. kubectl get nodes