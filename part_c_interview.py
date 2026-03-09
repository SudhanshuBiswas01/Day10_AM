# Part C - Interview Ready
# Q2: group_anagrams using sorted key + defaultdict
# Q3: Bugfix for char_freq function

from collections import defaultdict


# ---- Q2: Group Anagrams ----
def group_anagrams(words: list[str]) -> dict[str, list[str]]:
    anagram_map = defaultdict(list)
    for word in words:
        # sorted characters joined as a string = unique key for each anagram group
        key = ''.join(sorted(word))
        anagram_map[key].append(word)
    return dict(anagram_map)


# ---- Q3: Fixed char_freq ----
def char_freq(text):
    freq = {}
    for char in text:
        # Fix 1: use .get() to avoid KeyError on first occurrence
        freq[char] = freq.get(char, 0) + 1
    # Fix 2: return list of (char, count) tuples, not just keys
    sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    return sorted_freq


# ---- Output Demo ----
if __name__ == "__main__":
    print("=" * 55)
    print("  Part C - Interview Ready")
    print("=" * 55)

    print("\n--- Q2: group_anagrams ---")
    words = ['eat', 'tea', 'tan', 'ate', 'nat', 'bat']
    result = group_anagrams(words)
    for key, group in result.items():
        print(f"  '{key}': {group}")

    print("\n--- Q3: char_freq (fixed) ---")
    text = "hello world"
    freq = char_freq(text)
    print(f"  Input: '{text}'")
    print(f"  Output: {freq}")
