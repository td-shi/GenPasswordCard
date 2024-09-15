#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__  = "TD"
__version__ = "0.1"
__date__    = "2024-09-13"

from sys import stderr, stdout, exit
import uuid
import random
from base64 import b64encode
from copy import deepcopy
import argparse
import datetime
from typing import NamedTuple
from lxml import etree

LETTER_NUMBER = "0123456789"
LETTER_ALPHAL = "ABCDEFGHJKMNPQRSTVWXZY" # ignore 'ILOU'
LETTER_ALPHAS = "abcdefghjkmnpqrstvwxyz" # ignore 'ilou'
LETTER_MARK   = "!#$%&+/;<=>?@^"         # ignore ' "'()*,-.:[\]_`{|}~'
SVG_CHARACTER_CELL_15NUMBER = "nu15.svg"
SVG_CHARACTER_CELL_25NUMALP = "na25.svg"
SVG_CHARACTER_CELL_50ALL = "mx50.svg"
SVG_CARD_FRONT = "cardFront.svg"
SVG_CARD_BACK = "cardBack.svg"
SVG_CARD_TOP_Y = 37.041664
SVG_CARD_LEFT_X = 14.816665  # 15NUMBER, 50ALL
SVG_CARD_RIGHT_X = 226.48334 # 25NUMALP

class CharCell(NamedTuple):
    c: str = ""     # center
    lt: str = ""    # left top
    lb: str = ""    # left bottom
    rb: str = ""    # right bottom
    rt: str = ""    # right top
    deco: bool = "" # line decoration

def qPrint(quiet: bool, body: str, file:"file like object" = stderr) -> None:
    '''
    ログ出力をする.
    '''

    if not quiet:
        print(body, file=file)

def wrapChar(chars: list[str], leftTop: list[str], leftBottom: list[str], rightBottom: list[str], rightTop: list[str]) -> list[CharCell]:
    '''
    換字表を生成する.
    '''

    ret = [() for i in range(len(chars))]
    for i in range(len(chars)):
        if "|" in chars[i]:
            ret[i] = CharCell(chars[i][1], leftTop[i], leftBottom[i], rightBottom[i], rightTop[i], True)
        else:
            ret[i] = CharCell(chars[i], leftTop[i], leftBottom[i], rightBottom[i], rightTop[i], False)
    return ret

def genNumbers15() -> list[str]:
    '''
    数字のみ15文字を生成する.
    
    notes
    -----
    装飾予定があるものには"|"が付与される.
    '''

    onlyNumber = LETTER_NUMBER + "".join(random.sample(LETTER_NUMBER, 5))
    onlyNumber = random.sample(onlyNumber, len(onlyNumber))
    for i in random.sample(range(0, len(onlyNumber)), 3):
        onlyNumber[i] = "|" + onlyNumber[i]
    return onlyNumber

def wrapNumbers15(numbers: list[str]) -> list[CharCell]:
    '''
    数字のみ15用の換字表を生成する.
    '''

    leftTop     = list("ABCDEFGHIJKLMNO")
    rightBottom = list("PQRSTUVWXYZ") + [",.", "!?", ":;", "/&"]
    rightTop    = list("ガザダバパハマヤラワアカサタナ")
    return wrapChar(numbers, leftTop, ["" for i in range(15)], rightBottom, rightTop)

def genNumAlp25() -> list[str]:
    '''
    英数字25文字を生成する.
    
    notes
    -----
    装飾予定があるものには"|"が付与される.
    '''

    alp20 = random.sample(LETTER_ALPHAL, 20)
    numAlp = "".join(random.sample(LETTER_NUMBER, 5)) + "".join(alp20[:10]) + "".join(alp20[10:]).lower()
    numAlp = random.sample(numAlp, len(numAlp))
    for i in random.sample(range(0, len(numAlp)), 4):
        numAlp[i] = "|" + numAlp[i]
    return numAlp

