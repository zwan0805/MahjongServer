import os
from flask import Flask, request, jsonify
from PIL import Image
from ultralytics import YOLO

app = Flask(__name__)
model = YOLO('best_154.pt')

UPLOAD_FOLDER = 'C:\\Nodejs\\uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def code_to_number(code):
    if code.endswith('w') and code[:-1].isdigit() and 1 <= int(code[:-1]) <= 9:
        return int(code[:-1])
    elif code.endswith('d') and code[:-1].isdigit() and 1 <= int(code[:-1]) <= 9:
        return int(code[:-1]) + 10
    elif code.endswith('t') and code[:-1].isdigit() and 1 <= int(code[:-1]) <= 9:
        return int(code[:-1]) + 20
    elif code == 'e':
        return 31
    elif code == 'w':
        return 32
    elif code == 's':
        return 33
    elif code == 'n':
        return 34
    elif code == 'c':
        return 35
    elif code == 'f':
        return 36
    elif code == 'b':
        return 37

def number_to_mahjong(number):
    if 1 <= number <= 9:
        return f"{number}萬"
    elif 11 <= number <= 19:
        return f"{number-10}筒"
    elif 21 <= number <= 29:
        return f"{number-20}條"
    elif number == 31:
        return "東"
    elif number == 32:
        return "西"
    elif number == 33:
        return "南"
    elif number == 34:
        return "北"
    elif number == 35:
        return "中"
    elif number == 36:
        return "發"
    elif number == 37:
        return "白"
    else:
        return "未知"

def find_suits(numbers):
    has_wan = any(1 <= number <= 9 for number in numbers)
    has_tong = any(11 <= number <= 19 for number in numbers)
    has_tiao = any(21 <= number <= 29 for number in numbers)
    has_zi = any(31 <= number <= 37 for number in numbers)
    return has_wan, has_tong, has_tiao, has_zi



def find_sequences_and_triplets_and_pairs(numbers):
    sequences = []
    triplets = []
    pairs = []
    has_zhong_triplet = False
    has_fa_triplet = False
    has_bai_triplet = False
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
    
    i = 0
    while i < len(numbers) - 2:
        if numbers[i] == numbers[i + 1] == numbers[i + 2]:
            if numbers[i] == 31:
                has_east_triplet = True
            elif numbers[i] == 32:
                has_west_triplet = True
            elif numbers[i] == 33:
                has_south_triplet = True
            elif numbers[i] == 34:
                has_north_triplet = True
            elif numbers[i] == 36:
                has_fa_triplet = True
            elif numbers[i] == 35:
                has_zhong_triplet = True
            elif numbers[i] == 37:
                has_bai_triplet = True

            triplets.append([numbers[i], numbers[i], numbers[i]])
            numbers.pop(i)
            numbers.pop(i)
            numbers.pop(i)
        else:
            i += 1

    i=0
    while i < len(numbers) - 2:
        if numbers[i] + 1 == numbers[i + 1] and numbers[i + 1] + 1 == numbers[i + 2]:
            sequences.append([numbers[i], numbers[i + 1], numbers[i + 2]])
            numbers.pop(i)
            numbers.pop(i)
            numbers.pop(i)
        else:
            i += 1

    i = 0
    while i < len(numbers) - 1:
        if numbers[i] == numbers[i + 1]:
            if numbers[i] == 31:
                has_east_pair = True
            elif numbers[i] == 32:
                has_west_pair = True
            elif numbers[i] == 33:
                has_south_pair = True
            elif numbers[i] == 34:
                has_north_pair = True 
            elif numbers[i] == 36:  
                has_fa_pair = True
            elif numbers[i] == 35:  
                has_zhong_pair = True
            elif numbers[i] == 37:
                has_bai_pair = True

            pairs.append([numbers[i], numbers[i]])
            numbers.pop(i)
            numbers.pop(i) 
        else:
            i += 1

    return sequences, triplets, pairs, has_zhong_triplet, has_fa_triplet, has_bai_triplet, has_zhong_pair, has_fa_pair, has_bai_pair,  has_east_triplet, has_west_triplet, has_south_triplet, has_north_triplet, has_east_pair, has_west_pair, has_south_pair, has_north_pair


def is_winning_hand(sequences, triplets, pairs):
    return len(sequences) + len(triplets) >= 5 and len(pairs) == 1

def is_punpunhu(triplets):
    return len(triplets) == 5



