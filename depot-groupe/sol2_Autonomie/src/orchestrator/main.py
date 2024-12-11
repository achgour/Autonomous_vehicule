import asyncio
from fastapi import Body, FastAPI, Query
from typing import List, Optional, Union, Annotated
from pydantic import BaseModel
import contextlib
import threading
import json
import uvicorn
import time
import socket
import os
import logging
import requests
import argparse
from logger import setup_logger,setup_loggers

class Config:
    socket_path = "orchestrator.sock"
    
    def __init__(self, file : str = "server_params.json"):
        
        params = json.load(open(file))
        self.name : str = params["name"]
        self.robot_list : Union[dict,None] = params["robot_list"]
        self.robot_priority : list[str] = params["robot_priority"]

def getConfig():
    global config
    return config

# ---------------------------------------------------------------------------- #
#                           UNIX Socket to the robot                           #
# ---------------------------------------------------------------------------- #

class ClientSocket:
    """Client class for UNIX Socket used multiple times"""

    def __init__(self, socket_path: str, logger: str):
        """Constructor for ClientSocket class

        Args:
            socket_path (str): path to the file for the UNIX Socket
            logger (str): Name for the logger (from logging)
        """
        self.logger = setup_logger(logger)
        self.Socket = socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
        self.Socket.connect(socket_path)
        self.connection:socket.socket = None
        # This flag is used to stop the listening thread
        self.should_stop = False
        while not (os.path.exists(socket_path)):
            pass  # While the socket server doesn't exist
        self.logger.info("Connected to UNIX Socket")
        self.should_stop = False

    def stop(self):
        self.should_stop = True
        # We need to close the connection to avoid a deadlock
        if self.connection:
            self.connection.close()        

    def listen(self):
        """Get data sent on the UNIX Socketx
        """
        self.logger.debug("Entering listen")
        while not self.should_stop:
            data = (self.connection.recv(1024)).decode("utf-8")
            # self.logger.debug("Request received: " + data)
            data = data.split()
            
    def send(self, request: str):
        self.Socket.sendall(request.encode("utf-8"))

class Orchestrator(uvicorn.Server):
    def install_signal_handlers(self):
        pass
    # Allow uvicorn to run in a thread
    @contextlib.contextmanager
    def run_in_thread(self, config: Config):
        thread = threading.Thread(target=self.run)
        thread.start()
        try:
            while not self.started:
                time.sleep(1e-3)
            yield
        finally:
            self.should_exit = True
            thread.join()
            
# ---------------------------------------------------------------------------- #
#                                  Game Logic                                  #
# ---------------------------------------------------------------------------- #

class GameStatus:
    def __init__(self):
        self.marker_map = [int]*6
        self.robots_role = [str]
        self.logic = None   
    
    def setMarkerMap(self, map):
        self.marker_map = map

class Logic:
    
    ST_INIT = 0
    ST_ELECT_ROBOT = 1
    ST_COMPARE_ROBOTS_ROLE = 2
    
    def __init__(self, orchestrator_socket: ClientSocket, game_status: GameStatus, config: Config):
        self.logger = setup_logger("Logic")
        self.lastInstructionTime = 0.0
        self.currentTime = 0.0
        self.currentDeltaTimeWait = 0.0
        self.currentState = Logic.ST_INIT
        self.oSock = orchestrator_socket
        self.GS = game_status
        self.config = config
        
        # ------------------------------- elect_robot() ------------------------------ #
        self.er_list=self.config.robot_priority.copy()
        
        # --------------------------- compare_robots_role() -------------------------- #
        self.crr_list = self.GS.robots_role.copy()
    
    
    def elect_robot(self):
        if len(self.er_list) == 0:
            if self.currentTime - self.lastInstructionTime > self.currentDeltaTimeWait:
                self.currentState = Logic.ST_COMPARE_ROBOTS_ROLE
        else:
            robot = self.er_list[0]
            try:
                r = requests.get(f"http://{self.config.robot_list[robot]}/ping", timeout=2)
            except requests.exceptions.ReadTimeout:
                self.logger.warning(f"Robot {robot} is not responding")
            else:
                if r.status_code == 200:
                    self.logger.info(f"Robot {robot} is alive")
                    self.GS.robots_role.append(robot)
                    self.er_list.pop(0)
            if len(self.er_list) == 0:
                self.currentDeltaTimeWait = 2.0
                self.lastInstructionTime = self.currentTime

    def compare_robots_role(self):
        if len(self.crr_list) == 0:
            if self.currentTime - self.lastInstructionTime > self.currentDeltaTimeWait:
                self.currentState = Logic.ST_WAITING_MAP
        else:
            robot = self.crr_list[0]
            try:
                r = requests.post(f"http://{self.config.robot_list[robot]}/compare-robots-role", json=self.GS.robots_role, timeout=5)
            except requests.exceptions.ReadTimeout:
                self.logger.warning(f"Robot {robot} is not responding")
                self.currentState = Logic.ST_REDO_ELECT_ROBOT # TODO
            else:
                if r.status_code == 200:
                    self.logger.info(f"Robot {robot} has same roles")
                    self.crr_list.pop(0)
            if len(self.crr_list) == 0:
                self.currentDeltaTimeWait = 2.0
                self.lastInstructionTime = self.currentTime

