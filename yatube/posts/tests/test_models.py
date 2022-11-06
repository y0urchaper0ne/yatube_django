from django.test import TestCase
from ..models import Group, Post, User


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
        )

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        expected_results = [
            (str(self.post), self.post.text[:15]),
            (str(self.group), f'{self.group.title}'),
        ]
        for actual, expected in expected_results:
            with self.subTest(expected_text=expected):
                self.assertEqual(actual, expected)

    def test_help_text(self):
        """Проверяем, что у моделей правильно выводится help_text"""
        post = PostModelTest.post
        help_model = {
            'text': 'Введите текст поста',
            'group': 'Группа, к которой будет относиться пост',
        }
        for field, help_message in help_model.items():
            with self.subTest(field=field):
                help_text = post._meta.get_field(field).help_text
                self.assertEqual(help_text, help_message)
