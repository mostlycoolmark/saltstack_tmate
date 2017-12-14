import os
import uuid

def new_session(install_tmate = False):
  '''
  Used to create a new tmate session on the target and returns the ssh address.

  Returns ``ssh sessionname@host``

  CLI Example:

  salt 'host' tmate.new_session

  Optional: pass install argument to install tmate package (if absent)

  salt 'host' tmate.new_session install
  '''
  if (__salt__['pkg.version']('tmate') == ''):
    if (install_tmate.lower() == 'install'):
      if (__salt__['tmate.install']() == False):
        return "unable to install tmate package"
    else:
      return "tmate package is not currently installed."

  # Creating ssh keys if they do not exist. These are required for tmate to work.
  user_home_directory = os.path.expanduser('~')
  if not os.path.exists(user_home_directory + '/.ssh/id_rsa'):
    __salt__['cmd.run']('ssh-keygen -f ' + user_home_directory + '/.ssh/id_rsa -t rsa -N \'\'')

  # Creating /tmp/saltstack-tmate/ directory for storing sockets.
  if not os.path.exists('/tmp/saltstack-tmate'):
    __salt__['cmd.run']('mkdir -p /tmp/saltstack-tmate')
  
  # Generating random uuid consisting of hostname/time to use for the socket name.
  random_uuid = str(uuid.uuid1())

  __salt__['cmd.run']('tmate -S /tmp/saltstack-tmate/' + random_uuid + '.sock new-session -d')
  __salt__['cmd.run']('tmate -S /tmp/saltstack-tmate/' + random_uuid + '.sock wait tmate-ready')
  return __salt__['cmd.run']("tmate -S /tmp/saltstack-tmate/" + random_uuid + ".sock display -p '#{tmate_ssh}'")


def killall():
  '''
  Used to kill all tmate sessions and remove socket files.

  Returns ``True``

  CLI Example:

  salt 'host' tmate.killall
  '''
  __salt__['cmd.run']('killall -9 tmate', ignore_retcode=True)
  if os.path.exists('/tmp/saltstack-tmate'):
    __salt__['file.remove']('/tmp/saltstack-tmate')
  return True
  
def list_sessions():
  '''
  Used to list all open sessions on a host.

  Returns ``[ ssh sessionname@host ]``

  CLI Example:

  salt 'host' tmate.list_sessions
  '''
  session_list = []
  for filename in os.listdir('/tmp/saltstack-tmate/'):
    tmate_check_results = __salt__['cmd.run']("tmate -S /tmp/saltstack-tmate/" + filename + " display -p '#{tmate_ssh}'", ignore_retcode=True)
    if not "no server running " in tmate_check_results:
      session_list.append(tmate_check_results)
  return session_list

def test():
  '''
  Used to return True.

  Returns ``True``

  CLI Example:

  salt 'host' tmate.test
  '''
  return True

def validate():
  '''
  Validates if tmate is installed.

  Returns ``True`` or ``False``

  CLI Example:

  salt 'host' tmate.validate
  '''
  if (__salt__['pkg.version']('tmate') == ''):
    return False, 'tmate package is not installed'
  return True

def install():
  '''
  Installs the tmate package if available.

  Returns ``True`` or ``False``

  CLI Example:

  salt 'host' tmate.install
  '''
  try:
    __salt__['pkg.install']('tmate')
    return True
  except Exception, e:
    return False
