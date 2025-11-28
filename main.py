# main.py
from update_lotto_db import load_lotto_data   # ← 이게 정답!

# 무한 반복 로또 당첨 확인기 (종료할 때까지 계속!)
print("\n" + "="*70)
print("로또 당첨 확인기 - 무한 모드 ON!")
print("6개 번호 입력 → 당첨 여부 바로 확인 (4등 이상만 출력)")
print("종료하려면: 끝 / exit / q / quit 중 하나 입력")
print("="*70)

lotto_db = update_lotto_db()

while True:
    print("\n" + "-"*50)
    my_input = input("번호 입력 (예: 3 12 19 27 35 42) → ").strip().lower()
    
    # 종료 명령어
    if my_input in ["끝", "exit", "q", "quit", "ㅅ", ""]:
        print("로또 확인기를 종료합니다. 다음 주에 또 만나요!")
        break
    
    try:
        my_numbers = list(map(int, my_input.split()))
        
        # 입력 검증
        if len(my_numbers) != 6:
            print("번호 6개를 입력해주세요!")
            continue
        if len(set(my_numbers)) != 6:
            print("중복된 번호가 있어요! 서로 다른 6개 번호를 입력해주세요.")
            continue
        if any(n < 1 or n > 45 for n in my_numbers):
            print("1~45 사이의 숫자만 입력 가능합니다!")
            continue
        
        my_set = set(my_numbers)
        print(f"\n내 번호: {sorted(my_numbers)}")
        print("-"*60)
        
        found = False
        for no, info in lotto_db.items():
            win_set = set(info["numbers"])
            match = len(my_set & win_set)
            has_bonus = info["bonus"] in my_set
            
            if match >= 4:  # 4등 이상만 출력 (원하시면 3등도 가능)
                rank = {6:"1등", 5:"2등" if has_bonus else "3등", 4:"4등"}[match]
                print(f"{no}회 ({info['date']}) → {rank} 당첨!!!")
                print(f"   당첨번호: {sorted(info['numbers'])} + 보너스 {info['bonus']}")
                found = True
        
        if not found:
            print("이 번호로는 4등 이상 당첨된 적이 없습니다... 다음 기회에!")
        else:
            print("\n축하합니다!!! 대박 나세요!!!")
            
    except ValueError:
        print("숫자만 입력해주세요! (공백으로 구분)")
    except Exception as e:
        print(f"오류 발생: {e}")
