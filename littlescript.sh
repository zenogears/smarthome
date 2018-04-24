#!/bin/bash
for i in $(seq 5000); do ./tosqlite.py ; sleep 3600; done
