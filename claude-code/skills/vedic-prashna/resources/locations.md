# Prashna 提问地：时区与城市坐标

> **用途**：用户只给城市名、需要查 IANA 时区或经纬度时读。数据表，不含判读规则。

## 1. 提问地 → 时区

### 1.1 亚洲

| 地区 | IANA tz |
|---|---|
| 中国大陆(全境同 tz) | Asia/Shanghai |
| 中国台湾 | Asia/Taipei |
| 中国香港 | Asia/Hong_Kong |
| 中国澳门 | Asia/Macau |
| 日本 | Asia/Tokyo |
| 韩国 | Asia/Seoul |
| 朝鲜 | Asia/Pyongyang |
| 蒙古 | Asia/Ulaanbaatar |
| 新加坡 | Asia/Singapore |
| 马来西亚 | Asia/Kuala_Lumpur |
| 印尼西部(雅加达) | Asia/Jakarta |
| 印尼东部(巴厘岛/望加锡) | Asia/Makassar |
| 泰国 | Asia/Bangkok |
| 越南 | Asia/Ho_Chi_Minh |
| 菲律宾 | Asia/Manila |
| 印度 | Asia/Kolkata |
| 巴基斯坦 | Asia/Karachi |
| 阿联酋(迪拜) | Asia/Dubai |
| 沙特 | Asia/Riyadh |
| 以色列 | Asia/Jerusalem |
| 土耳其 | Europe/Istanbul |

### 1.2 欧洲

| 地区 | IANA tz |
|---|---|
| 英国 | Europe/London |
| 爱尔兰 | Europe/Dublin |
| 法国/德国/意大利/西班牙/荷兰 | Europe/Paris / Berlin / Rome / Madrid / Amsterdam |
| 俄罗斯莫斯科 | Europe/Moscow |
| 瑞士 | Europe/Zurich |
| 北欧(挪威/瑞典/丹麦/芬兰) | Europe/Oslo / Stockholm / Copenhagen / Helsinki |
| 希腊 | Europe/Athens |
| 波兰 | Europe/Warsaw |
| 乌克兰 | Europe/Kyiv |

### 1.3 美洲

| 地区 | IANA tz |
|---|---|
| 美东(纽约/波士顿/迈阿密/华盛顿) | America/New_York |
| 美中(芝加哥/达拉斯/休斯顿) | America/Chicago |
| 美西山地(丹佛) | America/Denver |
| 美西太平洋(旧金山/西雅图/洛杉矶) | America/Los_Angeles |
| 阿拉斯加 | America/Anchorage |
| 夏威夷 | Pacific/Honolulu |
| 加拿大多伦多 | America/Toronto |
| 加拿大温哥华 | America/Vancouver |
| 墨西哥城 | America/Mexico_City |
| 巴西圣保罗 | America/Sao_Paulo |
| 阿根廷 | America/Argentina/Buenos_Aires |
| 智利 | America/Santiago |

### 1.4 大洋洲 / 非洲

| 地区 | IANA tz |
|---|---|
| 澳东(悉尼/墨尔本) | Australia/Sydney |
| 澳中(阿德莱德) | Australia/Adelaide |
| 澳西(珀斯) | Australia/Perth |
| 新西兰 | Pacific/Auckland |
| 南非(约翰内斯堡/开普敦) | Africa/Johannesburg |
| 埃及 | Africa/Cairo |
| 尼日利亚 | Africa/Lagos |

**默认策略**：地点或时区无法确定时停止起盘并澄清。不得用机器时区冒充提问地时区。
用户说“现在”时，必须在提问地 IANA 时区于用户提出问题时捕获当前墙上钟时间，
保留秒和可用的小数秒；禁止等到处理或排盘开始后另取整分钟。

---

## 2. 提问地 → (lat, lon) 高频城市

以下坐标只用于用户仅报城市名时的中心点近似（取象单 `location` 记 `city`）。

| 城市 | (lat, lon) |
|---|---|
| 北京 | (39.90, 116.41) |
| 上海 | (31.23, 121.47) |
| 广州 | (23.13, 113.26) |
| 深圳 | (22.54, 114.06) |
| 成都 | (30.67, 104.07) |
| 杭州 | (30.27, 120.15) |
| 南京 | (32.06, 118.80) |
| 武汉 | (30.60, 114.30) |
| 重庆 | (29.56, 106.55) |
| 西安 | (34.34, 108.94) |
| 香港 | (22.30, 114.17) |
| 台北 | (25.03, 121.57) |
| 东京 | (35.68, 139.65) |
| 大阪 | (34.69, 135.50) |
| 首尔 | (37.57, 126.98) |
| 新加坡 | (1.35, 103.82) |
| 曼谷 | (13.76, 100.50) |
| 吉隆坡 | (3.14, 101.69) |
| 雅加达 | (-6.21, 106.85) |
| 德里 | (28.61, 77.21) |
| 孟买 | (19.08, 72.88) |
| 迪拜 | (25.20, 55.27) |
| 伦敦 | (51.51, -0.13) |
| 巴黎 | (48.86, 2.35) |
| 柏林 | (52.52, 13.40) |
| 罗马 | (41.90, 12.50) |
| 莫斯科 | (55.75, 37.62) |
| 纽约 | (40.71, -74.01) |
| 洛杉矶 | (34.05, -118.24) |
| 旧金山 | (37.77, -122.42) |
| 芝加哥 | (41.88, -87.63) |
| 多伦多 | (43.65, -79.38) |
| 温哥华 | (49.28, -123.12) |
| 悉尼 | (-33.87, 151.21) |
| 墨尔本 | (-37.81, 144.96) |
| 奥克兰 | (-36.85, 174.76) |

**未收录城市**：优先取得实际城市或经纬度。使用最近城市近似时必须显式标记；
判读按所给的时间地点为准，前后误差只在核对区记输入提示（`judgment-rubric.md` §13），不因此追问用户或停止判读。
