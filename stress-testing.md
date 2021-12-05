For testing, I generated a list of 2,000 URLs corresponding to our own API endpoint for 2,000 sequential patent numbers. 

```
for i in $(seq 10000000 10002000); do
    echo http://myserver/api/continuations/$i >> urls.txt;
done

time httpx -l urls.txt
```

In observing the connections via the k3s port-forwarding, I saw the following every so often:
    error copying from local connection to remote stream, read: connecion reset by peer


In attempting to run over 20,000 URLs, I found that flask and the vm itself lagged out and needed to be restarted. 50 threads per second might be too much to handle on this configuration. 
