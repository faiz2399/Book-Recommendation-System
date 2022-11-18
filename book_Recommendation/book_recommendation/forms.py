from django import forms
import pandas as pd

class userID(forms.Form):
    df_users = pd.read_excel(r'C:\Users\lasya\OneDrive\Desktop\Masters\UML\project\Book-Recommendation-System\Book-Recommendation-System\book_recommendation\app_book\book_genre\users.xlsx')
    l = df_users['User-ID'].to_list()
    OPTIONS = tuple()
    for i in l:
        dummy = tuple()
        dummy = (i,i),
        OPTIONS = OPTIONS + (dummy) 
        # OPTIONS = tuple(OPTIONS)
    # print(OPTIONS)
    user_id = forms.ChoiceField(required=True, choices=OPTIONS, widget=forms.Select(attrs={'class':'email'})
)


