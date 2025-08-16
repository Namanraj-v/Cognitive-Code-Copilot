import tempfile
import os
from radon.complexity import cc_visit
from bandit.core import manager as bandit_manager
from bandit.core import config as bandit_config

def run_bandit_scan(code: str) -> list:
    """Runs a bandit scan on a string of code and returns issues."""
    issues = []
    # Bandit needs a file to scan, so we write the code to a temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as tmp:
        tmp.write(code)
        tmp_filename = tmp.name

    try:
        # Run bandit scan
        b_config = bandit_config.BanditConfig()
        b_mgr = bandit_manager.BanditManager(b_config, "custom")
        b_mgr.discover_files([tmp_filename])
        b_mgr.run_tests()

        for result in b_mgr.results:
            issues.append({
                "severity": result.severity,
                "confidence": result.confidence,
                "line": result.lineno,
                "issue": result.test,
                "description": result.text,
            })
    finally:
        # Clean up the temporary file
        os.unlink(tmp_filename)
        
    return issues

def analyze_code(code: str) -> dict:
    """Analyzes code for complexity, maintainability, and security."""
    report = {}
    
    # 1. Cyclomatic Complexity
    try:
        complexity_results = cc_visit(code)
        total_complexity = sum(c.complexity for c in complexity_results)
        report['cyclomatic_complexity'] = total_complexity
    except Exception:
        report['cyclomatic_complexity'] = "Error"
    
    # 2. Identify Smells for RAG
    identified_smells = []
    if report.get('cyclomatic_complexity', 0) > 5:
        identified_smells.append("high_cyclomatic_complexity")
    if len(code.splitlines()) > 30:
        identified_smells.append("long_function")
    report['identified_smells'] = identified_smells

    # 3. NEW: Security Analysis
    report['security_issues'] = run_bandit_scan(code)
    
    return report