def wrapNumAlp25(numAlp: list[str]) -> list[CharCell]:
    '''
    英数字25用の換字表を生成する.
    '''

    leftTop     = list("ABCDEFGHIJKLMNOPQRSTUVW") + ["XZ", "Y"]
    rightTop    = list("ナニヌネノタチツテトサシスセソカキクケコアイウエオ")
    leftBottom  = list("ワ↓ーンヲラリルレロヤヰユヱヨマミムメモハヒフヘホ")
    return wrapChar(numAlp, leftTop, leftBottom, ["" for i in range(25)], rightTop)

def genMixNam50() -> list[str]:
    '''
    記号と英数字50文字を生成する.
    
    notes
    -----
    装飾予定があるものには"|"が付与される.
    '''

    mixNam = LETTER_NUMBER + "".join(random.sample(LETTER_ALPHAL, 15)) + "".join(random.sample(LETTER_ALPHAS, 15))  + "".join(random.sample(LETTER_MARK, 10))
    mixNam = random.sample(mixNam, len(mixNam))
    for i in random.sample(range(0, len(mixNam)), 5):
        mixNam[i] = "|" + mixNam[i]
    return mixNam

def wrapMixNam50(mixNam: list[str]) -> list[CharCell]:
    '''
    記号と英数字50用の換字表を生成する.
    '''

    rightTop    = list("ワ↓ーンヲラリルレロヤヰユヱヨマミムメモハヒフヘホナニヌネノタチツテトサシスセソカキクケコアイウエオ")
    leftBottom  = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ@,./1234567890:;?!&=$*%#")
    return wrapChar(mixNam, ["" for i in range(50)], leftBottom, ["" for i in range(50)], rightTop)

def svgCharAttribute(copiedCell: "svg", cc: CharCell, font:  str = "") -> dict:
    '''
    文字セルSVGのdeepcopyに各文字を置き換え, 埋め込みSVG用のattributeを返す.
    '''

    root = copiedCell.getroot()
    ns = {"x":root.nsmap[None]}

    t = copiedCell.xpath('//x:text', namespaces=ns)
    for x in t:
        if 0 < len(font):
            x.attrib['style'] = x.attrib['style'].replace("monospace", "{},monospace".format(font))
        if "text0" == x.attrib['id']:
            x.text = cc.c
        if "text1" == x.attrib['id']:
            x.text = cc.lt
        if "text2" == x.attrib['id']:
            x.text = cc.lb
        if "text3" == x.attrib['id']:
            x.text = cc.rb
        if "text4" == x.attrib['id']:
            x.text = cc.rt

    if cc.deco:
        p = copiedCell.xpath('//x:path', namespaces=ns)
        for x in p:
            x.attrib['style'] = x.attrib['style'].replace("stroke-dasharray:none;stroke-opacity:1", "stroke-dasharray:4.23326016,4.23326016;stroke-opacity:1;stroke-dashoffset:0")

    return {"preserveAspectRatio": "none", "width": "42.333332", "height":"42.333332", "{http://www.w3.org/1999/xlink}href":"data:image/svg+xml;base64,{}".format(b64encode(etree.tostring(copiedCell, method="xml", encoding="utf-8", xml_declaration=True)).decode())}

def putCharOnSvg(parsedCardSvg: "svg", parsedCharSvg: "svg", chars: list[CharCell], offsetX: float, offsetY: float, font: str = None) -> None:
    '''
    カードSVGの原本に換字表分の文字セルSVGを埋め込む.
    '''

    if None == font:
        font = ""

    cardRoot = parsedCardSvg.getroot()
    i = 0
    l = len(chars)
    for cc in chars:
        col = int(i/5)
        row = i % 5
        cha = svgCharAttribute(deepcopy(parsedCharSvg), cc, font=font)
        cha['id'] = "cell{}{}".format(l, i)
        cha['x'] = "{:.5f}".format(offsetX + float(cha['width']) * col)
        cha['y'] = "{:.5f}".format(offsetY + float(cha['height']) * row)
        i += 1
        cardRoot.append(etree.Element("image", attrib=cha, nsmap=cardRoot.nsmap))

