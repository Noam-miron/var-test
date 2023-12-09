# README
This project is an API for simple restaurant querying
it is built to deploy with Terraform to Azure and consists of a static site for testing, an API function and a CosmoDB.

It requires you create a terraform backend in azure

the Github actions pipeline requires Azure credentials that allow resource creation at the subscription level

The API recieves a query and returns a json in the following format:

{
restaurantRecommendation :
    {
    name: ‘Pizza hut’,
    style: ‘Italian’,
    address: ‘wherever street 99, somewhere’,
    openHour: 09:00,
    closeHour: 23:00,
    vegetarian : yes,
    isOpen: yes
    }
}

# Setup:
In order to create this project in your azure account you will need to set up a storage account in azure for tf state
and fill the storage account details in backend declaration site, function and db main.tf files

You will need an Azure Service Account with permissions to deploy resources at the subscription level.
If you already have one, you can save AZURE_CLIENT_ID, AZURE_SUBSCRIPTION_ID, AZURE_TENANT_ID as Github actions repo secrets.
Otherwise you can create one with azure_oidc.sh script, fill github organization(user)/repo/branch and Azure subscition and run the script, save the created AZURE_CLIENT_ID, AZURE_SUBSCRIPTION_ID, AZURE_TENANT_ID as Github actions repo secrets.

# Future Iterations
    1. Integrate function code deployment into workflow.
    2. Integrate automatic DB seeding into workflow.
    3. set up the query in DB (and parameterize it).
    4. Add code testing(both terraform and python tests).
    5. Add a branching strategy and branch protection.
