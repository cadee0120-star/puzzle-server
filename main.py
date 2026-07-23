from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from z3 import *
import random

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

THEMES = {
    "space": {
        "headers": ["우주선", "출신 행성", "핵심 동력", "우주 식량", "담당 구역", "담당 대원", "특수 장비"],
        "icons": ["🚀", "🪐", "⚡", "🥫", "🌌", "👨‍🚀", "🛡️"],
        "types": ["ship", "planet", "engine", "food", "sector", "person", "gear"],
        "pools": [
            ["오리온호", "이카로스호", "헬리오스호", "프로메테우스호", "크로노스호", "발키리호", "헤르메스호"],
            ["지구", "목성", "금성", "화성", "토성", "수성", "천왕성"],
            ["반물질 엔진", "초고속 이동기", "순간 이동기", "별 엔진", "빛 엔진", "불꽃 엔진", "양자 엔진"],
            ["젤리 캡슐", "알약 영양제", "합성 스테이크", "농축 단백질바", "건조과일", "해초팩", "열량 캔디"],
            ["가 구역", "나 구역", "다 구역", "라 구역", "마 구역", "바 구역", "아 구역"],
            ["강민우", "노동현", "도재석", "류성민", "박준서", "송태양", "윤지호"],
            ["탐지 안경", "무전 슈트", "드론 제어기", "광선총", "중력 장화", "산소 마스크", "보호막"]
        ]
    },
    "fantasy": {
        "headers": ["이름", "직업", "대표 장비", "반려 마수", "출신 국가", "기술", "길드 계급"],
        "icons": ["👤", "⚔️", "🛡️", "🐉", "🏰", "🪄", "🏅"],
        "types": ["person", "job", "item", "pet", "place", "magic", "rank"],
        "pools": [
            ["알릭", "칼렌", "세드릭", "다리아", "엘리온", "페린", "줄리"],
            ["전사", "마법사", "힐러", "도적", "궁수", "연금술사", "기사"],
            ["드래곤 슬레이어", "지팡이", "성서", "그림자 단검", "요정의 활", "룬 장갑", "불꽃검"],
            ["피닉스", "그리폰", "섀도우 캣", "골렘", "슬라임", "검은 늑대", "히드라"],
            ["장미 왕국", "숲의 왕국", "강철 성채", "용의 영지", "고귀한 요새", "영혼의 숲", "기사의 성"],
            ["빙결계", "뇌전계", "치유계", "환영계", "암흑계", "화염계", "보호계"],
            ["브론즈", "실버", "골드", "플래티넘", "다이아몬드", "영웅", "신화"]
        ]
    },
    "daily": {
        "headers": ["이름", "집", "반려동물", "음료", "취미", "이동수단", "계절"],
        "icons": ["🙋‍♂️", "🏠", "🐶", "☕", "🎨", "🚲", "🍂"],
        "types": ["person", "house", "pet", "drink", "hobby", "vehicle", "season"],
        "pools": [
            ["김철수", "이영희", "박민수", "최지우", "정현우", "한소희", "다니엘"],
            ["빨간 집", "파란 집", "노란 집", "초록 집", "하얀 집", "회색 집", "주황 집"],
            ["강아지", "고양이", "앵무새", "햄스터", "거북이", "금붕어", "라쿤"],
            ["커피", "홍차", "보리차", "딸기쉐이크", "녹차", "자몽에이드", "식혜"],
            ["독서", "요리", "꽃꽂이", "음악 감상", "사진 촬영", "수영", "조깅"],
            ["킥보드", "버스", "차", "오토바이", "지하철", "트램", "도보"],
            ["봄", "여름", "가을", "겨울", "환절기", "우기", "건기"]
        ]
    },
    "cooking": {
        "headers": ["요리사", "요리 분야", "특기 메뉴", "메인 식재료", "조리 도구", "조리 기구", "디저트"],
        "icons": ["👨‍🍳", "🍽️", "🍲", "🥩", "🔪", "🍳", "🍰"],
        "types": ["person", "field", "dish", "ingredient", "knife", "tool", "dessert"],
        "pools": [
            ["고든", "피에르", "라따뚜이", "윤남노", "정지선", "박은영", "최강록"],
            ["프렌치", "이탈리안", "일식", "분자요리", "한식", "양식", "멕시칸"],
            ["소고기 파이", "생선 초밥", "트러플 파스타", "스테이크", "해물찜", "자장면", "퀘사디아"],
            ["안심", "참치", "송이 버섯", "랍스터", "캐비아", "닭고기", "콩"],
            ["식칼", "국자", "중식도", "가위", "집게", "뒤집개", "과도"],
            ["오븐", "에어프라이어", "후라이팬", "그릴", "압력솥", "웍", "토치"],
            ["마카롱", "수플레", "푸딩", "아이스크림", "약과", "타르트", "츄러스"]
        ]
    }
}

