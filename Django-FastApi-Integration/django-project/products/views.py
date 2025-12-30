from django.shortcuts import render, redirect
from django.conf import settings
import httpx
from .forms import ProductForm, UserRegistationForm
from django.contrib import messages
# Create your views here.

FASTAPI_URL = settings.FASTAPI_BASE_URL

async def get_products():
    async with httpx.AsyncClient() as client:  # 비동기 http 커넥션
        try:
            response = await client.get(f'{FASTAPI_URL}/api/products')
            response.raise_for_status()  # 오류 발생시 예외 발생
            return response.json()
        except httpx.HTTPError as e:
            print(f"Error fetching products: {e}")
            return []
# 아이디에 대한 제품 조회 함수
async def get_product(product_id):
    async with httpx.AsyncClient() as client:  # 비동기 http 커넥션
        try:
            response = await client.get(f'{FASTAPI_URL}/api/products/{product_id}')
            response.raise_for_status()  # 오류 발생시 예외 발생
            return response.json()
        except httpx.HTTPError as e:
            print(f"Error fetching products: {e}")
            return None

async def create_product(data):
    async with httpx.AsyncClient() as client:  # 비동기 http 커넥션
        try:
            response = await client.post(f'{FASTAPI_URL}/api/products',json=data)
            response.raise_for_status()  # 오류 발생시 예외 발생
            return response.json()
        except httpx.HTTPError as e:
            print(f"Error creating product: {e}")
            return None

async def update_product(product_id, data):
    async with httpx.AsyncClient() as client:  # 비동기 http 커넥션
        try:
            response = await client.put(f'{FASTAPI_URL}/api/products/{product_id}',json=data)
            response.raise_for_status()  # 오류 발생시 예외 발생
            return response.json()
        except httpx.HTTPError as e:
            print(f"Error creating product: {e}")
            return None


###############################################################################################################

async def product_list(request):
    products = await get_products()
    return render(request,'products/product_list.html',{'products': products})


async def product_create(request):
    if request.method == 'GET':
        form = ProductForm()
    elif request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            # 폼에서 데이터 추출
            data = form.cleaned_data
            result = await create_product(data)
            if result:
                messages.success(request, '제품이 성공적으로 생성되었습니다.')
                return redirect('products:product_list')  # url 별칭
            else:
                messages.error(request, '제품 생성에 실패했습니다.')
    return render(request, 'products/product_form.html', {'form': form,'title':'제품등록'})


async def product_edit(request, product_id):
    # 아이디로 제품 조회 후 사용자가 전달한 값으로 업데이트 fastapi 요청
    product = await get_product(product_id)
    if not product:
        messages.error(request, '제품을 찾을 수 없습니다.')
        return redirect('products:product_list')
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            result = await update_product(product_id, data)
            if result:
                messages.success(request, '제품이 성공적으로 수정되었습니다.')
                return redirect('products:product_list')
            else:
                messages.error(request, '제품 수정에 실패했습니다.')
    else:
        form = ProductForm(initial=product)  # 폼을 호출하면서 product 값으로 초기화
    return render(request, 'products/product_form.html', 
                  {'form': form,'title':'제품수정'}
                  )

async def product_delete(request, product_id):
    # 해당 아이디의 제품이 있는지 확인하고 삭제 요청을 FastAPI로 보냄
    product = await get_product(product_id)    
    if not product:
        messages.error(request, '제품을 찾을 수 없습니다.')
        return redirect('products:product_list')    
    if request.method == 'POST':
        async with httpx.AsyncClient() as client:
            try:
                response = await client.delete(f'{FASTAPI_URL}/api/products/{product_id}')
                response.raise_for_status()
                messages.success(request, '제품이 성공적으로 삭제되었습니다.')
                return redirect('products:product_list')
            except httpx.HTTPError as e:
                messages.error(request, '제품 삭제에 실패했습니다.')
                return False
            

################################################ 인증 #################################
def register_view(request):
    '''회원가입'''             
    if request.method=='POST':
        form = UserRegistationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # form데이터 기반으로 user 객체를 생성
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
    else:
        form = UserRegistationForm()
    return render(request,'registration/register.html',{'form':form,'title':'회원가입'})




