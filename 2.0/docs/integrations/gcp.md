# Google Cloud Platform

We support two methods of authenticating your GCP account:

## 1. OAuth2 authentication

This is the simplest method, after authenticating your google account we will create a Service Account in a GCP project of your choice 

## 2. Creating service account for GKE

1. Select a project in GCP where you want to create your cluster. We recommend creating a separate project for Wodby resources to keep track on your cloud costs
2. Go to _IAM & Admin_, select _Service Accounts_ on the left menu
3. Click _CREATE SERVICE ACCOUNT_ 
4. On step 1 enter a unique name (we recommend using prefix `wodby` for identification)
5. On step 2 add following roles:
    - Kubernetes Engine Admin (`roles/container.admin`)
    - Compute Viewer (`roles/compute.admin`)
    - Service Account User (`roles/iam.serviceAccountUser`)
    - Viewer (`roles/viewer`)
6. On step 3 click _Done_
7. Click on the newly created service account
8. Add a new key with `JSON` type
9. Download JSON key and upload it on the new GCP integration form
