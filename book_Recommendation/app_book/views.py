from django.shortcuts import render
from . import machine_learning
import pandas as pd


def display_page(request):
    return render(request,'app_book/template-1.html')
def exam(request):
    u = pd.read_excel(r'C:\Users\lasya\OneDrive\Desktop\Masters\UML\project\Book-Recommendation-System\Book-Recommendation-System\book_recommendation\app_book\book_genre\u.xlsx')
    u = u['user-id'].to_list()[0]
    var = dict()
   
    var['ImagePop'] = machine_learning.pop()
    var['ImageTensor']= machine_learning.collab_filter(u)
    # var = var.to_dict()
    var['ImageUser'], var['ImageKnn'] = machine_learning.knn(u)
    var['ImageUI'] = machine_learning.user_item(u)
    # var['ImageCon'] =machine_learning.content(254)
    
    return render(request, 'app_book/template-1.html',context = var)



# Create your views here.
