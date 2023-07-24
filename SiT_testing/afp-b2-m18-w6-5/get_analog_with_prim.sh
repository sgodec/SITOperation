#!/bin/bash

echo "This is a script."

read -p "Enter starting number: " start
read -p "Enter ending number: " end

remote_user=root
remote_host=194.12.137.235
remote_path="/root/calibData/"

local_path="/home/simonsdell/Desktop/CERN/SiT_testing/afp-b2-m18-w6-5/"

# Loop through the range of numbers and copy directories one by one
for ((num=start; num<=end; num++))
do
    remote_dir="${remote_path}*00${num}"
    local_dir="${local_path}"
    
    # Copy the directory from remote to local using scp with recursive option
    scp -r "${remote_user}@${remote_host}:${remote_dir}" "${local_dir}"
done

