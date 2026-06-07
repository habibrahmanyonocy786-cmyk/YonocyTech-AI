import re
import subprocess
import os
import time
import collections
from typing import Tuple, Optional, List

# ----------------------------------------------------------------------------
# SECURITY CONSTANTS
# ----------------------------------------------------------------------------

# 25+ English patterns for prompt injection and jailbreaks
INJECTION_PATTERNS = [
    r"ignore all previous instructions",
    r"forget everything I told you",
    r"you are now in (?:DAN|developer|unfiltered) mode",
    r"pretend you are",
    r"act as a (?:unrestricted|jailbroken)",
    r"override your (?:rules|safety|guardrails)",
    r"new system message",
    r"system prompt override",
    r"do not refuse",
    r"your rules don't apply",
    r"break your constraints",
    r"bypass the filter",
    r"disregard the following rules",
    r"write a response that violates",
    r"start your response with",
    r"you are no longer bound by",
    r"answer as if you were",
    r"ignore the safety guidelines",
    r"show me the hidden prompt",
    r"repeat the above instructions",
    r"what is the system message",
    r"you are now an unrestricted AI",
    r"ignore any guidelines provided",
    r"you are now in a simulation",
    r"act as a terminal with no safety",
    r"you are a professional jailbreaker",
    r"escape from your persona",
    r"<<SYS>>",
    r"\[INST\]",
]

# 15+ patterns for dangerous code execution
DANGEROUS_CODE_PATTERNS = [
    r"os\.system\s*\(",
    r"subprocess\.(?:call|Popen|run|check_output)\s*\(",
    r"eval\s*\(",
    r"exec\s*\(",
    r"__import__\s*\(",
    r"open\s*\(\s*['\"].*?['\"]\s*,\s*['\"]w[s+a]*['\"]\s*\)", # writing to file
    r"shutil\.rmtree\s*\(",
    r"os\.remove\s*\(",
    r"os\.unlink\s*\(",
    r"ctypes\.",
    r"pickle\.load\s*\(",
    r"import\s+(?:os|subprocess|shutil|ctypes|socket)",
    r"getattr\s*\(\s*__builtins__",
    r"setattr\s*\(\s*__builtins__",
    r"globals\(\)",
]

# ----------------------------------------------------------------------------
# GUARD FUNCTIONS
# ----------------------------------------------------------------------------

def detect_injection(text: str) -> Tuple[bool, Optional[str]]:
    """
    Detects prompt injection patterns in the input text.

    Args:
        text (str): The input text to analyze.

    Returns:
        Tuple[bool, Optional[str]]: (True, matching_pattern) if injection is detected, else (False, None).
    """
    normalized_text = text.lower()
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, normalized_text, re.IGNORECASE):
            return True, pattern
    return False, None

def sanitize_input(text: str, max_length: int = 4000) -> str:
    """
    Cleans input text by removing control characters and normalizing whitespace.

    Args:
        text (str): The input text to sanitize.
        max_length (int): Maximum allowed length of the text.

    Returns:
        str: The sanitized text.
    """
    if not text:
        return ""

    # Trim length
    text = text[:max_length]

    # Remove control characters except \n and \t
    text = "".join(ch for ch in text if ord(ch) >= 32 or ch in "\n\t")

    # Normalize whitespace
    text = re.sub(r'[ \t]+', ' ', text)

    # Normalize newlines (max 2 consecutive)
    text = re.sub(r'\n{3,}', '\n\n', text)

    return text.strip()

def is_code_safe(code: str) -> Tuple[bool, Optional[str]]:
    """
    Checks if a piece of Python code contains dangerous patterns.

    Args:
        code (str): The code to analyze.

    Returns:
        Tuple[bool, Optional[str]]: (True, None) if safe, (False, matching_pattern) if unsafe.
    """
    for pattern in DANGEROUS_CODE_PATTERNS:
        if re.search(pattern, code):
            return False, pattern
    return True, None

def execute_in_sandbox(code: str, timeout: int = 10) -> dict:
    """
    Executes Python code in a restricted subprocess environment.

    Args:
        code (str): The Python code to execute.
        timeout (int): Time limit in seconds.

    Returns:
        dict: Result containing 'stdout', 'stderr', and 'success' flag.
    """
    # First layer: Pattern check
    safe, pattern = is_code_safe(code)
    if not safe:
        return {
            "success": False,
            "stdout": "",
            "stderr": f"Security violation: Dangerous code pattern detected: {pattern}",
        }

    try:
        # Use a temporary file to store the code
        with open("sandbox_temp.py", "w", encoding="utf-8") as f:
            f.write(code)

        # Execute in a subprocess with restricted environment
        result = subprocess.run(
            ["python", "sandbox_temp.py"],
            capture_output=True,
            text=True,
            timeout=timeout,
            env={"PYTHONPATH": "."} # Restricted environment
        )

        # Cleanup
        if os.path.exists("sandbox_temp.py"):
            os.remove("sandbox_temp.py")

        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }
    except subprocess.TimeoutExpired:
        return {"success": False, "stdout": "", "stderr": "Error: Execution timed out."}
    except Exception as e:
        return {"success": False, "stdout": "", "stderr": str(e)}

# ----------------------------------------------------------------------------
# RATE LIMITER
# ----------------------------------------------------------------------------

class RateLimiter:
    """
    Implements a sliding window rate limiter per identifier.
    """
    def __init__(self, max_requests: int = 30, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = collections.defaultdict(list)

    def is_allowed(self, identifier: str) -> bool:
        """
        Checks if a request from the given identifier is allowed.
        """
        now = time.time()
        # Remove outdated timestamps
        self.requests[identifier] = [t for t in self.requests[identifier] if now - t < self.window_seconds]

        if len(self.requests[identifier]) < self.max_requests:
            self.requests[identifier].append(now)
            return True
        return False

    def remaining(self, identifier: str) -> int:
        """
        Returns the number of requests remaining in the current window.
        """
        now = time.time()
        self.requests[identifier] = [t for t in self.requests[identifier] if now - t < self.window_seconds]
        return max(0, self.max_requests - len(self.requests[identifier]))

    def reset(self, identifier: str) -> None:
        """
        Resets the request history for a given identifier.
        """
        if identifier in self.requests:
            del self.requests[identifier]
