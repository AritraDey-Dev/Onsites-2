Make a daemon to monitor for long running unused docker containers. 
Check if a container and all the related (same network except bridge) containers are running more than a specified threshold, then stop all those containers. 
If only some are old, then keep it all as it is. Whenever any container is stopped, log it's details.
The threshold refers to a specific time period the containers are running for.
without external libraries
