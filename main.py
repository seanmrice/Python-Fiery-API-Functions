import requests
import urllib3
import re
from main import log_text, log_file

# API Key obtainable via developer.efi.com
APIKey = """YOUR API KEY HERE"""
# API User is from the Fiery server itself, cannot be Admin/Administrator/Guest
APIUser = "APIUSER"
# API Password is the password for the above API User
APIPassword = "APIPASSWORD"
API_Payload = {"username": APIUser, "password": APIPassword, "apikey": APIKey}

# Disable HTTPS certificate warnings for Fiery self-signed certificates
# https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings
# Set to True only if you understand the risks
Disable_HTTPS_Cert_Warning = True
if Disable_HTTPS_Cert_Warning:
    urllib3.disable_warnings()

# NOTES: Unless otherwise stated, "serverName" accepts the IP address of the Fiery server *or* the DNS name of the Fiery Server
# It is highly recommended to supply the IP address and not the DNS address of the Fiery since DNS can tend to be flaky
# Fiery API documentation is available at https://developer.efi.com/ - but in my opinion it is extremely unclear and incomplete
# I recommend running the FieryPullHeld() function on a few jobs first, so you can see what options and attributes are actually
# available in your environment - then modifying the FieryJobUpdate() to reflect your needs.

def FieryLogin(serverName):
    # Call FieryLogin before any other function (most functions have this function integrated)
    # Store the fiery_session output from the function into a variable to pass on to other functions if required
    fiery_session = requests.Session()
    fiery_session.post("https://" + serverName + "/live/api/v5/login", data=API_Payload, verify=False)
    return fiery_session


def FieryPullHeld(serverName):
  # Function attempts to log into the specified server, and pull a JSON formatted list of all the held jobs
    fiery_session = FieryLogin(serverName)
    if fiery_session is None:
        try:
            FieryLogin(serverName)
        except:
            log_text(log_file, "Unable to log into Fiery at " + str(serverName))
            return False
    r_held = fiery_session.get("https://" + serverName + "/live/api/v5/jobs/held", data=API_Payload, verify=False)
    FieryLogout(serverName, fiery_session)
    return r_held.json()


def FieryLogout(serverName, session):
    # ALWAYS log out of the Fiery between API calls, or you will eventually get a failure to log in until the Fiery is rebooted
    r_out = session.post("https://" + serverName + "/live/api/v5/logout", data=API_Payload, verify=False)
    return r_out.json()


def FieryStatus(serverName):
    # Returns True if the supplied Fiery IP/DNS name is in a running state
    # Returns False if the Fiery cannot be reached, or if it is not in a running state
    # If it returns False, it will also log to the central logging location
    fiery_session = FieryLogin(serverName)
    if fiery_session is None:
        try:
            FieryLogin(serverName)
        except:
            log_text(log_file, "Unable to log into Fiery at " + str(serverName))
            return False
    try:
        r_status = fiery_session.get("https://" + serverName + "/live/api/v5/status", verify=False).json()
        if r_status['data']['item']['fiery'] == "running":
            return True
        elif r_status['data']['item']['fiery'] != "running":
            return False
        else:
            return False
    except:
        return False
    finally:
        FieryLogout(serverName, fiery_session)

def FieryJobUpdate(job_id, new_copycount, serverName):
    # Update the copy count of a job
    # Requires the job ID (obtainable via FieryPullHeld)
    # In this case the function is updating the job copy count (num copies) attribute
    fiery_session = FieryLogin(serverName)
    if fiery_session is None:
        try:
            FieryLogin(serverName)
        except:
            return False
    try:
        job_payload = {"attributes": {"num copies": new_copycount}}
        fiery_session.post("https://" + serverName + "/live/api/v5/jobs/" + job_id + "/", json=job_payload, verify=False)
        return True
    except:
        return False
    finally:
        FieryLogout(serverName, fiery_session)


def FieryPullPresets(serverName):
  # Pull a JSON list of all the job presets / workflows on the Fiery Server
    fiery_session = FieryLogin(serverName)
    if fiery_session is None:
        try:
            FieryLogin(serverName)
        except:
            return False
    try:
        fiery_presets = fiery_session.get("https://" + serverName + "/live/api/v5/presets", verify=False).json()
        return fiery_presets
    except:
        return False
    finally:
        FieryLogout(serverName, fiery_session)

def Fiery_BWJob(serverName, job_id):
    # Change a job to grayscale on a color Fiery
    bw_payload = {"attributes": {"EFColorMode": "Grayscale"}}
    fiery_session = FieryLogin(serverName)
    if fiery_session is None:
        try:
            FieryLogin(serverName)
        except:
            return False
    try:
        fiery_session.post("https://" + serverName + "/live/api/v5/jobs/" + job_id + "/", json=bw_payload, verify=False)
        return True
    except:
        return False
    finally:
        FieryLogout(serverName, fiery_session)


def Fiery_Preset_Apply(serverName, job_id, presetID):
  # Apply a preset to a specific job
  #presetID is obtainable via FieryPullPresets
    preset_payload = {"preset": presetID}
    fiery_session = FieryLogin(serverName)
    if fiery_session is None:
        try:
            FieryLogin(serverName)
        except:
            return False
    try:
        fiery_session.post("https://" + serverName + "/live/api/v5/jobs/" + job_id + "/", json=preset_payload, verify=False)
        return True
    except:
        return False
    finally:
        FieryLogout(serverName, fiery_session)
