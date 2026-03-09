# Part B - Server Log Analyzer
# Uses Counter and defaultdict to analyze simulated server logs

from collections import Counter, defaultdict
import re

# ---- Simulated log data ----
# Format: YYYY-MM-DD HH:MM:SS - LEVEL - module - message

raw_logs = [
    "2025-03-01 08:12:01 - INFO - auth - User login successful",
    "2025-03-01 08:13:45 - ERROR - database - Connection timeout after 30s",
    "2025-03-01 08:14:10 - INFO - api - GET /products returned 200",
    "2025-03-01 08:15:22 - WARNING - auth - Failed login attempt for user admin",
    "2025-03-01 08:16:00 - ERROR - database - Connection timeout after 30s",
    "2025-03-01 08:17:33 - INFO - api - POST /orders returned 201",
    "2025-03-01 08:18:05 - CRITICAL - payment - Payment gateway not responding",
    "2025-03-01 08:19:14 - ERROR - api - Unhandled exception in /checkout",
    "2025-03-01 08:20:00 - INFO - auth - User logout successful",
    "2025-03-01 08:21:11 - WARNING - cache - Cache miss rate above threshold",
    "2025-03-01 08:22:30 - ERROR - database - Query execution failed: timeout",
    "2025-03-01 08:23:00 - INFO - api - GET /users returned 200",
    "2025-03-01 08:24:15 - ERROR - auth - Token verification failed",
    "2025-03-01 08:25:00 - WARNING - auth - Failed login attempt for user admin",
    "2025-03-01 08:26:45 - INFO - api - DELETE /session returned 200",
    "2025-03-01 08:27:30 - ERROR - database - Connection timeout after 30s",
    "2025-03-01 08:28:00 - CRITICAL - payment - Payment gateway not responding",
    "2025-03-01 08:29:10 - INFO - cache - Cache cleared successfully",
    "2025-03-01 08:30:00 - ERROR - api - Unhandled exception in /checkout",
    "2025-03-01 08:31:20 - INFO - auth - User login successful",
    "2025-03-01 08:32:00 - WARNING - database - Slow query detected: 5.2s",
    "2025-03-01 08:33:45 - ERROR - auth - Token verification failed",
    "2025-03-01 08:34:00 - INFO - api - GET /products returned 200",
    "2025-03-01 08:35:10 - CRITICAL - payment - Insufficient funds error",
    "2025-03-01 08:36:00 - ERROR - database - Query execution failed: timeout",
]


# ---- Parse a single log line into a dict ----
def parse_log_line(line):
    # Pattern: timestamp - level - module - message
    pattern = r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) - (\w+) - (\w+) - (.+)$'
    match = re.match(pattern, line.strip())
    if match:
        return {
            'timestamp': match.group(1),
            'level':     match.group(2),
            'module':    match.group(3),
            'message':   match.group(4)
        }
    return None


# ---- Parse all log lines ----
def parse_all_logs(logs):
    parsed = []
    for line in logs:
        entry = parse_log_line(line)
        if entry:
            parsed.append(entry)
    return parsed


# ---- Analyze logs using Counter and defaultdict ----
def analyze_logs(parsed_logs):
    level_counter   = Counter()
    message_counter = Counter()
    module_counter  = Counter()
    errors_by_module = defaultdict(list)

    for entry in parsed_logs:
        level   = entry.get('level', '')
        module  = entry.get('module', '')
        message = entry.get('message', '')

        level_counter[level] += 1
        module_counter[module] += 1

        # Track error and critical messages separately
        if level in ('ERROR', 'CRITICAL'):
            message_counter[message] += 1
            errors_by_module[module].append(message)

    return level_counter, message_counter, module_counter, errors_by_module


# ---- Build summary dict ----
def generate_summary(parsed_logs):
    total = len(parsed_logs)
    if total == 0:
        return {'total_entries': 0, 'error_rate': '0%', 'top_errors': [], 'busiest_module': 'N/A'}

    level_counter, message_counter, module_counter, errors_by_module = analyze_logs(parsed_logs)

    error_count = level_counter.get('ERROR', 0) + level_counter.get('CRITICAL', 0)
    error_rate  = round((error_count / total) * 100, 1)
    top_errors  = message_counter.most_common(3)
    busiest     = module_counter.most_common(1)[0][0] if module_counter else 'N/A'

    return {
        'total_entries': total,
        'error_rate': f"{error_rate}%",
        'top_errors': top_errors,
        'busiest_module': busiest
    }


# ---- Main output ----
if __name__ == "__main__":
    print("=" * 55)
    print("  Server Log Analyzer")
    print("=" * 55)

    parsed = parse_all_logs(raw_logs)

    print(f"\nTotal parsed log entries: {len(parsed)}")
    print("\nSample parsed entry:")
    print(f"  {parsed[0]}")

    level_c, msg_c, mod_c, errors_mod = analyze_logs(parsed)

    print("\n--- Log Level Distribution ---")
    for level, count in sorted(level_c.items()):
        print(f"  {level}: {count}")

    print("\n--- Most Active Modules ---")
    for module, count in mod_c.most_common():
        print(f"  {module}: {count} entries")

    print("\n--- Most Common Error Messages ---")
    for msg, count in msg_c.most_common(5):
        print(f"  [{count}x] {msg}")

    print("\n--- Errors Grouped by Module ---")
    for module, errs in errors_mod.items():
        print(f"  {module}: {len(errs)} error(s)")
        for e in set(errs):
            print(f"    - {e}")

    print("\n--- Summary ---")
    summary = generate_summary(parsed)
    for k, v in summary.items():
        print(f"  {k}: {v}")

    print("\n--- Self-Study Note ---")
    print("  Python's logging module uses format strings like:")
    print("  '%(asctime)s - %(levelname)s - %(name)s - %(message)s'")
    print("  To use it in a real app:")
    print("    import logging")
    print("    logging.basicConfig(level=logging.DEBUG, format='...')")
    print("    logger = logging.getLogger(__name__)")
    print("    logger.info('Server started')")
