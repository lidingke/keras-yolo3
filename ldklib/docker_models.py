import docker
import grpc
import ctpn_pb2
import ctpn_pb2_grpc
import yolo_pb2
import yolo_pb2_grpc
import crnn_pb2
import crnn_pb2_grpc
import cv2
import json
import numpy as np

class CTPN_Docker(object):

    def __init__(self,docker_client = 'unix://var/run/docker.sock',
                    host_port = 'localhost:50053',run_args=None,run_kwargs=None):
        self.client = docker.DockerClient(base_url=docker_client)
        channel = grpc.insecure_channel(host_port)
        self.stub = ctpn_pb2_grpc.ModelStub(channel)
        self.run_args = run_args if run_args else []
        self.run_kwargs = {'image': "trnet/ctpn:1.0.1",
                           'runtime': 'nvidia',
                           "command" : "python rpc/server.py",
                           'environment': ["CUDA_VISIBLE_DEVICES=1"],
                           'ports': {'50051/tcp': '50053'},
                           'detach': True,
                           'auto_remove': True}
        if run_kwargs:
            self.run_kwargs.update(run_kwargs)
#         pass
    
    def run(self,img):
        assert isinstance(img,np.ndarray), 'img must be a numpy array.'
        imgstr = img.tobytes()
        shape = json.dumps(img.shape)
#         stub = ctpn_pb2_grpc.ModelStub(grpc.insecure_channel('localhost:50051'))
        response = self.stub.predict(ctpn_pb2.rect_request(img=imgstr, shape=shape))
        return json.loads(response.message)

    def __enter__(self):
        self.container = self.client.containers.run(*self.run_args,**self.run_kwargs)
        for line in self.container.logs(stream=True):
            if line.strip().find(b'grpc_server_start') >= 0:
                break
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.container.stop()
        print('container has stopped.')
        
        
class YOLO_Docker(object):

    def __init__(self,docker_client = 'unix://var/run/docker.sock',
                    host_port = 'localhost:50053'):
        self.client = docker.DockerClient(base_url=docker_client)
        channel = grpc.insecure_channel(host_port)
        self.stub = yolo_pb2_grpc.YOLOModelStub(channel)
        self.run_args = []
        self.run_kwargs = {'image' : "yolo_server",
                    'runtime':'nvidia',
                    'environment' : ["CUDA_VISIBLE_DEVICES=1"],
                    'ports' : {'50051/tcp':'50053'},
                    'detach':True,
                    'auto_remove' : True}


    def run(self,img):
        assert isinstance(img,np.ndarray), 'img must be a numpy array.'
        imgstr = img.tobytes()
        shape = json.dumps(img.shape)
        response = self.stub.predict(yolo_pb2.rect_request(img=imgstr, shape=shape))
        return json.loads(response.message)

    def __enter__(self):
        self.container = self.client.containers.run(*self.run_args,**self.run_kwargs)
        for line in self.container.logs(stream=True):
            if line.strip() == b'grpc_server_start':
                break
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.container.stop()
        print('container has stopped.')


class CRNN_Docker(object):
    """
    __init__
    :param docker_client:unix://var/run/docker.sock
    :param host_port:'localhost:50053'
    :param run_args:[]
    :param run_kwargs:default-
        'image': "trnet/crnn:1.0.2",
        'runtime': 'nvidia',
        "command" : "python server.py",
        'environment': ["CUDA_VISIBLE_DEVICES=1"],
        'ports': {'50054/tcp': '50054'},
        'detach': True,
        'auto_remove': True
    """

    def __init__(self, docker_client='unix://var/run/docker.sock',
                 host_port='localhost:50054',run_args=None,run_kwargs=None):

        self.client = docker.DockerClient(base_url=docker_client)
        channel = grpc.insecure_channel(host_port)
        self.stub = crnn_pb2_grpc.GreeterStub(channel)
        self.run_args = run_args if run_args else []
        self.run_kwargs = {'image': "trnet/crnn:1.0.2",
                           'runtime': 'nvidia',
                           "command" : "python server.py",
                           'environment': ["CUDA_VISIBLE_DEVICES=0"],
                           'ports': {'50054/tcp': '50054'},
                           'detach': True,
                           'auto_remove': True}
        if run_kwargs:
            self.run_kwargs.update(run_kwargs)
        # self.run_kwargs = default_k



    def run(self,im):
        assert isinstance(im,np.ndarray), 'img must be a numpy array.'
        shape = json.dumps(im.shape)
        ymax, xmax, _ = im.shape
        xmin, ymin = 0, 0
        boxline = xmin, ymin, xmax, ymax
        box = json.dumps([boxline])
        response = self.stub.idc_crnn(crnn_pb2.CrnnRequest(img=im.tobytes(), shape=shape, box_list=box))
        return response.message

    def __enter__(self):
        self.container = self.client.containers.run(*self.run_args,**self.run_kwargs)
        for line in self.container.logs(stream=True):
            # print(line)
            if line.strip().find(b'crnn_serve_start') >= 0:
                break
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.container.stop()
        print('container has stopped.')