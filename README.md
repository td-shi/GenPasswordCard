# パスワード生成カード

## Overview

UUIDをシリアルナンバーとするパスワード生成カードを作図する.
Python3の仕様上ではrandomモジュールは同じseed値を与える限り同じ乱数系を返すので,
同じUUIDであれば同じパスワード生成カードが得られるハズである.

## Requirement

- Python 3.9以降
  + lxmlモジュール
- 閲覧, 印刷には別途SVGが取り扱えるものが必要

## Principle

UUIDをPython3のramdomモジュールのseed値として, 数字15文字, 英数字25文字, 記号と英数字50文字の
換字暗号表をカードの表と裏に相当するSVG画像として作図する.

Python3の仕様上ではrandomモジュールは同じseed値を与える限り同じ乱数系を返すので,
UUIDを控えておけば, 同じSVG画像が得られるハズである.

SVG画像は縦横比がクレジットカードの縦横比とほとんど同じであるため,
縮小印刷などの手加工により, 財布や名刺ケースに収めることができる.

作図の際には以下のSVG画像を元に埋め込みや加工を行う.

- 数字15文字のうちの1つ分 :: nu15.svg
- 英数字25文字のうちの1つ分 :: na25.svg
- 記号と英数字50文字のうちの1つ分 :: mx50.svg
- カード表(数字15文字, 英数字25文字, UUID) :: cardFront.svg
- カード裏(記号と英数字50文字) :: cardBack.svg

## Usage

実際に利用する際には, このPythonコードと実行時のシリアルコードのバックアップや,
印刷したカードの保護(テープ補強やケース封入など)を推奨する.

### `$> python3 genPasswordCard.py`

UUIDv4を自動生成し, それをシリアルコードとしたパスワード生成カードのSVG画像を
'<日付>\_card-front.svg' と '<日付>\_card-back.svg'としてファイル作成する.
標準出力には, シリアルコード(UUID), 数字15文字, 英数字25文字, 記号と英数字50文字のリストを出力する.

### `$> python3 genPasswordCard.py -u <UUID>`

シリアルコードを与えられたUUIDに設定する.
他の動作は引数なしの動作と同じ.

### `$> python3 genPasswordCard.py -q`

標準出力へのシリアルコード出力や生成されたSVG画像ファイル名などのログ情報の出力をしない.
他の動作は引数なしの動作と同じ.

## License

- Python本体コードとSVG :: [CC0 (publick domain)](https://creativecommons.org/publicdomain/zero/1.0/legalcode)

## Author

TD
