**本项目用于爬取ncbi的xml文件形式的数据**

**事先提醒，若担心数据量太大，代码中间报错，可以自己进行分批次处理，每次将n条数据（例如200条）复制到"待处理.xlsx"文件中然后运行代码。**

# 操作步骤

1.下载项目文件

2.配置环境

  pip install requests
  
  pip install bs4
  
  pip install pandas
  
  pip install tqdm
  
  pip install openpyxl
  
3.更改cookie（此步骤非必须，若下载不到结果可能是因为cookie的问题，可以尝试添加此步骤）

  1）打开浏览器
  
  2）打开开发者工具（按F12），选择Network
  ![image](https://github.com/user-attachments/assets/c76e724b-1640-4140-ade8-235d07cb45b5)

  3）打开网站https://www.ncbi.nlm.nih.gov/pmc/?term=content
  此时Network里可以看到很多网络请求信息

  4）按照图片找到cookie的值，复制
  ![image](https://github.com/user-attachments/assets/a31d5f10-ecb7-4839-ae17-5c6191060c72)

  5）将刚刚复制的cookie粘贴到代码中替换掉原来的cookie值
  ![image](https://github.com/user-attachments/assets/a1aad84c-6e94-405b-84ee-1cad00c7ed5e)

4.将要下载的数据的期刊名和搜索词复制到"待处理.xlsx"文件中，该文件包括第一行的标题"name"及各年份，以及复制进来的期刊名和搜索词
![image](https://github.com/user-attachments/assets/ec6e75fd-2d2e-4fd1-86fb-b5a8f58f8248)
5.执行代码

6.下载的结果在results文件夹中

7.有问题的下载信息会记录在error_location_response.txt和error_xml_response.txt文件中，可以查看到具体是哪条数据没下载成功，可以与results中的结果进行比较进行确认，没下载成功的数据可以手动下载，也可以询问我原因



