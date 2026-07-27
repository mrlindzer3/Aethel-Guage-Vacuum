import os
import time

class CGroupThrottleManager:
    def __init__(self, cgroup_path=None):
        self.cgroup_path = cgroup_path or "/sys/fs/cgroup"

    def apply_throttle(self, cpu_max_val="50000 100000"):
        """Applies a CPU quota throttle if the cgroup interface is writable."""
        target = os.path.join(self.cgroup_path, "cpu.max")
        try:
            if os.path.exists(target):
                with open(target, "w") as f:
                    f.write(cpu_max_val)
                print(f"[ThrottleManager] Successfully applied throttle: {cpu_max_val}")
                return True
            else:
                print(f"[ThrottleManager] cgroup path {target} not found. Running unthrottled.")
                return False
        except PermissionError:
            print("[ThrottleManager] Permission denied writing to cgroup. Run with appropriate privileges if needed.")
            return False
        except Exception as e:
            print(f"[ThrottleManager] Error applying throttle: {e}")
            return False

if __name__ == "__main__":
    manager = CGroupThrottleManager()
    manager.apply_throttle()
