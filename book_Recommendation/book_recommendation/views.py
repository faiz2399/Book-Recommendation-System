from django.http.response import HttpResponse, Http404, HttpResponseNotFound,HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
import pandas as pd
from .forms import userID

df_users = pd.read_excel(r'C:\Users\lasya\OneDrive\Desktop\Masters\UML\project\Book-Recommendation-System\Book-Recommendation-System\book_recommendation\app_book\book_genre\users.xlsx')


def homepage(request):

    # var = {'users':df_users['User-ID'].to_list()}
    if request.method == 'POST':
        form = userID(request.POST)
        if form.is_valid():
            u = pd.DataFrame({'user-id':[form.cleaned_data['user_id']]})
            u.to_excel(r'C:\Users\lasya\OneDrive\Desktop\Masters\UML\project\Book-Recommendation-System\Book-Recommendation-System\book_recommendation\app_book\book_genre\u.xlsx')
            return redirect(reverse('app_book:exam'))

    else:
        form = userID()
    
        return render(request,'login.html', context={'form':form})