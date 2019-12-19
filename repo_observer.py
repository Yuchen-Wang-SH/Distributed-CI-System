import time
import subprocess
import os
import argparse

import helper

def observe():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dispatch-server', 
        help='The location of the dispatch-server' \
            " by default we use localhost:8888", 
        default='localhost:8888')
    parser.add_argument('--repo-location',
        help='The path to the repo we observe')
    args = parser.parse_args()
    dispatch_host, dispatch_port = args.dispatch_server.split(':')
    try:
        dispatch_port = int(dispatch_port)
    except ValueError as e:
        raise ValueError('Port number is not valid integer!')
    repo_location = args.repo_location

    while True:
        try:
           subprocess.run(['./update_repo.sh', repo_location]) 
        except subprocess.CalledProcessError as e:
            raise Exception('Could not run the shell script in a new process. The reason is %s' % e.output)

        if (os.path.exists('./commit_id')):
            # We find a new commit. Now we can send this commid id to the dispatch server
            # First, let's test whether our dispatch server still online
            res = helper.communicate(dispatch_host, dispatch_port, 'status')
            if res != 'OK':
                raise Exception('Something wrong with the dispatch server.')

            with open('./commit_id') as f:
               commit_id = f.read()
            res = helper.communicate(dispatch_host, dispatch_port, 'dispatch:%s' % commit_id) 
            if res != 'OK':
                raise Exception('We cannot dispatch %s to the dispatch server' % commit_id) 
            print('Commit_id: %s successfully dispatched!' % commit_id)

        time.sleep(5)
    
if __name__ == "__main__":
    observe()