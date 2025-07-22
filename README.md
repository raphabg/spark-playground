# Spark Standalone Cluster with PySpark Apps

This repository sets up an **Apache Spark standalone cluster** using Docker and Docker Compose, and provides a framework to **submit PySpark applications** (drivers) to the cluster.

---

## Repository Structure

```
.
├── docker/
│   ├── resources/         # Spark configuration files and additional resources
│   ├── dockerfile         # Docker image definition for Spark nodes
│   ├── docker-compose.yml # Orchestrates Spark Master, Workers, and History Server
│   ├── build.sh           # Builds the custom Spark Docker image
│   ├── start.sh           # Starts the Spark cluster
│   ├── restart.sh         # Restarts the Spark cluster
│   └── stop.sh            # Stops the Spark cluster
├── python/
│   ├── requirements.txt   # Python dependencies for PySpark applications
│   ├── Scenarios/         # PySpark application scripts (e.g., hello_world.py)
│   └── utils/             # Utility modules (e.g., Spark session creation)
```

---

## Directory Purpose

### **docker/**
- Contains everything related to building and orchestrating the Spark cluster:
  - `dockerfile` – Defines the Spark image.
  - `docker-compose.yml` – Defines the multi-container cluster (Master, Workers, History Server).
  - `resources/` – Spark configuration files (e.g., `spark-defaults.conf`, `log4j2.properties`).
  - Scripts: `build.sh`, `start.sh`, `restart.sh`, `stop.sh` for lifecycle management.

### **python/**
- Contains PySpark application code and helper utilities:
  - `Scenarios/` – PySpark jobs to be submitted to the cluster.
  - `utils/` – Modules for reusable components (e.g., `SparkSession` factory).
  - `requirements.txt` – Python dependencies for running driver scripts.

---

## Application Workflow

### **1. Cluster Setup**
1. **Build Spark Image**  
   Use `docker/build.sh` to build the custom Spark image.

2. **Start Spark Cluster**  
   Use `docker/start.sh` to launch:
   - **Spark Master** (`localhost:8080`)
   - **Spark Workers** (`localhost:8081`, `localhost:8082`)
   - **History Server** (`localhost:18080`)

---

### **2. Driver Setup**
Drivers can run on your **host machine** or inside a **container**.

#### **Host Machine Driver**
1. **Set Environment Variables**  
   Configure paths for Spark:
   ```bash
   export SPARK_CONF_DIR=/path/to/conf
   export SPARK_DRIVER_LOGS_DIR=/path/to/logs
   ```
   These are used by both `spark-defaults.conf` and `log4j`.

2. **Install Python Dependencies**  
   ```bash
   cd python
   pip install -r requirements.txt
   ```

3. **Submit a PySpark Job**  
   Use the pre-configured Spark session in `utils/spark_session.py`:
   ```python
   from utils.spark_session import spark

   df = spark.range(10)
   df.show()
   ```

#### **Container Driver (To Do)**
- Add instructions for running drivers from a container (future enhancement).

---

### **3. Cluster Management**
- **Restart the cluster:**  
  ```bash
  ./docker/restart.sh
  ```
- **Stop the cluster:**  
  ```bash
  ./docker/stop.sh
  ```

---

## Cluster Setup Instructions

### **Build Docker Image**
```bash
cd docker
./build.sh
```

### **Start Spark Cluster**
```bash
./start.sh
```

This starts:
- Spark Master UI at [http://localhost:8080](http://localhost:8080)
- Spark Worker UIs at [http://localhost:8081](http://localhost:8081) and [http://localhost:8082](http://localhost:8082)
- Spark History Server at [http://localhost:18080](http://localhost:18080)

---

## Useful URLs
- **Spark Master UI:** [http://localhost:8080](http://localhost:8080)
- **Worker UI (Worker-1):** [http://localhost:8081](http://localhost:8081)
- **Worker UI (Worker-2):** [http://localhost:8082](http://localhost:8082)
- **History Server UI:** [http://localhost:18080](http://localhost:18080)

---

## Next Steps
- Add new PySpark scripts under `python/Scenarios/`.
- Use `utils/spark_session.py` for consistent Spark session creation.
- Customize Spark settings in `docker/resources/` (e.g., `spark-defaults.conf`, `log4j2.properties`).
