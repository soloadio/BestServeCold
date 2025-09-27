import threading
from queue import Queue
from typing import Callable, Any, Iterable, Optional


class Multitasker:
    @staticmethod
    def _target_wrapper(worker_func, main_arg, extra_args, result_queue: Queue):
        """
        main_arg: the main input (e.g., URL)
        extra_args: tuple of additional arguments to unpack (same for all workers)
        """
        try:
            result = worker_func(main_arg, *extra_args)
            result_queue.put(result)
        except Exception as e:
            result_queue.put(e)

    def run(
        self,
        worker_func: Callable,
        main_args: Iterable,        # list of main arguments (e.g., URLs)
        extra_args: tuple = (),     # extra args, same for all workers
        validator: Callable = lambda x: True,
        stop_on_first_valid: bool = True
    ) -> Optional[Any]:
        """
        Run worker_func in parallel using threads, where each main_arg gets its own thread.
        """
        result_queue = Queue()
        threads = []

        # Start a thread for each main_arg
        for main_arg in main_args:
            t = threading.Thread(
                target=self._target_wrapper,
                args=(worker_func, main_arg, extra_args, result_queue)
            )
            t.start()
            threads.append(t)

        results = []
        for _ in main_args:
            result = result_queue.get()
            if isinstance(result, Exception):
                print(f"Worker raised an exception: {result}")
                continue

            results.append(result)
            if stop_on_first_valid and validator(result):
                # Stop remaining threads by simply not waiting for them further
                return result

        # Wait for all threads to finish
        for t in threads:
            t.join()
        
        print("Here are the results of this worker: ", results)
        return None if stop_on_first_valid else results
