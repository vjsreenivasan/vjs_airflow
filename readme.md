# Installation Guide For Mac

## Docker - Prod

1. Clone repo.

```bash
git clone https://github.com/syl3/airflow.git
```

2. Create .env file
```bash
vim .env
```
```
AIRFLOW_IMAGE_NAME=airflow-spark-local
AIRFLOW_UID=50000

DBT_PATH=<path_to>/dbt
DBT_PROFILE_PATH=<path_to>/.dbt
```

3. Build Docker Image.
```bash
docker build -t airflow-spark-local .
```

4. Start the Docker Compose service.
```bash
docker compose up -d
```

5. Go into container
```bash
docker exec -it airflow-airflow-webserver-1 bash
```

6. Import connection info.
```bash
airflow connections import connections.json 
```

7. Import variables.
```bash
airflow variables import variables.json
```

8. Update dags.
```bash
airflow dags reserialize
```


## Local - Dev
1. Create virtual environment.
```bash
conda create --name <myenv> python=3.9
```
2. Activate virtual environment.
```bash
conda activate <myenv>
```
3. Download Java11 to /spark/resources.
```bash
wget https://github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.19%2B7/OpenJDK11U-jdk_x64_mac_hotspot_11.0.19_7.tar.gz
```
4. Unzip the file.
```bash
tar xzfv OpenJDK11U-jdk_x64_mac_hotspot_11.0.19_7.tar.gz
```
5. Download Spark to /spark/resources.
```bash
wget https://archive.apache.org/dist/spark/spark-3.3.2/spark-3.3.2-bin-hadoop3.tgz
```
6. Unzip the file.
```bash
tar xzfv spark-3.3.2-bin-hadoop3.tgz
```
### Add environment variables.
7. cd to environment directory
```bash
cd $CONDA_PREFIX
```
8. Create folder.
```bash
mkdir -p ./etc/conda/activate.d
```
9. Create file.
```bash
vim ./etc/conda/activate.d/env_vars.sh
```

```bash
#!/bin/sh

export AIRFLOW_HOME=<path_to>/airflow

export JAVA_HOME=<path_to>/spark/resources/jdk-11.0.19+7/Contents/Home
export PATH=${JAVA_HOME}/bin:${PATH}

export SPARK_HOME=<path_to>/spark/resources/spark-3.3.2-bin-hadoop3
export PATH=${SPARK_HOME}/bin:${PATH}

export PYTHONPATH=${SPARK_HOME}/python/:${PYTHONPATH}
export PYTHONPATH=${SPARK_HOME}/python/lib/py4j-0.10.9.5-src.zip:${PYTHONPATH}

export PYSPARK_PYTHON=/usr/local/anaconda3/envs/<myenv>/bin/python
export PYSPARK_DRIVER_PYTHON=/usr/local/anaconda3/envs/<myenv>/bin/python
```
#### PYSPARK_PYTHON and PYSPARK_DRIVER_PYTHON can be checked by the following python code.
```python
import os
import sys

print(f'PYSPARK_PYTHON={sys.executable}')
print(f'PYSPARK_DRIVER_PYTHON={sys.executable}')
```

10. Import connections to airflow.db
```bash
airflow connections import connections.json
```