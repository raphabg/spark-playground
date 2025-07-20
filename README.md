# Spark Standalone Cluster with PySpark Apps

This repository sets up an **Apache Spark standalone cluster** using Docker and Docker Compose, and provides a framework to **submit PySpark applications** to the cluster.

---

## Repository Structure

```
.
├── docker/
│   ├── resources/         # Spark configuration and additional resources
│   ├── dockerfile         # Docker image definition for Spark nodes
│   ├── docker-compose.yml # Compose file to orchestrate Spark Master, Workers, and History Server
│   ├── build.sh           # Script to build the custom Spark Docker image
│   ├── restart.sh         # Helper script to restart the Spark cluster
│   └── stop.sh            # Helper script to stop the Spark cluster
├── python/
│   ├── requirements.txt   # Python dependencies for PySpark applications
│   ├── Scenarios/         # Directory for PySpark applications (e.g., hello_world.py)
│   └── utils/             # Utility modules (e.g., Spark session creation)
```

### Directory Purpose
- **docker/**  
  Contains everything related to building and orchestrating the Spark cluster.  
  - `dockerfile` defines the Spark image.
  - `docker-compose.yml` defines the multi-container cluster (Master, Workers, History Server).
  - Scripts like `build.sh`, `restart.sh`, and `stop.sh` are provided for cluster lifecycle management.
  - `resources/` holds Spark configuration files (e.g., `spark-history-defaults.conf`).

- **python/**  
  Contains PySpark application code and utilities.  
  - `Scenarios/` includes PySpark jobs to be submitted to the Spark cluster.
  - `utils/` contains helper modules (e.g., creating a `SparkSession`).
  - `requirements.txt` specifies Python dependencies for your PySpark environment.

---

## Application Workflow

1. **Build Spark Cluster**  
   The `dockerfile` builds a Spark image with the required version and settings.
   
2. **Run Spark Cluster**  
   The `docker-compose.yml` starts a Spark standalone cluster:
   - `spark-master` – Master node for the cluster.
   - `spark-worker-1` and `spark-worker-2` – Worker nodes.
   - `spark-history` – History server to track jobs.

3. **Submit PySpark Applications**  
   Once the cluster is running, you can submit PySpark jobs (e.g., `hello_world.py`) to the `spark-master`.

---

## Step-by-Step Setup

### **1. Build Docker Image**
Run the following from the `docker/` directory:
```bash
./build.sh
```
This will create the custom Spark Docker image (e.g., `balogo-spark-4.0.0:latest`).

---

### **2. Start the Spark Cluster**
From the `docker/` directory, run:
```bash
./start.sh
```
This will launch:
- Spark Master at `localhost:8080`
- Spark Worker UIs at `localhost:8081`, `localhost:8082`
- Spark History Server at `localhost:18080`

---

### **3. Install Python Dependencies**
In your local Python environment (or a virtual environment), install dependencies:
```bash
cd python
pip install -r requirements.txt
```

---

### **4. Submit a PySpark Job**
Once the cluster is running, you can run any PySpark job by leveraging the `spark` variable from the `utils/spark_session.py` module.  

For example:
```python
from utils.spark_session import spark

# Your PySpark code here
df = spark.range(10)
df.show()
`````
---

### **5. Cluster Management**
- **Restart the cluster:**
  ```bash
  ./restart.sh
  ```
- **Stop the cluster:**
  ```bash
  ./stop.sh
  ```

---

## Useful URLs
- **Spark Master UI:** [http://localhost:8080](http://localhost:8080)
- **Worker UI (Worker-1):** [http://localhost:8081](http://localhost:8081)
- **Worker UI (Worker-2):** [http://localhost:8082](http://localhost:8082)
- **History Server UI:** [http://localhost:18080](http://localhost:18080)

---

## Next Steps
- Add new PySpark scripts to `python/Scenarios/`.
- Use `utils/spark_session.py` for consistent Spark session creation.
- Configure Spark further by editing files in `docker/resources/`.

---
