import ssl
from unicodedata import category
from urllib import response
from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post, Category, Tag, Comment
from django.contrib.auth.models import User

class TestView(TestCase) :
    def setUp(self) :
        self.client = Client()
        # 유저명이 trump, obama인 유저 생성
        self.user_trump = User.objects.create_user(username = 'trump', password = 'somepassword')
        self.user_obama = User.objects.create_user(username = 'obama', password = 'somepassword')
        
        # 권한 부여 : obama에게 스태프 권한 부여함
        self.user_obama.is_staff = True
        self.user_obama.save()
        
        # Category 레코드 생성
        self.category_programming = Category.objects.create(name = 'programming', slug = 'programming')
        self.category_music = Category.objects.create(name = 'music', slug = 'music')

        # 태그 생성
        self.tag_python_kor = Tag.objects.create(name = '파이썬 공부', slug = '파이썬-공부')
        self.tag_python = Tag.objects.create(name = 'python', slug = 'python')
        self.tag_hello = Tag.objects.create(name = 'hello', slug = 'hello')
        
        # 포스트 3개 생성
        self.post_001 = Post.objects.create(
            title = '나비야 나비야 이리 날아와봐라',
            content = '호랑나비 흰나비',
            category = self.category_music,
            author = self.user_trump,
        )
        self.post_001.tag.add(self.tag_hello)    

        self.post_002 = Post.objects.create(
            title = 'Django gongbu',
            content = 'this is english',
            category = self.category_programming,
            author = self.user_obama,
        )
        
        self.post_003 = Post.objects.create(
            title = '1등',
            content = '이건 카테고리가 없는 포스트',
            author = self.user_obama,
        )
        self.post_003.tag.add(self.tag_python_kor)
        self.post_003.tag.add(self.tag_python)
        
        # 댓글 작성하기
        self.comment_001 = Comment.objects.create(
            post = self.post_001,
            author = self.user_obama,
            content = '첫 번째 댓글입니다.'
        )

    # category_card_test 함수
    def category_card_test(self, soup) :
        categories_card = soup.find('div', id = 'categories-card')
        self.assertIn('Categories', categories_card.text)
        self.assertIn(f'{self.category_programming.name} ({self.category_programming.post_set.count()})', categories_card.text)
        self.assertIn(f'{self.category_music.name} ({self.category_music.post_set.count()})', categories_card.text)
        self.assertIn(f'미분류 (1)', categories_card.text)
    
    # 내비게이션 바의 정상 여부 확인하는 테스트 코드는
    # test_post_list 함수와 test_post_detail 함수에 동일하게 들어있어서
    # 따로 만들어주기
    def navbar_test(self, soup) :
        navbar = soup.nav
        self.assertIn('Blog', navbar.text)
        self.assertIn('About Me', navbar.text)
        
        logo_btn = navbar.find('a', text = 'Do It Django')
        self.assertEqual(logo_btn.attrs['href'], '/')
        
        logo_btn = navbar.find('a', text = 'Home')
        self.assertEqual(logo_btn.attrs['href'], '/')        
        
        logo_btn = navbar.find('a', text = 'Blog')
        self.assertEqual(logo_btn.attrs['href'], '/blog/')
        
        logo_btn = navbar.find('a', text = 'About Me')
        self.assertEqual(logo_btn.attrs['href'], '/about_me/')
        
    def test_post_list(self) :
        # # 1.1 포스트 목록 페이지를 가져옴
        # response = self.client.get('/blog/')
        # # 1.2 정상적으로 페이지가 로드됨
        # self.assertEqual(response.status_code, 200)
        # # 1.3 페이지 타이틀은 'Blog'임
        # soup = BeautifulSoup(response.content, 'html.parser')
        # self.assertEqual(soup.title.text, 'Blog')
        # # # 1.4 내비게이션 바가 있음
        # # navbar = soup.nav
        # # # 1.5 Blog, About Me 라는 문구가 내비게이션 바에 있음
        # # self.assertIn('Blog', navbar.text)
        # # self.assertIn('About Me', navbar.text)
        # # 내비게이션 바의 정상 여부 파악 함수
        # self.navbar_test(soup)
        
        # # 2.1 메인 영역에 게시물이 하나도 없으면
        # self.assertEqual(Post.objects.count(), 0)
        # # 2.2 '아직 게시물이 없습니다.'라는 문구 출력
        # main_area = soup.find('div', id = 'main-area')
        # self.assertIn('아직 게시물이 없습니다.', main_area.text)
        
        
        # # 3.1 게시물이 2개 있다면
        # post_001 = Post.objects.create(
        #     title = '첫번째 포스트입니다.',
        #     content = '안녕하세요.',
        #     author = self.user_trump,
        # )
        # post_002 = Post.objects.create(
        #     title = '첫번째 포스트입니다.',
        #     content = '안녕하세요.',
        #     author = self.user_obama,
        # )
        # self.assertEqual(Post.objects.count(), 2)
        # # 3.2 포스트 목록 페이지를 새로고침했을 때
        # response = self.client.get('/blog/')
        # soup = BeautifulSoup(response.content, 'html')
        # self.assertEqual(response.status_code, 200)
        # # 3.3 메인 영역에 포스트 2개의 타이틀이 존재함
        # main_area = soup.find('div', id = 'main-area')
        # self.assertIn(post_001.title, main_area.text)
        # self.assertIn(post_002.title, main_area.text)
        # # 3.4 더이상 '아직 게시물이 없습니다.'라는 문구는 보이지 않음
        # self.assertNotIn('아직 게시물이 없습니다.', main_area.text)
        
        # self.assertIn(self.user_trump.username.upper(), main_area.text)
        # self.assertIn(self.user_trump.username.upper(), main_area.text)
        
        # 포스트가 있는 경우
        self.assertEqual(Post.objects.count(), 3)
        
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        self.navbar_test(soup)
        self.category_card_test(soup)
        
        main_area = soup.find('div', id = 'main-area')
        self.assertNotIn('아직 게시물이 없습니다.', main_area.text)
        
        post_001_card = main_area.find('div', id = 'post-1')
        self.assertIn(self.post_001.title, post_001_card.text)
        self.assertIn(self.post_001.category.name, post_001_card.text)
        # 여기부터 post_001의 태그를 확인하는 코드
        self.assertIn(self.tag_hello.name, post_001_card.text)
        self.assertNotIn(self.tag_python.name, post_001_card.text)
        self.assertNotIn(self.tag_python_kor.name, post_001_card.text)
        
        post_002_card = main_area.find('div', id = 'post-2')
        self.assertIn(self.post_002.title, post_002_card.text)
        self.assertIn(self.post_002.category.name, post_002_card.text)
        # 여기부터 post_002의 태그를 확인하는 코드
        self.assertNotIn(self.tag_hello.name, post_002_card.text)
        self.assertNotIn(self.tag_python.name, post_002_card.text)
        self.assertNotIn(self.tag_python_kor.name, post_002_card.text)
        
        post_003_card = main_area.find('div', id = 'post-3')
        self.assertIn('미분류', post_003_card.text)
        self.assertIn(self.post_003.title, post_003_card.text)
        self.assertIn(self.post_003.author.username.upper(), post_003_card.text)
        # 여기부터 post_003의 태그를 확인하는 코드
        self.assertNotIn(self.tag_hello.name, post_003_card.text)
        self.assertIn(self.tag_python.name, post_003_card.text)
        self.assertIn(self.tag_python_kor.name, post_003_card.text)
        
        self.assertIn(self.user_trump.username.upper(), main_area.text)
        self.assertIn(self.user_obama.username.upper(), main_area.text)
        
        # 포스트가 없는 경우
        Post.objects.all().delete()
        self.assertEqual(Post.objects.count(), 0)
        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.content, 'html')
        main_area = soup.find('div', id = 'main-area')
        self.assertIn('아직 게시물이 없습니다.', main_area.text)
        
    def test_post_detail(self) :
        # # 1.1 Post가 하나 있음
        # post_001 = Post.objects.create(
        #     title = '첫번째 포스트입니다.',
        #     content = '안녕하세요.',
        #     # 작성자명 추가
        #     author = self.user_trump,
        # )
        
        # 1.2 그 포스트의 url은 'blog/1/'임
        self.assertEqual(self.post_001.get_absolute_url(), '/blog/1/')
        
        # 2. 첫번째 포스트의 상세 페이지 테스트
        # 2.1 첫번째 post url로 접근하면 정상적으로 작동함(status_code : 200)
        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # # 2.2 포스트 목록 페이지와 똑같은 내비게이션 바가 있음
        # navbar = soup.nav
        # self.assertIn('Blog', navbar.text)
        # self.assertIn('About Me', navbar.text)
        # 내비게이션 바의 정상 여부 파악 함수
        self.navbar_test(soup)
        
        self.category_card_test(soup)
        
        # 2.3 첫번째 포스트의 title이 웹브라우저 탭에 들어있음
        self.assertIn(self.post_001.title, soup.title.text)
        
        # 2.4 첫번째 포스트의 title이 포스트 영역에 있음
        main_area = soup.find('div', id = 'main-area')
        post_area = main_area.find('div', id = 'post-area')
        self.assertIn(self.post_001.title, post_area.text)
        self.assertIn(self.category_music.name, post_area.text)
        
        # 2.5 첫번째 포스트의 작성자(author)가 포스트 영역에 있음
        # 아직 작성 안함
        
        # 2.6 첫번째 포스트의 content가 포스트 영역에 있음
        self.assertIn(self.post_001.content, post_area.text)

        self.assertIn(self.tag_hello.name, post_area.text)
        self.assertNotIn(self.tag_python_kor.name, post_area.text)
        self.assertNotIn(self.tag_python.name, post_area.text)
        
        # 댓글이 있는지 확인함
        comments_area = soup.find('div', id = 'comment-area')
        comment_001_area = comments_area.find('div', id = 'comment-1')
        self.assertIn(self.comment_001.author.username, comment_001_area.text)
        self.assertIn(self.comment_001.content, comment_001_area.text)
        
    def test_category_page(self) :
        # 원래는 Post 모델에서 get_absolute_url로 고유 url을 만들었던 것처럼 Category 모델에서도 만들어야 하지만
        # 나중에 만들기로 하고 일단 테스트 코드에 넣어서 그 페이지를 읽어오고 status_code가 200인지 확인
        response = self.client.get(self.category_music.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        
        # 성공적으로 읽어왔으면 BeautifulSoup으로 파싱하고 내비게이션 바와 뱃지가 정상적으로 있는지 확인
        soup = BeautifulSoup(response.content, 'html.parser')
        self.navbar_test(soup)
        self.category_card_test(soup)
        
        # 페이지 상단에 카테고리 뱃지가 잘 있는지 확인
        # 타이틀 옆 카테고리 벳지는 h1 태그로 쓸거라서 h1 태그에 카테고리 이름이 있는지 확인하면 됨
        self.assertIn(self.category_music.name, soup.h1.text)
        
        # 위쪽에서 선택한 카테고리 이름인 music이 있는지 확인하고
        # 이 카테고리에 해당하는 포스트만 화면에 있는지 확인
        # post_002, post_003의 타이틀은 메인 화면에 있으면 안 됨
        main_area = soup.find('div', id = 'main-area')
        self.assertIn(self.category_music.name, main_area.text)
        self.assertIn(self.post_001.title, main_area.text)
        self.assertNotIn(self.post_002.title, main_area.text)
        self.assertNotIn(self.post_003.title, main_area.text)

    def test_tag_page(self) :
        response = self.client.get(self.tag_hello.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        self.navbar_test(soup)
        self.category_card_test(soup)

        self.assertIn(self.tag_hello.name, soup.h1.text)
        
        main_area = soup.find('div', id = 'main-area')
        self.assertIn(self.tag_hello.name, main_area.text)
        
        self.assertIn(self.post_001.title, main_area.text)
        self.assertNotIn(self.post_002.title, main_area.text)
        self.assertNotIn(self.post_003.title, main_area.text)
        
    def test_create_post(self) :
        # 로그인하지 않으면 status_code가 200이면 안 됨
        response = self.client.get('/blog/create_post/')
        self.assertNotEqual(response.status_code, 200)
        
        # 스태프가 아닌 trump가 로그인 시도함
        self.client.login(username = 'trump', password = 'somepassword')
        response = self.client.get('/blog/create_post/')
        
        # 스태프가 아니기 때문에 status_code는 200이면 안 됨
        self.assertNotEqual(response.status_code, 200)
        
        # 스태프인 obama가 로그인 시도
        self.client.login(username = 'obama', password = 'somepassword')
        response = self.client.get('/blog/create_post/')
        
        # 스태프는 status_code가 200임
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        self.assertEqual('Create Post - Blog', soup.title.text)
        main_area = soup.find('div', id = 'main-area')
        self.assertIn('Create New Post', main_area.text)

        # id가 id_tags_str인 input 태그가 있는지 확인
        tag_str_input = main_area.find('input', id = 'id_tags_str')
        self.assertTrue(tag_str_input)

        # 포스트 작성 페이지에서 포스트를 작성한 후 submit 버튼 클릭하는 행동 구현
        self.client.post(
            '/blog/create_post/',
            {
                'title' : 'Post Form 만들기',
                'content' : 'Post Form 페이지를 만듭시다.',
                # new tag와 한글 태그라는 태그를 생성함(python은 원래 있던 태그)
                # 세미콜론이랑 쉼표는 구분자로 작동하늕지 그냥 넣은거임
                'tags_str' : 'new tag; 한글 태그, python'
            }
        )
        self.assertEqual(Post.objects.count(), 4)
        last_post = Post.objects.last()
        self.assertEqual(last_post.title, 'Post Form 만들기')
        self.assertEqual(last_post.author.username, 'obama')

        self.assertEqual(last_post.tag.count(), 3)
        self.assertTrue(Tag.objects.get(name = 'new tag'))
        self.assertTrue(Tag.objects.get(name = '한글 태그'))
        self.assertEqual(Tag.objects.count(), 5)

    def test_update_post(self) :
        update_post_url = f'/blog/update_post/{self.post_003.pk}/'

        # 로그인하지 않은 경우
        response = self.client.get(update_post_url)
        self.assertNotEqual(response.status_code, 200)

        # 로그인은 했지만 작성자가 아닌 경우
        self.assertNotEqual(self.post_003.author, self.user_trump)
        self.client.login(
            username = self.user_trump.username,
            password = 'somepassword'
        )
        response = self.client.get(update_post_url)
        self.assertEqual(response.status_code, 403)

        # 작성자가 접근하는 경우
        self.client.login(
            username = self.post_003.author.username,
            password = 'somepassword'
        )
        response = self.client.get(update_post_url)
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.assertEqual('Edit Post - Blog', soup.title.text)
        main_area = soup.find('div', id = 'main-area')
        self.assertIn('Edit Post', main_area.text)
        
        tag_str_input = main_area.find('input', id = 'id_tags_str')
        self.assertTrue(tag_str_input)
        self.assertIn('파이썬 공부; python', tag_str_input.attrs['value'])

        response = self.client.post(
            update_post_url,
            {
                'title' : '세 번째 포스트 수정',
                'content' : '포스트 수정 테스트',
                'category' : self.category_music.pk,
                'tags_str' : '파이썬 공부; 한글 태그, some tag'
            },
            follow = True
        )
        soup = BeautifulSoup(response.content, 'html.parser')
        main_area = soup.find('div', id = 'main-area')
        self.assertIn('세 번째 포스트 수정', main_area.text)
        self.assertIn('포스트 수정 테스트', main_area.text)
        self.assertIn(self.category_music.name, main_area.text)
        self.assertIn('파이썬 공부', main_area.text)
        self.assertIn('한글 태그', main_area.text)
        self.assertIn('some tag', main_area.text)
        self.assertNotIn('python', main_area.text)
        
    def test_comment_form(self) :
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(self.post_001.comment_set.count(), 1)
        
        # 로그인하지 않은 상태
        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        comment_area = soup.find('div', id = 'comment-area')
        self.assertIn('Sign in and leave a comment', comment_area.text)
        self.assertFalse(comment_area.find('form', id='comment-form'))
        
        self.client.login(username='obama', password='somepassword')
        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        comment_area = soup.find('div', id='comment-area')
        self.assertNotIn('Sign in and leave a comment', comment_area.text)
        
        comment_form = comment_area.find('form', id='comment-form')
        self.assertTrue(comment_form.find('textarea', id='id_content'))
        response = self.client.post(
            self.post_001.get_absolute_url() + 'new_comment/',
            {
                'content' : '오바마의 댓글입니다.',
            },
            follow = True
        )
        
        self.assertEqual(response.status_code, 200)
        
        self.assertEqual(Comment.objects.count(), 2)
        self.assertEqual(self.post_001.comment_set.count(), 2)
        new_comment = Comment.objects.last()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertIn(new_comment.post.title, soup.title.text)
        
        comment_area = soup.find('div', id='comment-area')
        new_comment_div = comment_area.find('div', id=f'comment-{new_comment.pk}')
        self.assertIn('obama', new_comment_div.text)
        self.assertIn('오바마의 댓글입니다.', new_comment_div.text)
        
    def test_comment_update(self) :
        comment_by_trump = Comment.objects.create(
            post = self.post_001,
            author = self.user_trump,
            content = '트럼프의 댓글입니다.'
        )
        
        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        comment_area = soup.find('div', id = 'comment-area')
        self.assertFalse(comment_area.find('a', id = 'comment-1-update-btn'))
        self.assertFalse(comment_area.find('a', id = 'comment-2-update-btn'))
        
        # 로그인한 상태
        self.client.login(username = 'obama', password = 'somepassword')
        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        comment_area = soup.find('div', id = 'comment-area')
        self.assertFalse(comment_area.find('a', id = 'comment-2-update-btn'))
        comment_001_update_btn = comment_area.find('a', id ='comment-1-update-btn')
        self.assertIn('edit', comment_001_update_btn.text)
        self.assertEqual(comment_001_update_btn.attrs['href'], '/blog/update_comment/1/')
        
        self.assertIn('edit', comment_001_update_btn.text)
        self.assertEqual(comment_001_update_btn.attrs['href'], '/blog/update_comment/1/')
        
        response = self.client.get('/blog/update_comment/1/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        self.assertEqual('Edit Comment - Blog', soup.title.text)
        update_comment_form = soup.find('form', id = 'comment-form')
        content_textarea = update_comment_form.find('textarea', id = 'id_content')
        self.assertIn(self.comment_001.content, content_textarea.text)
        
        response = self.client.post(
            f'/blog/update_comment/{self.comment_001.pk}/',
            {
                'content' : '오바마의 댓글을 수정합니다.'
            },
            follow = True
        )
        
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        comment_001_div = soup.find('div', id = 'comment-1')
        self.assertIn('오바마의 댓글을 수정합니다.', comment_001_div.text)
        self.assertIn('Update: ', comment_001_div.text)
        
    def test_delete_comment(self) :
        comment_by_trump = Comment.objects.create(
            post = self.post_001,
            author = self.user_trump,
            content = '트럼프의 댓글입니다.'
        )
        
        self.assertEqual(Comment.objects.count(), 2)
        self.assertEqual(self.post_001.comment_set.count(), 2)
        
        # 로그인하지 않은 상태
        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        comment_area = soup.find('div', id = 'comment-area')
        self.assertFalse(comment_area.find('a', id = 'comment-1-delete-btn'))
        self.assertFalse(comment_area.find('a', id = 'comment-2-delete-btn'))
        
        # trump로 로그인한 상태
        self.client.login(username = 'trump', password = 'somepassword')
        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        comment_area = soup.find('div', id = 'comment-area')
        self.assertFalse(comment_area.find('a', id = 'comment-1-delete-btn'))
        comment_002_delete_modal_btn = comment_area.find('a', id = 'comment-2-delete-modal-btn')
        self.assertIn('delete', comment_002_delete_modal_btn.text)
        self.assertEqual(comment_002_delete_modal_btn.attrs['data-bs-target'], '#deleteCommentModal-2')
        
        delete_comment_modal_002 = soup.find('div', id = 'deleteCommentModal-2')
        self.assertIn('Are You Sure?', delete_comment_modal_002.text)
        really_delete_btn_002 = delete_comment_modal_002.find('a')
        self.assertIn('Delete', really_delete_btn_002.text)
        self.assertEqual(really_delete_btn_002.attrs['href'], '/blog/delete_comment/2/')
        
        response = self.client.get('/blog/delete_comment/2/', follow = True)
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertIn(self.post_001.title, soup.title.text)
        comment_area = soup.find('div', id = 'comment-area')
        self.assertNotIn('트럼프의 댓글입니다.', comment_area)
        
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(self.post_001.comment_set.count(), 1)
        
    def test_search(self) :
        post_about_python = Post.objects.create(
            title = '파이썬에 대한 포스트입니다.',
            content = 'Hello World!',
            author = self.user_trump
        )
        
        response = self.client.get('/blog/search/파이썬/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        main_area = soup.find('div', id = 'main-area')
        
        self.assertIn('Search: 파이썬 - 2개의 관련 포스트', main_area.text)
        self.assertNotIn(self.post_001.title, main_area.text)
        self.assertNotIn(self.post_002.title, main_area.text)
        self.assertIn(self.post_003.title, main_area.text)
        self.assertIn(post_about_python.title, main_area.text)