from django.db import models


class QuestionCategory(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория вопросов'
        verbose_name_plural = verbose_name


class Question(models.Model):
    title = models.CharField(max_length=255)
    answer = models.TextField(max_length=3000)
    category = models.ForeignKey(to=QuestionCategory, on_delete=models.CASCADE, related_name='question')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = verbose_name


class Callback(models.Model):
    SUBJECT = (
        ('Жалоба', 'Жалоба'),
        ('Предложение', 'Предложение')
    )
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=30, choices=SUBJECT, default='Жалоба')
    text = models.TextField(max_length=2000)
    created_on = models.DateTimeField(auto_now_add=True)
    checked = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Обратная связь'
        verbose_name_plural = verbose_name


class PolicyConf(models.Model):
    title = models.CharField(max_length=255, default='Политика конфиденциальности')
    text = models.TextField(max_length=10000)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Политика конфиденциальности'
        verbose_name_plural = verbose_name
