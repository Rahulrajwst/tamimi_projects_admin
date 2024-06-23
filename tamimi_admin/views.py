from django.shortcuts import render
from . models import CategoryModel,DeviceModel,SectionModel,ParentSectionModel
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
import ast
from .serializer import DeviceSerializer,SectionSerializer,ParentSectionSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response



# Create your views here.
@api_view(['GET'])
def getDeviceData(request):
    # devicelist = CategoryModel.objects.prefetch_related('base_category')
    
    devicelist = DeviceModel.objects.all()
    serializer = DeviceSerializer(devicelist, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getSectionData(request):
    sectionlist = SectionModel.objects.all()
    serializer = SectionSerializer(sectionlist, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getParentData(request):
    sectionlist = ParentSectionModel.objects.all()
    serializer = ParentSectionSerializer(sectionlist, many=True)
    return Response(serializer.data)

def home_view(request):
    if '_sync' in request.POST:
            print('sync')
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

            existdata=CategoryModel.objects.all()
            if existdata.count==0:
                for i in result['collections']['nodes']:
                    category=CategoryModel(catid=i['id'],categoryname=i['title'],handle=i['handle'])
                    category.save()
            else:

                for i in result['collections']['nodes']:                   

                    tmp_instance=CategoryModel.objects.get(catid=i['id'])
                    if tmp_instance is None:
                        category=CategoryModel(catid=i['id'],categoryname=i['title'],handle=i['handle'])
                        category.save()
                    else:
                        tmp_instance.catid=i['id']
                        tmp_instance.categoryname=i['title']
                        tmp_instance.handle=i['handle']
                        tmp_instance.save()

            updateddata=CategoryModel.objects.all()
            for modelitem in updateddata:
                exist=False
                for resultitem in result['collections']['nodes']:
                    if modelitem.catid==resultitem['id']:
                        exist=True
                        break
                if exist==False:
                    modelitem.delete()
                    
            
    
    return render(request,'home.html')

def all_devices_view(request):

    if request.POST:
        if '_create' in request.POST:
            print('create')
            catid = request.POST.get('selected_option') 
            print(catid)       
            formdata = CategoryModel.objects.get(catid=catid)
            image = request.FILES.get('image')
            device = DeviceModel(category=formdata,deviceimage=image)
            device.save()
        elif '_delete' in request.POST:
            id = request.POST.get('_delete')
            tmp_instance=DeviceModel.objects.get(pk=id)
            tmp_instance.delete()
            print('delete') 

    categorylist=CategoryModel.objects.all()
    devicelist=DeviceModel.objects.all()
    unselected_options=[]
    for i in categorylist:
        exist=False
        for j in devicelist:
            if i.catid==j.category.catid:
                exist=True
                print(i.categoryname)
                break
        if exist==False:
            unselected_options.append(i)
    devicelist_data=DeviceModel.objects.all()

    data={'devicelist_data':devicelist_data,'options':unselected_options}
    
    return render(request,'device_page.html',data)

def all_sections_view(request):

    if request.POST:
        if '_create' in request.POST:
            print('create')
            catid = request.POST.get('selected_option') 
            print(catid)       
            formdata = CategoryModel.objects.get(catid=catid)
            image = request.FILES.get('image')
            section = SectionModel(category=formdata,sectionimage=image)
            section.save()
        elif '_delete' in request.POST:
            id = request.POST.get('_delete')
            tmp_instance=SectionModel.objects.get(pk=id)
            tmp_instance.delete()
            print('delete') 

    categorylist=CategoryModel.objects.all()
    sectionlist=SectionModel.objects.all()
    unselected_options=[]
    
    for i in categorylist:
        exist=False
        for j in sectionlist:
            if i.catid==j.category.catid:
                exist=True
                print(i.categoryname)
                break
        if exist==False:
            unselected_options.append(i)
    sectionlist_data=SectionModel.objects.all()

    data={'devicelist_data':sectionlist_data,'options':unselected_options}
    
    return render(request,'section_page.html',data)

def all_parent_sections_view(request):

    if request.POST:
        if '_create' in request.POST:
            name = request.POST.get('_parent_section') 
            print(name)       
            image = request.FILES.get('image')
            section = ParentSectionModel(parentsectionname=name,parentsectionimage=image)
            section.save()
        elif '_delete' in request.POST:
            id = request.POST.get('_delete')
            tmp_instance=ParentSectionModel.objects.get(pk=id)
            tmp_instance.delete()
            print('delete') 

    
    parentsectionlist=ParentSectionModel.objects.all()

    data={'parentsectionlist':parentsectionlist}
    
    return render(request,'parent_section_page.html',data)


    
def child_section_view(request,pk):
    
    parent=ParentSectionModel.objects.get(pk=pk)
    if request.POST:
        if '_create' in request.POST:
            
            childid = request.POST.get('_selected_option') 
            child=SectionModel.objects.get(pk=childid)
            child.parentsection=parent
            child.save()
        elif '_delete' in request.POST:
            childid = request.POST.get('_delete') 
            child=SectionModel.objects.get(pk=childid)
            child.parentsection=None
            child.save()
    
    
    sectionlist=SectionModel.objects.all()
    unselected_options=[]
    selected_options=[]
    for i in sectionlist:
        if i.parentsection is None:
            unselected_options.append(i)
            print('none')
        else: 
            if i.parentsection==parent:
                selected_options.append(i)
        
    data={'parentname':parent.parentsectionname,'unselected_options':unselected_options,'selected_options':selected_options}

    return render(request,'child_section_page.html',data)