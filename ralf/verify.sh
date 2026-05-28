#!/usr/bin/env bash
# Verify the Fantasy Bakery proposal v2 ships correctly.
# Exits 0 when all locked decisions are reflected in the LIVE deployed page.

set -uo pipefail

URL="https://tranquilvedapvtltd.github.io/fantasy-bakery-proposal/"
TMP=$(mktemp)
trap 'rm -f "$TMP"' EXIT

# Fetch with cache-bust
if ! curl -fsSL "${URL}?cb=$(date +%s)" -o "$TMP"; then
    echo "FAIL: could not fetch $URL"
    exit 1
fi

errors=0

check() {
    local pattern="$1"
    local label="$2"
    if grep -qE "$pattern" "$TMP"; then
        echo "OK   : $label"
    else
        echo "FAIL : $label  (pattern: $pattern)"
        errors=$((errors+1))
    fi
}

check_absent() {
    local pattern="$1"
    local label="$2"
    if grep -qE "$pattern" "$TMP"; then
        echo "FAIL : $label is present but must be ABSENT  (pattern: $pattern)"
        errors=$((errors+1))
    else
        echo "OK   : $label is absent (as required)"
    fi
}

# Pricing reflects locked decisions
check 'Vinayak'                          "addresses Vinayak"
check '₹3,95,000|3,95,000'                "setup total ₹3,95,000 present"
check '3,75,000'                          "platform line ₹3,75,000 present"
check '₹20,000'                           "WhatsApp bot setup ₹20,000 present"
check '15,000|₹15,000'                   "platform retainer ₹15K present (was ₹10K)"
check '25,000|₹25,000'                   "total monthly ₹25K present"
check '12 weeks|twelve weeks|12-week'    "timeline 12 weeks present"
check 'AI Cake Studio|Fantasy Cake Studio' "AI Cake Studio mentioned"
check 'custom cake'                       "custom cake positioning present"
check 'job card'                          "job card mentioned"
check '3 iteration|three iteration|3-iteration|three-time|3 times|three times|3 customisation|three customisation|3 revision|three revision|hard cap' "iteration cap mentioned"
check 'shruti@jarvisdaily.com'            "Shruti email present"
check '9673758777'                        "Shruti phone present"

# Hard constraints — must be absent
check_absent 'Vallabh'                    "Vallabh"
check_absent '&mdash;|—|&#8212;'         "em-dash"
check_absent '\bM1\b|\bM2\b|\bM3\b'      "M1/M2/M3 phase tags"

# Pricing math sanity: setup payment schedule sums to ₹3,75,000
# (40% = 1,50,000, 30% = 1,12,500, 30% = 1,12,500) for ₹3,75,000
# We don't enforce exact split markers — just that the displayed totals match what we expect.

if [ "$errors" -gt 0 ]; then
    echo
    echo "VERIFY: $errors check(s) failed"
    exit 1
fi

echo
echo "VERIFY: PASS"
exit 0
