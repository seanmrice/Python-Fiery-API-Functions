import requests
import urllib3

# API Key obtainable via developer.efi.com
APIKey = """YOUR API KEY HERE"""
# API User is from the Fiery server itself, cannot be Admin/Administrator/Guest
APIUser = "API_USER"
# API Password is the password for the above API User
APIPassword = "API_PASSWORD"
API_Login_Payload: dict = {"username": APIUser, "password": APIPassword, "apikey": APIKey}

# Disable HTTPS certificate checks and warnings for Fiery self-signed certificates
# https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings
# Set to True only if you understand the risks
disable_https_cert_warning: bool = False
if disable_https_cert_warning:
    # verify_bool sets whether to ignore that the Fiery server certificate (usually self-signed) should be
    # checked for validity.  If using this API on a local network only, you should be OK to do so safely,
    # but verify that it meets your respective security policy FIRST.
    verify_bool: bool = False
    urllib3.disable_warnings()
else:
    verify_bool: bool = True


# NOTES: Unless otherwise stated, "serverName" accepts the IP address of the Fiery server *or* the DNS name of the
# Fiery Server I highly recommended supplying the IP address and not the DNS address of the Fiery since DNS can
# tend to be flaky Fiery API documentation is available at https://developer.efi.com/ - but in my opinion it is
# extremely unclear and incomplete I recommend running the FieryPullHeld() function on a few jobs first, so you can
# see what options and attributes are actually available in your environment - then modifying the FieryJobUpdate() to
# reflect your needs.

def FieryLogin(serverName):
    # Call FieryLogin before any other function (most functions have this function integrated)
    # Store the fiery_session output from the function into a variable to pass on to other functions if required
    fiery_session = requests.Session()
    fiery_session.post(f"https://{serverName}/live/api/v5/login", data=API_Login_Payload, verify=verify_bool)
    return fiery_session


def FieryLogout(serverName, session):
    # ALWAYS log out of the Fiery between API calls, or you will eventually get a failure to log in until the Fiery
    # is rebooted
    r_out = session.post(f"https://{serverName}/live/api/v5/logout", data=API_Login_Payload, verify=verify_bool)
    return r_out.json()


def FieryStatus(serverName):
    # Returns True if the supplied Fiery IP/DNS name is in a running state
    # Returns False if the Fiery cannot be reached, or if it is not in a running state
    fiery_session = FieryLogin(serverName)
    if fiery_session is None:
        try:
            FieryLogin(serverName)
        except Exception:
            print(f"Unable to log into Fiery at {serverName}")
            return False
    try:
        r_status = fiery_session.get(f"https://{serverName}//live/api/v5/status", verify=verify_bool).json()
        r_status = r_status['data']['item']['fiery']
        if r_status == "running":
            return True
        if r_status != "running":
            return False
    except Exception:
        return False
    finally:
        FieryLogout(serverName, fiery_session)


def FieryPullHeld(serverName):
    # Function attempts to log into the specified server, and pull a JSON formatted list of all the held jobs
    fiery_session = FieryLogin(serverName)
    if fiery_session is None:
        try:
            FieryLogin(serverName)
        except Exception:
            print(f"Unable to log into Fiery at {serverName}")
            return False
    held = fiery_session.get(f"https://{serverName}/live/api/v5/jobs/held", data=API_Login_Payload, verify=verify_bool)
    FieryLogout(serverName, fiery_session)
    return held.json()


def FieryPullPrinting(serverName):
    # Function attempts to log into the specified server, and pull a JSON formatted list of all the printing jobs
    fiery_session = FieryLogin(serverName)
    if fiery_session is None:
        try:
            FieryLogin(serverName)
        except Exception:
            print(f"Unable to log into Fiery at {serverName}")
            return False
    printing = fiery_session.get(f"https://{serverName}/live/api/v5/jobs/printing", data=API_Login_Payload,
                                 verify=verify_bool)
    FieryLogout(serverName, fiery_session)
    return printing.json()


def FieryPullPrinted(serverName):
    # Function attempts to log into the specified server, and pull a JSON formatted list of all the printed jobs
    fiery_session = FieryLogin(serverName)
    if fiery_session is None:
        try:
            FieryLogin(serverName)
        except Exception:
            print(f"Unable to log into Fiery at {serverName}")
            return False
    printed = fiery_session.get(f"https://{serverName}/live/api/v5/jobs/printed", data=API_Login_Payload,
                                verify=verify_bool)
    FieryLogout(serverName, fiery_session)
    return printed.json()


