Place all packages in the "packages" folder. To make those packages available for import:

~~~BASH
add2virtualenv /home/oligavin/workspace/Y4Sem1/CS4227SoftwareDesignAndArchitecture/project/code/packages
~~~

This allows the framework to be used in the client without relative imports.
You probably need to add the same path to your IDE.

Download and install [dynamodb-local](http://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.html#DynamoDBLocal.DownloadingAndRunning)
and follow the instructions to run it.