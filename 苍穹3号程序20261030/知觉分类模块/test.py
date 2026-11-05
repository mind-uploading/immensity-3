#1.引入cv2
import cv2

#2.主函数
if __name__ == '__main__':
    print(0)
    #3.打开笔记本摄像头
    cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    
    assert cap.isOpened(), 'Cannot capture source' #摄像头没有正常打开则报错
    print(1)
    #4.摄像头能打开则获取图像帧，显示图像
    while cap.isOpened():
        #read()函数返回两个参数,第一个为参数为bool值，表示是否获取到图像，
        #第二个参数为当前帧图像
        ret, frame = cap.read()
        # 将获取到的当前帧水品翻转
        # 第二个参数：  1 表示水平翻转; 0 表示垂直翻转;  小于0 表示水平垂直翻转
        frame = cv2.flip(frame,1)
        # 设置拍摄图像的保存路径，不设置默认为当前目录
        cv2.imwrite("pic.png", frame)
       
        cv2.imshow('mycreame',frame)  #显示当前帧
        if ( cv2.waitKey(30)  == 27 ):   #按下Esc键则退出    waitKey()方法表示等待键盘输入，单位为毫秒
            break
    #5.关闭所有窗口
    cv2.destroyAllWindows()