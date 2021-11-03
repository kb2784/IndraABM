from lru import LRU
from multiprocessing import Process, Pipe, cpu_count
from APIServer.model_api import run_model, create_model, create_model_for_test
from APIServer.api_utils import json_converter
from APIServer.model_process import createModelProcess, Message, CommunicationType
import uuid

modelManager = None

class ProcessPipePair:
    def __init__(self, process, parent_conn):
        self.process = process
        self.parent_conn = parent_conn

class ModelManager:
    def __init__(self):
        print("Creating new model manager")
        self.processes = LRU(cpu_count() * 5 + 1)       # Not too many processes but also not too less

    def spawn_model(self, model_id, payload, indra_dir):
        parent_conn, child_conn = Pipe()
        exec_key = str(uuid.uuid4())
        new_process = Process(target=createModelProcess, args=(child_conn, model_id, payload, indra_dir))
        mp = ProcessPipePair(new_process, parent_conn)
        self.processes[exec_key] = mp
        new_process.start()
        model = parent_conn.recv()
        model.exec_key = exec_key
        return model

    def run_model(self, exec_key, runtime):
        modelProcess = self.processes[exec_key]
        if(modelProcess is None):
            return None
        message = Message(CommunicationType.RUN_MODEL, {runtime})
        modelProcess.parent_conn.send(message)
        model = modelProcess.parent_conn.recv()
        model.exec_key = exec_key
        return model

modelManager = ModelManager()