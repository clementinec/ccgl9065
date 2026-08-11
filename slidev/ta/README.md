# CCGL9065 TA toolkit

Two unlisted Slidev decks support the tutorial programme:

- `onboarding.md` introduces prospective and newly appointed TAs to the course,
  facilitation model, evidence checks, portfolio crits and escalation boundaries.
- `tutorial.md` is the reusable student-facing control deck for weekly tutorials.

## Reuse the tutorial deck

Edit only `session.json` to set the week, topic, current task and next-class
prompt. Then rebuild:

```sh
npm run build:tutorial
```

The tutorial sequence itself should remain stable. It creates no additional
student deliverable.

## Build both decks

```sh
npm install
npm run build
```

Output:

- `../../slides/ta/tutorial/`
- `../../slides/ta/onboarding/`

The public site links these decks only from the unlisted `/ta/` toolkit page.
That page is intentionally absent from student navigation, but it is not
password-protected.
