# Simplified Horizons Task — web port

Browser port of `TimeSearch_190603.py` (PsychoPy) from Zhuang, Niebaum & Munakata (2023),
*Developmental Psychology*, 59(8), 1532–1542.

## Running it

Open `index.html` in Chrome, Edge, Safari, or Firefox — on a computer or on an iPad.
Nothing to install, no server needed, works offline. Keep `index.html` and the `stim/`
folder together.

Enter a participant ID, pick the age group, choose the rendering options, press **Start**.

| Action | Computer | iPad |
|---|---|---|
| Advance an instruction screen | **Space** | tap the **bottom-right corner** (a faint dot marks it) |
| Make a choice | click a canister | tap a canister |
| Save / review data mid-session | **D** | long-press the **top-left corner** for 1.5 s |
| Quit and save | **Esc** | long-press top-left, then close the browser |

At the end the CSV downloads automatically **and** is shown on screen, so it can be copied
and pasted if the download is missed. On iPad downloads land in Files › Downloads.

### Saving and file names

Data lives in browser memory during the session, so it saves itself at three points. Every
file is **cumulative** — each one contains all trials completed so far, not just the recent
ones.

| When | File name ends with |
|---|---|
| before the break at trial 6 | `_partial-t5.csv` |
| before the break at trial 12 | `_partial-t11.csv` |
| after the last trial | `_FINAL.csv` |
| experimenter saved by hand (**D**, or long-press top-left) | `_manual.csv` |
| session quit early (**Esc**) | `_ABORTED.csv` |

Full name: `<participant>_TimeSearch_<start timestamp>_<tag>.csv`

**For a normal session, keep the `_FINAL` file and ignore the partials.** The partials only
matter if the browser crashed or the iPad was closed mid-session — then the newest partial
is the most complete record, and at most five trials are lost.

### On iPad

- Turn on **Guided Access** (Settings › Accessibility › Guided Access) before handing the
  device to a child. It locks the app so swipes cannot exit the task.
- Or use **Add to Home Screen** in Safari to run it without browser chrome.
- Instruction screens deliberately do **not** advance on a tap anywhere — only in the
  bottom-right corner — so a child's stray taps cannot skip a screen. The experimenter is
  present throughout, as in the original procedure.
- Choices register on **touch down**, not on lift, so reaction times do not include the time
  taken to raise a finger. A second simultaneous touch (e.g. a resting palm) is ignored.
- Pinch-zoom, double-tap zoom, scrolling and text selection are all disabled.

### One thing to check before testing children on iPad

Geometry is preserved exactly across devices — the task draws into a fixed 1440×900 canvas
that is scaled to fit — so proportions are identical on any screen. **Absolute physical size
is not.** An iPad screen is smaller than a desktop monitor, so every splash is physically
smaller, and the child usually holds it closer, which partly compensates.

The concern is the smallest rewards. Test trial 18 has values from 0.29 to 1.15, which on a
10.2" iPad render as splashes roughly 4–15 mm across. The paper's claim that adjacent reward
sizes are discriminable rests on ratios between options, which are preserved, but if the
smallest splashes are hard to see at all, that is a floor the original did not have. Pilot
this with a few children, or scale all splashes up by a constant factor — a single multiplier
in `splashSize()` — which preserves every ratio in the design.

## What is reproduced exactly

- **Trial lists** — the 5 practice trials (`TimeSearch_TrialList_Demo.csv`) and the 18 test
  trials (`TimeSearch_TrialList_Pilot.csv`), verbatim: reward values, positions,
  `start_info_state`, colours, horizon condition, order.
- **Horizon conditions** — 6 long (4 picks), 6 short (1 pick), 6 ambiguous
  (`horizons_known = 0`; 3 of them are actually 4 picks and 3 are actually 1).
- **Layout** — configs F (diamond) and G (square) at the original norm-unit coordinates.
- **Horizon cue** — hands for known horizons, dropped one at a time from the right as picks
  are used; cloud only (never hands) for the whole free-choice portion of ambiguous trials.
- **Breaks** — before test trials 6 and 12, matching `trials.thisTrialN == 5` and `== 11`.
  (The code comment in the original says "10th trial" and "12th trial"; the code itself
  says 6th and 12th. The code wins here.)
- **Instruction screens** — the original PNGs, in the original order.
- **Flow** — spacebar advances screens, Esc quits, as in the original.

## Rendering options

Both default to **on**. Turn both off to reproduce the original display exactly.

### Correct splash aspect ratio

The original set the splash size with a single PsychoPy scalar in `norm` units:
`size = round(reward_state[i]/10, 2)`. In norm units a scalar maps to
`(s × half-width, s × half-height)` in pixels, so on the lab's 16:10 display every splash
was stretched about **1.6× horizontally**. The canisters were not affected — the author
compensated for them explicitly with `target_size = (0.3*1.3, 0.5*1.3)`, which is only
circular at 16:10, and that is how the aspect ratio of the original display was recovered.

