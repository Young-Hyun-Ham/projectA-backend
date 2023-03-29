from typing import List
from collections import Counter
from fastapi import APIRouter, status, Depends, Body, HTTPException

from config.db import session
from models.lotto import lottoTable, lotto, lottoOut

import random

router = APIRouter()


def 로또번호추출(excludList: list = []) -> List:
    arr = []

    # 보너스까지 7개의 1~45까지의 난수 발생
    for i in range(0, 6):
        arr.append(random.randrange(1, 46))
        # 랜덤 값이 제외 하는 값과 같을 경우 다시 값을 가져온다.
        if excludList:
            for e in excludList:
                # print(f"============>{arr} :::: {e}")
                # print(f"====> {arr[i]} == {e[0]}::::{arr[i] == e[0]}")
                if arr[i] == e[0]:
                    arr[i] = random.randrange(1, 46)
                    if i > 0:
                        i = i - 1

    # 정렬
    arr.sort()

    arr = [0, 0, 0, 0, 0, 0, 0]  # 기본 int형은 int32 이다.
    for i in range(len(arr)):
        count = 0
        for j in range(len(arr)):
            if arr[i] == arr[j]:
                count += 1

        # Double check with the same number
        if count > 1:
            # print(f"before===>{arr}")
            arr[i] = random.randrange(1, 46)
            i = 0
            # print(f"after===>{arr}")

    # print(f"finlly===>{arr}")
    return arr

# 기본패턴으로 현재까지 당첨 번호와 일치 한 것이 있는지만 확인 하여 추첨번호를 추출한다.


def 기본패턴_번호추출(임시추첨번호: list = [], 전체회차_데이터: list = []) -> List:
    추첨번호 = 로또번호추출()

    # 성공여부
    flag = True

    while (flag):
        for item in 전체회차_데이터:
            if item.num1 == int(임시추첨번호[0]) & item.num2 == int(임시추첨번호[1]) & item.num3 == int(임시추첨번호[2]) & item.num4 == int(임시추첨번호[3]) & item.num5 == int(임시추첨번호[4]) & item.num6 == int(임시추첨번호[5]):
                # 번호 재 추첨
                추첨번호 = 로또번호추출()
            else:
                if item == 전체회차_데이터[-1]:
                    flag = False

    return 추첨번호

# 당첨된 로또 전 회자 데이터 가져오기


def 전체회차_데이터_가져오기() -> List:
    return session.query(lottoTable).all()

# 당첨된 번호중 가장 많이 나온 번호 6개를 빼고 랜덤을 돌린다.


def 당첨번호_중복_데이터_가져오기(sortType: str) -> List:

    sql = f"""
            WITH tmp AS (
                SELECT T.num, COUNT(T.num) AS cnt, RANK() OVER(ORDER BY COUNT(T.num) {sortType}) AS ranking
                FROM (
                    SELECT num1 AS num
                        FROM t_lotto
                    UNION ALL
                    SELECT num2 AS num
                        FROM t_lotto
                    UNION ALL
                    SELECT num3 AS num
                        FROM t_lotto
                    UNION ALL
                    SELECT num4 AS num
                        FROM t_lotto
                    UNION ALL
                    SELECT num5 AS num
                        FROM t_lotto
                    UNION ALL
                    SELECT num6 AS num
                        FROM t_lotto
                ) T
                GROUP BY T.num
            )
            SELECT num, cnt, ranking
            FROM tmp
            WHERE ranking < 7
            ORDER BY ranking
          """
    dupList = session.execute(sql).all()

    return dupList

# 유형별 패턴을 분석 하여 가장 많이 나온 값을 가져온다.


def 유형별_패턴분석_번호추출() -> List:
    # 추첨번호 = [기본패턴_번호추출() for _ in range(100)]
    추첨번호 = []
    추첨번호_리스트 = []

    임시추첨번호 = 로또번호추출()
    전체회차데이터 = 전체회차_데이터_가져오기()
    dupList = 당첨번호_중복_데이터_가져오기("desc")
    dupList2 = 당첨번호_중복_데이터_가져오기("asc")

    for i in range(100):
        추첨번호_리스트.append(기본패턴_번호추출(임시추첨번호, 전체회차데이터))

    for i in range(100):
        추첨번호_리스트.append(로또번호추출(dupList))

    for i in range(100):
        추첨번호_리스트.append(로또번호추출(dupList2))

    # print(추첨번호_리스트)
    전체아이템 = []
    for 추첨번호_아이템 in 추첨번호_리스트:
        for item in 추첨번호_아이템:
            전체아이템.append(item)

    c = Counter(전체아이템).most_common()
    # print(f"=========>  {c}")
    loopCount = 0
    for item in c:
        if loopCount < 6:
            # print(f"=====>{item}")
            추첨번호.append(item[0])
            loopCount = loopCount + 1
        else:
            break

    # 정렬
    추첨번호.sort()
    return 추첨번호


