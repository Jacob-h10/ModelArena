#scans user hardware for cpu, gpu, ram, vram, os
#append data to formatted json

#imports
import platform
import psutil
import cpuinfo
import GPUtil

def get_hardware_info():
    info = cpuinfo.get_cpu_info()

    cpu = info['brand_raw']

    gb_size = round(psutil.virtual_memory().total / (1024 ** 3))
    gb_size = f"{gb_size:.2f}"

    #get gpu
    gpu_specs = GPUtil.getGPUs()
    for gpu in gpu_specs:
        gpu = gpu.name

    #finding os
    def get_os():
        if platform.system() == "Windows":
            windows_version = platform.release()
            if windows_version == "10":
                _, _, build, _ = platform.win32_ver()
                build_suffix = build.split(".")[-1]
                numeric_build = "".join(filter(str.isdigit, build_suffix))

                if numeric_build and int(numeric_build) >= 22000:
                    return "Windows 11"
                else:
                    return "Windows 10"
            
            elif windows_version == "7":
                return "Windows 7"
        elif platform.systems() == "Darwin":
            mac_version = platform.mac_ver()[0]
            return mac_version
        else:
            return "Linux"



    #bundle variables
    hardware = {"CPU": str(cpu), "RAM": str(gb_size), "Graphics Card": str(gpu), "Operating System": str(get_os())}

    return hardware
