#!/bin/bash
for u in 10 100 500; do
  for i in 1 2 3; do
    echo "Running load test with $u users and $i instances"
    locust -f locustfile.py --headless -u $u -r 10 --run-time 120s --host=http://172.28.224.1:80 --csv=./teste_carga/output_u_${u}_i_${i}
  done
done