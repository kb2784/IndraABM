from lru import LRU
from multiprocessing import Process, Pipe
from APIServer.model_api import run_model, create_model, create_model_for_test
from APIServer.api_utils import json_converter
import uuid

processManager = None

def createModelProcess(conn, model_id, payload, indra_dir):
    model = create_model(model_id, payload, indra_dir)
    conn.send(model)
    while True:
        periods = conn.recv()
        model.runN(int(periods))
        conn.send(model)

class ModelProcess:
    def __init__(self, process, parent_conn):
        self.process = process
        self.parent_conn = parent_conn

class ProcessManager:
    def __init__(self):
        print("Creating new process manager")
        self.processes = LRU(20)

    def spawn_model(self, model_id, payload, indra_dir):
        parent_conn, child_conn = Pipe()
        new_process = Process(target=createModelProcess, args=(child_conn, model_id, payload, indra_dir))
        mp = ModelProcess(new_process, parent_conn)
        exec_key = str(uuid.uuid4())
        self.processes[exec_key] = mp
        new_process.start()
        model = parent_conn.recv()
        model.exec_key = exec_key
        return model

    def run_model(self, exec_key, runtime):
        modelProcess = self.processes[exec_key]
        if(modelProcess is None):
            return None
        modelProcess.parent_conn.send(runtime)
        model = modelProcess.parent_conn.recv()
        model["exec_key"] = exec_key
        return model

processManager = ProcessManager()