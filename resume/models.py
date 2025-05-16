from django.db import models

class PersonalInfo(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    linkedin = models.URLField()

    def __str__(self):
        return self.name

class Education(models.Model):
    degree = models.CharField(max_length=100)
    university = models.CharField(max_length=100)
    start = models.CharField(max_length=4)
    end = models.CharField(max_length=4)
    person = models.ForeignKey(PersonalInfo, on_delete=models.CASCADE, related_name='education')

    def __str__(self):
        return f"{self.degree} - {self.university}"

class Experience(models.Model):
    title = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    start = models.CharField(max_length=4)
    end = models.CharField(max_length=4)
    description = models.TextField()
    person = models.ForeignKey(PersonalInfo, on_delete=models.CASCADE, related_name='experience')

    def __str__(self):
        return f"{self.title} at {self.company}"

class Skill(models.Model):
    name = models.CharField(max_length=50)
    person = models.ForeignKey(PersonalInfo, on_delete=models.CASCADE, related_name='skills')

    def __str__(self):
        return self.name

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    link = models.URLField()
    person = models.ForeignKey(PersonalInfo, on_delete=models.CASCADE, related_name='projects')

    def __str__(self):
        return self.name