Checked: the splash keeps its source aspect ratio, at the same displayed area.

### Equalise ink area across colours

The size scalar sets the **image bounding box**, not the paint. The nine splash PNGs differ
a lot in how much of their box is actually ink:

| colour | source px | ink coverage |
|---|---|---|
| bluedark | 600×475 | 50.1% |
| yellow | 288×288 | 47.6% |
| green | 360×360 | 45.7% |
| magenta | 635×601 | 39.2% |
| blue | 460×460 | 37.3% |
| brown | 730×730 | 32.8% |
| orange | 600×573 | 32.7% |
| purple | 720×720 | 31.8% |
| red | 360×360 | 27.7% |

The same reward value therefore showed roughly **1.8× more visible paint in dark blue than
in red**. Colour is constant within a trial, so within-trial comparisons — the thing the
task actually asks participants to do — are unaffected. It matters between trials, which is
where the exploit-reward-size analysis lives, and colour is not balanced across conditions
in the original list (magenta appears only in long trials, orange only in short).

Checked: each colour is rescaled by `sqrt(0.383 / ink_colour)` so equal reward values show
equal paint area. 0.383 is the mean coverage across the nine files, so overall scale is
unchanged.

### Corrected horizons instruction screen

`horizons_intro_screen.png` says the pick count appears "on the top of the screen"; it
appears in the middle (`freechoice_pos` y = 0, `cloud_pos = [0,0]`). The `.jpg` version of
the same slide has the corrected wording but carries a leftover experimenter note,
`[press 'x']`. The included `horizons_intro_screen_corrected.png` has the correct wording
and no note. Uncheck to use the original PNG.

## Data columns

Original columns are kept under their original names so existing R code needs minimal
changes. New columns:

| column | meaning |
|---|---|
| `phase` | `practice` or `test` |
| `horizon_condition` | `long` / `short` / `ambiguous`, derived from `horizons` + `horizons_known` |
| `explore_pos`, `exploit_pos` | which canister was the explore / exploit option (`a`–`d`) |
| `initial_choice` | `explore` / `exploit` / `other` — the paper's main outcome, computed per trial |
| `freechoice_resp.time` | reaction time in seconds for every free choice, as a list |
| `initial_rt` | RT of the first free choice — the paper's main outcome pairs with this |
| `rt1`–`rt4` | **one numeric column per free choice**, blank past the trial's pick count |
| `choice1`–`choice4` | which canister (`a`–`d`) was picked at each free choice |
| `reward_gain1`–`reward_gain4` | reward collected at each free choice |
| `render_aspect_corrected`, `render_ink_equalised` | which rendering options were active |

`rt1`–`rt4`, `choice1`–`choice4` and `reward_gain1`–`reward_gain4` follow the convention the
original merged data already used for `reward_gain1..4` and `info_gain1..4`: one column per
choice, so nothing has to be parsed out of a bracketed string. Short-horizon trials have one
free choice, so columns 2–4 are empty and read as `NA`. The bracketed list columns are kept
alongside them for compatibility with the original format.

`freechoice_resp.time` is the addition worth flagging. The original script did log click
times, but they are not in the shared merged data (`SearchCosts_TimeSearch_MergedData_20200427.csv`,
31 columns, no time field), which is why the paper reports that RT was unavailable and
leaves the "is exploration prepotent in young children?" question open. This port records
it by default.

## Known deviations from the original

1. **Timings between phases** are approximations — 700 ms store transition, 500 ms after a
   fixed choice, 450 ms after a free choice, 700 ms next-store. The original used frame
   loops; exact durations were not recoverable from the script. Adjust the `sleep()` calls
   in `runTrial()` if you want different pacing.
2. **Fixed-choice order** follows canister position order (a → b → c → d) among the two
   canisters flagged `0` in `start_info_state`. The original's sequence is not explicit in
   the script.
3. **Practice trials: 5, not 4.** `TimeSearch_TrialList_Demo.csv` contains five rows; the
   paper's Method section says four practice trials. Unchecking "include practice" skips
   them entirely.
4. **The paint-tube progress meter is not implemented.** It exists in the original only as
   commented-out code (`reward_bar`, `reward_intro` routine, with the author's note
   `#200 isn't the correct number....`), so it was not part of the administered task
   despite `reward_intro_screen.jpg` describing it.
5. **Reward accounting** follows the original: `reward_trial` sums the raw `reward_state`
   values of the two fixed choices plus every free choice. Note that displayed *area* goes
   as the square of that value, so "reward gained in pixels sq" in the paper is really
   linear in the size scalar. Monotonic either way, so group comparisons are unaffected,
   but worth deciding explicitly before you report units.
6. **Stage is a fixed 1440×900 (16:10) canvas** scaled to fit the window, so geometry is
   identical on any monitor. The original ran fullscreen at the display's native
   resolution.

## Files

```
index.html   the whole task — layout, trial lists, engine, CSV export
stim/        24 images: 9 splashes, canister, hands, cloud, store icons, 9 instruction screens
README.md    this file
```
