#!/bin/bash
set -e

if [ $# -eq 0 ]; then
    echo "Usage: $0 <ROS_DOMAIN_ID>"
    exit 1
fi

if [ $1 -lt 0 ]; then
    echo "ROS_DOMAIN_ID has to be a positive integer"
    exit 1
fi

if [ $1 -gt 101 ]; then
    echo "Maximum allowed value for ROS_DOMAIN_ID is 101"
    exit 1
fi

echo "export ROS_DOMAIN_ID=$1" >> ~/.bashrc
export ROS_DOMAIN_ID=$1
echo "Using ROS_DOMAIN_ID=$ROS_DOMAIN_ID"