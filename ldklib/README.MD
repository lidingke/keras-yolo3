这是工具集合的工作目录，比较成熟的封装好的库都在ldklib里面。

iou.py是计算iou的库。

voc_xml是导入导出VOC格式的xml信息的，常用来操作Annotations文件夹下的xml。
是按照VOC格式的目标检测框选文件的格式适配的。

docker_models是几个模型的docker版本调用接口的父类。使用的demo一般放在/docker_demo文件夹内。

grpc_install.ipynb是几个模型的grpc的安装脚本。