from typing import Any
from django.db import models
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

# Create your models here.

class CategoryInfoModel(models.Model):

    
    catid=models.CharField(max_length=250)
    categoryname=models.CharField(max_length=250)
    handle=models.CharField(max_length=250)
    categoryhomeimage=models.ImageField(upload_to='images/',null=True, blank=True)
    categorysectionimage=models.ImageField(upload_to='images/',null=True, blank=True)
    def __str__(self):
        return self.categoryname



class DeviceModel(models.Model):
    # Define a field that will hold dynamic choices
    category = models.CharField(max_length=100, choices=[])
    categoryid = models.CharField(max_length=100, null=True, editable=False)
    handle = models.CharField(max_length=100, null=True, editable=False)
    categoryname = models.CharField(max_length=100, null=True, editable=False)

    def update_dynamic_choices(self):
        
        transport = AIOHTTPTransport(url='https://@tamimi-projects.myshopify.com/api/2024-01/graphql', headers={'X-Shopify-Storefront-Access-Token': '14f4edb606d4404e7f14efdc1f979640'})
    
        client = Client(transport=transport)

        query = gql(
        """
        query Collections @inContext(language: EN){
            collections(first: 200) {
                totalCount
                nodes {
                    handle
                    id
                    onlineStoreUrl
                    title
                }
            }
        }
        """
        )
    

        # Execute the query on the transport
        result = client.execute(query)


        # Extract choices from API response
        # if result['collections'] != []:
        #     choices_data = result['collections']['nodes'] # Assuming API returns JSON data
        #     print(choices_data)
        #     # Format choices for Django choice field
        #     choices = [(choice['id'], choice['title']) for choice in choices_data]
        #     # Update choices of the field
        #     self._meta.get_field('category').choices = choices


    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.update_dynamic_choices()

    def __str__(self):
        return self.categoryname