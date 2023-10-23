import os
import re
from flask import Flask, request, jsonify
from PIL import Image
from ultralytics import YOLO
from ast import Break
from math import fabs

app = Flask(__name__)
model = YOLO('best_956_239.pt')

def code_to_number(code):
    if code.endswith('w') and code[:-1].isdigit() and 1 <= int(code[:-1]) <= 9:
        return int(code[:-1])
    elif code.endswith('d') and code[:-1].isdigit() and 1 <= int(code[:-1]) <= 9:
        return int(code[:-1]) + 9
    elif code.endswith('t') and code[:-1].isdigit() and 1 <= int(code[:-1]) <= 9:
        return int(code[:-1]) + 18
    elif code == 'e':
        return 28
    elif code == 'w':
        return 29
    elif code == 's':
        return 30
    elif code == 'n':
        return 31
    elif code == 'c':
        return 32
    elif code == 'f':
        return 33
    elif code == 'b':
        return 34
def number_to_mahjong(number):
    if 1 <= number <= 9:
        return f"{number}萬"
    elif 10 <= number <= 18:
        return f"{number-9}筒"
    elif 19 <= number <= 27:
        return f"{number-18}條"
    elif number == 28:
        return "東"
    elif number == 29:
        return "西"
    elif number == 30:
        return "南"
    elif number == 31:
        return "北"
    elif number == 32:
        return "中"
    elif number == 33:
        return "發"
    elif number == 34:
        return "白"
    else:
        return "未知"


