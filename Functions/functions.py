import bpy
import subprocess
import json
import os, signal


O = bpy.ops


def select_object(self, obj):
    C = bpy.context
    O = bpy.ops
    try:
        O.object.select_all(action='DESELECT')
        C.view_layer.objects.active = obj
        obj.select_set(True)
    except:
        self.report({'INFO'}, "Object {} not in View Layer".format(obj.name))
    
def select_object_by_mat(self, mat):
    obj_found = None
    D = bpy.data
    for obj in D.objects:
        if obj.type != "MESH":
            continue
        object_materials = [slot.material for slot in obj.material_slots]
        if mat in object_materials:
            obj_found = obj
            select_object(self, obj)

def get_config_file():
    script_file = os.path.realpath(__file__)
    script_dir = os.path.dirname(script_file)
    process_list_path = os.path.join(script_dir , '..',"Server\process_list.json")
    return process_list_path

def start_server(server_file_path,file_path,port):
    
    process_list_path = get_config_file()
    
    # read pid from file
    with open(process_list_path) as f:
        pid_list = json.load(f)

    if len(pid_list)>0:
        cleaned_pid_list = stop_server()
        pid_list = cleaned_pid_list
    
    server_process = subprocess.Popen([bpy.app.binary_path_python, server_file_path, file_path,str(port)])
    pid_list.append(server_process.pid)
    
    # write pid to file
    with open(process_list_path,'w') as f:
         json.dump(pid_list, f)

def stop_server():
    
    process_list_path = get_config_file()

    # read pid from file
    with open(process_list_path) as f:
        pid_list = json.load(f)
        
    for pid in pid_list:
        try:
            os.kill(pid, signal.SIGTERM)
            pid_list.remove(pid)
            print("Closed process " + str(pid))
        except OSError:
            continue
    

    # write pid to file
    with open(process_list_path,'w') as f:
         json.dump(pid_list, f)
         
    return pid_list


def convert_umlaut(str):
    spcial_char_map = {ord('ä'):'ae', ord('ü'):'ue', ord('ö'):'oe', ord('ß'):'ss'}
    return str.translate(spcial_char_map)

