# Google Cloud Platform

## Auth

We support two methods of authenticating your GCP account:

### 1. OAuth2

This is the simplest method. After creating the integration and passing through the OAuth2 authentication flow you will be asked to select an appropriate GCP project. All resources we create will be created under the selected project.


### 2. Creating service account for GKE

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

## GKE

Wodby provides native integration with Google Kubernetes Engine. 

- We use deployment manager to create and manage all resources we create
- We currently do not support serverless clusters
- All resources we create have `wodby-gke-` prefix
- GKE cluster can be either highly available (multi-AZ) or not (single zone)
- Since GKE cluster comes with a metrics server we use it for the basic Wodby kubernetes monitoring
- Node disk size can be configured upon creation

### Storage

Persistent storage is provided by GCP Compute Engine Persistent Disks via the default storage class. We create a new block storage volume for each persistent volume claim.

### Supported regions

We support the following OVH regions:
- BHS
- DE
- GRA
- SBG5
- SGP
- SYD
- UK
- WAW

## Cloud SQL

Wodby provides native integration with Google Cloud SQL.

- We support MySQL and PostgreSQL
- All resources we create have `wodby-sql-` prefix
- Databases can be resided with a GKE cluster created under the same integration
- We create database with SSD disks
- Auto resize can be optionally enabled (with the limit of twice the size)
- Database server can either be highly available (regional) or not (zonal)
- We use backend type `SECOND_GEN`
- You can manage your DBs and users form Wodby dashboard

## Cloud Storage

Integration with GCP Cloud Storage is coming soon...
