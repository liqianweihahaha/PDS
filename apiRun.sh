@echo off
echo 开始清除日志
@echo on

del /f /s /q  D:\speedaf_pds_api\report\tmp\*.json
del /f /s /q  D:\speedaf_pds_api\report\tmp\*.jpg
del /f /s /q  D:\speedaf_pds_api\report\report


@echo off
echo 日志清除完毕
@echo on


cd D:/speedaf_pds_api/testCase
pytest -s --alluredir=../report/tmp
allure generate ../report/tmp -o ../report/report  --clean


@echo off
echo 任务执行结束
@echo on