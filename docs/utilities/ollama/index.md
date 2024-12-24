# ollama

[Ollama](https://ollama.com) is an open-source app that lets you create, run, and share large language models (LLMs) locally with a CLI for Mac and Linux. You can also install ollama on Windows, but Unix support is better (as of 11/11/24).

The utility is developed by Meta (I know...but they've developed a lot of great open source tools like the React.js framework), but Meta keeps their grubby paws off your data. All LLMs executed with ollama are local-only and private.

## System Requirements

LLMs require a *lot* of power to run. Ollama uses weights differently from LLMs like chatGPT, shrinking the model size and enabling them to be run on (powerful enough) home devices.

!!! warning

    Just because ollama is lighter than other LLMs does not mean it is "light." While ollama can run on a regular CPU, it's much better to have a dedicated Graphics card with at least 6GB of VRAM. The "heavier" the model you wish to use with ollama, the more system resources you will need.

    Ollama's Github has a [page listing supported GPUs](https://github.com/ollama/ollama/blob/main/docs/gpu.md) so you can quickly check if yours is supported and ollama will run without issue, or if you'll have to struggle and optimize to get this working on your device.

I was not able to find an official source for system requirements, but the table below is often cited as the minimum requirements to run an ollama local server:

| Resource | Minimum Required | Notes |
| -------- | ---------------- | ----- |
| OS |Linux: Ubuntu 18.04 or later, macOS: macOS 11 Big Sur or later | There is technically Windows support, but ollama runs best on Unix. |
| RAM |8GB for running 3B models, 16GB for running 7B models, 32GB for running 13B models | The more the better. Models are loaded into RAM, and very large models (like [dolphin-mixtral](https://ollama.com/library/dolphin-mixtral), which is ~26GB) will crash without sufficient memory. |
| Storage | 12GB for installing Ollama and the base models, Additional space required for storing model data, depending on the models you use. | The more storage the better, especially if you plan to experiment with a lot of different models. These things are big. |
| CPU | Any modern CPU with at least 4 cores is recommended, for running 13B models, a CPU with at least 8 cores is recommended. | ollama is less efficient running via CPU than GPU, make sure you have a decently powerful CPU if going this route. |
| GPU(Optional) | [Guide to help you pick a compatible CPU](https://www.arsturn.com/blog/best-gpus-compatible-with-ollama) | A GPU is not required for running Ollama, but it can improve performance, especially for running larger models. If you have a GPU, you can use it to accelerate training of custom models. |

## Installing ollama

- You can [download ollama right from their website](https://ollama.com/download).
- On Linux, you can simple use this command:

```shell title="Install/upgrade ollama on Linux"
curl -fsSL https://ollama.com/install.sh | sh
```

## Choosing a model

You can [browse available models on ollama's website](https://ollama.com/library). You can install multiple models side-by-side and switch between them at will, you're really only limited to how many models you can download by the size of your disk.

Once you've installed ollama, you can download a model by running:

```shell title="Download an ollama model"
ollama pull <model-name>
```

For example, to get started with the `llama3.2` model (current as of 11/11/24), you can run:

```shell title="Download llama3.2 model"
ollama pull llama3.2
```

To run your new model, open your CLI and run (the model will be downloaded if you have not already run `ollama pull`):

```shell title="Run an ollama model"
ollama run <model-name>
```

## Ollama control script

This Bash script can help manage ollama. The script includes the following arguments:

- `start`: Start the ollama service & server
- `stop`: Stop the ollama server & stop/disable the service
- `install`: Install the ollama server if you have not already
- `upgrade`: Upgrading ollama is as simple as re-running the install script. This script takes care of that for you if you use this argument

```shell title="ollama_ctl.sh" linenums="1"
#!/bin/bash

## ollama systemd service name
SERVICE_NAME="ollama"
## pid of this script (avoid terminating this script when ./ollama_ctl.sh stop is called)
CURRENT_SCRIPT_PID=$$

## Ensure at least 1 command was run
if [ $# -ne 1 ]; then
    echo "Usage: $0 {start|stop|install|update}"
    exit 1
fi

## Assign user's CLI arg to a variable
COMMAND=$1

case $COMMAND in
    start)
        ## Start the ollama service
        echo "Attempting to start the ${SERVICE_NAME} service..."

        ## Check if ollama service is already running
        if systemctl is-active --quiet "${SERVICE_NAME}"; then
            echo "${SERVICE_NAME} service is already running."
        else
            ## Start ollama service
            echo "Starting and enabling ${SERVICE_NAME} service..."
            sudo systemctl enable "${SERVICE_NAME}"
            sudo systemctl start "${SERVICE_NAME}"

            if systemctl is-active --quiet "${SERVICE_NAME}"; then
                echo "${SERVICE_NAME} service started successfully."
            else
                ## ollama startup failed
                echo "Failed to start ${SERVICE_NAME} service. Check system logs for details."
                exit 1
            fi
        fi
        ;;
    stop)
        ## Stop the ollama service
        echo "Attempting to stop the ${SERVICE_NAME} service and any running 'ollama' processes..."

        ## Stop & disable systemd service
        if systemctl is-active --quiet "${SERVICE_NAME}"; then
            echo "Stopping ${SERVICE_NAME} service..."
            sudo systemctl stop "${SERVICE_NAME}"
            sudo systemctl disable "${SERVICE_NAME}"
        else
            ## ollama service is not running
            echo "${SERVICE_NAME} service is not running."
        fi

        # Stop any remaining 'ollama' processes, excluding this script
        OLLAMA_PIDS=$(pgrep -f ollama | grep -v "$CURRENT_SCRIPT_PID")

        if [ "${OLLAMA_PIDS}" ]; then
            ## Kill any ollama process that is not this script
            echo "Killing remaining 'ollama' processes with PIDs: ${OLLAMA_PIDS}"
            echo "${OLLAMA_PIDS}" | xargs -r sudo kill
        else
            ## No ollama processes found
            echo "No additional 'ollama' processes found."
        fi

        echo "Completed stopping processes."
        ;;
    install | update)
        ## The install & update command are the same for ollama, simply re-running the
        #  curl command used to install ollama. For install or update args, run the same command.
        echo "Running ${COMMAND} command for Ollama..."
        curl -fsSL https://ollama.com/install.sh | sh
        echo "Completed ${COMMAND} command."
        ;;
    *)
        echo "Invalid command. Usage: $0 {start|stop|install|update}"
        exit 1
        ;;
esac

```

## Links

- [Ollama Home](https://ollama.com)
  - [Ollama Download](https://ollama.com/download)
- [Ollama Github](https://github.com/ollama/ollama)
