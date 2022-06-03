import os
import subprocess
from typing import Any, Optional, List


def run_cmd(cmd: str,
            background_process: bool = False,
            stdout: Optional[Any] = subprocess.DEVNULL,
            stderr: Optional[Any] = subprocess.STDOUT) -> None:
    cmd_list = cmd.split(" ")
    if background_process:
        cmd_list = ["nohup"] + cmd_list
        subprocess.Popen(cmd_list,
                         stdout=stdout,
                         stderr=stderr)
        return
    else:
        exit_code = subprocess.call(cmd_list, stdout=stdout, stderr=stderr)
        assert exit_code == 0, f"`{cmd}` failed. Exit code: {exit_code}"


def ray_submit(cluster_cfg: str,
               path_to_script: str,
               script_arguments: Optional[List[str]] = None,
               background_process: bool = False,
               stdout: Optional[Any] = subprocess.DEVNULL,
               stderr: Optional[Any] = subprocess.STDOUT) -> None:
    if script_arguments is None:
        script_arguments = []

    script_arguments_str = " ".join(script_arguments)
    cmd = f"ray submit --no-config-cache --start --stop {cluster_cfg} {path_to_script}"
    if script_arguments:
        cmd = f"{cmd} -- {script_arguments_str}"

    run_cmd(cmd, background_process=background_process, stdout=stdout, stderr=stderr)
    print(f"Submitted script on Ray cluster '{cluster_cfg}' with command '{cmd}'")


def ray_up(cluster_cfg: str) -> None:
    print(f"Starting Ray cluster '{cluster_cfg}'")
    run_cmd(f"ray up {cluster_cfg} -y --no-config-cache --no-restart")
    print(f"Started Ray cluster '{cluster_cfg}'")


def get_head_node_ip(cluster_cfg: str) -> str:
    print(f"Getting Ray cluster head node IP for '{cluster_cfg}'")
    proc = subprocess.run(
        f"ray get-head-ip {cluster_cfg}",
        shell=True,
        capture_output=True,
        text=True,
        check=True)
    # the head node IP should be the last line printed to stdout
    head_node_ip = proc.stdout.splitlines()[-1]
    print(f"Ray cluster head node IP for '{cluster_cfg}': {head_node_ip}")
    return head_node_ip


def ray_init(host, port) -> Any:
    ray_init_uri = f"ray://{host}:{port}"
    print(f"Connecting Ray Client to '{ray_init_uri}'")
    client = ray.init(ray_init_uri, allow_multiple=True)
    print(f"Connected Ray Client to '{ray_init_uri}'")
    return client