def checkSvgName(frontName: str, backName: str) -> None:
    '''
    カードSVGファイルの名前衝突を検証する.
    '''

    if frontName in [SVG_CHARACTER_CELL_15NUMBER, SVG_CHARACTER_CELL_25NUMALP, SVG_CHARACTER_CELL_50ALL, SVG_CARD_FRONT, SVG_CARD_BACK]:
        exit("Bad a name of the card front.")
    if backName in [SVG_CHARACTER_CELL_15NUMBER, SVG_CHARACTER_CELL_25NUMALP, SVG_CHARACTER_CELL_50ALL, SVG_CARD_FRONT, SVG_CARD_BACK]:
        exit("Bad a name of the card back.")

def main(serial: "uuid", frontName: str, backName: str, font: str = None, quiet: bool = False) -> None:
    '''
    本体.
    
    notes
    -----
    1. ランダムシード設定
    2. 各換字表生成 (数字のみ15, 英数字25, 記号と英数字50)
    3. 表面カード生成
    4. 裏面カード生成
    '''

    checkSvgName(nameFront, nameBack)

    random.seed(serial.int)
    qPrint(quiet, str(serial), file=stdout)

    # BEGIN RANDOM
    onlyNumber = genNumbers15()
    numAlp = genNumAlp25()
    mixNam = genMixNam50()

    wnum15 = wrapNumbers15(onlyNumber)
    walp25 = wrapNumAlp25(numAlp)
    wmix50 = wrapMixNam50(mixNam)
    qPrint(quiet, wnum15, file=stdout)
    qPrint(quiet, walp25, file=stdout)
    qPrint(quiet, wmix50, file=stdout)
    # END RANDOM

    cardFront = etree.parse(SVG_CARD_FRONT)
    cardRoot = cardFront.getroot()
    putCharOnSvg(cardFront, etree.parse(SVG_CHARACTER_CELL_15NUMBER), wnum15, SVG_CARD_LEFT_X, SVG_CARD_TOP_Y, font=font)
    putCharOnSvg(cardFront, etree.parse(SVG_CHARACTER_CELL_25NUMALP), walp25, SVG_CARD_RIGHT_X, SVG_CARD_TOP_Y, font=font)
    tSerial = cardRoot.xpath('//x:text[@id="textS"]', namespaces={"x":cardRoot.nsmap[None]})
    for x in tSerial:
        x.text = str(serial)
    cardFront.write(frontName, method="xml", xml_declaration=True, encoding="utf-8")
    qPrint(quiet, "Generated {}.".format(frontName))

    cardBack = etree.parse(SVG_CARD_BACK)
    putCharOnSvg(cardBack, etree.parse(SVG_CHARACTER_CELL_50ALL), wmix50, SVG_CARD_LEFT_X, SVG_CARD_TOP_Y, font=font)
    cardBack.write(backName, method="xml", xml_declaration=True, encoding="utf-8")
    qPrint(quiet, "Generated {}.".format(backName))

if "__main__" == __name__:
    parser = argparse.ArgumentParser(description='UUIDをシリアルコードとした, パスワード生成カードのSVGを作成する.')
    parser.add_argument('-u','--uuid', help='an UUID for the serial of the card.')
    parser.add_argument('-outf', '--output_card_front_name', help='a name of the card front.')
    parser.add_argument('-outb', '--output_card_back_name', help='a name of the card back.')
    parser.add_argument('-font', help='characters font family.')
    parser.add_argument('-q','--quiet', action='store_true', help='No log at stdout and stderr.')

    nowTime = (datetime.datetime.now()).strftime('%Y-%m-%dT%H%M%S')
    args = parser.parse_args()
    serial = uuid.uuid4() if None == args.uuid else uuid.UUID(args.uuid) # "4f03bf89-f37e-4af5-8191-59b5020576f0"
    nameFront = "{}_card-front.svg".format(nowTime) if None == args.output_card_front_name else args.output_card_front_name
    nameBack = "{}_card-back.svg".format(nowTime) if None == args.output_card_back_name else args.output_card_back_name

    main(serial, nameFront, nameBack, font=args.font, quiet=args.quiet)
