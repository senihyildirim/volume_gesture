import cv2
import mediapipe as mp
import subprocess


def detect_hand_gesture(image, x1, y1, x2, y2):
    # Görüntünün boyutlarını al
    frame_height, frame_width, _ = image.shape

    # RGB formata dönüştür
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Elleri tespit et
    output = my_hands.process(rgb_image)
    hands = output.multi_hand_landmarks

    # Eğer eller tespit edildiyse
    if hands:
        for hand in hands:
            # Ellerin üzerine anahtar noktaları çiz
            drawing_utils.draw_landmarks(image, hand)
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)
                if id == 8:
                    # İlk anahtar noktaya bir daire çiz ve koordinatları güncelle
                    cv2.circle(img=image, center=(x, y), radius=8, color=(0, 255, 255), thickness=3)
                    x1 = x
                    y1 = y
                if id == 4:
                    # İkinci anahtar noktaya bir daire çiz ve koordinatları güncelle
                    cv2.circle(img=image, center=(x, y), radius=8, color=(0, 0, 255), thickness=3)
                    x2 = x
                    y2 = y
                cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 5)
        # İki anahtar nokta arasındaki mesafeyi ölç
        dist = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

        # Mesafeye göre ses kontrolü yap
        if dist > 50:
            subprocess.run(
                ["osascript", "-e", "set volume output volume (output volume of (get volume settings) + 10)"])
        else:
            subprocess.run(
                ["osascript", "-e", "set volume output volume (output volume of (get volume settings) - 10)"])

    return image, x1, y1, x2, y2


# Webcam'ı başlat
webcam = cv2.VideoCapture(0)
my_hands = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils

x1 = x2 = y1 = y2 = 0

while True:
    # Webcam'dan görüntü al
    _, image = webcam.read()

    # Elleri tespit et ve ses kontrolü yap
    image, x1, y1, x2, y2 = detect_hand_gesture(image, x1, y1, x2, y2)

    # Görüntüyü ekranda göster
    cv2.imshow("Hand Volume Control", image)

    # Klavyeden herhangi bir tuşa basılmasını bekle
    key = cv2.waitKey(10)
    if key == 27:  # 27 ASCII kodu escape tuşunu temsil eder
        break

# Webcam'ı serbest bırak ve pencereleri kapat
webcam.release()
cv2.destroyAllWindows()
