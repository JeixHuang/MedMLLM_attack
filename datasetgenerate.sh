#!/bin/bash

# Make sure we're using the correct Python interpreter
# Adjust `python3` to `python` or another Python version if necessary

# Run 1.py
python3 imgpair.py
if [ $? -ne 0 ]; then
    echo "Error running 1.py"
    exit 1
fi

# Run 2.py
python3 randommatch.py
if [ $? -ne 0 ]; then
    echo "Error running 2.py"
    exit 1
fi

# Run 3.py
python3 count.py
if [ $? -ne 0 ]; then
    echo "Error running 3.py"
    exit 1
fi

echo "All scripts executed successfully"
