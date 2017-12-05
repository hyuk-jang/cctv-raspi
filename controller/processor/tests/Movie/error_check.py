# -*- coding:utf-8 -*-

# 이상한 번호를 입력하는지 체크
def choice(c, max):

    print " c choice : ", c
    print " len menu : ", str(max)
    if len(c)!=1 or int(c)<0 or int(c)>max:
        print "\n★ ★ ★ what? 다시 선택해 주세요. ★ ★ ★\n\n"
        return False
    else : return int(c)-1



def choice_Movie(chN, chT, moveList):

    listNumber=None

    for i in range(len(moveList)) :
        if chN==moveList[i].mName : listNumber=i
        else : chN=False

    try:
        moveList[listNumber].mTime.index(chT)
    except : chT=False

    # 리스트 안에 있으면 참 없으면 거짓
    return chN, chT
