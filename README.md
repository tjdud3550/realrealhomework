# 멋쟁이사자처럼 7기 세션 CRUD + 추가기능

게시물과 댓글 CRUD기능

### 추가기능
1. 게시글 카테고리 선택
2. 게시글 필터 및 정렬
3. 댓글 수정 및 삭제


### 1. 게시글 카테고리 선택

forms.py
<pre><code>
class NewBlog(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['category', 'title', 'body']
        #카테고리 필드 추가
</code></pre>

models.py
<pre><code>
# 카테고리 셀렉트 필드 추가
category_select = (
    ('일반','일반'),
    ('공지', '공지'),
    ('과제','과제'),
)

class Blog(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    body = models.TextField()
    # 카테고리 셀렉트
    category = models.CharField(max_length=20, choices=category_select, default='일반')
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
</code></pre>

이후 마이그레이션즈 와 마이그레이트 진행


### 2. 게시글 필터 및 정렬

veiws.py
<pre><code>
def read(request):
    blogs = Blog.objects.all().filter(category='과제').order_by('-created_date')
    return render(request, 'funccrud/funccrud.html', {'blogs':blogs})

    # queryset = queryset.order_by('field1') # 지정 필드 오름차순 요청
    # queryset = queryset.order_by('-field1') # 지정 필드 내림차순 요청
    # queryset = queryset.order_by('field2', 'field3') # 1차기준, 2차기준
</code></pre>

### 3. 댓글 수정 및 삭제

views.py
<pre><code>
# 추가하고, url도 추가
def del_comment(request, pk):
    comment = get_object_or_404(Comment, pk = pk)
    comment.delete()
    return redirect('home')

 # 댓글 수정   
@login_required(login_url='/login/')
def edit_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment.save()
            return redirect('home')
    else:
        form = CommentForm(instance=comment)
    return render(request, 'funccrud/add_comment.html', {'form': form})
</code></pre>

urls.py
<pre><code>
urlpatterns = [
    # comment
    path('delcomment/<int:pk>', views.del_comment, name='del_comment'),
    path('editcomment/<int:pk>', views.edit_comment, name='edit_comment'),
]
</code></pre>