def attach_josa(word, j_type):
    if not word: return ""
    last_char = ord(word[-1])
    has_batchim = (last_char - 0xac00) % 28 != 0
    if j_type == '은는': return f"'{word}'" + ('은' if has_batchim else '는')
    if j_type == '을를': return f"'{word}'" + ('을' if has_batchim else '를')
    if j_type == '이가': return f"'{word}'" + ('이' if has_batchim else '가')
    if j_type == '와과': return f"'{word}'" + ('과' if has_batchim else '와')
    if j_type == '의': return f"'{word}'의"
    if j_type == '에': return f"'{word}'에"
    return f"'{word}'"

def format_natural_clue(itemA, typeA, itemB, typeB, clueType, param=None):
    if clueType == 'NOT_SAME':
        if typeB in ['job', 'field', 'rank']:
            return f"{attach_josa(itemA, '은는')} {attach_josa(itemB, '이가')} 아니다."
        elif typeB in ['item', 'drink', 'food', 'knife', 'gear', 'tool', 'dessert']:
            return f"{attach_josa(itemA, '은는')} {attach_josa(itemB, '을를')} 사용(소비)하지 않는다."
        elif typeB in ['house', 'planet', 'sector', 'place']:
            return f"{attach_josa(itemA, '은는')} {attach_josa(itemB, '에')} 위치해 있지 않다."
        elif typeB == 'pet':
            return f"{attach_josa(itemA, '은는')} {attach_josa(itemB, '을를')} 기르지 않는다."
        return f"{attach_josa(itemA, '와과')} {attach_josa(itemB, '은는')} 함께 위치하지 않는다."

    if clueType == 'SAME':
        if typeB in ['job', 'rank']: return f"{attach_josa(itemA, '은는')} {attach_josa(itemB, '이다')}."
        if typeB in ['house', 'planet', 'sector', 'place']: return f"{attach_josa(itemA, '은는')} {attach_josa(itemB, '에')} 있다."
        if typeB in ['item', 'food', 'drink', 'gear', 'tool', 'dessert']: return f"{attach_josa(itemA, '은는')} {attach_josa(itemB, '을를')} 선택(사용)한다."
        return f"{attach_josa(itemA, '와과')} {attach_josa(itemB, '은는')} 같은 위치에 배치된다."

    if clueType == 'ADJACENT': return f"{attach_josa(itemA, '와과')} {attach_josa(itemB, '은는')} 바로 옆에 위치한다."
    if clueType == 'GAP_1': return f"{attach_josa(itemA, '와과')} {attach_josa(itemB, '은는')} 사이에 정확히 1개의 공간을 두고 있다."
    if clueType == 'NOT_EDGE': return f"{attach_josa(itemA, '은는')} 대열의 양 끝에 위치하지 않는다."
    if clueType == 'IS_EDGE': return f"{attach_josa(itemA, '은는')} 대열의 양 끝 중 한 곳에 위치한다."
    if clueType == 'DIRECT_POS': return f"{attach_josa(itemA, '은는')} {param}번 공간에 위치한다."
    return ""

def count_z3_solutions(width, height, headers, elements, clues, max_limit=2):
    s = Solver()
    grid = {}
    for r, h in enumerate(headers):
        for c in range(width):
            grid[(r, c)] = Int(f"cell_{r}_{c}")
            s.add(grid[(r, c)] >= 0, grid[(r, c)] < width)
        s.add(Distinct([grid[(r, c)] for c in range(width)]))

    for cl in clues:
        r1 = headers.index(cl['h1'])
        idxA = elements[cl['h1']].index(cl['e1'])
        posA = grid[(r1, idxA)]

        if cl['type'] == 'DIRECT_POS':
            s.add(posA == cl['param'] - 1)
        elif cl['type'] == 'NOT_EDGE':
            s.add(posA != 0, posA != width - 1)
        elif cl['type'] == 'IS_EDGE':
            s.add(Or(posA == 0, posA == width - 1))
        else:
            r2 = headers.index(cl['h2'])
            idxB = elements[cl['h2']].index(cl['e2'])
            posB = grid[(r2, idxB)]

            if cl['type'] == 'SAME':
                s.add(posA == posB)
            elif cl['type'] == 'NOT_SAME':
                s.add(posA != posB)
            elif cl['type'] == 'ADJACENT':
                s.add(Or(posA - posB == 1, posB - posA == 1))
            elif cl['type'] == 'GAP_1':
                s.add(Or(posA - posB == 2, posB - posA == 2))

    sol_count = 0
    solutions = []
    while s.check() == sat:
        sol_count += 1
        m = s.model()
        cur_sol = {}
        block = []
        for r, h in enumerate(headers):
            for c in range(width):
                val = m[grid[(r, c)]].as_long()
                block.append(grid[(r, c)] != val)
        solutions.append(m)
        s.add(Or(block))
        if sol_count >= max_limit:
            break
    return sol_count

