from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post
from django.contrib.auth.models import User

class TestView(TestCase) :
    def setUp(self) :
        self.client = Client()
        # 유저명이 trump, obama인 유저 생성
        self.user_trump = User.objects.create(username = 'trump', password = 'somepassword')
        self.user_obama = User.objects.create(username = 'obama', password = 'somepassword')
    
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
        # 1.1 포스트 목록 페이지를 가져옴
        response = self.client.get('/blog/')
        # 1.2 정상적으로 페이지가 로드됨
        self.assertEqual(response.status_code, 200)
        # 1.3 페이지 타이틀은 'Blog'임
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(soup.title.text, 'Blog')
        # # 1.4 내비게이션 바가 있음
        # navbar = soup.nav
        # # 1.5 Blog, About Me 라는 문구가 내비게이션 바에 있음
        # self.assertIn('Blog', navbar.text)
        # self.assertIn('About Me', navbar.text)
        # 내비게이션 바의 정상 여부 파악 함수
        self.navbar_test(soup)
        
        # 2.1 메인 영역에 게시물이 하나도 없으면
        self.assertEqual(Post.objects.count(), 0)
        # 2.2 '아직 게시물이 없습니다.'라는 문구 출력
        main_area = soup.find('div', id = 'main-area')
        self.assertIn('아직 게시물이 없습니다.', main_area.text)
        
        
        # 3.1 게시물이 2개 있다면
        post_001 = Post.objects.create(
            title = '첫번째 포스트입니다.',
            content = '안녕하세요.',
            author = self.user_trump,
        )
        post_002 = Post.objects.create(
            title = '첫번째 포스트입니다.',
            content = '안녕하세요.',
            author = self.user_obama,
        )
        self.assertEqual(Post.objects.count(), 2)
        # 3.2 포스트 목록 페이지를 새로고침했을 때
        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.content, 'html')
        self.assertEqual(response.status_code, 200)
        # 3.3 메인 영역에 포스트 2개의 타이틀이 존재함
        main_area = soup.find('div', id = 'main-area')
        self.assertIn(post_001.title, main_area.text)
        self.assertIn(post_002.title, main_area.text)
        # 3.4 더이상 '아직 게시물이 없습니다.'라는 문구는 보이지 않음
        self.assertNotIn('아직 게시물이 없습니다.', main_area.text)
        
        self.assertIn(self.user_trump.username.upper(), main_area.text)
        self.assertIn(self.user_trump.username.upper(), main_area.text)
        
    def test_post_detail(self) :
        # 1.1 Post가 하나 있음
        post_001 = Post.objects.create(
            title = '첫번째 포스트입니다.',
            content = '안녕하세요.',
            # 작성자명 추가
            author = self.user_trump,
        )
        # 1.2 그 포스트의 url은 'blog/1/'임
        self.assertEqual(post_001.get_absolute_url(), '/blog/1/')
        
        # 2. 첫번째 포스트의 상세 페이지 테스트
        # 2.1 첫번째 post url로 접근하면 정상적으로 작동함(status_code : 200)
        response = self.client.get(post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # # 2.2 포스트 목록 페이지와 똑같은 내비게이션 바가 있음
        # navbar = soup.nav
        # self.assertIn('Blog', navbar.text)
        # self.assertIn('About Me', navbar.text)
        # 내비게이션 바의 정상 여부 파악 함수
        self.navbar_test(soup)
        
        # 2.3 첫번째 포스트의 title이 웹브라우저 탭에 들어있음
        self.assertIn(post_001.title, soup.title.text)
        
        # 2.4 첫번째 포스트의 title이 포스트 영역에 있음
        main_area = soup.find('div', id = 'main-area')
        post_area = main_area.find('div', id = 'post-area')
        self.assertIn(post_001.title, post_area.text)
        
        # 2.5 첫번째 포스트의 작성자(author)가 포스트 영역에 있음
        # 아직 작성 안함
        
        # 2.6 첫번째 포스트의 content가 포스트 영역에 있음
        self.assertIn(post_001.content, post_area.text)