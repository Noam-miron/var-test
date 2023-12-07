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
