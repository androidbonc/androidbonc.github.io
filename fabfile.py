from fabric.api import env
from fabric.colors import blue, red
import fabric.contrib.project as project

env.hosts = ["192.81.133.96"]
env.user = "root"
env.colorize_errors = True
env.local_output = "_site/"
env.remote_output = "/opt/blog.tankywoo.com/"
env.rsync_delete = False

def deploy():
    if not env.remote_output:
        if env.rsync_delete:
            print(red("You can't enable env.rsync_delete option "
                      "if env.remote_output is not set!!!"))
            print(blue("Exit"))
            exit()

        print(red("Warning: env.remote_output directory is not set!\n"
                  "This will cause some problems!!!"))
        ans = raw_input(red("Do you want to continue? (y/N) "))
        if ans != "y":
            print(blue("Exit"))
            exit()

    project.rsync_project(
        local_dir=env.local_output,
        remote_dir=env.remote_output.rstrip("/") + "/",
        delete=env.rsync_delete
    )
