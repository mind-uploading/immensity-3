import cv2
# 如果是调用笔记本自带的摄像头，参数就为0；如果是外置USB摄像头，参数就为1。
cap = cv2.VideoCapture(0)
# 设置一下摄像头窗口的宽高，参数3代表宽度
cap.set(3, 640)
# 参数4代表的高度
cap.set(4, 480)
# 参数10代表亮度
cap.set(10, 100)
while True:

    success, img = cap.read()
    frame = cv2.flip(img, 1)
    # show a frame
    cv2.imshow('frame', frame)
    # 调整拍拍摄角度，确认后按‘q’键退出后，释放摄像头资源
    if cv2.waitKey(1) & 0xFF == ord('q'):
        # 设置拍摄图像的保存路径，不设置默认为当前目录
        cv2.imwrite("test.png", frame)
        break
cap.release()
cv2.destroyAllWindows()


