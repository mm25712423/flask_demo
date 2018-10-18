import psutil
import time
import os
import pynvml


def getDockerInfo():
    try:
        import docker
        client = docker.from_env()
        infos = client.info()
    except:
        return

    result = dict()
    result.update({'os': infos['OperatingSystem']})
    result.update({'total_container': infos['Containers']})
    result.update({'stop_container': infos['ContainersStopped']})
    result.update({'run_container': (infos['Containers'] - infos['ContainersStopped'])})
    result.update({'kernel_version': infos['KernelVersion']})
    result.update({'server_version': infos['ServerVersion']})
    result.update({'num_images': infos['Images']})

    return result


def getContainerInfo():
    try:
        import docker
        client = docker.from_env()
        infos = client.info()
    except:
        return None, None

    gpu_result = []
    cpu_result = []
    client = docker.APIClient(base_url='unix://var/run/docker.sock')
    containers = client.containers(size=True)

    for container in containers:
        res = dict()
        mount = []
        port = []
        res.update({'name': container['Names']})
        res.update({'image': container['Image']})
        res.update({'status': container['Status']})
        res.update({'extra_size': container['SizeRw']})
        res.update({'vistual_size': container['SizeRootFs']})
        for i in range(len(container['Mounts'])):
            mount_dict = dict()
            mount_dict.update({'source': container['Mounts'][i].get('Source')})
            mount_dict.update({'destination': container['Mounts'][i].get('Destination')})
            mount.append(mount_dict)

        for i in range(len(container['Ports'])):
            port_dict = dict()
            port_dict.update({'private_port': container['Ports'][i].get('PrivatePort')})
            port_dict.update({'public_port': container['Ports'][i].get('PublicPort')})
            port.append(port_dict)

        res.update({'mount': mount})
        res.update({'port': port})

        if (container['Labels'] is not None):
            res.update({'cuda': container['Labels'].get('com.nvidia.cuda.version')})
            res.update({'cudnn': container['Labels'].get('com.nvidia.cudnn.version')})
            gpu_result.append(res)
        else:
            cpu_result.append(res)

    return gpu_result, cpu_result


def getCpuInfo():
    result = dict()
    result.update({'usage': psutil.cpu_percent(interval=0.5)})
    result.update({'core': psutil.cpu_count(logical=True)})
    result.update({'logicial': psutil.cpu_count(logical=False)})

    return result


def getMemoryInfo():
    result = dict()
    result.update({'total': psutil.virtual_memory().total})
    result.update({'used': psutil.virtual_memory().used})
    result.update({'free': psutil.virtual_memory().free})
    result.update({'usage': psutil.virtual_memory().percent})

    return result


def getDiskInfo():
    disks = psutil.disk_partitions()
    result = dict()
    for path in disks:
        res = dict()
        try:
            dev = psutil.disk_usage(os.path.abspath(path.device))
            res.update({'total': dev.total})
            res.update({'used': dev.used})
            res.update({'free': dev.free})
            res.update({'usage': dev.percent})
            result.update({path.device: res})
        except:
            continue
    return result


def getNetworkInfo():
    network = psutil.net_io_counters(pernic=True)
    ifaces = psutil.net_if_addrs()
    networks = list()
    for k, v in ifaces.items():
        for val in v:
            ip = val.address
            print(ip)
            data = network[k]
            ifnet = dict()
            ifnet['ip'] = ip
            ifnet['iface'] = k
            ifnet['sent'] = '%.2fMB' % (data.bytes_sent / 1024 / 1024)
            ifnet['recv'] = '%.2fMB' % (data.bytes_recv / 1024 / 1024)
            ifnet['packets_sent'] = data.packets_sent
            ifnet['packets_recv'] = data.packets_recv
            ifnet['errin'] = data.errin
            ifnet['errout'] = data.errout
            ifnet['dropin'] = data.dropin
            ifnet['dropout'] = data.dropout
            networks.append(ifnet)

    return networks


def getGpuInfo():
    pynvml.nvmlInit()
    deviceCount = pynvml.nvmlDeviceGetCount()
    result = list()
    for i in range(deviceCount):
        handle = pynvml.nvmlDeviceGetHandleByIndex(i)
        util = pynvml.nvmlDeviceGetUtilizationRates(handle)
        mem = pynvml.nvmlDeviceGetMemoryInfo(handle)
        info_dict = {
            'util': int(util.gpu),
            'mem': {'total': int(mem.total), 'free': int(mem.free), 'used': int(mem.used)}
        }

        result.append(info_dict)

    return result
