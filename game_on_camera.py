import cvzone
import cv2
import random
from cvzone.HandTrackingModule import HandDetector

# Setup OpenCV capture and window size
capture = cv2.VideoCapture(0)
capture.set(3, 1280)
capture.set(4, 720)

score = 0
gameOver = False
Restart = False
WIDTH, HEIGHT = 1280, 720
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60
FRUIT_SIZE = 150
BOMB_SIZE = 150
GRAVITY = 0.35

# Load images
fruit_types = ['apple.png', 'mango.png', 'orange.png', 'pearl.png', 'pineapple.png', 'strawberry.png', 'watermelon.png']
bomb_image = cv2.imread('bomb.png', cv2.IMREAD_UNCHANGED)
bomb_image = cv2.resize(bomb_image, (BOMB_SIZE, BOMB_SIZE))

# Fruit and bomb lists
fruits = []
bombs = []

detect = HandDetector(detectionCon=0.8, maxHands=3)

def update(mainIMG, pointIndex):
    global score, gameOver
    if(score == 40):
        cvzone.putTextRect(mainIMG, "You Win", [50, 350], scale=8, thickness=4, colorT=(255, 255, 255), colorR=(0, 255, 0), offset=20)
        cvzone.putTextRect(mainIMG, f'Your Score: {score}', [250, 500], scale=8, thickness=5, colorT=(255, 255, 255), colorR=(0, 255, 0), offset=20)
        gameOver = True
    elif gameOver:
        cvzone.putTextRect(mainIMG, "Game Over", [50, 350], scale=8, thickness=4, colorT=(255, 255, 255), colorR=(0, 0, 255), offset=20)
        cvzone.putTextRect(mainIMG, f'Your Score: {score}', [250, 500], scale=8, thickness=5, colorT=(255, 255, 255), colorR=(0, 0, 255), offset=20)
    else:
        # Add new fruits and bombs
        if score < 10:
            if random.random() < 0.01:
                add_fruit()
            if random.random() < 0.004:
                add_bomb()
        elif score < 20:
            if random.random() < 0.015:
                add_fruit()
            if random.random() < 0.005:
                add_bomb()
        else:
            if random.random() < 0.025:
                add_fruit()
            if random.random() < 0.01:
                add_bomb()
        
        # Update fruits
        for fruit in fruits[:]:
            fruit['vy'] += GRAVITY
            fruit['x'] += int(fruit['vx'])
            fruit['y'] += int(fruit['vy'])
            if fruit['y'] > HEIGHT or fruit['x'] < 0 or fruit['x'] > WIDTH:
                fruits.remove(fruit)
            else:
                mainIMG = cvzone.overlayPNG(mainIMG, fruit['image'], (fruit['x'], fruit['y']))
        
        # Update bombs
        for bomb in bombs[:]:
            bomb['vy'] += GRAVITY
            bomb['x'] += int(bomb['vx'])
            bomb['y'] += int(bomb['vy'])
            if bomb['y'] > HEIGHT or bomb['x'] < 0 or bomb['x'] > WIDTH:
                bombs.remove(bomb)
            else:
                mainIMG = cvzone.overlayPNG(mainIMG, bomb_image, (bomb['x'], bomb['y']))
        
        # Collision check
        for fruit in fruits[:]:
            if fruit['x'] < pointIndex[0] < fruit['x'] + FRUIT_SIZE and fruit['y'] < pointIndex[1] < fruit['y'] + FRUIT_SIZE:
                fruits.remove(fruit)
                score += 1
        for bomb in bombs[:]:
            if bomb['x'] < pointIndex[0] < bomb['x'] + BOMB_SIZE and bomb['y'] < pointIndex[1] < bomb['y'] + BOMB_SIZE:
                gameOver = True

        # Display score
        cvzone.putTextRect(mainIMG, f'Your Score: {score}', [50, 80], scale=3, thickness=3, offset=10, colorT=WHITE, colorR=BLACK)
    
    return mainIMG

# Function to choose a random fruit
def choose_fruit():
    chosen_fruit = random.choice(fruit_types)
    fruit_image = cv2.imread(chosen_fruit, cv2.IMREAD_UNCHANGED)
    fruit_image = cv2.resize(fruit_image, (FRUIT_SIZE, FRUIT_SIZE))
    return fruit_image

# Function to add a fruit
def add_fruit():
    x = random.randint(0, WIDTH - FRUIT_SIZE)
    y = HEIGHT
    if x < WIDTH / 2:
        vx = random.uniform(1, 3)
    else:
        vx = random.uniform(-3, 1)  # Horizontal velocity
    vy = -random.uniform(17, 20)  # Vertical velocity
    fruit_image = choose_fruit()
    fruit_image = cv2.resize(fruit_image, (FRUIT_SIZE, FRUIT_SIZE))
    fruits.append({'x': x, 'y': y, 'vx': vx, 'vy': vy, 'image': fruit_image})

# Function to add a bomb
def add_bomb():
    x = random.randint(0, WIDTH - BOMB_SIZE)
    y = HEIGHT
    if x < WIDTH / 2:
        vx = random.uniform(1, 3)
    else:
        vx = random.uniform(-3, 1)  # Horizontal velocity
    vy = -random.uniform(17, 20)  # Vertical velocity
    bombs.append({'x': x, 'y': y, 'vx': vx, 'vy': vy})

while True:
    success, img = capture.read()  # Read a frame from the video capture
    img = cv2.flip(img, 1)  # Flip the camera horizontally
    hands, img = detect.findHands(img, flipType=False)  # Detect hands in the camera

    if hands:
        landmarkList = hands[0]['lmList']  # Get the landmark list for the detected hand
        pointIndex = landmarkList[8][0:2]  # Get the location of the index finger tip
        img = update(img, pointIndex)
    else:
        img = update(img, (0, 0))

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == ord('r'):
        gameOver = False
        score = 0  # Reset the score to 0
        fruits.clear()
        bombs.clear()
    if key == ord('q'):
        break

cv2.destroyAllWindows()
capture.release()
