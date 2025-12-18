from ..models import *
from django.apps import apps
from django.contrib.contenttypes.models import ContentType

#"""根据科目dataset获取习题模型"""
def get_exercise_model(subject_dataset):
    model_map = {
        '数学': 'MathExercise',
        '语文': 'ChineseExercise',
        '英语': 'EnglishExercise',
    }

    Exercise = model_map.get(subject_dataset)
    if not Exercise:
        return None

    try:
        return apps.get_model('learning', Exercise)
    except LookupError:
        return None

#"""根据科目dataset和习题ID获取习题"""
def get_exercise_by_id(subject_dataset, exercise_id):
    """根据科目和ID获取习题"""
    Exercise = get_exercise_model(subject_dataset)
    if not Exercise:
        return None

    try:
        return Exercise.objects.get(id=exercise_id)
    except Exercise.DoesNotExist:
        return None