@router.get("/todayNubmer", description="""pattenType [1] : 기본패턴 번호추출 (전체회차 당첨번호를 제외 하고 랜덤으로 생성 <br/>
                                                                 pattenType [2] : [1] 패턴 + 당첨 번호에 많이 등록된 6개 번호를 제외 시키고 랜덤으로 생성 <br/>
                                                                 pattenType [3] : [1] 패턴 + 당첨 번호에 적게 등록된 6게 번호를 제외 시키고 랜덤으로 생성 <br/>
                                                                 pattenType [4] : [1] + [2] + [3] 패턴을 각각 100번씩 돌려서 가장 많이 나온 6개의 숫자 <br/>
            """,
            # response_model=any,
            status_code=status.HTTP_200_OK)
async def 추첨번호추출(pattenType: str = "1"):
    최종추첨번호 = [0, 0, 0, 0, 0, 0]

    if pattenType == "1":
        최종추첨번호 = 기본패턴_번호추출(로또번호추출(), 전체회차_데이터_가져오기())
    elif pattenType == "2":
        최종추첨번호.clear()
        중복데이터 = 당첨번호_중복_데이터_가져오기("desc")
        for 데이터 in 중복데이터:
            최종추첨번호.append(데이터[0])
    elif pattenType == "3":
        최종추첨번호.clear()
        중복데이터 = 당첨번호_중복_데이터_가져오기("asc")
        for 데이터 in 중복데이터:
            최종추첨번호.append(데이터[0])
    elif pattenType == "4":
        최종추첨번호 = 유형별_패턴분석_번호추출()

    data = {"num1": int(최종추첨번호[0]),
            "num2": int(최종추첨번호[1]),
            "num3": int(최종추첨번호[2]),
            "num4": int(최종추첨번호[3]),
            "num5": int(최종추첨번호[4]),
            "num6": int(최종추첨번호[5])}
    # if item_id not in items:
    #     raise HTTPException(status_code=404, detail="Item not found")
    return {"statusCode": 200, "data": lotto(**data), "resultCode": "L_SUCCESS", "resultMessage": "성공"}
    # lottoOut.statusCode = 200
    # lottoOut.data = Lotto(**data)
    # lottoOut.resultCode = "L_SUCCESS"
    # lottoOut.resultMessage = "성공"
    # return lottoOut


@router.get("/get/{no}")
def 당첨회차번호가져오기(no: int):
    당첨번호 = session.query(lottoTable).filter(lottoTable.no == no).first()

    if 당첨번호:
        data = {"no": int(당첨번호.no),
                "num1": int(당첨번호.num1),
                "num2": int(당첨번호.num2),
                "num3": int(당첨번호.num3),
                "num4": int(당첨번호.num4),
                "num5": int(당첨번호.num5),
                "num6": int(당첨번호.num6),
                "bonus": int(당첨번호.bonus)}
        return {"statusCode": 200, "data": lotto(**data), "resultCode": "L_SUCCESS", "resultMessage": "성공"}
    else:
        return {"statusCode": 200, "data": {}, "resultCode": "L_NO_RESULT", "resultMessage": "조회된 결과가 없습니다."}


@router.post("/select", response_model=str)
def 당첨회차번호등록(l: lotto) -> str:
    # 기존에 있는 회차 이면 등록 하지 못한다.
    getLotto = session.query(lottoTable).filter(lottoTable.no == l.no).first()

    if getLotto:
        return f"{l.no} create failed"
    else:
        lotto = lottoTable()
        lotto.no = l.no
        lotto.num1 = l.num1
        lotto.num2 = l.num2
        lotto.num3 = l.num3
        lotto.num4 = l.num4
        lotto.num5 = l.num5
        lotto.num6 = l.num6
        lotto.bonus = l.bonus

        session.add(lotto)
        session.commit()

        return f"{l.no} created..."


@router.put("/update", response_model=str)
def 당첨회차번호수정(l: List[lotto]) -> str:
    for i in l:
        lotto = session.query(lottoTable).filter(lottoTable.no == i.no).first()
        lotto.num1 = i.num1
        lotto.num2 = i.num2
        lotto.num3 = i.num3
        lotto.num4 = i.num4
        lotto.num5 = i.num5
        lotto.num6 = i.num6
        lotto.bonus = i.bonus

        session.commit()
    return f"{i.no} updated..."


@router.delete("/delete/{no}", response_model=str)
def 당첨회차삭제(no: int) -> str:
    session.query(lottoTable).filter(lottoTable.no == no).delete()
    session.commit()
    return f"deleted..."
