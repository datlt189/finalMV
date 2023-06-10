import cv2
import utlis

#------------------------------------------------------------------------
webcam = True # Chương trình sẽ sử dụng webcam để lấy hình ảnh đầu vào.   
cap = cv2.VideoCapture(0) # Lấy 1 khung hình từ video webcam
# Cấu hình các thông số của thiết bị đầu vào video
# 10 là mã chỉ định thuộc tính cv2.CAP_PROP_BRIGHTNESS: điều chỉnh độ sáng, và 160 là giá trị được đặt cho thuộc tính này
cap.set(10,160)
cap.set(3,1920) # Chiều rộng khung hình
cap.set(4,1080) # Chiều cao khung hình
scale = 3
wP = 210 *scale # Chiều rộng của ảnh đích sau khi wrap và scale
hP= 297 *scale # Chiều cao của ảnh đích sau khi wrap và scale
#------------------------------------------------------------------------

#------------------------------------------------------------------------
# Xử lý hình ảnh từ webcam
#------------------------------------------------------------------------
while True:
    if webcam:success,img = cap.read() # Đọc hình ảnh từ webcam
    # Gọi hàm con tìm đường viền
    imgContours , conts = utlis.getContours(img,minArea=50000,filter=4)
    # Lấy đường viền lớn nhất nếu đường viền được tìm thấy
    if len(conts) != 0:
        biggest = conts[0][2]
        # Thực hiện biến đổi, chỉnh lại kích thước và góc nhìn của ảnh 
        # sao cho đường viền lớn nhất trở thành một hình chữ nhật có kích thước cố định (wP và hP)
        imgWarp = utlis.warpImg(img, biggest, wP,hP)
        # Thực hiện tìm đường viền của đối tượng vật thể dựa trên ảnh đã xử lý thay đổi góc nhìn
        imgContours2, conts2 = utlis.getContours(imgWarp,
                                                 minArea=2000, filter=4,
                                                 cThr=[50,50],draw = False)
        
        # Tiếp tục xử lý nếu đường viền được tìm thấy
        if len(conts) != 0:
            # Mỗi đường viền được lưu trữ trong biến obj
            for obj in conts2:
                # Vẽ đường viền lên ảnh imgContours2 bằng màu xanh lá cây.
                cv2.polylines(imgContours2,[obj[2]],True,(0,255,0),2)
                # Sắp xếp lại các điểm của đường viền obj[2] theo thứ tự đúng (theo góc nhìn)
                nPoints = utlis.reorder(obj[2])
                # Tính toán chiều dài, chiều rộng của đối tượng dựa trên khoảng cách giữa hai điểm đầu tiên và thứ hai trong nPoints
                # Khoảng cách này được chia cho scale để đưa về đơn vị pixel ban đầu, 
                # sau đó chia thêm cho 10 để chuyển đổi sang đơn vị cm. 
                # Kết quả là một số thập phân được làm tròn đến 1 chữ số sau dấu phẩy.
                nW = round((utlis.findDis(nPoints[0][0]//scale,nPoints[1][0]//scale)/10),1)
                nH = round((utlis.findDis(nPoints[0][0]//scale,nPoints[2][0]//scale)/10),1)
                # Vẽ mũi tên chỉ ra chiều dài và chiều rộng trên ảnh imgContours2
                cv2.arrowedLine(imgContours2, (nPoints[0][0][0], nPoints[0][0][1]), (nPoints[1][0][0], nPoints[1][0][1]),
                                (255, 0, 255), 3, 8, 0, 0.05)
                cv2.arrowedLine(imgContours2, (nPoints[0][0][0], nPoints[0][0][1]), (nPoints[2][0][0], nPoints[2][0][1]),
                                (255, 0, 255), 3, 8, 0, 0.05)
                x, y, w, h = obj[3]
                # Thêm kích thước đã tính toán lên các mũi tên chỉ chiều dài chiều rộng
                cv2.putText(imgContours2, '{}cm'.format(nW), (x + 30, y - 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5,
                            (255, 0, 255), 2)
                cv2.putText(imgContours2, '{}cm'.format(nH), (x - 70, y + h // 2), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5,
                            (255, 0, 255), 2)\
        # Hiển thị hình ảnh kết quả
        cv2.imshow('A4', imgContours2)
    # Hiển thị ảnh gốc
    # Thay đổi kích thước ảnh để nó phù hợp với kích thước hiển thị trên màn hình
    img = cv2.resize(img,(0,0),None,0.5,0.5)
    cv2.imshow('Original',img)
    # Nhấn A hoặc a để kết thúc chương trình
    if cv2.waitKey(33) == ord('a') or cv2.waitKey(33) == ord('A'):
        break