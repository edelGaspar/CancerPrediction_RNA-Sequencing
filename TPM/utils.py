import numpy as np
import matplotlib.pyplot as plt
import cv2
import os
import json
import pickle

def learning_curve_plot(history, run_folders):
    plt.figure()
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.axis([0, history.epoch[-1], 0, max(history.history['loss'] + history.history['val_loss'])])
    plt.legend(['loss', 'val_loss'], loc='upper right')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.savefig(run_folders["model_path"] + run_folders["exp_name"]+"/viz/"+"training_loss.png")
    plt.close()

def create_environment(run_folders):
    # Creating base folders    
    if not os.path.exists(run_folders["model_path"]):
        os.makedirs(run_folders["model_path"])

    if not os.path.exists(run_folders["results_path"]):
        os.makedirs(run_folders["results_path"])

    # Preparing required I/O paths for each experiment
    if len(os.listdir(run_folders["model_path"])) == 0:
        exp_idx = 1
    else:
        exp_idx = len(os.listdir(run_folders["model_path"])) + 1

    exp_name = "exp_%04d" % exp_idx
    run_folders["exp_name"] = exp_name

    exp_model_folder = run_folders["model_path"] + os.sep + run_folders["exp_name"] + '/'
    exp_res_model = run_folders["results_path"] + os.sep + run_folders["exp_name"] + '/'

    try:
        os.mkdir(exp_model_folder)
    except:
        pass
    try:
        os.mkdir(exp_res_model)
    except:
        pass
    try:
        os.mkdir(os.path.join(exp_model_folder, 'viz'))
    except:
        pass
    try:
        os.mkdir(os.path.join(exp_model_folder, 'weights'))
    except:
        pass
    try:
        os.mkdir(os.path.join(exp_model_folder, 'images'))
    except:
        pass

def save_reconstructed_images(y_true, y_pred, run_folders):
    for i in range(0, y_pred.shape[0]):
        original = (y_true[i] * 255).astype("uint8")
        recon = (y_pred[i] * 255).astype("uint8")
        output = np.hstack([original, recon])
        cv2.imwrite(run_folders["results_path"] + run_folders["exp_name"] + "/image_" + str(i) + ".png", output)


def create_json(hyperparameters, run_folders):
    with open(run_folders["model_path"]+run_folders["exp_name"]+"/hyperparameters.json", 'w') as fp:
        json.dump(hyperparameters, fp)


def save_datasets(path, tag, dict_dfs):
    for df_name, dataset_data in dict_dfs.items():
        df_full_path = f'{path}/df_{df_name}_{tag}.pkl'  # Nombre del archivo de salida
        with open(df_full_path, 'wb') as df_file:
            pickle.dump(dataset_data, df_file)
            print(f'Data set {df_file} saved.')


def save_pickle_object(list_o, file_name):
    with open(file_name, 'wb') as file:
        pickle.dump(list_o, file)
    print(f"List of objects has been saved to {file_name}.")

def load_pickle_object(file_name):
    try:
        with open(file_name, 'rb') as file:
            list_o = pickle.load(file)
        print(f"List of objects has been loaded from {file_name}.")
        return list_o
    except FileNotFoundError:
        print(f"The file {file_name} does not exist.")
        return None
    except Exception as e:
        print(f"An error occurred while loading the file: {e}")
        return None