@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["image"]
    img = Image.open(file.stream)
    results = model.predict(source=img)
    ret = []
    for result in results:
        boxes = result.boxes.cpu().numpy()
        for i, box in enumerate(boxes):
            ret.append(result.names[int(box.cls)])
            
    input_codes = input("請輸入代號，用逗號分開：")
    codes = input_codes.replace(' ', '').split(',')
    
    numbers = []
    true_numbers = []
    
    for code in codes:
        true_numbers.append(code_to_number(code))

    for code in codes:
        numbers.append(code_to_number(code))

    sequences, triplets, pairs, has_zhong_triplet, has_fa_triplet, has_bai_triplet, has_zhong_pair, has_fa_pair, has_bai_pair, has_east_triplet, has_west_triplet, has_south_triplet, has_north_triplet, has_east_pair, has_west_pair, has_south_pair, has_north_pair  = find_sequences_and_triplets_and_pairs(numbers)
    has_wan, has_tong, has_tiao, has_zi = find_suits(true_numbers)

    card_Type = " "
    tai = 0

    if is_punpunhu(triplets):
         card_Type += "碰碰胡" 
         tai += 4
    if has_bai_triplet and has_fa_triplet and has_zhong_triplet:
         card_Type += "大三元"
         tai += 8
    elif  (has_bai_pair and has_fa_triplet and has_zhong_triplet) or \
          (has_bai_triplet and has_fa_pair and has_zhong_triplet) or \
         (has_bai_triplet and has_fa_triplet and has_zhong_pair):
         card_Type += "小三元"
         tai += 4
    elif has_bai_triplet and not has_fa_triplet and not has_zhong_triplet:
         card_Type += "白板"
         tai+=1
    elif not has_bai_triplet and  has_fa_triplet and not has_zhong_triplet:
         card_Type += "發財"
         tai+=1
    elif not has_bai_triplet and not has_fa_triplet and  has_zhong_triplet:
         card_Type += "紅中"
         tai+=1
    elif has_bai_triplet and  has_fa_triplet and not has_zhong_triplet:
         card_Type += "白板,發財"
         tai+=2
    elif not has_bai_triplet and  has_fa_triplet and  has_zhong_triplet:
         card_Type += "發財,紅中"
         tai+=2
    elif has_bai_triplet and  not has_fa_triplet and  has_zhong_triplet:
         card_Type += "白板,發財"
         tai+=2

    if has_east_triplet and has_west_triplet and has_south_triplet and has_north_triplet:
         card_Type += "大四喜"
         tai += 16
    elif (has_east_pair and has_west_triplet and has_south_triplet and has_north_triplet) or\
         (has_east_triplet and has_west_triplet and has_south_pair and has_north_triplet) or\
         (has_east_triplet and has_west_triplet and has_south_triplet and has_north_pair):
         card_Type += "小四喜"
         tai += 8


    if ( has_wan and not has_tong and not has_tiao and  has_zi) or \
         (not has_wan and has_tong and not has_tiao and  has_zi) or \
         (not has_wan and not has_tong and  has_tiao and  has_zi):
         card_Type += "混一色"
         tai += 4
    elif (has_wan and not has_tong and not has_tiao and not has_zi) or \
         (not has_wan and has_tong and not has_tiao and not has_zi) or \
         (not has_wan and not has_tong and has_tiao and not has_zi):
         card_Type += "清一色"
         tai += 8
    elif not has_wan and not has_tong and not has_tiao and has_zi:
         card_Type += "字一色"
         tai += 8

    print("轉換後的整數：", true_numbers)
    print("麻將花色：", [number_to_mahjong(true_number) for true_number in true_numbers])
    print("找到的顺子：", [list(map(number_to_mahjong, sequence)) for sequence in sequences])
    print("找到的刻子：", [list(map(number_to_mahjong, triplet)) for triplet in triplets])
    print("找到的雀頭：", [list(map(number_to_mahjong, pair)) for pair in pairs])
    print("胡牌的種類：", card_Type)
    print("該副牌的台數：", tai)


    if is_winning_hand(sequences, triplets, pairs):
        print("這是一個胡牌的手牌！")
    else:
        print("這不是一個胡牌的手牌。")
        
    response_data = {
        "msg": "success",
        "result": ",".join(ret),
        "mahjong_hand": {
            "numbers": true_numbers,
            "suits": [number_to_mahjong(true_number) for true_number in true_numbers],
            "sequences": [list(map(number_to_mahjong, sequence)) for sequence in sequences],
            "triplets": [list(map(number_to_mahjong, triplet)) for triplet in triplets],
            "pairs": [list(map(number_to_mahjong, pair)) for pair in pairs],
            "winning_hand": is_winning_hand(sequences, triplets, pairs),
            "card_type": card_Type,
            "tai": tai
        }
    }
    
    return jsonify(response_data)

if __name__ == '__main__':
    ssl_cert = 'C:\Openssl\certificate.crt' 
    ssl_key = 'C:\Openssl\private_key.key'   
    context = (ssl_cert, ssl_key) 
    app.run(host='192.168.151.207', port=6666, ssl_context=context, debug=True)