def FieryJobUpdate(job_id, new_copy_count, serverName):
    # Update the copy count of a job
    # Requires the job ID (obtainable via FieryPullHeld)
    # In this case the function is updating the job copy count (num copies) attribute
    fiery_session = FieryLogin(serverName)
    if fiery_session is None:
        try:
            FieryLogin(serverName)
        except Exception:
            return False
    try:
        job_payload = {"attributes": {"num copies": new_copy_count}}
        fiery_session.post(f"https://{serverName}/live/api/v5/jobs/{job_id}/", json={job_payload},
                           verify=verify_bool)
        return True
    except Exception:
        return False
    finally:
        FieryLogout(serverName, fiery_session)


def FieryPullPresets(serverName):
    # Pull a JSON list of all the job presets / workflows on the Fiery Server
    fiery_session = FieryLogin(serverName)
    if fiery_session is None:
        try:
            FieryLogin(serverName)
        except Exception:
            return False
    try:
        fiery_presets = fiery_session.get(f"https://{serverName}/live/api/v5/presets", verify=verify_bool).json()
        return fiery_presets
    except Exception:
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
        except Exception:
            return False
    try:
        fiery_session.post(f"https://{serverName}/live/api/v5/jobs/{job_id}/", json=bw_payload, verify=verify_bool)
        return True
    except Exception:
        return False
    finally:
        FieryLogout(serverName, fiery_session)


def Fiery_Preset_Apply(serverName, job_id, presetID):
    # Apply a preset to a specific job
    # presetID is obtainable via FieryPullPresets
    preset_payload = {"preset": presetID}
    fiery_session = FieryLogin(serverName)
    if fiery_session is None:
        try:
            FieryLogin(serverName)
        except Exception:
            return False
    try:
        fiery_session.post(f"https://{serverName}/live/api/v5/jobs/{job_id}/", json=preset_payload, verify=verify_bool)
        return True
    except Exception:
        return False
    finally:
        FieryLogout(serverName, fiery_session)


def FieryOperation(serverName, request):
    # In addition to serverName (IP/DNS Name of the Fiery Server)
    # "request" is the operation you want to perform on the Fiery
    # Supported requests are: restart, reboot, stop, clear, pause, resume, cancelprinting, cancelripping]
    allow = 0
    methods = ('restart', 'reboot', 'stop', 'clear', 'pause', 'resume', 'cancelprinting', 'cancelripping')
    for each in methods:
        if request is each:
            allow = 1
    if allow == 1:
        fiery_session = FieryLogin(serverName)
        if fiery_session is None:
            try:
                FieryLogin(serverName)
            except Exception:
                return False
        try:
            method_payload = {"method": {request}}
            fiery_session.post(f"https://{serverName}/live/api/v5/server", json=method_payload, verify=verify_bool)
            return True
        except Exception:
            return False
        finally:
            FieryLogout(serverName, fiery_session)
    else:
        print("Invalid request")
        return False


def FieryJobLog(serverName):
    fiery_session = FieryLogin(serverName)
    if fiery_session is None:
        try:
            FieryLogin(serverName)
        except Exception:
            return False
    try:
        job_log = fiery_session.post(f"https://{serverName}/live/api/v5/accounting", verify=verify_bool).json()
        return job_log
    except Exception:
        return False
    finally:
        FieryLogout(serverName, fiery_session)


def FieryStatePull(serverName, printState):
    # Pull all jobs based on the specified state (printState)
    # printState supports: held, processed, spooled, printed, waiting to process,
    # waiting to print, printing, processing, archived
    allow = 0
    possible_states = ('held', 'processed', 'spooled', 'printed', 'waiting to process', 'waiting to print', 'printing',
                       'processing', 'archived')
    for each in possible_states:
        if printState is each:
            allow = 1
    if allow == 1:
        fiery_session = FieryLogin(serverName)
        if fiery_session is None:
            try:
                FieryLogin(serverName)
            except Exception:
                return False
        try:
            jobs_by_state = fiery_session.post(f'https://{serverName}/live/api/v5/server/jobs/{printState}',
                                               data=API_Login_Payload, verify=verify_bool).json()
            return jobs_by_state
        except Exception:
            return False
        finally:
            FieryLogout(serverName, fiery_session)
    else:
        print("Invalid request")
        return False
