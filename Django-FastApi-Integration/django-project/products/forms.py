# 화면구성을 클래스형태로 구현해서 html에서 표시   ----.html 을 대신
from django import forms
from .models import User

class ProductForm(forms.Form):
    name = forms.CharField(max_length=200,label='제품명',
                    widget=forms.TextInput(attrs={'placeholder':'제품명을 입력하세요'})
                    )
    description = forms.CharField(required=False,label='제품설명',
                    widget=forms.Textarea(attrs={'rows':4,'placeholder':'제품설명을 입력하세요'}))
    price = forms.FloatField(label='제품가격',
                    widget=forms.NumberInput(attrs={'min':0,'step':0.01,'placeholder':'제품가격을 입력하세요'}))
    stock = forms.IntegerField(initial=0, label='재고수량',
                    widget=forms.NumberInput(attrs={'min':0,'placeholder':'재고수량을 입력하세요'}))
 
 ######################################### 인증 #####################################
class UserRegistationForm(forms.ModelForm):
    '''회원가입 폼'''
    password = forms.CharField(label='비밀번호',
                               widget=forms.PasswordInput(attrs={'placeholder':'비밀번호를 입력하세요'}))
    password_confirm = forms.CharField(label='비밀번호 확인',
                               widget=forms.PasswordInput(attrs={'placeholder':'비밀번호를 입력하세요'}))
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder':'사용자명을 입력하세요'}),
            'email': forms.EmailInput(attrs={'placeholder':'이메일을 입력하세요'}),
            'first_name':forms.TextInput(attrs={'placeholder':'이름을 입력하세요'}),
            'last_name':forms.TextInput(attrs={'placeholder':'성을 입력하세요'}),
        }
        labels={
            'username':'사용자명',
            'email':'이메일',
            'first_name':'이름',
            'last_name':'성'
        }
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('비밀번호가 일치하지 않습니다.')
        return cleaned_data

class UserLoginForm(forms.Form):
    '''로그인 폼'''
    username = forms.CharField(label='사용자명',
                            widget=forms.TextInput(attrs={'placeholder':'사용자명을 입력하세요'}))
    password = forms.CharField(label='비밀번호',
                            widget=forms.PasswordInput(attrs={'placeholder':'비밀번호를 입력하세요'}))



