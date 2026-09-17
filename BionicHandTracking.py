import cv2
import mediapipe as mp
import serial
import time
import math


arduino = serial.Serial('COM7', 9600)
time.sleep(2)


mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)

cap = cv2.VideoCapture(0)


last_index = 0
last_middle = 180
last_ring = 0
last_pinky = 180
last_thumb = 0

first_frame = True



def get_angle(a, b, c):
    ang = math.degrees(
        math.atan2(c[1]-b[1], c[0]-b[0]) -
        math.atan2(a[1]-b[1], a[0]-b[0])
    )
    ang = abs(ang)
    if ang > 180:
        ang = 360 - ang
    return ang


def norm(x):
    return max(0, min(1, (180 - x) / 180))



def is_fist(lm):
    return (
        abs(lm[8].y - lm[5].y) < 0.06 and
        abs(lm[12].y - lm[9].y) < 0.06 and
        abs(lm[16].y - lm[13].y) < 0.06 and
        abs(lm[20].y - lm[17].y) < 0.06
    )



def is_thumbs_up(lm):
    wrist = lm[0]
    middle_mcp = lm[9]

    
    hx = middle_mcp.x - wrist.x
    hy = middle_mcp.y - wrist.y

    
    tx = lm[4].x - wrist.x
    ty = lm[4].y - wrist.y

    dot = hx * tx + hy * ty
    thumb_extended = dot < 0  

    fingers_curled = (
        lm[8].y > lm[6].y and
        lm[12].y > lm[10].y and
        lm[16].y > lm[14].y and
        lm[20].y > lm[18].y
    )

    return thumb_extended and fingers_curled



while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    result = hands.process(rgb)

    
    if first_frame:
        last_index = 0
        last_middle = 180
        last_ring = 0
        last_pinky = 180
        last_thumb = 0
        first_frame = False

    if result.multi_hand_landmarks:
        for hand in result.multi_hand_landmarks:
            lm = hand.landmark

            def pt(i):
                return (lm[i].x, lm[i].y)

           

            if is_fist(lm):
                last_index = 130
                last_middle = 90
                last_ring = 120
                last_pinky = 90
                last_thumb = 160

            elif is_thumbs_up(lm):
                last_index = 130
                last_middle = 90
                last_ring = 120
                last_pinky = 90
                last_thumb = 0

            else:
               
                index_b = norm(get_angle(pt(5), pt(6), pt(8)))
                index_raw = int(130 * index_b)

                if index_raw <= 20:
                    last_index = 0
                elif index_raw <= 60:
                    last_index = 60
                elif index_raw <= 110:
                    last_index = 100
                else:
                    last_index = 135
                    

                
                middle_b = norm(get_angle(pt(9), pt(10), pt(12)))
                middle_raw = int(180 - (90 * middle_b))

                if middle_raw >= 165:
                    last_middle = 180
                elif middle_raw >= 150:
                    last_middle = 140
                elif middle_raw >= 120:
                    last_middle = 110
                else:
                    last_middle = 90

               
                ring_b = norm(get_angle(pt(13), pt(14), pt(16)))
                ring_raw = int(150 * ring_b)

                if ring_raw <= 15:
                    last_ring = 0
                elif ring_raw <= 30:
                    last_ring = 30
                elif ring_raw <= 55:
                    last_ring = 50
                elif ring_raw <= 80:
                    last_ring = 70
                else:
                    last_ring = 120

                
                pinky_b = norm(get_angle(pt(17), pt(18), pt(20)))
                pinky_raw = int(180 - (90 * pinky_b))

                if pinky_raw >= 165:
                    last_pinky = 180
                elif pinky_raw >= 145:
                    last_pinky = 130
                elif pinky_raw >= 120:
                    last_pinky = 90
                else:
                    last_pinky = 90

                
                thumb_b = norm(get_angle(pt(1), pt(2), pt(4)))
                thumb_raw = int(180 - (120 * thumb_b))

                if thumb_raw >= 155:
                    last_thumb = 0
                elif thumb_raw >= 130:
                    last_thumb = 100
                elif thumb_raw >= 90: 
                    last_thumb = 160

    
    data = f"{last_index},{last_middle},{last_ring},{last_thumb},{last_pinky}\n"
    arduino.write(data.encode())

    
    cv2.imshow("Hand", img)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
