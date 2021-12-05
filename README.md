




Tested on a e2-standard-2 (2 vCPU, 8 GB memory) Google Cloud VM instance
Debian Linux 10 buster
10 GB disk 
Allow HTTP
Allow HTTPS


1. Launch vm
2. sudo apt install -y git tmux
3. tmux
4. git clone https://github.com/jede4830/project
5. cd project
6. sudo ./doitall.sh 
    - port-forwarding at the end will likely fail if the pods are not done being created

To check pod status from root folder:

7. sudo ./monitor.sh 
    - you can do this to check the status of the pods

8. Once all the pods are up and running: sudo ./port-forwarding.sh 
9. If a pod fails to start or runs into an error (worker -or- rest): 
    - cd into the folder for that pod
    - sudo ./restart.sh 

10. To finally forward port 5000 out:
    - Add a firewall policy for port 5000 in Google Cloud 
    - sudo $(tail -n1 doitall.sh) 

