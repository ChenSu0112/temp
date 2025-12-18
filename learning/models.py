from django.db import models
from accounts.models import User
import os
import uuid
from django.core.validators import FileExtensionValidator
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

#对应数据库learning_subject
class Subject(models.Model):
    name = models.CharField(max_length=100, verbose_name="科目名称")
    description = models.TextField(blank=True, verbose_name="科目描述")
    dataset = models.CharField(max_length=100, default="", verbose_name="关联数据集", help_text="对应习题表的模型名称，如：MathExercise, ChineseExercise")

    class Meta:
        verbose_name = "科目"
        verbose_name_plural = "科目"

    def __str__(self):
        return self.name

    #"""获取该科目对应的习题模型"""
    def get_exercise_model(self):

        from utils.exercise_utils import get_exercise_model
        return get_exercise_model(self.name)

    def get_exercise_table(self):
        """获取该科目的习题表名"""
        model = self.get_exercise_model()
        if model:
            return model._meta.db_table
        return None

    def get_exercise_count(self):
        """获取该科目的习题数量"""
        model = self.get_exercise_model()
        if model:
            return model.objects.filter(subject=self).count()
        return 0


# """教师授课关系（关联Subject=课程）"""
class TeacherSubject(models.Model):

    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="teaching_subjects", verbose_name="教师")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="teachers", verbose_name="课程")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    class Meta:
        verbose_name = "教师授课"
        verbose_name_plural = "教师授课"
        unique_together = ("teacher", "subject")  # 防止重复关联

    def __str__(self):
        return f"{self.teacher.username} - {self.subject.name}"

#"""学生选课关系（关联Subject=课程）"""
class StudentSubject(models.Model):

    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="enrolled_subjects", verbose_name="学生")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="students", verbose_name="课程")
    enrolled_at = models.DateTimeField(auto_now_add=True, verbose_name="选课时间")

    class Meta:
        verbose_name = "学生选课"
        verbose_name_plural = "学生选课"
        unique_together = ("student", "subject")  # 防止重复选课

    def __str__(self):
        return f"{self.student.username} - {self.subject.name}"

#对应数据库learning_knowledgepoint
class KnowledgePoint(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="所属科目")
    name = models.CharField(max_length=200, verbose_name="知识点名称")
    child = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                               related_name='children', verbose_name="子知识点")
    class Meta:
        verbose_name = "知识点"
        verbose_name_plural = "知识点"

    def __str__(self):
        return f"{self.subject.name} - {self.name}"

# """数学习题表"""
class MathExercise(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="所属科目")
    problemsets = models.CharField(max_length=200, default="", verbose_name="习题集ID")
    title = models.CharField(max_length=200, verbose_name="习题标题")
    content = models.TextField(verbose_name="习题内容")
    question_type = models.CharField(max_length=10, default='single', verbose_name="题型")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="创建者", default=1)
    option_text = models.CharField(max_length=1000, verbose_name="选项内容", default=None)
    answer = models.CharField(max_length=500, verbose_name="答案", default=None)
    difficulty_level = models.IntegerField(choices=[(1, '简单'), (2, '中等'), (3, '困难')], default=2)

    # 添加 GenericRelation 以支持反向查询
    answer_logs = GenericRelation('AnswerLog',content_type_field='content_type',object_id_field='object_id',related_query_name='math_exercises')

    class Meta:
        db_table = 'learning_math_exercise'  # 指定表名
        verbose_name = "数学习题"
        verbose_name_plural = "数学习题"

    def __str__(self):
        return self.title

#"""语文习题表"""
class ChineseExercise(models.Model):
    """语文习题表"""
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="所属科目")
    problemsets = models.CharField(max_length=200, default="", verbose_name="习题集ID")
    title = models.CharField(max_length=200, verbose_name="习题标题")
    content = models.TextField(verbose_name="习题内容")
    question_type = models.CharField(max_length=10, default='single', verbose_name="题型")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="创建者", default=1)
    option_text = models.CharField(max_length=1000, verbose_name="选项内容", default=None)
    answer = models.CharField(max_length=500, verbose_name="答案", default=None)
    difficulty_level = models.IntegerField(choices=[(1, '简单'), (2, '中等'), (3, '困难')], default=2)
    # 添加 GenericRelation 以支持反向查询
    answer_logs = GenericRelation('AnswerLog', content_type_field='content_type', object_id_field='object_id',related_query_name='math_exercises')

    class Meta:
        db_table = 'learning_chinese_exercise'
        verbose_name = "语文习题"
        verbose_name_plural = "语文习题"

    def __str__(self):
        return self.title

