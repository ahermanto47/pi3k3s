Sequence of ops:

1. Apply the metallb external load balancer:
```
kubectl apply -f metallb-native.yaml
```

2. Apply the range ips for metallb:
```
kubectl apply -f metallb-layer2.yaml
```

3. Apply the persistent volume claim:
```
kubectl apply -f mosquitto-pvc.yaml
```

4. Apply the mosquitto mqtt broker:
```
kubectl apply -f mosquitto-pv.yaml
```

5. Finally apply the service for mosquitto pods:
```
kubectl apply -f mosquitto-lb.yaml
```