from django.db import models


class Bot(models.Model):
    """
    Модель бота. Твиттер добавлен только для того, чтобы было видно, что это работает
    """
    owner = models.ForeignKey('auth.User', related_name='bots', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True)
    AGE_CHOICES = (
        ('1', 'до 20'),
        ('2', '20-35'),
        ('3', '35-50'),
        ('4', '50+'),
    )
    age = models.PositiveIntegerField(null=False, choices=AGE_CHOICES)

    SOCIAL_NETWORK_CHOICES = (
        ('VK', 'VK'),
        #('Twitter', 'Twitter'),
        #('Facebook', 'Facebook'),
    )
    social_network = models.CharField(choices=SOCIAL_NETWORK_CHOICES, null=False, max_length=100)

    SEX_CHOICES = (
        ('1', 'мужской'),
        ('2', 'женский'),
    )
    gender = models.PositiveIntegerField(null=False, choices=SEX_CHOICES)

    login = models.CharField(unique=True, max_length=100, null=False)
    password = models.CharField(max_length=100, null=False)
    active_messages = models.BooleanField(blank=False, null=False, default=False)
    active_posts = models.BooleanField(blank=False, null=False, default=False)
    active_friends = models.BooleanField(blank=False, null=False, default=False)
    TIME_CHOICES = (
        ('*/10 * * * *', 'десять минут'),
        ('*/30 * * * *', 'полчаса'),
        ('0 * * * *', 'час'),
        ('0 */2 * * *', 'два часа'),
        ('0 */3 * * *', 'три часа'),
        ('0 */5 * * *', 'пять часов'),
        ('0 */12 * * *', 'двенадцать часов'),
        ('0 0 * * *', 'день'),
        ('0 0 */2 * *', 'два дня'),
        ('0 0 */3 * *', 'три дня'),
        ('0 0 0 * *', 'неделя'),
    )
    time = models.CharField(max_length=50, null=True, blank=True, choices=TIME_CHOICES)
