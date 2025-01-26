from django.db import models

# Create your models here.
class Question(models.Model):
    qno=models.IntegerField(primary_key=True)
    qtext=models.CharField(max_length=150)
    answer=models.CharField(max_length=50)
    op1=models.CharField(max_length=50)
    op2=models.CharField(max_length=50)
    op3=models.CharField(max_length=50)
    op4=models.CharField(max_length=50)
    subject=models.CharField(max_length=50)

    def __str__(self):
        return f"{self.qno ,self.qtext, self.answer, self.op1,self.op2,self.op3,self.op4}"

    class Meta:
        db_table='question'

    
class Result(models.Model):
    username=models.CharField(max_length=50,primary_key=True)
    subject=models.CharField(max_length=50)
    score=models.IntegerField()

    def __str__(self):
        return f"username= {self.username} | subject= {self.subject} | score= {self.score}"
    
    class Meta:
        db_table='result'