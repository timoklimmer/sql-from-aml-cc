# Query SQL from Azure Machine Learning Compute Cluster

Quick example to demonstrate how an AML Compute Cluster can query an Azure SQL database using a managed identity.

To make this work, you need to fulfill several prerequisites.


## 1. Ensure you have a Compute Cluster in AML with

- a managed identity assigned (to the AML Compute Cluster, NOT the Azure SQL (MI) service)
  <br/>
  Note: It's probably better to use a system-assigned identity as it needs less configuration steps and should suffice
        for this case here.

- an environment that has pyodbc + unixodbc + Microsoft ODBC 17/18 Driver for SQL Server (Linux) properly installed.
  <br/>
  Several curated images like the *mcr.microsoft.com/azureml/openmpi4.1.0-cuda11.1-cudnn8-ubuntu20.04:latest* image
  have a Microsoft ODBC driver pre-installed, so you only need to add the pyodbc package as a dependency. If pip does
  not work, try using the pyodbc package from conda.


## 2. Ensure you have an Azure SQL instance** (Managed Instance should work, too, but hasn't been tested yet)

- network access enabled between the AML Compute Cluster and the Azure SQL MI instance
    * either using public endpoint (incl. usage of public endpoint network address then) or
    * sharing same VNET and NSGs not blocking the connection

- At least Azure AD authentication enabled in Azure SQL MI. SQL authentication can optionally be added but is best
    avoided anyway.

- user and required permissions for the managed identity of your AML cluster(!) in Azure SQL MI
    <br/>
    ```
    # create user for managed identity
    CREATE USER [<name of the AML cluster managed identity>] FROM EXTERNAL PROVIDER
    
    # give managed identity permissions
    EXEC sp_addrolemember 'db_datareader', '<name of your managed identity>'
    ```

    If you are unsure about the name of your managed identity, run `az ad sp show --id <id shown in cluster details in AML Studio>`
    and take the name shown there. It should be something like `MyResourceGroup/computes/my-cluster`.


## 3. Script adjustments
- Make sure that the driver variable contains the right driver version (17 or 18).
- Adjust the script to whatever you need it.


## 4. Environment variable adjustments in commandJob.yml
- Adjust the environment variable values in commandJob.yml to your needs.


Once adjustments were made, you can submit the command job, eg. by using the `az ml job create ...` command, or by
simply clicking on the AML icon top right when the commandJob.yml file is opened in VS.Code and the Azure ML extension
is installed.


## Disclaimer
As always, I am providing this "as is". Feel free to use but don't blame me if things go wrong.