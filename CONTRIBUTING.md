# Contributing / المساهمة

Contributions that improve correctness, portability, tests, documentation, or accessibility are welcome.

1. Fork the repository and create a focused branch.
2. Use Python 3.10+ and install with `python -m pip install -e . pytest`.
3. Run `python -m compileall -q src tests` and `pytest -q`.
4. Keep networking behavior conservative: no stealth scanning, evasion, exploitation, credential handling, or unsafe defaults.
5. Add tests for behavioral changes and keep the CLI documentation accurate.
6. Open a focused pull request describing the motivation and validation performed.

Arabic: نرحب بالمساهمات التي تحسن الدقة والتوافق والاختبارات والتوثيق. يرجى إبقاء سلوك الشبكة محافظًا وآمنًا، وإضافة اختبارات لأي تغيير وظيفي، وعدم تضمين أسرار أو بيانات حساسة.

Maintainer / المشرف: Radwan Abdulhadi Ahmed — رضوان عبدالهادي أحمد — @rad03i2
