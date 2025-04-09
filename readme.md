# Beans Model Inference API

## Updating 
docker build -t your-local-image-name .
docker tag your-local-image-name gcr.io/computer-vision-research-lab/bmia
docker push gcr.io/computer-vision-research-lab/bmia

gcloud run deploy --image gcr.io/computer-vision-research-lab/bmia --region europe-west1 --platform managed --allow-unauthenticated --memory 512Mi --cpu 1 --project computer-vision-research-lab