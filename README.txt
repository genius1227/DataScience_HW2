方法
本次作業屬於Time Series Analysis類型，找過幾個方法後決定使用FB所開發的fbprophet framework處理。


Data
1. 將training和testing合併，並從自動分配日期 2017/1/1 ~ ...。


作業使用方式
1. 請先依照env_setup安裝conda環境以及fbprophet套件，使用pip install prophet會遇到其他問題，故使用conda安裝最為方便。
2. 執行 python trader.py 或者 python trader.py --training "PATH TO YOUR TRAINING DATA(.csv should in the same directory)"  --testing "PATH TO YOUR TESTING DATA(.csv should in the same directory)" --output "OUTPUT FILE NAME(.csv in the same directory)"
3. 輸出output.csv，19次預測隔日結果所進行的當日操作。