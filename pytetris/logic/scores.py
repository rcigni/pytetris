
def read_scores(filename: str) -> list[int]:
    try:
        with open(filename, "r") as f:
            scores = [int(line) for line in f.readlines() if line.strip() != "" and line.strip().isnumeric()]
            scores.sort(reverse=True)
            return scores
    except FileNotFoundError:
        return []


def append_score(filename: str, score: int) -> None:
    if score > 0:
        with open(filename, "a") as f:
            f.write(f"{score}\n")
