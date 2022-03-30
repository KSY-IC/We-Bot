
# We-Bot制御ライブラリ (C) 2020 KSY
KSY社製のWe-Botを制御するためのライブラリです。

## License
このライブラリはMITライセンスで配布します。
MITライセンスの詳細はLICENSE.txtを参照ください。

## 必要な環境
本ライブラリはPython 3.7以降で動作確認を行っています。
また、以下のライブラリを別途必要とします。
- smbus2
- pigpio

## インストール方法
ソースコードをダウンロード後、以下のコマンドでセットアップしてください。

```
python3 setup.py install
```

## 使用するハードウエア
### 基板の説明
![基板説明](https://github.com/KSY-IC/We-Bot/blob/main/image/board.png?raw=true )


We Botではモーター制御にTexas Instruments社製　DRV8872を2個、バッテリーなどの電圧取得にTexas Instruments社製　TLA2024を一つ搭載しています。
本ライブラリではこれらデバイスの制御に以下のハードウエアリソースを使用しています。


### GPIO
| GPIOピン番号 | I/O | 用途 |
----|----|----
| 5 | Out | Enable |
| 6 | In | FAULT |
| 12 | Out | PWM1 |
| 13 | Out | PWM2 |
| 24 | Out | DIR1 |
| 25 | Out | DIR2 |

PWM周期は20KHzで動作します。

### I2C
| デバイス | アドレス | 用途 |
----|----|----
| TLA2024 | 0x48 | ADC(バッテリー電源、5Vライン、外部入力) |


## 使い方

以下にサンプルコードを記載します。

```
from webot import WeBot

webot = WeBot()

webot.readVoltage(2)  # read Battery voltage
webot.readVoltage(3)  # read 5V line voltage

webot.forward(400)    # move to forward
webot.back(400)       # move to back
webot.left(400)       # turn left
webot.right(400)      # turn right
webot.stop()          # stop motor

webot.setSpeed(400,200)  # Set motor speed
```

## API
本ライブラリのAPIを開設します。

---

### enableMotor()
モータードライバを有効にします。

引数：なし
戻り値：なし

使い方
```
from webot import WeBot

webot = WeBot()
webot.enableMotor()
```
---

### disableMotor()
モータードライバを無効にします。

引数：なし
戻り値：なし

使い方
```
from webot import WeBot

webot = WeBot()
webot.disableMotor()
```
---

### getFault()
モータードライバのFAIL出力状態を取得します。

引数：なし
戻り値：int ( 0 正常/ 1 異常)

使い方
```
from webot import WeBot

webot = WeBot()
fault = webot.getFault()
```
---

### setSpeedOffset( offset1, offset2 )
モータードライバの出力補正値を行います。
We-Botではモーターを２個使用していますが、モーターのばらつきにより、同じPWM出力値で電圧を出力しても、実際に回転数が一致しない場合があります。
そのような場合、このメソッドを用いて出力補正値を設定することで調整を行います。

引数：
    offset1  モーター1の調整係数(0.00-1.00)
    offset2  モーター2の調整係数(0.00-1.00)

戻り値：なし

使い方
```
from webot import WeBot

webot = WeBot()
fault = webot.setSpeedOffset( 1.00, 0.99 )
```
---


### setSpeed(　speed1, speed2 )
モータードライバの出力を行います。

引数：
    speed1  モーター1の出力値(0 - 480)
    speed2  モーター2の出力値(0 - 480)

戻り値：なし

使い方
```
from webot import WeBot

webot = WeBot()
fault = webot.setSpeed( 480, 480 )
```
---

### setMaxSpeed(speed)
出力できる最大値を設定します。

引数：
    speed1  モーター1の出力値(0 - 480)
    speed2  モーター2の出力値(0 - 480)

戻り値：なし

使い方
```
from webot import WeBot

webot = WeBot()
fault = webot.setMaxSpeed( 300 )
```
---

### getMaxSpeed()
出力できる最大値を取得します。

引数：なし

戻り値：設定値

使い方
```
from webot import WeBot

webot = WeBot()
max_speed = webot.getMaxSpeed( 300 )
```
---

### stop()
We-Botを停止します。

引数：なし
戻り値：なし

使い方
```
from webot import WeBot

webot = WeBot()
webot.stop()
```
---

### forward(speed)
We-Botを前進させます。

引数：
speed 前進する速度
戻り値：なし

使い方
```
from webot import WeBot

webot = WeBot()
webot.forward(480)
```
---

### back(speed)
We-Botを後進させます。

引数：
speed 前進する速度
戻り値：なし

使い方
```
from webot import WeBot

webot = WeBot()
webot.forward(480)
```
---

### left(speed)
We-Botをその場で左回転させます。

引数：
speed 回転する速度
戻り値：なし

使い方
```
from webot import WeBot

webot = WeBot()
webot.left(480)
```
---

### right(speed)
We-Botをその場で右回転させます。

引数：
speed 回転する速度
戻り値：なし

使い方
```
from webot import WeBot

webot = WeBot()
webot.right(480)
```
---

### readVoltage( port )
ADCのアナログ入力の電圧値を取得します。

引数：
port  取得する入力ポート指定( 0 - 3 )
戻り値：取得した電圧値（単位はV(ボルト)）

ポート番号と対応する入力は以下の通りです。

|ポート番号|対応|
----|----
|0 | アナログ入力1 |
|1 | アナログ入力2 |
|2 | バッテリー電圧 |
|3 | 5V電圧 |

使い方
```
from webot import WeBot

webot = WeBot()
battery = webot.readVoltage(2)
```
---


# 故障などの場合
故障が疑われる場合や保守部品の入手などは問い合わせ窓口までお問い合わせください。
https://raspberry-pi.ksyic.com/info/index

