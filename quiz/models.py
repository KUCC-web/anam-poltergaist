from django.db import models


class Quiz(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Question(models.Model):
    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE)
    question = models.CharField(max_length=100, null=False)
    score = models.IntegerField(default=0, null=False)
    image_url = models.CharField(max_length=1000)
    description = models.CharField(max_length=1000, default="")

    def __str__(self):
        return '{} ({})'.format(self.question, str(self.score))

    def __gt__(self, other):
        return self.pk > other

    def __ge__(self, other):
        return self.pk >= other

    def __lt__(self, other):
        return self.pk < other

    def __le__(self, other):
        return self.pk <= other

    def __eq__(self, other):
        return self.pk == other


class Grade(models.Model):
    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE)
    text = models.CharField(max_length=100)
    min = models.IntegerField(null=False)
    max = models.IntegerField(null=False)

    def __str__(self):
        return '[{}] ({}~{}) {}'.format(str(self.quiz.name), str(self.min), str(self.max), self.text)
