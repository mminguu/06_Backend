# 화면 구성을 클래스 형태로 구현해서 html에서 표시 ----.html 을 대신
from django import forms

class ProductForm(forms.Form):
    forms.CharField(max_length=200 , label='제품명' , 
                    widget=forms.TextInput(attrs={'placeholder':'제품명을 입력하세요'})
                    )
    description = forms.CharField(required=False , label='제품 설명',
                                widget=forms.Textarea(attrs={'rows':4,'placeholder':'제품설명을 입력하세요'}))
    price = forms.FloatField(required=False , label='제품 가격',
                                widget=forms.NumberInput(attrs={'min':0,'step':0.01,'placeholder':'제품 가격을 입력하세요'}))
    stock = forms.IntegerField(initial=0 , label='재고수량',
                            widget=forms.NumberInput(attrs={'min':0,'step':0.01,'placeholder':'제품 수량을 입력하세요'}))
