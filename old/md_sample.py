      
 python ase_md.py --params l0_pseudo_false/params-c3f945fe-3bb8-4b00-aae0-6980105fabf5.json \
 --data data-full-R.npz \
     --thermostat nve --temperature 0.0 --steps 1000 \
     --traj-interval 1 --n-replicas 16 --output l0.test.npz --dt 0.1  --electric-field 0.0 0.0 0.0
      
 python ase_md.py --params l1_pseudo_false/params-84887c6e-ce35-4ac2-8176-fe12d7bd75c0.json \
 --data data-full-R.npz \
     --thermostat nve --temperature 0.0 --steps 10000 \
     --traj-interval 1 --n-replicas 16 --output l1.test.npz --dt 0.1 --electric-field 0.0 0.0 0.0
     
     
  python ase_md.py --params l2_pseudo_false/params-781e2d5e-13ac-4284-9c1b-8b419ad8e032.json \
 --data data-full-R.npz \
     --thermostat nve --temperature 0.0 --steps 1000 \
     --traj-interval 1 --n-replicas 16 --output l2.test.npz --dt 0.1 --electric-field 0.0 0.0 0.0
     
     
   python ase_md.py --params l3_pseudo_false/params-683eecc8-7070-4816-a702-2fb472354ab5.json    \
 --data data-full-R.npz \
     --thermostat nve --temperature 0.0 --steps 10000 \
     --traj-interval 1 --n-replicas 16 --output l3.test.npz --dt 0.1 --electric-field 0.0 0.0 0.0
     
  python ase_md.py --params l4_pseudo_false/params-46e02bbf-39ee-49c8-b1a4-b48e86e41014.json --data data-full-R.npz   --thermostat nve --temperature 0.0 --steps 10000 --traj-interval 1 --n-replicas 16 --output l4.test.npz --dt 0.1 --electric-field 0.0 0.0 0.0
     

