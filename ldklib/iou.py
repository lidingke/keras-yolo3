import cv2
import numpy as np
def calcIOU(a_xmin, a_ymin, a_xmax, a_ymax, b_xmin, b_ymin, b_xmax, b_ymax):
    a_w,a_h,b_w,b_h = a_xmax-a_xmin, a_ymax-a_ymin, b_xmax-b_xmin, b_ymax-b_ymin,
    a_core_x,a_core_y,b_core_x,b_core_y=(a_xmin+a_xmax)//2,(a_ymin+a_ymax)//2,\
                                        (b_xmin+b_xmax)//2,(b_ymin+b_ymax)//2,
#     print(a_w,a_h,b_w,b_h)
#     print(a_core_x,a_core_y,b_core_x,b_core_y)
    if not ((abs(a_core_x - b_core_x) < ((a_w + b_w) / 2.0)) and\
       (abs(a_core_y - b_core_y) < ((a_h + b_h) / 2.0))):
        return 0,(0,0,0,0)
    lu_x_inter = max(a_xmin, b_xmin)
    lu_y_inter = min(a_ymax, b_ymax) #((one_y + (one_h / 2.0)), (two_y + (two_h / 2.0)))

    rd_x_inter = min(a_xmax, b_xmax)   #((one_x + (one_w / 2.0)), (two_x + (two_w / 2.0)))
    rd_y_inter = max(a_ymin, b_ymin) #((one_y - (one_h / 2.0)), (two_y - (two_h / 2.0)))

    inter_w = abs(rd_x_inter - lu_x_inter)
    inter_h = abs(lu_y_inter - rd_y_inter)

    inter_square = inter_w * inter_h
    union_square = (a_w * a_h) + (b_w * b_h) - inter_square

    iou = inter_square / union_square * 1.0
    return iou,(lu_x_inter,lu_y_inter,rd_x_inter,rd_y_inter)


def cut_rects(rects,boundary,h_thresh=10):
    results = []
    for r in rects:
        label,xmin,ymin,xmax,ymax = r
        iou,ibox = calcIOU(xmin,ymin,xmax,ymax,*boundary)
        if iou>0 and abs(ibox[3]-ibox[1]) > h_thresh:
            _ = (label,*ibox)
            results.append(_)
    return results

def main():
    img = np.zeros((1500,2000,3))
    r1 = (1692,269,1799,301)
    r2 = (1756,265,1785,277)
    cv2.rectangle(img, (r1[0],r1[1]), (r1[2],r1[3]), (255, 0, 0), 2)
    cv2.rectangle(img, (r2[0],r2[1]), (r2[2],r2[3]), (255, 0, 0), 2)
    c,box = calcIOU(*r1,*r2)
    if c > 0:
        cv2.rectangle(img, (box[0],box[1]), (box[2],box[3]), (0, 255, 0), -1)
    print(c,box)
    r1 = (1637, 1057, 1685, 1084)
    r2 = ( 1670, 1047, 1681, 1064)
    cv2.rectangle(img, (r1[0],r1[1]), (r1[2],r1[3]), (255, 0, 0), 2)
    cv2.rectangle(img, (r2[0],r2[1]), (r2[2],r2[3]), (255, 0, 0), 2)
    c,box = calcIOU(*r1,*r2)
    if c > 0:
        cv2.rectangle(img, (box[0],box[1]), (box[2],box[3]), (0, 255, 0), -1)
    print(c,box)
    r1 = (1781,1057,1790,1064)
    r2 = (1756,1069,1772,1087)
    cv2.rectangle(img, (r1[0],r1[1]), (r1[2],r1[3]), (255, 0, 0), 2)
    cv2.rectangle(img, (r2[0],r2[1]), (r2[2],r2[3]), (255, 0, 0), 2)
    c,box = calcIOU(*r1,*r2)
    if c > 0:
        cv2.rectangle(img, (box[0],box[1]), (box[2],box[3]), (0, 255, 0), -1)
    print(c,box)
    plt.imshow(img[1000:1300,1500:1800])

if __name__ == '__main__':
    main()