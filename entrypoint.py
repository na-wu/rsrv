import os
import multiprocessing
import time
from job import job
from datetime import datetime, timedelta
import settings
def run_command(cmd):
	""" execute cmd via the shell. """
	today = datetime.today()
	target = today + timedelta(days=10)
	
	args = {
        "target_date": target,
        "party_size": 2,
        "venue_id": settings.jua,
        "time_floor": target.replace(hour=17, minute=0, second=0, microsecond=0),
        "time_ceiling": None
    }

	# for i in range(10):
		# job(**args)
	while True:
		time.sleep(1)
		job(**args)

# def run_commands(commands, n_parallel):
# 	""" run commands (up to n_parallel in parallel). """
# 	worker = multiprocessing.Pool(n_parallel)
# 	worker.map(run_command, commands)

if __name__ == "__main__":
	# run_commands([
	# 	1,
	# 	2,
	# 	3,
	# 	4
	# ], n_parallel=4)

	run_command(None)