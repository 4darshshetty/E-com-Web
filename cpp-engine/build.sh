#!/bin/bash
echo "Building discount.so for Linux/Mac..."
g++ -shared -o discount.so discount.cpp -fPIC
if [ $? -eq 0 ]; then
    echo "Build successful! discount.so created."
else
    echo "Build failed! Make sure g++ is installed."
    exit 1
fi

