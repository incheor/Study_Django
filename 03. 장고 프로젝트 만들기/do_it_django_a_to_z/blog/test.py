from unicodedata import category
from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post, Category
from django.contrib.auth.models import User

class TestView(TestCase) :
    def setUp(self) :
        self.client = Client()
        # 유저명이 trump, obama인 유저 생성
        self.user_trump = User.objects.create(username = 'trump', password = 'somepassword')
        self.user_obama = User.objects.create(username = 'obama', password = 'somepassword')
        
        # Category 레코드 생성
        self.category_programming = Category.objects.create(name = 'programming', slug = 'programming')
        self.category_music = Category.objects.create(name = 'music', slug = 'music')
        
        # 포스트 3개 생성
        self.post_001 = Post.objects.create(
            title = '나비야 나비야 이리 날아와봐라',
            content = '호랑나비 흰나비',
            category = self.category_music,
            author = self.user_trump,
        )
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
        
        post_002_card = main_area.find('div', id = 'post-2')
        self.assertIn(self.post_002.title, post_002_card.text)
        self.assertIn(self.post_002.category.name, post_002_card.text)
        
        post_003_card = main_area.find('div', id = 'post-3')
        self.assertIn('미분류', post_003_card.text)
        self.assertIn(self.post_003.title, post_003_card.text)
        
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