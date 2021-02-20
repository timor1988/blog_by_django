from django import forms


class SearchForm(forms.Form):
    query = forms.CharField(label="请输入搜索关键字")
