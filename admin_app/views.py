from django.shortcuts import render
from django.http import HttpResponse
from . models import CategoryInfoModel
import shopify
import requests
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
import ast
from .serializer import DataSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response


# Create your views here.
@api_view(['GET'])
def getData(request):
    app = CategoryInfoModel.objects.all()
    serializer = DataSerializer(app, many=True)
    return Response(serializer.data)

def home_page(request):
    
    # url = "https://@tamimi-projects.myshopify.com/api/2024-01/graphql.json"
  
    # body = """ 
    # query Query { 
    # allFilms { 
    #     films { 
    #     title 
    #     } 
    # } 
    # } 
    # """

    # response = requests.post(url=url, json={"query": body}) 
    # print("response status code: ", response.status_code) 
    # if response.status_code == 200: 
	#     print("response : ", response.content) 

    

    

    # allitem=CategoryInfo.objects.all()
    # url = 'https://myshop.myshopify.com/admin/api/2021-04/products.json'
    # headers = {
    #     'X-Shopify-Storefront-Access-Token':'14f4edb606d4404e7f14efdc1f979640',
    #     'Content-Type':'application/json'
    # },
    # r = requests.get(url, headers=headers)
    # result = r.json()
    # print(result)

    # url = 'https://api.github.com/graphql'
    # json = { 'query' : '{ products(first: 200, query: "cards") { edges { cursor node { handle id title }}}}' }
    # headers = {
    #     'X-Shopify-Storefront-Access-Token':'14f4edb606d4404e7f14efdc1f979640',
    #     'Content-Type':'application/json'
    # },

    # r = requests.post(url=url, json=json, headers=headers)
    # print(r.text)
    # return Response(status=200, data={"data": result})

    

    catvalues=CategoryInfoModel.objects.all()
    
    return render(request,'home.html',{'catvalues':catvalues})


# def category_page(request,id):

#     current=CategoryInfo.objects.get(id=id)
#     frm=CategoryInfo(instance=current) 
#     return render(request,'category.html',{'frm':frm})

def create_page(request):

    

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
    
    if request.POST:
        
        
        selected = request.POST.get('selected_option')
        selected_dict=ast.literal_eval(selected)
        print(selected)
        catid = selected_dict.get('id')
        categoryname = selected_dict.get('title')
        handle = selected_dict.get('handle')
        imagehome = request.FILES.get('image-home')
        imagesection = request.FILES.get('image-section')
        cat=CategoryInfoModel(catid=catid,categoryname=categoryname,handle=handle,categoryhomeimage=imagehome,categorysectionimage=imagesection)
        cat.save()
        catvalues=CategoryInfoModel.objects.all()
    
        return render(request,'home.html',{'catvalues':catvalues})
        
    
    return render(request,'create.html',result)