@app.get("/")
def home():
    return {"message": "아인슈타인 퍼즐 Z3 초고속 백엔드 엔진 작동 중!"}

@app.get("/api/generate")
def generate_puzzle(width: int = Query(6, ge=3, le=7), height: int = Query(6, ge=2, le=7), theme: str = "space"):
    t_data = THEMES.get(theme, THEMES["space"])
    sel_headers = t_data["headers"][:height]
    sel_icons = t_data["icons"][:height]
    sel_types = t_data["types"][:height]
    
    shuffled_pools = [random.sample(p[:width], width) for p in t_data["pools"][:height]]
    
    actual_elements = {}
    for idx, h in enumerate(sel_headers):
        actual_elements[h] = shuffled_pools[idx]

    solution_matrix = []
    for i in range(width):
        row = {}
        for col_idx, h in enumerate(sel_headers):
            row[h] = shuffled_pools[col_idx][i]
        solution_matrix.append(row)

    indirect_candidates = []
    direct_candidates = []

    # 1. 간접 힌트 생성 (우선순위)
    for h1 in range(height):
        for h2 in range(h1 + 1, height):
            for i in range(width):
                itemA = solution_matrix[i][sel_headers[h1]]
                itemB = solution_matrix[i][sel_headers[h2]]
                indirect_candidates.append({
                    'type': 'SAME', 'h1': sel_headers[h1], 'e1': itemA, 'h2': sel_headers[h2], 'e2': itemB,
                    'text': format_natural_clue(itemA, sel_types[h1], itemB, sel_types[h2], 'SAME')
                })

    for h1 in range(height):
        for h2 in range(height):
            for i in range(width):
                for j in range(width):
                    if i == j: continue
                    itemA = solution_matrix[i][sel_headers[h1]]
                    itemB = solution_matrix[j][sel_headers[h2]]
                    dist = abs(i - j)
                    if dist == 1:
                        indirect_candidates.append({
                            'type': 'ADJACENT', 'h1': sel_headers[h1], 'e1': itemA, 'h2': sel_headers[h2], 'e2': itemB,
                            'text': format_natural_clue(itemA, sel_types[h1], itemB, sel_types[h2], 'ADJACENT')
                        })
                    elif dist == 2:
                        indirect_candidates.append({
                            'type': 'GAP_1', 'h1': sel_headers[h1], 'e1': itemA, 'h2': sel_headers[h2], 'e2': itemB,
                            'text': format_natural_clue(itemA, sel_types[h1], itemB, sel_types[h2], 'GAP_1')
                        })

    for h in range(height):
        for i in range(width):
            itemA = solution_matrix[i][sel_headers[h]]
            if i in [0, width - 1]:
                indirect_candidates.append({
                    'type': 'IS_EDGE', 'h1': sel_headers[h], 'e1': itemA,
                    'text': format_natural_clue(itemA, sel_types[h], None, None, 'IS_EDGE')
                })
            else:
                indirect_candidates.append({
                    'type': 'NOT_EDGE', 'h1': sel_headers[h], 'e1': itemA,
                    'text': format_natural_clue(itemA, sel_types[h], None, None, 'NOT_EDGE')
                })

    # 2. 직접 힌트 생성 (최소한만 사용)
    for h in range(height):
        for i in range(width):
            itemA = solution_matrix[i][sel_headers[h]]
            direct_candidates.append({
                'type': 'DIRECT_POS', 'h1': sel_headers[h], 'e1': itemA, 'param': i + 1,
                'text': format_natural_clue(itemA, sel_types[h], None, None, 'DIRECT_POS', i + 1)
            })

    random.shuffle(indirect_candidates)
    random.shuffle(direct_candidates)

    selected_clues = []

    # [Step 1] 유일해(Count === 1) 만족시까지 간접 힌트 누적
    for cl in indirect_candidates:
        selected_clues.append(cl)
        if count_z3_solutions(width, height, sel_headers, actual_elements, selected_clues) == 1:
            break

    # [Step 2] 부족할 경우 직접 힌트 최소한 보충
    if count_z3_solutions(width, height, sel_headers, actual_elements, selected_clues) != 1:
        for cl in direct_candidates:
            selected_clues.append(cl)
            if count_z3_solutions(width, height, sel_headers, actual_elements, selected_clues) == 1:
                break

    # [Step 3] 중복 및 불필요 단서 100% 제거 (Pruning)
    for i in range(len(selected_clues) - 1, -1, -1):
        temp_clues = [c for idx, c in enumerate(selected_clues) if idx != i]
        if count_z3_solutions(width, height, sel_headers, actual_elements, temp_clues) == 1:
            selected_clues.pop(i)

    final_clue_texts = [c['text'] for c in selected_clues]
    random.shuffle(final_clue_texts)

    return {
        "theme": theme,
        "headers": sel_headers,
        "icons": sel_icons,
        "elements": actual_elements,
        "solution": solution_matrix,
        "clues": final_clue_texts
    }
