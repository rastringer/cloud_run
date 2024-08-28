### Deploying Hugging Face models on Cloud Run

```
gcloud config set project PROJECT_ID
```

```
gcloud config set run/region us-central1
```

Create an artifact registry repo

```
gcloud artifacts repositories create REPOSITORY \
  --repository-format=docker \
  --location=us-central1
```

Build container

```
gcloud builds submit \
   --tag us-central1-docker.pkg.dev/PROJECT_ID/REPOSITORY/bert-legal \
   --machine-type e2-highcpu-32
```

Deploy as Cloud Run service

```
gcloud beta run deploy bert-legal \
  --image us-central1-docker.pkg.dev/PROJECT_ID/REPOSITORY/bert-legal \
  --cpu 4 \
  --set-env-vars OLLAMA_NUM_PARALLEL=4 \
  --gpu 1 \
  --gpu-type nvidia-l4 \
  --max-instances 7 \
  --memory 32Gi \
  --allow-unauthenticated \
```