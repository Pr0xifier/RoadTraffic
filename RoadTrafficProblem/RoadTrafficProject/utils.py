import configparser
from sumolib import checkBinary
import os
import sys


def import_train_configuration(config_file):
    """
    Read the config file regarding the training and import its content
    """
    content = configparser.ConfigParser()
    content.read(config_file)
    config = {'gui': content['simulation'].getboolean('gui'),
              'total_episodes': content['simulation'].getint('total_episodes'),
              'max_steps': content['simulation'].getint('max_steps'),
              'n_cars_generated': content['simulation'].getint('n_cars_generated'),
              'green_duration': content['simulation'].getint('green_duration'),
              'yellow_duration': content['simulation'].getint('yellow_duration'),
              'num_layers': content['model'].getint('num_layers'),
              'width_layers': content['model'].getint('width_layers'),
              'batch_size': content['model'].getint('batch_size'),
              'learning_rate': content['model'].getfloat('learning_rate'),
              'training_epochs': content['model'].getint('training_epochs'),
              'memory_size_min': content['memory'].getint('memory_size_min'),
              'memory_size_max': content['memory'].getint('memory_size_max'),
              'num_states': content['agent'].getint('num_states'),
              'num_actions': content['agent'].getint('num_actions'),
              'gamma': content['agent'].getfloat('gamma'),
              'models_path_name': content['dir']['models_path_name'],
              'sumocfg_file_name': content['dir']['sumocfg_file_name']}
    return config


def import_test_configuration(config_file):
    """
    Read the config file regarding the testing and import its content
    """
    content = configparser.ConfigParser()
    content.read(config_file)
    config = {'gui': content['simulation'].getboolean('gui'), 'max_steps': content['simulation'].getint('max_steps'),
              'n_cars_generated': content['simulation'].getint('n_cars_generated'),
              'episode_seed': content['simulation'].getint('episode_seed'),
              'green_duration': content['simulation'].getint('green_duration'),
              'yellow_duration': content['simulation'].getint('yellow_duration'),
              'num_states': content['agent'].getint('num_states'),
              'num_actions': content['agent'].getint('num_actions'),
              'sumocfg_file_name': content['dir']['sumocfg_file_name'],
              'models_path_name': content['dir']['models_path_name'],
              'model_to_test': content['dir'].getint('model_to_test')}
    return config


def set_sumo(gui, sumocfg_file_name, max_steps):
    """
    Configure various parameters for SUMO
    """
    # need to import python modules from the $SUMO_HOME/tools directory
    if 'SUMO_HOME' in os.environ:
        tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
        sys.path.append(tools)
    else:
        sys.exit("please declare environment variable 'SUMO_HOME'")

    # setting the cmd mode or the visual mode    
    if not gui:
        sumo_binary = checkBinary('sumo')
    else:
        sumo_binary = checkBinary('sumo-gui')
 
    # setting the cmd command to run sumo at simulation time
    sumo_cmd = [sumo_binary, "-c", os.path.join('intersection', sumocfg_file_name), "--no-step-log", "true", "--waiting-time-memory", str(max_steps)]

    return sumo_cmd


def set_train_path(models_path_name):
    """
    Create a new model path with an incremental integer, also considering previously created model paths
    """
    models_path = os.path.join(os.getcwd(), models_path_name, '')
    os.makedirs(os.path.dirname(models_path), exist_ok=True)

    dir_content = os.listdir(models_path)
    if dir_content:
        previous_versions = [int(name.split("_")[1]) for name in dir_content]
        new_version = str(max(previous_versions) + 1)
    else:
        new_version = '1'

    data_path = os.path.join(models_path, 'model_'+new_version, '')
    os.makedirs(os.path.dirname(data_path), exist_ok=True)
    return data_path 


def set_test_path(models_path_name, model_n):
    """
    Returns a model path that identifies the model number provided as argument and a newly created 'test' path
    """
    model_folder_path = os.path.join(os.getcwd(), models_path_name, 'model_'+str(model_n), '')

    if os.path.isdir(model_folder_path):    
        plot_path = os.path.join(model_folder_path, 'test', '')
        os.makedirs(os.path.dirname(plot_path), exist_ok=True)
        return model_folder_path, plot_path
    else: 
        sys.exit('Model number specified does not exist in the models folder')