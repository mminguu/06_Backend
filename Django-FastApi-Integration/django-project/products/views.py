from django.shortcuts import render , redirect
from django.conf import settings
import httpx
from .forms import ProductForm
from django.contrib import messages

FASTAPI_URL = settings.FASTAPI_BASE_URL


# 비동기 http 통신 (커넥션)
async def get_products():
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f'{FASTAPI_URL}/api/products')
            response.raise_for_status() # 오류 발생 시 예외 발생 시킴
            return response.json()
        except httpx.HTTPError as e:
            print(f'Error fetching products: {e}')
            return []

# create_product(data) 함수 작성하기

async def product_list(request):
    products = await get_products()
    return render(request,'products/product_list.html',{'products':products})

async def product_create(request):
    if request.method == 'GET':
        form = ProductForm()
    elif request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            # form에서 데이터 추출
            data = form.cleaned_data
            result = await create_product(data)
            if result:
                messages.success(request, '제품이 성공적으로 생성되었습니다.')
                return redirect('products:product_list')
            else:
                messages.error(request , '제품 생성에 실패하였습니다.')
    return 