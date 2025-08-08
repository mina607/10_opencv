import easyocr
import cv2

# EasyOCR 리더 생성
reader = easyocr.Reader(['ko', 'en'], gpu=False)

# 웹캠 연결
cap = cv2.VideoCapture(0)

# 신뢰도 임계값
THRESHOLD = 0.5

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # OCR 수행 (OpenCV 이미지는 BGR이므로 그대로 전달 가능)
    results = reader.readtext(frame)

    # 텍스트 인식 결과 처리
    for bbox, text, conf in results:
        if conf >= THRESHOLD:
            print(f"{text} ({conf:.2f})")
            # 좌표 정수화
            top_left = tuple(map(int, bbox[0]))
            bottom_right = tuple(map(int, bbox[2]))
            # 박스 및 텍스트 출력
            cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)
            cv2.putText(frame, text, (top_left[0], top_left[1] - 10), cv2.FONT_HERSHEY_SIMPLEX,
                        0.8, (0, 255, 0), 2)

    # 화면에 출력
    cv2.imshow("OCR Webcam", frame)

    # 종료 조건: 'q' 키 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 자원 해제
cap.release()
cv2.destroyAllWindows()