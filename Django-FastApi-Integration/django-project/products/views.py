from django.shortcuts import render, redirect
from django.conf import settings
import httpx
from .forms import ProductForm
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
async def create_product(data):
    async with httpx.AsyncClient() as client:  # 비동기 http 커넥션
        try:
            response = await client.post(f'{FASTAPI_URL}/api/products',json=data)
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
                return redirect('products:product_list') # url 별칭
            else:
                messages.error(request, '제품 생성에 실패했습니다.')
    return render(request, 'products/product_form.html', {'form': form,'title':'제품등록'})


async def product_edit(request , product_id):
    pass

async def product_delete(request , product_id):
    pass