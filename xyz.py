import cv2
import json

img = cv2.imread("card.jpg")

points = {}

order = [
    "name_first",
    "name_rest",
    "street",
    "address_rest",
    "nid"
]

i = 0

def click(event, x, y, flags, param):
    global i

    if event == cv2.EVENT_LBUTTONDOWN:

        if i >= len(order):
            return

        key = order[i]

        points[key] = [x, y]

        print(f"{key}: ({x}, {y})")

        cv2.circle(img, (x, y), 5, (0, 0, 255), -1)

        cv2.putText(
            img,
            key,
            (x + 10, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 0, 255),
            2
        )

        cv2.imshow("Template", img)

        i += 1

        if i == len(order):

            with open("config.json", "w", encoding="utf-8") as f:
                json.dump(points, f, ensure_ascii=False, indent=4)

            print("\nSaved config.json")
            print(json.dumps(points, ensure_ascii=False, indent=4))

cv2.imshow("Template", img)
cv2.setMouseCallback("Template", click)

print("Click in this order:")
for j, item in enumerate(order, 1):
    print(f"{j}. {item}")

cv2.waitKey(0)
cv2.destroyAllWindows()