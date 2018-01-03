# 計算理論Telegram Bot Project
          F74046373  柯采妍
### Link to my Bot
- [bot link](http://t.me/Work_Search_bot)

### My FSM
![](https://i.imgur.com/Pu6NRcs.png)


### 運行指令
`./ngrok http -bind-tls=true 8888`
`python3 bot.py`

### How to react with my Bot
- 第一次執行bot時，以`/start`指令開啟服務
- 順利啟動會得到三個功能選項按鈕
    1. `info`: 前往說明頁面
    2. `search`: 使用搜尋功能
    3. `recommend`: 使用推薦功能
- 在所有狀態下使用`/restart`指令可以重新開始
#### **search**:
    step1. 輸入要搜尋的人事物 ex: 天海祐希
    step2. 選擇頁面語言
    step3. 得到結果, 重新返回step1
    
#### **recommend**
    step1. 選擇想要演員推薦或是作品推薦
    step2. 得到結果
    step3. 選擇是否連結至維基百科
    step4. 得到結果, 重新返回step1

### 使用技術
- 網頁爬蟲
- send photo
- inline keyboard
