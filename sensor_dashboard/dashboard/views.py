from django.http import JsonResponse
from django.shortcuts import render
from dashboard.models import FordATest
from tensorflow.keras.models import load_model
import pandas as pd
import numpy as np

# 모델 로드
model = load_model('dashboard/my_classification_model.keras')

# 전역 변수로 현재 인덱스를 관리
current_index = 0

def reshape_to_image(data):
    images = []
    for i in range(len(data)):
        row = data[i]
        reshaped_image = row.reshape(20, 25, 1)  # 20x25로 재배열하고 채널 추가
        images.append(reshaped_image)
    return np.array(images)

def dashboard_view(request):
    return render(request, 'dashboard/index.html')

def process_data(request):
    global current_index

    # 데이터베이스에서 현재 인덱스에 해당하는 행을 가져옵니다.
    data = FordATest.objects.all()

    if current_index >= len(data):
        return JsonResponse({"status": "No more data"})

    current_data = data[current_index]

    # 다음 호출 시 다음 행을 가져오도록 인덱스 증가
    current_index += 1

    # 모델의 필드 이름을 동적으로 가져옵니다.
    fields = [f.name for f in FordATest._meta.fields if f.name.startswith('att')]

    # 데이터를 모델에 넣을 수 있도록 DataFrame으로 변환합니다.
    df = pd.DataFrame([{field: getattr(current_data, field) for field in fields}])

    # 데이터의 형태를 모델이 기대하는 이미지 형식(20x25x1)으로 변환합니다.
    reshaped_input = reshape_to_image(df.values)

    # 모델 예측
    prediction = model.predict(reshaped_input)
    prediction_value = float(prediction[0][0])  # float32를 float으로 변환

    # 예측값이 0.5를 넘으면 양품, 그렇지 않으면 불량품으로 설정
    quality = "양품" if prediction_value > 0.5 else "불량품"

    # 예측 결과와 품질 상태를 반환
    return JsonResponse({
        'status': 'Success',
        'prediction': prediction_value,
        'quality': quality,
        'sensorData': {
            'sensor1': float(df.iloc[0, 0]),  # 예: att1 값 반환
            'sensor2': float(df.iloc[0, 1]),  # 예: att2 값 반환
            'sensor3': float(df.iloc[0, 2]),  # 예: att3 값 반환
            'sensor4': float(df.iloc[0, 3])   # 예: att4 값 반환
        }
    })
