from django.core.management.base import BaseCommand
from scipy.io import arff
import pandas as pd
from dashboard.models import FordATest

class Command(BaseCommand):
    help = 'Load ARFF data into the database'

    def handle(self, *args, **kwargs):
        file_path = 'dashboard/management/commands/FordA_TEST.arff'  # ARFF 파일 경로
        data, meta = arff.loadarff(file_path)
        df = pd.DataFrame(data)

        # 데이터 삽입
        for _, row in df.iterrows():
            attributes = {f'att{i+1}': row[f'att{i+1}'] for i in range(500)}
            attributes['target'] = int(row['target'].decode('utf-8'))

            FordATest.objects.create(**attributes)
        
        self.stdout.write(self.style.SUCCESS('Successfully loaded ARFF data'))
