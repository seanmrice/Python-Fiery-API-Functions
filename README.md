# Python-Fiery-API-Functions 
[![CodeFactor](https://www.codefactor.io/repository/github/seanmrice/python-fiery-api-functions/badge)](https://www.codefactor.io/repository/github/seanmrice/python-fiery-api-functions)

A functional repository of various preformatted API call functions for Fiery print servers, written in Python and updated for Fiery API v5

Compatible with all Fiery servers running API v5 - https://developer.efi.com/fieryapi/api/v5

## Authors

Project created by [@seanmrice](https://github.com/seanmrice)

An extension of the example work done by [@fieryapi](https://github.com/fieryapi)


## Documentation

#### Environmental Variables
* APIKey - This is your API key, retrieved from the [EFI Developer Site](https://developer.efi.com/)
* APIUser - This is the username on your Fiery (Not Admin) that has API access
* APIPassword - The password for the API user above (configured via your Fiery device center)
* disable_https_cert_warning - **IMPORTANT**: This disables strict SSL certificate checking and warning prompts for SSL verification failures.  The reason this is included is that Fiery print servers have self-signed SSL certificates by default, so SSL verification for API calls will always fail without it.  You **MUST** set this to **True** if you have not configured your own VALID SSL certificates!
### Functions
##### Unless otherwise noted, "serverName" refers to the IP address of your Fiery server.  You may also use a DNS name, but it is not recommended in a production environment since DNS can be a bit flaky on some networks.
* **FieryLogin(serverName)**: Log into the specified server using the supplied credentials and return a session.
* **FieryLogout(serverName**, session): Log out of the specified server with the supplied session from FieryLogin.
* **FieryStatus(serverName)**: Returns True if the specified Fiery is in the running state, otherwise returns False
* **FieryPullHeld(serverName)**: Return a JSON list of print jobs in the Held queue from the specified server.
* **FieryPullPrinting(serverName)**: Returns a JSON list of print jobs in the Printing state from the specified server.
* **FieryPullPrinted(serverName)**: Returns a JSON list of the most recently printed jobs on the specified server.
* **FieryJobUpdate(job_id, new_copy_count, serverName)**: Update the copy count of the specified job (job_id is retrieved using one of the Pull[state]) funcitons.  
* **FieryPullPresets(serverName)**: Pull a JSON formatted list of the presets/workflows on the specified server.
* **Fiery_BWJob(serverName, job_id)**: Convert the specifed job on the specified server from color to grayscale.
* **Fiery_Preset_Apply(serverName, job_id, presetID)**:  Apply a preset to the specified job on the specified server.  The presetID can be obtained from the FieryPullPresets funcion.  The job_id can be obtained from the Pull[state] functions (usually used in combination with the Held state).
* **FieryOperation(serverName, request)**: For the specified server, perform a system-wide operation.  Available methods are 'restart', 'reboot', 'stop', 'clear', 'pause', 'resume', 'cancelprinting', 'cancelripping'.
* **FieryJobLog(serverName)**: Retrieve the job log from the specified server and return it in JSON format.
* **FieryStatePull(serverName, printState)**: Pull a JSON list of jobs in the specified print state from the specified server.  Valid states are 'held', 'processed', 'spooled', 'printed', 'waiting to process', 'waiting to print', 'printing',
                       'processing', and 'archived'.