def logic_loop(orchestrator_socket: ClientSocket, orchestrator_logger: logging.Logger):
    last_health_check_time = time.time()
    logic = Logic(orchestrator_socket, game_status, config)
    game_status.logic = logic
    while True:
        current_time = time.time()
        if current_time>last_health_check_time:
            last_health_check_time = current_time
            logic.currentTime = current_time

        # ---------------------------------- States ---------------------------------- #
        if logic.currentState == Logic.ST_INIT:
            logic.er_list=logic.config.robot_priority.copy()
            logic.currentState = Logic.ST_ELECT_ROBOT
        elif logic.currentState == Logic.ST_ELECT_ROBOT:
            logic.elect_robot()
        elif logic.currentState == Logic.ST_COMPARE_ROBOTS_ROLE:
            logic.compare_robots_role()

# ---------------------------------------------------------------------------- #
#                               Orchestrator API                               #
# ---------------------------------------------------------------------------- #

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello group 2!"}

# ------------------------------ Preparing Game ------------------------------ #

class MarkerMap(BaseModel):
    map: list[int]
    
class RoleList(BaseModel):
    roles: list[str]

@app.get("/ping")
async def get_pinged():
    """Returns the name of the robot to check if he is alive"""
    return {"name": config.name}
    
@app.post("/compare-robots-role")
async def post_compare_robots_role(robots_role: RoleList = Body()):
    if robots_role:
        if game_status.robots_role == robots_role:
            return {"message": "OK"}
        else:
            return {"message": "Not the same list"}, 406
    else:
        return {"message": "Missing robots role"}, 400
    
@app.get("/redo-elect-robot")
async def get_redo_elect_robot():
    """Tell a robot to redo the elect robot"""
    if game_status.logic:
        game_status.logic.currentState = Logic.ST_INIT
        return {"message": "OK"}
    else:
        return {"message": "Logic not initialized"}, 500

@app.post("/marker-map")
async def post_marker_map(marker_map: Annotated[MarkerMap, Body()]):
    """Tell a robot what is the current marker map"""
    if marker_map:
        game_status.setMarkerMap(marker_map)
        return {"message": "OK"}
    else:
        return {"message": "Missing marker map"}, 400

# -------------------------------- Collisions -------------------------------- #
@app.post("/collision/seen")
async def post_collision_seen():
    """Tell a robot that he has seen a collision"""
    return {"message": "OK"}

# ------------------------------- Human Control ------------------------------ #
@app.get("/human-control/start")
async def get_human_control_start():
    """Start the robot array"""
    return {"message": "OK"}


# ---------------------------------------------------------------------------- #
#                                   mainloop                                   #
# ---------------------------------------------------------------------------- #

def mainloop(config: Config, game_status: GameStatus, no_socket: bool):
    setup_loggers()
    orchestrator_logger = setup_logger("Orchestrator")
    orchestrator_logger.info("Starting Orchestrator")
    
    uvconfig = uvicorn.Config("main:app", host="127.0.0.1", port=5000, log_level="info")
    server = Orchestrator(config=uvconfig)

    with server.run_in_thread(config):
        if not(no_socket):
            while not(os.path.exists(Config.socket_path)):
                pass
            orchestrator_socket = ClientSocket(Config.socket_path, "Orchestrator")
            
            # Start the listening thread
            orchestrator_socket.logger.debug("Thread Listening")
            orchestrator_listening = threading.Thread(target=orchestrator_socket.listen)
            orchestrator_listening.start()
        else:
            orchestrator_socket = None
            orchestrator_listening = None
    
        # List of early exit flags
        # 0     normal exit
        # -1    CTRL-C catched
        early_exit_flag = 0
        while True:
            try:
                logic_loop(orchestrator_socket,orchestrator_logger)
                break
            except KeyboardInterrupt:
                early_exit_flag = -1
                break
            except Exception as e:
                orchestrator_logger.error(e)
                # TODO: Don't raise in production, continue instead
                raise e
                continue

    if not early_exit_flag:
        orchestrator_logger.debug("The program exited normally")
    else:
        orchestrator_logger.warning(f"The program exited early with code ({early_exit_flag})")

    orchestrator_socket.stop()
    orchestrator_listening.join()
    exit(0)
    

if __name__ == "__main__":
    # ---------------------------------- parser ---------------------------------- #
    parser = argparse.ArgumentParser(description="Orchestrator")
    parser.add_argument("--params", type=str, default="server_params.json", help="Path to the parameters file")
    parser.add_argument("--nosocket", action=argparse.BooleanOptionalAction, help="Don't use UNIX Socket")
    args = parser.parse_args()
    
    params_file = os.path.join(os.path.dirname(__file__), args.params)
    config = Config(file=params_file)
    game_status = GameStatus()
    
    mainloop(config, game_status, args.nosocket)
    