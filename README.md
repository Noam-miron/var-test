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
    vegetarian : yes
    }
}

# TORUN
# create terraform backend in azure, fill details in tf main files(site,function,db)
# fill github org/repo/branch, azure subscription in azure_oidc.sh and run it to create service account
# save service account details as repo secrets for github workflow
# AZURE_CLIENT_ID
# AZURE_SUBSCRIPTION_ID
# AZURE_TENANT_ID

# AZURE_FUNCTION_APP_PUBLISH_PROFILE (additional github secret)

# TODO
# modulate terraform files, create one resource group in a seperate module with ramdom name generator
# create one consolidated root module that defines a single backend and not three seperate(maybe not to keep modularity?)
# add code testing and/or formatting before deployment
# set up branching and protection in repo
# add certificate for function
# parameterize query, create stored procedure?
# app publish profile usage from within workflow instead of external secret