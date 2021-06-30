from django.test import TestCase
from django.test import Client
from .models import Post, Group, Follow
from django.contrib.auth import get_user_model 
from django.urls import reverse
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.cache import cache


User = get_user_model() 

class TestStringMethods(TestCase):

    def setUp(self):
        self.client = Client()
        self.client2 = Client()
        self.user = User.objects.create_user(username ="test_user", 
            email ="testuser@gmail.com", 
            password ="12345",
        )
        self.user2 = User.objects.create_user(username ="test_user2", 
            email ="testuser@gmail.com", 
            password ="123456",
        )
        self.group = Group.objects.create(title ="TEST", slug ="TEST",)
        self.client.force_login(self.user)
        self.post = Post.objects.create(text="test", 
            author=self.user,
            group = self.group,
        )
        self.post_id = self.post.id
                
    def test_profile(self):
        response = self.client.get(reverse("profile", 
            kwargs={"username": self.user.username}
        ))
        self.assertEqual(response.status_code, 200)

    def test_create_post(self):
        response = self.client.get(reverse('profile', 
            kwargs={"username": self.user.username}
        ))
        self.assertEqual(Post.objects.all().count(), 1)
        self.assertEqual(str(self.post.author), self.user.username)
        self.assertEqual(self.post.group, self.group)
        self.assertEqual(str(self.post), self.post.text)
    
    def test_guest(self):
        response = self.client2.post(reverse('new_post'), 
            {'text': 'try_qweewqtext'})
        self.assertRedirects(response, reverse('login') + 
            '?next=' + reverse('new_post'))
        self.assertEqual(Post.objects.filter(text="try_qweewqtext").count(), 0)

    def test_new_post(self): 
        self.client.force_login(self.user) 
        cache.clear()
        self.post = Post.objects.create( 
            text="New test post",  
            author=self.user, 
            ) 
        newpost = self.post 
        self.url_list_response(newpost)
        
    def test_change_post(self):
        self.client.force_login(self.user)
        post = Post.objects.get(author=self.user.id)
        response = self.client.post(
            reverse("post_edit",
            kwargs={"username": self.user.username, "post_id": self.post.id}
            ),
            { "text": "New post text", "author": self.user.id, "group": self.group},
            follow=False
        )
        post_new = Post.objects.get(author=self.user.id)
        response = self.client.get(
            reverse("group", kwargs={"slug": self.group.slug}))
        self.url_list_response(post_new)

    def url_list_response(self, created_post):
        url_list = (
            reverse("index"),
            reverse("profile", kwargs={"username": self.user.username}),
            reverse("post", kwargs={"username": self.user
                    .username, "post_id": self.post.id}))
        for url in url_list:
            response = self.client.get(url)
            self.assertContains(response, created_post.text)
            self.assertEqual(created_post.group, self.post.group)
            self.assertEqual(response.status_code, 200)

    def test_page_not_found(self):
        response = self.client.get("false_page/")
        self.assertEqual(response.status_code, 404)
    
    def test_img(self):
        self.client.force_login(self.user)
        img = Image.new('RGBA', (200, 200), 'red')
        img.save("media/cache/img.png")
        cache.clear()
        posts = Post.objects.create(author = self.user, 
            text= 'post image', group =self.group, image="img")
        url_list = (
            reverse("index"),
            reverse("profile", kwargs={"username": self.user.username}),
            reverse("post", kwargs={"username": self.user
                    .username, "post_id": 2}))
        for url in url_list:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "<img")

    def test_not_img(self):
        self.client.force_login(self.user)
        not_img = SimpleUploadedFile(
            name="test.txt",
            content=b"not img",
            content_type ="text/plain" 
        )
        url = reverse("new_post")
        response = self.client.post(url, {"text":"new_test_text", "image": not_img})
        self.assertFormError(
            response,
            "form",
            "image",
            errors ="Загрузите правильное изображение. Файл, который вы загрузили," 
                    " поврежден или не является изображением."
        )
    
    def test_following_user(self):
        self.client.force_login(self.user)
        user2_profile = self.client.get(
            reverse("profile", args=[self.user2.username]
            ))
        self.assertContains(user2_profile, "Подписаться")
        follow_user2 = self.client.get(
            reverse("profile_follow", args=[self.user2.username]
            ))
        self.assertEqual(Follow.objects.all().count(), 1)
    
    def test_unfollowing_user(self):
        self.client.force_login(self.user)
        user2_profile = self.client.get(
            reverse("profile", args=[self.user2.username]
            ))
        follow_user2 = self.client.get(
            reverse("profile_follow", args=[self.user2.username]
            ))
        user2_profile = self.client.get( 
            reverse("profile", args=[self.user2.username] 
            ))
        self.assertContains(user2_profile, "Отписаться")
        unfollow_user2 = self.client.get(
            reverse("profile_unfollow", args=[self.user2.username]
            ))
        self.assertEqual(Follow.objects.all().count(), 0)
 
    def test_post_follow(self):
        self.client.force_login(self.user)
        follow_user = self.client.get(
            reverse("profile_follow", args=[self.user2.username]
            ))
        self.assertEqual(Follow.objects.all().count(), 1)
        response = self.client.get(reverse("follow_index"))
        self.assertContains(response, self.post.text)
        
    def test_new_post_follow(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("follow_index"))
        self.posts = Post.objects.create(text="test_follow", 
            author=self.user,
            group = self.group,
        )
        self.assertNotContains(response, self.posts.text)
    
    def test_cahe_index(self):
        self.client.force_login(self.user) 
        response = self.client.get(reverse("index"))
        self.assertNotContains(response, "New chek post")
        self.post_chek = Post.objects.create( 
            text="New chek post",  
            author=self.user,
            group = self.group 
            )
        self.assertNotContains(response, self.post_chek.text)
        cache.clear()
        response = self.client.get(reverse("index"))
        self.assertContains(response, self.post_chek.text)
        