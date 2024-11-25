+----------+     +-----------+     +-----------+     +---------+  
| Kubernetes |-----| K8s Nodes |-----| CXL Memory |-----| Memory  |  
|            |     |           |     | Controller|     | Layers  |  
| (Master)   |     | (Workers) |     |           |     |---------+  
|            |     |           |     |           |     | DRAM    |  
|            |     |           |     |           |-----| PMEM    |  
|            |     |           |     |           |     | SSD     |  
+----------+     +-----------+     +-----------+     +---------+  
  
                                  ^  
                                  |  
                       Kubernetes CMI (Container Memory Interface)