#"""英语习题表"""
class EnglishExercise(models.Model):
    """英语习题表"""
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="所属科目")
    problemsets = models.CharField(max_length=200, default="", verbose_name="习题集ID")
    title = models.CharField(max_length=200, verbose_name="习题标题")
    content = models.TextField(verbose_name="习题内容")
    question_type = models.CharField(max_length=10, default='single', verbose_name="题型")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="创建者", default=1)
    option_text = models.CharField(max_length=1000, verbose_name="选项内容", default=None)
    answer = models.CharField(max_length=500, verbose_name="答案", default=None)
    difficulty_level = models.IntegerField(choices=[(1, '简单'), (2, '中等'), (3, '困难')], default=2)
    # 添加 GenericRelation 以支持反向查询
    answer_logs = GenericRelation('AnswerLog', content_type_field='content_type', object_id_field='object_id',related_query_name='math_exercises')

    class Meta:
        db_table = 'learning_english_exercise'
        verbose_name = "英语习题"
        verbose_name_plural = "英语习题"

    def __str__(self):
        return self.title

#对应数据库learning_qmatrix
class QMatrix(models.Model):
    # 添加通用外键
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,verbose_name="关联模型",null=True,blank=True)
    object_id = models.PositiveIntegerField(verbose_name="关联对象ID",null=True,blank=True)
    exercise = GenericForeignKey('content_type', 'object_id')

    knowledge_point = models.ForeignKey(KnowledgePoint, on_delete=models.CASCADE, verbose_name="知识点")
    weight = models.FloatField(default=1.0, verbose_name="权重")

    class Meta:
        verbose_name = "Q矩阵"
        verbose_name_plural = "Q矩阵"

    def __str__(self):
        return f"{self.exercise.title} - {self.knowledge_point.name}"

#对应数据库learning_answerlog
class AnswerLog(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="学生")

    # 添加通用外键
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,verbose_name="关联模型",null=True,blank=True)
    object_id = models.PositiveIntegerField(verbose_name="关联对象ID",null=True,blank=True)
    exercise = GenericForeignKey('content_type', 'object_id')

    text_answer = models.TextField(blank=True, verbose_name="文本答案")
    is_correct = models.BooleanField(null=True, verbose_name="是否正确")
    time_spent = models.IntegerField(default=0, verbose_name="答题耗时(秒)")
    submitted_at = models.DateTimeField(auto_now_add=True, verbose_name="提交时间")

    class Meta:
        verbose_name = "答题记录"
        verbose_name_plural = "答题记录"

    def __str__(self):
        return f"{self.student.username} - {self.exercise.title}"

# 添加models
class DiagnosisModel(models.Model):
    name = models.CharField('模型名称', max_length=100)
    description = models.TextField('模型描述', blank=True)
    is_active = models.BooleanField('是否启用', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

#对应数据库learning_studentdiagnosis
class StudentDiagnosis(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="学生")
    knowledge_point = models.ForeignKey(KnowledgePoint, on_delete=models.CASCADE, verbose_name="知识点")
    mastery_level = models.FloatField(default=0.0, verbose_name="掌握程度")
    last_practiced = models.DateTimeField(auto_now=True, verbose_name="最后练习时间")
    practice_count = models.IntegerField(default=0, verbose_name="练习次数")
    correct_count = models.IntegerField(default=0, verbose_name="正确次数")

    class Meta:
        verbose_name = "学生诊断"
        verbose_name_plural = "学生诊断"

    def __str__(self):
        return f"{self.student.username} - {self.knowledge_point.name}"

#对应数据库learning_exercisefile
def exercise_file_upload_path(instance, filename):
    """生成文件上传路径"""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4().hex}.{ext}"
    return f'exercise_files/{instance.teacher.id}/{filename}'
class ExerciseFile(models.Model):
    FILE_STATUS = [
        ('pending', '待处理'),
        ('processing', '处理中'),
        ('completed', '已完成'),
        ('error', '处理失败'),
    ]

    FILE_TYPES = [
        ('txt', '文本文件'),
        ('pdf', 'PDF文件'),
        ('doc', 'Word文档'),
        ('docx', 'Word文档'),
        ('xls', 'Excel文件'),
        ('xlsx', 'Excel文件'),
    ]

    teacher = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="上传教师")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="所属科目")
    file = models.FileField(
        upload_to=exercise_file_upload_path,
        validators=[FileExtensionValidator(allowed_extensions=['txt', 'pdf', 'doc', 'docx', 'xls', 'xlsx'])],
        verbose_name="习题文件"
    )
    original_filename = models.CharField(max_length=255, verbose_name="原始文件名")
    file_type = models.CharField(max_length=10, choices=FILE_TYPES, verbose_name="文件类型")
    status = models.CharField(max_length=20, choices=FILE_STATUS, default='pending', verbose_name="处理状态")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="上传时间")
    processed_at = models.DateTimeField(null=True, blank=True, verbose_name="处理完成时间")
    exercise_count = models.IntegerField(default=0, verbose_name="生成的习题数量")
    error_message = models.TextField(blank=True, verbose_name="错误信息")

    class Meta:
        verbose_name = "习题文件"
        verbose_name_plural = "习题文件"
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.teacher.username} - {self.original_filename}"

    def delete(self, *args, **kwargs):
        """删除模型实例时同时删除文件"""
        if self.file:
            if os.path.isfile(self.file.path):
                os.remove(self.file.path)
        super().delete(*args, **kwargs)