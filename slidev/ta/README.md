# CCGL9065 TA toolkit

Three unlisted Slidev decks support the tutorial programme:

- `onboarding.md` introduces prospective and newly appointed TAs to the course,
  facilitation model, evidence checks, portfolio crits and escalation boundaries.
- `tutorial01.md` is the one-off week-1 set-up session: Slack sign-up, Notion
  walk-through, a timed prep sprint, pair work and an open share. It is fixed
  and needs no per-week editing.
- `tutorial.md` is the reusable student-facing control deck used from week 2.

## Reuse the tutorial deck

Edit only `session.json` to set the week, topic, current task and next-class
prompt. Then rebuild:

```sh
npm run build:tutorial
```

The tutorial sequence itself should remain stable. It creates no additional
student deliverable.

## Build all decks

```sh
npm install
npm run build
```

Output:

- `../../slides/ta/tutorial/`
- `../../slides/ta/tutorial01/`
- `../../slides/ta/onboarding/`

The public site links these decks only from the unlisted `/ta/` toolkit page.
That page is intentionally absent from student navigation, but it is not
password-protected.
