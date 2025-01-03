import cv2

cap = cv2.VideoCapture("videoplayback.mp4")
timer = 10000

while True:
    success, img = cap.read()
    if not success:
        print("The video ended or the image was not captured.")
        break
    
    outfile = 'output/img_%s.jpg' % (timer)
    timer += 1
    print(outfile)
    
    cv2.imwrite(outfile, img)
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('t'):
        break

cap.release()
cv2.destroyAllWindows()
