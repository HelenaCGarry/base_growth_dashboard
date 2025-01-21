#  Streamlit deployment tutorial
## How to deploy a streamlit app using Azure services

1. If you don't have one already, create Storage account to access the Azure Cloud Shell

2. clone your github private repo in the storage account
    - create a PAT on github at Setting > Developer Settings > Personal Access Tokens
    - in the Cloud Shell execute: `git clone https://<your account>:<your_pat>@github.com/<your account or organization>/<repo name>.git`

3. Create a Container Registry in the <resource group name> resource group (select the basic sku).
    - in Settings > Access keys,  enable Admin user

4. Build the docker image in the Container Registry:
    - if you are not already in your directory: `cd <repo name>`
    - `az acr build --registry <container registry name> --resource-group <resource group name> --image <image name of your choosing> . `

5. If you don't have one already, create an App Service Plane. Choose the basic plan (B1: 1).

6. Create your Web App choosing your App Service Plan and your image from the Azure Container registry. 

Your app should be available after a couple of minutes at the web address you created!

:exclamation: If you don't plan on modifying your app and it is heavy you can delete the Storage account once you are done. It is not required once the image is created and it can create extra costs.
