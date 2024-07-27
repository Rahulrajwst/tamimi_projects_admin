from django.shortcuts import render, redirect
from . models import CategoryModel,DeviceModel,SectionModel,ParentSectionModel,DeviceOrderModel,SectionOrderModel
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from .serializer import DeviceSerializer,SectionSerializer,ParentSectionSerializer,DeviceOrderSerializer,SectionOrderSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .forms import ParentForm,CreateUserForm,LoginForm
from django.http import HttpResponse
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login

from django.contrib.auth.decorators import login_required

# apis
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

@api_view(['GET'])
def getDeviceOrderData(request):
    devicelist = DeviceOrderModel.objects.all().order_by('sortno')
    serializer = DeviceOrderSerializer(devicelist, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getSectionOrderData(request):
    sectionlist = SectionOrderModel.objects.all().order_by('sortno')
    serializer = SectionOrderSerializer(sectionlist, many=True)
    return Response(serializer.data)


# Views
@login_required(login_url='login')
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
                    try:
                        tmp_instance=CategoryModel.objects.get(catid=i['id'])
                        tmp_instance.catid=i['id']
                        tmp_instance.categoryname=i['title']
                        tmp_instance.handle=i['handle']
                        tmp_instance.save()
                    except CategoryModel.DoesNotExist: 
                        category=CategoryModel(catid=i['id'],categoryname=i['title'],handle=i['handle'])
                        category.save()

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

@login_required(login_url='login')
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

@login_required(login_url='login')
def all_sections_view(request):

    if request.POST:
        if '_create' in request.POST:
            print('create')
            catid = request.POST.get('selected_option') 
            print(catid)       
            formdata = CategoryModel.objects.get(catid=catid)
            image = request.FILES.get('image')
            section = SectionModel(category=formdata,sectionimage=image)
            
            try:
                section.save()
            except:
                print("can not save")
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

@login_required(login_url='login')
def all_parent_sections_view(request):


    frm=ParentForm()
    if request.POST:
        if '_create' in request.POST:
            frm=ParentForm(request.POST, request.FILES)
            if frm.is_valid():
                frm.save()
        elif '_delete' in request.POST:
            id = request.POST.get('_delete')
            tmp_instance=ParentSectionModel.objects.get(pk=id)
            tmp_instance.delete()
            print('delete') 

    
    parentsectionlist=ParentSectionModel.objects.all()

    data={'parentsectionlist':parentsectionlist,'frm':frm}
    
    
    return render(request,'parent_section_page.html',data)


@login_required(login_url='login')
def child_section_view(request,pk):
    
    parent=ParentSectionModel.objects.get(pk=pk)
    if request.POST:
        if '_create' in request.POST:
            
            childid = request.POST.get('_selected_option') 
            child=SectionModel.objects.get(pk=childid)
            child.parentsection=parent
            try:
                child.save()
            except:
                print("can not save")
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


def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponse("The user was registered!")
        
    context = {'form':form}

    return render(request, 'register_page.html', context)

def login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            username = request.POST.get ('username')
            password = request.POST. get ('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('home_page')


            form.save()
            return HttpResponse("")
        
    context = {'form':form}

    return render(request, 'login_page.html', context)

def logout(request):
    
    auth.logout(request)

    return redirect("login")


@login_required(login_url='login')
def device_order_view(request):

    edit_flag=False
    selected_order=None
    if request.POST:
        if '_create' in request.POST:
            
            device_id = request.POST.get('new_option') 
            if device_id is None:
                print(device_id)
            else:
                print('create')
                device_order_count = DeviceOrderModel.objects.count()
                print(device_order_count)
                device_order_count=device_order_count+1
                selected_device = DeviceModel.objects.get(pk=device_id)
                new_device_order = DeviceOrderModel(sortno=device_order_count,device=selected_device)
                new_device_order.save()
            
        elif '_delete' in request.POST:
            edit_flag=False
            selected_order=None
            id = request.POST.get('_delete')
            tmp_instance=DeviceOrderModel.objects.get(pk=id)
            tmp_instance.delete()

            device_order_list=DeviceOrderModel.objects.all().order_by('sortno')
            counter=1
            for item in device_order_list:
                item.sortno=counter
                item.save()
                counter+=1
            print('delete')
        elif '_deleteall' in request.POST:
            print('delete all')
            DeviceOrderModel.objects.all().delete()
        elif '_edit' in request.POST:
            id=request.POST.get('_edit')
            selected_order=DeviceOrderModel.objects.get(pk=id)
            edit_flag=True

        
        elif '_save' in request.POST:
            print('save start') 
            order_id = request.POST.get('_save')   
            selected_order = DeviceOrderModel.objects.get(pk=order_id)

            sortno = request.POST.get('edit_option')
            stored_order=DeviceOrderModel.objects.get(sortno=sortno)
            

            
            stored_order.sortno=selected_order.sortno
            selected_order.sortno=sortno


            try:
                selected_order.save()
                stored_order.save()
                
            except:
                print("can not save")
            edit_flag=False
            selected_order=None
            print('save end')
        elif '_cancel' in request.POST:
            edit_flag=False
            selected_order=None
            print('cancel')
    

    devicelist=DeviceModel.objects.all()
    device_order_list=DeviceOrderModel.objects.all().order_by('sortno')
    
    unselected_options=[]
    for i in devicelist:
        exist=False
        for j in device_order_list:
            if i==j.device:
                exist=True
                break
        if exist==False:
            unselected_options.append(i)
        

    # print(edit_flag)
    # print(selected_order)
    # print(devicelist)
    # print('running after request=========')
    data={'device_order_list':device_order_list,'unselected_options':unselected_options,'edit_flag':edit_flag, 'selected_order':selected_order}
    
    return render(request,'device_order_page.html',data)

@login_required(login_url='login')
def section_order_view(request):

    edit_flag=False
    selected_order=None
    type_id='0'  # '0' stands for parent, '1' stands for section
    if request.POST:
        if '_create' in request.POST:
            parentflag=False

            section_order_count = SectionOrderModel.objects.count()
            print('section_order_count',section_order_count)
            section_order_count=section_order_count+1
            type_id = request.POST.get('_type') 
            print('type_id:',type_id)
            if type_id=='0':
                parentflag=True
                parent_id = request.POST.get('parent_option')
                try:
                    
                     
                    parentsection=ParentSectionModel.objects.get(pk=parent_id)
                    newsection=SectionOrderModel(sortno=section_order_count,parent=parentflag,parentsection=parentsection)
                
                    newsection.save()
                except:
                    print("can not save")
            else:
                child_id = request.POST.get('section_option') 
                try:
                    
                    childsection=SectionModel.objects.get(pk=child_id)
                    newsection=SectionOrderModel(sortno=section_order_count,parent=parentflag,normalsection=childsection)
                
                    newsection.save()
                except:
                    print("can not save")
        elif '_type' in request.POST:
            type_id = request.POST.get('_type') 
            print('type_id:',type_id)

            
        elif '_delete' in request.POST:
            edit_flag=False
            selected_order=None
            id = request.POST.get('_delete')
            tmp_instance=SectionOrderModel.objects.get(pk=id)
            tmp_instance.delete()

            list=SectionOrderModel.objects.all().order_by('sortno')
            counter=1
            for item in list:
                item.sortno=counter
                item.save()
                counter+=1
            print('delete')

        elif '_deleteall' in request.POST:
            print('delete all')
            SectionOrderModel.objects.all().delete()

        elif '_edit' in request.POST:
            id=request.POST.get('_edit')
            selected_order=SectionOrderModel.objects.get(pk=id)
            edit_flag=True

        
        elif '_save' in request.POST:
            print('save start') 
            order_id = request.POST.get('_save')   
            selected_order = SectionOrderModel.objects.get(pk=order_id)

            sortno = request.POST.get('edit_option')
            stored_order=SectionOrderModel.objects.get(sortno=sortno)
            
            stored_order.sortno=selected_order.sortno
            selected_order.sortno=sortno


            try:
                selected_order.save()
                stored_order.save()
            except:
                print("can not save")
            edit_flag=False
            selected_order=None
            print('save end')

        elif '_cancel' in request.POST:
            edit_flag=False
            selected_order=None
            print('cancel')
    

    sectionlist=SectionModel.objects.all()
    parentlist=ParentSectionModel.objects.all()
    section_order_list=SectionOrderModel.objects.all().order_by('sortno')
    
    unselected_sections=[]
    unselected_parents=[]
    

    for parent in parentlist:
        parent_exist=False
        for order in section_order_list:
            if parent==order.parentsection:
                parent_exist=True
                break
        if parent_exist==False:
            unselected_parents.append(parent)
        
    
    for section in sectionlist:
        section_exist=False
        for order in section_order_list:
            if section==order.normalsection:
                section_exist=True
                break
        if section_exist==False:
            unselected_sections.append(section)    

        
    data={'section_order_list':section_order_list,'unselected_parents':unselected_parents,'unselected_sections':unselected_sections,'edit_flag':edit_flag, 'selected_order':selected_order, 'type_id':type_id}
    
    return render(request,'section_order_page.html',data)