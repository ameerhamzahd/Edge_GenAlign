from flask import Flask, render_template, request
import numpy as np

app = Flask(__name__)

# Function for Needleman-Wunsch Global Alignment
def needleman_wunsch(seq1, seq2):
    match_score = 1
    mismatch_penalty = -1
    gap_penalty = -2

    len1, len2 = len(seq1), len(seq2)
    dp = np.zeros((len1 + 1, len2 + 1), dtype=int)

    # Initialize scoring matrix
    for i in range(len1 + 1):
        dp[i][0] = i * gap_penalty
    for j in range(len2 + 1):
        dp[0][j] = j * gap_penalty

    # Fill scoring matrix
    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            match = dp[i - 1][j - 1] + (match_score if seq1[i - 1] == seq2[j - 1] else mismatch_penalty)
            delete = dp[i - 1][j] + gap_penalty
            insert = dp[i][j - 1] + gap_penalty
            dp[i][j] = max(match, delete, insert)

    # Traceback for alignment
    align1, align2 = '', ''
    i, j = len1, len2
    while i > 0 and j > 0:
        current_score = dp[i][j]
        if seq1[i - 1] == seq2[j - 1]:
            align1 += seq1[i - 1]
            align2 += seq2[j - 1]
            i -= 1
            j -= 1
        elif current_score == dp[i - 1][j] + gap_penalty:
            align1 += seq1[i - 1]
            align2 += '-'
            i -= 1
        elif current_score == dp[i][j - 1] + gap_penalty:
            align1 += '-'
            align2 += seq2[j - 1]
            j -= 1

    # Add remaining sequence if any
    while i > 0:
        align1 += seq1[i - 1]
        align2 += '-'
        i -= 1
    while j > 0:
        align1 += '-'
        align2 += seq2[j - 1]
        j -= 1

    align1, align2 = align1[::-1], align2[::-1]

    # Calculate alignment details
    matches = sum(1 for a, b in zip(align1, align2) if a == b and a != '-')
    identity = matches / len(align1) * 100
    similarity = matches / len(align1) * 100  # Simplified similarity calculation
    gaps = sum(1 for a, b in zip(align1, align2) if a == '-' or b == '-')

    result = {
        "align1": align1,
        "align2": align2,
        "score": dp[len1][len2],
        "alignment_length": len(align1),
        "identity": f"{matches}/{len(align1)} ({identity:.2f}%)",
        "similarity": f"{matches}/{len(align1)} ({similarity:.2f}%)",
        "gaps": f"{gaps}/{len(align1)} ({(gaps / len(align1) * 100):.2f}%)"
    }

    return result


@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        seq1 = request.form['seq1'].upper()
        seq2 = request.form['seq2'].upper()

        if not all(c in 'ACGT' for c in seq1) or not all(c in 'ACGT' for c in seq2):
            result = "Error: Sequences must only contain the characters A, C, G, and T."
        else:
            result = needleman_wunsch(seq1, seq2)
    return render_template('index.html', result=result)


if __name__ == '__main__':
    app.run(debug=True)