@app.route("/upload", methods=["POST"])
def upload():
    has_1w = False
    has_2w = False
    has_3w = False
    has_4w = False
    has_5w = False
    has_6w = False
    has_7w = False
    has_8w = False
    has_9w = False
    has_1d = False
    has_2d = False
    has_3d = False
    has_4d = False
    has_5d = False
    has_6d = False
    has_7d = False
    has_8d = False
    has_9d = False
    has_1t = False
    has_2t = False
    has_3t = False
    has_4t = False
    has_5t = False
    has_6t = False
    has_7t = False
    has_8t = False
    has_9t = False
    has_wan = False
    has_tong= False
    has_tiao = False
    zz = False
    has_zhong_triplet = False
    has_bai_triplet = False
    has_fa_triplet = False
    has_zhong_pair = False
    has_fa_pair = False
    has_bai_pair = False
    has_east_triplet = False
    has_west_triplet = False
    has_south_triplet = False
    has_north_triplet = False
    has_east_pair = False
    has_west_pair = False
    has_south_pair = False
    has_north_pair = False

    names=['c', '1t', '2t', '3t', '4t', '5t', '6t', '7t', '8t', '9t', 'f', '1d', '2d', '3d', '4d', '5d', '6d', '7d', '8d', '9d', 'b', '1w', '2w', '3w', '4w', '5w', '6w', '7w', '8w', '9w', 'e', 'w', 's', 'n']
    file = request.files["image"]
    img = Image.open(file.stream)
    results = model.predict(source=img)
    ret = []
    for result in results:
        boxes = result.boxes.cpu().numpy()
        for i, box in enumerate(boxes):
            #ret.append(result.names[int(box.cls)])
            ret.append(names[int(box.cls)])
    print(ret)
    codes = ret
    numbers = []

    for code in codes:
        numbers.append(code_to_number(code))
        numbers = sorted(numbers) 


    car = 0 
    i = 0
    pair = 0
    while i < len(numbers) - 2:
       if numbers[i] == numbers[i + 1] :
           if numbers[i] == 1:
               if numbers[i+1] == numbers [i+2]:
                    car += 1
                    has_1w = True
                    del numbers[i:i+3]
                    continue
               else:
                        
                    i += 1
                    continue
           elif numbers[i] == 2:
               if numbers[i+1] == numbers [i+2]:
                        has_2w = True
                        del numbers[i:i+3]
                        car += 1
                        continue
               else:
                   i += 1 
                   continue
           elif numbers[i] == 3:
                if numbers[i+1] == numbers [i+2]:
                        has_3w = True
                        del numbers[i:i+3]
                        car += 1
                        continue
                else:
                        i += 1 
                        continue
           elif numbers[i] == 4:
                if numbers[i+1] == numbers [i+2]:
                        has_4w = True
                        del numbers[i:i+3]
                        car += 1
                        continue
                else:
                        i += 1 
                        continue
           elif numbers[i] == 5:
                if numbers[i+1] == numbers [i+2]:
                        has_5w = True
                        del numbers[i:i+3]
                        car += 1
                        continue
                else:
                        i += 1 
                        continue
           elif numbers[i] == 6:
                if numbers[i+1] == numbers [i+2]:
                        has_6w = True
                        del numbers[i:i+3]
                        car += 1
                        continue
                else:
                        i += 1 
                        continue
           elif numbers[i] == 7:
                if numbers[i+1] == numbers [i+2]:
                        has_7w = True
                        del numbers[i:i+3]
                        car += 1
                        continue
                else:
                        i += 1 
                        continue
           elif numbers[i] == 8:
                if numbers[i+1] == numbers [i+2]:
                        has_8w = True
                        del numbers[i:i+3]
                        car += 1
                        continue
                else:
                        i += 1 
                        continue
           elif numbers[i] == 9:
                if numbers[i+1] == numbers [i+2]:
                        has_9w = True
                        del numbers[i:i+3]
                        car += 1
                        continue
                else:
                        i += 1 
                        continue
           elif numbers[i] == 10:
                if numbers[i+1] == numbers [i+2]:
                        has_1d = True
                        del numbers[i:i+3]
                        car += 1
                        continue
                else:
                        i += 1 
                        continue
           elif numbers[i] == 11:
                if numbers[i+1] == numbers [i+2]:
                        has_2d = True
                        del numbers[i:i+3]
                        car += 1
                        continue
                else:
                        i += 1 
                        continue
           elif numbers[i] == 12:
                if numbers[i+1] == numbers [i+2]:
                        has_3d = True
                        del numbers[i:i+3]
                        car += 1
                        continue
                else:
                        i += 1 
                        continue
           elif numbers[i] == 13:
                if numbers[i+1] == numbers [i+2]:
                        has_4d = True
                        del numbers[i:i+3]
                        car += 1
                        continue
                else:
                        i += 1 
                        continue
           elif numbers[i] == 14:
                if numbers[i+1] == numbers [i+2]:
                        has_5d = True
                        del numbers[i:i+3]
                        car += 1
                        continue
                else:
                        i += 1 
                        continue
           elif numbers[i] == 15:
                if numbers[i+1] == numbers [i+2]:
                        has_6d = True
                        del numbers[i:i+3]
                        car += 1
                        continue
                else:
                        i += 1 
                        continue
           elif numbers[i] == 16:
                if numbers[i+1] == numbers [i+2]:
                        has_7d = True
                        del numbers[i:i+3]
                        car += 1
                        continue
                else:
                        i += 1 
                        continue
           elif numbers[i] == 17:
                if numbers[i+1] == numbers [i+2]:
                        has_8d = True
                        del numbers[i:i+3]
                        car += 1
                        continue
                else:
                        i += 1 
                        continue
           elif numbers[i] == 18:
                if numbers[i+1] == numbers [i+2]:
                        has_9d = True
                        del numbers[i:i+3]
                        car += 1
                        continue
                else:
                        i += 1 
                        continue
           elif numbers[i] == 19:
                if numbers[i+1] == numbers [i+2]:
                        has_1t = True
                        del numbers[i:i+3]
                        car += 1
                        continue
                else:
                        i += 1 
                        continue
           elif numbers[i] == 20:
                if numbers[i+1] == numbers [i+2]:
                        has_2t = True
                        del numbers[i:i+3]
                        car += 1
                        continue
                else:
                        i += 1 
                        continue
           elif numbers[i] == 21:
                if numbers[i+1] == numbers [i+2]:
                        has_3t = True
                        del numbers[i:i+3]
                        car += 1
                        continue
                else:
                        i += 1 
                        continue
           elif numbers[i] == 22:
                if numbers[i+1] == numbers [i+2]:
                        has_4t = True
                        del numbers[i:i+3]
                        car += 1
                        continue
                else:
                        i += 1 
                        continue
           elif numbers[i] == 23:
                if numbers[i+1] == numbers [i+2]:
                        has_5t = True
                        del numbers[i:i+3]
                        car += 1
                        continue
                else:
                        i += 1 
                        continue
           elif numbers[i] == 24:
                if numbers[i+1] == numbers [i+2]:
                        has_6t = True
                        del numbers[i:i+3]
                        car += 1
                        continue
                else:
                        i += 1 
                        continue
           elif numbers[i] == 25:
                if numbers[i+1] == numbers [i+2]:
                        has_7t = True
                        del numbers[i:i+3]
                        car += 1
                        continue
                else:
                        i += 1 
                        continue
           elif numbers[i] == 26:
                if numbers[i+1] == numbers [i+2]:
                        has_8t = True
                        del numbers[i:i+3]
                        car += 1
                        continue
                else:
                        i += 1 
                        continue
           elif numbers[i] == 27:
                if numbers[i+1] == numbers [i+2]:
                        has_9t = True
                        del numbers[i:i+3]
                        car += 1
                        continue
                else:
                        i += 1 
                        continue
           elif numbers[i] == 28:
                if numbers[i+1] == numbers [i+2]:
                        has_east_triplet = True
                        del numbers[i:i+3]
                        car += 1
                        continue
                else:
                        has_east_pair = True
                        i += 2
                        continue
           elif numbers[i] == 29:
                if numbers[i+1] == numbers [i+2]:
                        has_west_triplet = True
                        del numbers[i:i+3]
                        car += 1
                        continue
                else:
                        has_west_pair = True
                        i += 2 
                        continue
           elif numbers[i] == 30:
                if numbers[i+1] == numbers [i+2]:
                        has_south_triplet = True
                        del numbers[i:i+3]
                        car += 1
                        continue
                else:
                        has_south_pair = True
                        i += 2 
                        continue
           elif numbers[i] == 31:
                if numbers[i+1] == numbers [i+2]:
                        has_north_pair = True
                        del numbers[i:i+3]
                        car += 1
                        continue
                else:
                        has_north_pair = True
                        i += 2 
                        continue
           elif numbers[i] == 32:
                if numbers[i+1] == numbers [i+2]:
                        has_zhong_triplet = True
                        car += 1
                        
                        del numbers[i:i+3]
                        continue
                else:
                        has_zhong_pair = True
                        i += 2 
                        continue
           elif numbers[i] == 33:
                if numbers[i+1] == numbers [i+2]:
                        has_fa_triplet = True
                        del numbers[i:i+3]
                        car += 1
                        continue
                else:
                        has_fa_pair = True
                        i += 2 
                        continue
           elif numbers[i] == 34:
                if numbers[i+1] == numbers [i+2]:
                        has_bai_triplet = True
                        del numbers[i:i+3]
                        car += 1
                        continue
                else:
                        has_bai_pair =True
                        i += 2 
                        continue
            
            
           else :
                i +=1
                
       else :
        if numbers[i] == numbers[i + 1] -1:
            if numbers[i+1] == numbers[i+2]-1 :
                del numbers[i :i+3]
                car +=1
                continue
            elif numbers[i+1] == numbers[i+3]-1:
                del numbers[i]
                del numbers[i]
                del numbers[i+1]
                car +=1
                continue
                   
        else:
                   i+=1
    if numbers[0] == numbers[1] : 
        pair += 1


    card_Type = "0"
    tai = 0



    if has_bai_triplet and has_fa_triplet and has_zhong_triplet and car == 5 and pair ==1:
        card_Type += "大三元"
        tai += 8
    
    elif (has_bai_pair and has_fa_triplet ==False and has_zhong_triplet == False and car == 5 and pair ==1) or \
    (has_bai_triplet ==False and has_fa_pair == False and has_zhong_triplet and car == 5 and pair ==1) or \
    (has_bai_triplet == False and has_fa_triplet and has_zhong_pair==False and car == 5 and pair ==1):
        card_Type += "三元刻"
        tai += 1
    elif (has_bai_pair and has_fa_triplet and has_zhong_triplet == False  and car == 5 and pair ==1) or \
    (has_bai_triplet and has_fa_pair == False and has_zhong_triplet and car == 5 and pair ==1) or \
    (has_bai_triplet == False and has_fa_triplet and has_zhong_pair and car == 5  and pair ==1):
        card_Type += "小三元"
        tai += 4

    if has_east_triplet and has_west_triplet and has_south_triplet and has_north_triplet and car == 5 and pair ==1:
        card_Type += "大四喜"
        tai += 16
    elif (has_east_pair and has_west_triplet and has_south_triplet and has_north_triplet and car == 5 and pair ==1) or\
     (has_east_triplet and has_west_pair and has_south_triplet and has_north_triplet and car == 5 and pair ==1) or\
     (has_east_triplet and has_west_triplet and has_south_pair and has_north_triplet and car == 5 and pair ==1) or\
     (has_east_triplet and has_west_triplet and has_south_triplet and has_north_pair and car == 5 and pair ==1):
       card_Type += "小四喜"
       tai += 8

    if (has_1w or has_2w or has_3w or has_4w or has_5w or has_6w or has_7w or has_8w or has_9w) :
        has_wan = True
    if (has_1t or has_2t or has_3t or has_4t or has_5t or has_6t or has_7t or has_8t or has_9t) :
        has_tong = True
    if (has_1d or has_2d or has_3d or has_4d or has_5d or has_6d or has_7d or has_8d or has_9d) :
        has_tiao = True


    if (has_north_triplet or has_north_pair or has_east_pair or has_west_pair or has_south_pair or  has_east_triplet or has_west_triplet or has_west_triplet):
        zz = True
    if (has_fa_pair or has_bai_pair or has_fa_triplet or has_zhong_pair or has_zhong_triplet or has_bai_triplet):
       zz = True
    if ( has_wan and not has_tong and not has_tiao and  car ==5 and pair ==1 and zz == True) or \
   (not has_wan and has_tong and not has_tiao and  car ==5 and pair ==1  and zz == True) or \
   (not has_wan and not has_tong and  has_tiao and  car ==5 and pair ==1 and zz == True):
      card_Type += "混一色"
      tai += 4
    elif (has_wan and not has_tong and not has_tiao and not car ==5 and pair ==1) or \
     (not has_wan and has_tong and not has_tiao and not car ==5 and pair ==1) or \
     (not has_wan and not has_tong and has_tiao and not car ==5 and pair ==1):
      card_Type += "清一色"
      tai += 8
    elif not has_wan and not has_tong and not has_tiao and car ==5:
      card_Type += "字一色"
      tai += 16

    if car == 5:
          response_data = {
                "msg": "success",
                "result": ",".join(ret),
                "hu_info": {
                      "card_Type": card_Type,
                      "tai": tai
                }
        }
          print("這是一個胡牌的手牌！")
          print(tai, "台數")
    else:
          response_data = {
                "msg": "success",
                "result": ",".join(ret),
                "hu_info": {
                      "card_Type": "0",  # 未胡牌
                      "tai": 0
                }
        }
          print("這不是一個胡牌的手牌。")

    print(response_data)
    return jsonify(response_data)


if __name__ == '__main__':
    ssl_cert = 'C:\Openssl\certificate.crt' 
    ssl_key = 'C:\Openssl\private_key.key'   
    context = (ssl_cert, ssl_key) 
    app.run(host='0.0.0.0', port=5000, ssl_context=context, debug=True)
