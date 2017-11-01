# Post-deployment Scripts

* [Intro](#intro)
* [Available environment variables](#available-environment-variables)
* [Cleanup pipeline](#cleanup-pipeline)
* [Pipeline stages](#pipeline-stages)
    * [Command stage](#command-stage)
    * [Shell script stage](#shell-script-stage)
    * [Parallel stages](#parallel-stages)
    * [Reusing the results from stages](#reusing-the-results-from-stages)
    * [Wait for running stages until the conditions are satisfied](#wait-for-running-stages-until-the-conditions-are-satisfied)
        * [State values](#state-values)
* [Creating your own pipeline stage](#creating-your-own-pipeline-stage)
* [Logs](#logs)
* [Examples](#examples)

## Intro

Wodby provides you a way to run your scripts after each deployment. You can do it by adding `wodby.yml` file to the docroot of your app. Inside wodby.yml you can describe pipelines like this (example for [command stage](#command-stage)):

```yml
pipeline:
  - name: Drupal 8 clear cache on dev
    type: command
    command: drush cr
    directory: $APP_ROOT
    only_if: test "$WODBY_ENVIRONMENT_TYPE" = "dev" 
```    
    
Or like this (example for [shell stage](#shell-script-stage)):

```yml
pipeline:
  - name: Run my custom script
    type: command
    command: sh my-script.sh
    directory: $APP_ROOT
```

> The pipeline is an automated manifestation of your deployment process. In other words, it's just a set of post-deployment actions to execute

##  Available environment variables

See [Environment Variables article](../infrastructure/environment-variables.md). 

## Cleanup pipeline

wodby.yml can have one cleanup block; cleanup is another pipeline which needs to be executed after a pipeline has either failed or passed. In the cleanup block, we can add command or shell script stages. The below example create a log file in pipeline and then cleanup the log file in the cleaup steps.

```yml
pipeline:
  - name: start pipeline
    command: echo “pipeline” > log/log.txt
cleanup:
  - name: cleanup
    command:  rm log/*
```

## Pipeline stages

Stage in pipeline has three elements, name, type and configurations. configuration elements are optional. The elements of configurations depend on the type. For example `command_stage` type has command configuration, which specify the shell command run in the stage. The following is the table on the type and the parameters.

### Command stage

Command stage executes one command. Users specify Command stage adding command in type.

The following is the parameter of Command stage.

|  Configuration | Optional   | meaning                                                                     |
|:--------------:|:----------:|:----------------------------------------------------------------------------|
|   `command`      | false      | shell command run in the stage                                              |
|   `only_if`      | true       | run specified command on when the condition written in only_if is satisfied |
|   `directory`    | true       | the directory where wodby runs the specified command                       |

### Shell script stage

Shell script stage executes specified shell script file. Users specify Shell script stage adding shell in type.

The following is the parameter of Shell script stage.

|  Configuration   | Optional   | meaning                                |
|:----------------:|:----------:|:--------------------------------------:|
|   `file`           | false      | shell script file run in the stage     |

### Parallel stages

You can set child stages and run these stages in parallel like this.

```yml
pipeline:
  - name: parallel stages
    parallel:
      - name: parallel command 1
        type: command
        command: parallel command 1
      - name: parallel command 2
        type: command
        command: parallel command 2
      - name: parallel command 3
        type: command
        command: parallel command 3
```

In the above setting, parallel command 1, parallel command 2 and parallel command 3 are executed in parallel.

### Reusing the results from stages

Wodby stores the results of preceding stages. The stages can make use of the results of finished stages using the three special variables (**\_\_OUT**, **\_\_ERR**, **\_\_COMBINED** and **\_\_RESULT**) in wodby.yml configuration files.
                                                                                                                                          
* **\_\_OUT** -  output flushed to standard output 
* **\_\_ERR** - output flushed to standard error 
* **\_\_COMBINED** - combined output of stdout and stderr
* **\_\_RESULT** - execution result (true or false)
                                                                                                                                          
The three variables are maps whose keys are stage names and the value are results of the stages. For example, we want the standard output result of the stage named "stage1", we write __OUT["stage1"].

The following is a sample configuration with a special value.

```yml
pipeline:
  - name: stage_1
    command: echo "hello world"
  - name: stage_2
    command: echo __OUT["stage_1"]
```

Wodby with the above configuration outputs "hello world" twice, since the second stage (stage_2) flushes the standard output result of the first stage (stage_1).

### Wait for running stages until the conditions are satisfied

The stage starts immediately after the previous stage finish, but some stages need to wait for some action such as port is ready or file are created. wait_for feature supports the actions which need to be ready before the stages begin.

`wait_for` is defined as a property of stage.

```yml
pipeline:
  - name: launch solr
    command: bin/solr start
  - name: post data to solr index
    command: bin/post -d ~/tmp/foobar.js
    wait_for: host=localhost port=8983 state=ready
```

The wait_for property takes the key value pairs. Key has several variations. The value depends on the key type. The following table shows the supported key value pairs and the description.

| Key     | Value (value type)  | Description                                         |
|:--------|:--------------------|:----------------------------------------------------|
| delay   | second (float)      | Seconds to wait after the previous stage finish     |
| port    | port number (int)   | Port number                                         |
| file    | file name (string)  | File to be created in the previous stages           |
| host    | host (string)       | IP address or host name                             |
| state   | state of the other key (string) | Four types of states are supported. The possible value is dependent to the other Keys. |

#### State values

There are several state values and possible state values are depend on the other key.

There are seveal **state** values and possible state values are depend on the other key.

| State value       | Description                                         |
|:------------------|:----------------------------------------------------|
| present / ready   | Specified port is ready or file is created.         |
| absent  / unready | port is not active or file does not exist           |

## Creating your own pipeline stage

You can create your own pipeline stage and then use them in your pipeline.

The the example below where we define two simple pipelines `hello` and `goodbye`.

```yml
namespace: mypackage

stages:
  - def:
      name: hello
      command: echo "May I help you majesty!"
  - def:
      name: goodbye
      command: echo "Goobye majesty."
```

To import stages to pipeline configuration file, we use require block and add the list of file names into the block.

For example, the following example import the stages defined in `conf/mystage.yml`

```yml
require:
    - conf/mystages.yml

pipeline:
  - call: mypackage::hello
  - call: mypackage::goodbye
```

In the above setting, the stages (`mypackage::hello` and `mypackage::goodbye`) which are defined in `mystage.yml` are specified.

The files specified in pipeline configuration file need to have two blocks **namespace** and **stages**. In namespace, we add the package name, the package name is need to avoid collisions of the stage names in multiple required files. The stages block contains the list of stage definitions. We can define the stages same as the stages in pipeline configurations.

## Logs

You can find output logs of executed post-deployment scripts under `Application > Tasks`
