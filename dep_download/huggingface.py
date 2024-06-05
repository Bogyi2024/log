#@title 1. Login to Huggingface hub
try:
  hub_ok # My packaged dep didn't contains this (but stil have the folder)
except:
  print("Setting up huggingface_hub...")
  !pip install --force-reinstall -qqqq huggingface_hub
  hub_ok = True
from IPython.display import clear_output
from huggingface_hub import login
clear_output()

#@markdown 1. Of course, you need a Huggingface account first.
#@markdown 2. To create a huggingface token, go to [this link](https://huggingface.co/settings/tokens), then `create new token` or copy available token with the `Write` role.

write_token = "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" #@param {type:"string"}
login(write_token, add_to_git_credential=True)

from huggingface_hub.utils import validate_repo_id, HfHubHTTPError
from huggingface_hub import HfApi


api = HfApi()
user = api.whoami(write_token)

#@markdown #### If your model repo didn't exist, it will automatically create your repo.
repo_name = "my_downloads" #@param{type:"string"}
make_this_repo_private_if_not_exist = False #@param{type:"boolean"}
clone_with_git = True #@param{type:"boolean"}

model_repo = user['name']+"/"+repo_name.strip()

validate_repo_id(model_repo)

if repo_name != "":
  try:
      api.create_repo(repo_id=model_repo,
                      private=make_this_repo_private_if_not_exist)
      print("Model Repo didn't exists, creating repo")
      print("Model Repo: ",model_repo,"created!\n")

  except HfHubHTTPError as e:
      print(f"Model Repo: {model_repo} exists, skipping create repo\n")

if clone_with_git:
  !git lfs install --skip-smudge
  !export GIT_LFS_SKIP_SMUDGE=1
  !git clone https://huggingface.co/{model_repo} /content/{repo_name}


#-->Start

import os
import sys
import ipywidgets as widgets
from IPython.display import clear_output
from huggingface_hub import HfApi, login
from huggingface_hub.utils import validate_repo_id, HfHubHTTPError
from IPython.utils import capture


paths_map = {
    "Models" : "/content/sdw/models/Stable-diffusion",
    "VAEs" : "/content/sdw/models/VAE",
    "LORAs" : "/content/sdw/models/Lora",
    "Embeddings" : "/content/sdw/embeddings",
    "Hypernetworks" : "/content/sdw/models/hypernetworks",
}

#@title  3.1 Upload via huggingface_hub (Fun way)
#@markdown ## **How to use this?**<br>
#@markdown 1. Run this cell after you ran the login cell
#@markdown 2. Select model you want to upload (use `ctrl/shift` for multiple selection)
#@markdown 3. Click on upload button
folder = "Models" #@param ["Models", "VAEs", "LORAs", "Embeddings", "Hypernetworks"]
commit_message = "Upload with Google Colab"  #@param{type:"string"}

models_path = paths_map[folder]
upload_path = '/content/upload_models'

api = HfApi()
username_repo = user['name']+"/"+repo_name.strip()
validate_repo_id(username_repo)

def get_file_list(path):
  res = []
  for (dir_path, dir_names, file_names) in os.walk(path):
      res.extend(file_names)
  return res

selected = widgets.SelectMultiple(
    options=get_file_list(models_path),
    rows=10,
    disabled=False,
)

button = widgets.Button(
    description='Upload',
    disabled=False,
    button_style='success',
    tooltip='Upload to huggingface',
)
dropdown = widgets.Dropdown(
    options=paths_map.keys(),
    value=folder,
    description='Folder',
)

out = widgets.Output()

def on_folder_change(change):
  if change['type'] == 'change' and change['name'] == 'value':
      models_path = paths_map[change["new"]]
      selected.options = get_file_list(models_path)

def upload_it(b):
  with out:
    if selected.value is not None:
      clear_output()
      !mkdir -p {upload_path}


      #hard link each file
      for selected_model in selected.value:
        if not os.path.exists(os.path.join(upload_path,selected_model)):
          os.link(os.path.join(paths_map[dropdown.value],selected_model),os.path.join(upload_path,selected_model)) #hardlinking to save colab's space

      #delete .ipynb_checkpoint
      if os.path.exists(os.path.join(upload_path,".ipynb_checkpoints")):
        !rm {upload_path}/.ipynb_checkpoints
      print("Selected:", ", ".join(selected.value))
      print("Uploading to https://huggingface.co/"+username_repo)
      print("Please wait... Might look stuck, but it's not 👍")

      # Comment this for file based upload
      api.upload_folder(
          folder_path=upload_path,
          repo_id=username_repo,
          commit_message=commit_message
      )

      # Uncomment for file based upload
      # for filename in os.listdir(upload_path):
      #   f = os.path.join(upload_path, filename)
      #   # checking if it is a file
      #   if os.path.isfile(f):
      #     api.upload_file(
      #       path_or_fileobj=f,
      #       path_in_repo=filename,
      #       repo_id=username_repo,
      #       commit_message=commit_message
      #     )

      print("Done!")
      #delete hardlink
      !rm -rf {upload_path}/*
    else:
      print("Nothing is selected")

dropdown.observe(on_folder_change)
button.on_click(upload_it)
print("Upload target: https://huggingface.co/"+username_repo)
print("👇 Select models you want to upload (use ctrl/shift for multiple selection) ")
display(dropdown,selected,button,out)
