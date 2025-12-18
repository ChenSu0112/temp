# diagnose_tables.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edu_system.settings')
django.setup()

from django.db import connection
from django.apps import apps
from django.db.migrations.executor import MigrationExecutor


def diagnose_issue():
    print("=" * 80)
    print("数据库诊断报告")
    print("=" * 80)

    # 1. 检查Django认为的表结构
    print("\n1. Django认为的模型字段:")
    for model_name in ['MathExercise', 'ChineseExercise', 'EnglishExercise']:
        model = apps.get_model('learning', model_name)
        print(f"\n{model_name}:")
        for field in model._meta.fields:
            print(f"  {field.name}: {field.__class__.__name__}")

    # 2. 检查实际数据库表结构
    print("\n2. 实际数据库表结构:")
    tables = ['learning_math_exercise', 'learning_chinese_exercise', 'learning_english_exercise']

    for table in tables:
        print(f"\n{table}:")
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"DESC {table}")
                for row in cursor.fetchall():
                    print(f"  {row[0]:20} {row[1]:15} {row[2]}")
        except Exception as e:
            print(f"  错误: {e}")

    # 3. 检查迁移状态
    print("\n3. 迁移状态检查:")
    try:
        from django.db.migrations.recorder import MigrationRecorder
        recorder = MigrationRecorder(connection)
        applied = recorder.applied_migrations()
        print(f"已应用的迁移数量: {len(applied)}")

        # 查找learning应用的迁移
        learning_migrations = [m for m in applied if m[0] == 'learning']
        print(f"learning应用的迁移: {len(learning_migrations)}个")

        # 显示最近的5个迁移
        print("最近5个迁移:")
        for migration in list(learning_migrations)[-5:]:
            print(f"  {migration[1]}")
    except Exception as e:
        print(f"检查迁移状态出错: {e}")

    # 4. 检查是否有数据
    print("\n4. 表数据统计:")
    for table in tables:
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"{table}: {count} 条记录")
        except Exception as e:
            print(f"{table}: 错误 - {e}")


if __name__ == "__main__":
    diagnose_issue()