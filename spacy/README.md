# Deploying NLP apps on Cloud Run

Cloud Run is a fully managed serverless platform on Google Cloud Platform (GCP) that lets you run containers without having to worry about managing servers or infrastructure. It's designed for modern, microservices-based applications that need to scale automatically and efficiently.

In this brief tutorial, we will make a simple web app that loads the spaCy library and performs entity recognition on submitted text files and URLs.

### Here is our file structure:

spacy/
    |--main.py
    |--Dockerfile
    |--requirements.txt
    |--README.md
    |--templates/
        |--index.html
        |--results.html

### The Cloud Run part

With the Google Cloud SDK installed, run 

```
gcloud init
```

then set your project with billing enabled:

```
gcloud config set project <your project id>
```

Enable the necessary IAM permissions either for your admin account or a service account (service account example here):

```
gcloud projects add-iam-policy-binding PROJECT_ID \
    --member=serviceAccount: PROJECT_ID-compute@developer.gserviceaccount.com \
    --role=roles/cloudbuild.builds.builder
```

Now the simple command:

```
gcloud run deploy
```

will build the container and deploy the service. 

The terminal will display a URL to access and test the app.

Head to the Cloud Run [console](https://console.cloud.google.com/run/) to look at customization and scale options.

